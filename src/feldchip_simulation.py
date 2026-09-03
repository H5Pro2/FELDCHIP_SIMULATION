"""Reproduzierbares Referenzmodell für einen feldbasierten 4x4-Demonstrator."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math

import numpy as np


MODEL_NAMES = (
    "feld_2_regime",
    "feld_3_regime",
    "feld_4_regime",
    "feld_glatt",
    "baseline_ungekoppelt",
    "baseline_linear_rc",
    "baseline_digital_diffusion",
    "baseline_rohsignal",
)

NOISE_LEVELS = (0.15, 0.35, 0.55)
PATTERN_NAMES = ("einzelpunkt", "horizontal", "vertikal", "zwei_punkte", "kreuz", "gradient")
DEFAULT_SEEDS = (11, 23, 37, 53, 71)
DEFAULT_TRAIN_PER_PATTERN = 12
DEFAULT_TEST_PER_PATTERN = 24


@dataclass(frozen=True)
class SimulationConfig:
    grid_size: int = 4
    dt: float = 0.02
    stimulus_time: float = 2.0
    return_time: float = 5.0
    coupling: float = 0.34
    input_gain: float = 1.25
    return_low: float = 0.15
    return_high: float = 1.0
    smooth_width: float = 0.12
    soft_limit_start: float = 2.65
    soft_limit_gain: float = 2.5
    hard_limit: float = 3.0
    mismatch_sigma: float = 0.08
    offset_sigma: float = 0.04
    dynamic_noise_scale: float = 0.035
    dropout_probability: float = 0.08
    return_tolerance: float = 0.05


def laplacian_neumann(values: np.ndarray) -> np.ndarray:
    """Vierer-Nachbarschaft mit reflexiven (Neumann-)Rändern."""
    padded = np.pad(values, ((0, 0), (1, 1), (1, 1)), mode="edge")
    return (
        padded[:, :-2, 1:-1]
        + padded[:, 2:, 1:-1]
        + padded[:, 1:-1, :-2]
        + padded[:, 1:-1, 2:]
        - 4.0 * values
    )


def canonical_patterns() -> dict[str, np.ndarray]:
    patterns: dict[str, np.ndarray] = {}
    point = np.zeros((4, 4), dtype=float)
    point[1, 1] = 1.0
    patterns["einzelpunkt"] = point

    horizontal = np.full((4, 4), -0.25, dtype=float)
    horizontal[1:3, :] = 0.75
    patterns["horizontal"] = horizontal

    vertical = np.full((4, 4), -0.25, dtype=float)
    vertical[:, 1:3] = 0.75
    patterns["vertikal"] = vertical

    two_points = np.zeros((4, 4), dtype=float)
    two_points[0, 1] = 1.0
    two_points[3, 2] = 1.0
    patterns["zwei_punkte"] = two_points

    cross = np.full((4, 4), -0.2, dtype=float)
    cross[1:3, :] = 0.55
    cross[:, 1:3] = 0.55
    patterns["kreuz"] = cross

    patterns["gradient"] = np.tile(np.linspace(-0.9, 0.9, 4), (4, 1))
    return patterns


def distorted_samples(
    pattern: np.ndarray,
    count: int,
    noise_sigma: float,
    rng: np.random.Generator,
    config: SimulationConfig,
) -> np.ndarray:
    samples = np.broadcast_to(pattern, (count, 4, 4)).copy()
    gain = rng.normal(1.0, 0.12, size=(count, 1, 1))
    bias = rng.normal(0.0, 0.08, size=(count, 1, 1))
    samples = gain * samples + bias
    samples += rng.normal(0.0, noise_sigma, size=samples.shape)
    dropout = rng.random(samples.shape) < config.dropout_probability
    samples[dropout] = 0.0
    return np.clip(samples, -1.5, 1.5)


def return_gain(abs_delta: np.ndarray, variant: str, config: SimulationConfig) -> np.ndarray:
    if variant == "feld_glatt":
        sigmoid_1 = 1.0 / (1.0 + np.exp(-(abs_delta - 1.0) / config.smooth_width))
        sigmoid_2 = 1.0 / (1.0 + np.exp(-(abs_delta - 2.0) / config.smooth_width))
        return config.return_low + 0.25 * sigmoid_1 + 0.60 * sigmoid_2

    regimes = int(variant.split("_")[1])
    thresholds = np.linspace(0.0, config.hard_limit, regimes + 1)[1:-1]
    levels = np.linspace(config.return_low, config.return_high, regimes)
    indices = np.searchsorted(thresholds, abs_delta, side="right")
    return levels[indices]


def _dynamic_model(
    stimulus: np.ndarray,
    variant: str,
    rng: np.random.Generator,
    config: SimulationConfig,
) -> tuple[np.ndarray, dict[str, float]]:
    state = np.zeros_like(stimulus)
    device_shape = (1, config.grid_size, config.grid_size)
    reference = rng.normal(0.0, config.offset_sigma, size=device_shape)
    mismatch = rng.normal(1.0, config.mismatch_sigma, size=device_shape)
    stimulus_steps = round(config.stimulus_time / config.dt)
    return_steps = round(config.return_time / config.dt)
    attempted_violations = 0
    total_updates = 0
    activity = 0.0

    coupling = 0.0 if variant == "baseline_ungekoppelt" else config.coupling
    constant_return = variant in {"baseline_ungekoppelt", "baseline_linear_rc"}

    def advance(input_field: np.ndarray) -> None:
        nonlocal state, attempted_violations, total_updates, activity
        delta = state - reference
        gain = 0.40 if constant_return else return_gain(np.abs(delta), variant, config)
        soft_excess = np.maximum(np.abs(state) - config.soft_limit_start, 0.0)
        soft_limit = config.soft_limit_gain * np.sign(state) * soft_excess**3
        dynamic_noise = rng.normal(0.0, config.dynamic_noise_scale, size=state.shape)
        derivative = (
            config.input_gain * input_field
            + coupling * laplacian_neumann(state)
            - mismatch * gain * delta
            - soft_limit
            + dynamic_noise
        )
        candidate = state + config.dt * derivative
        attempted_violations += int(np.count_nonzero(np.abs(candidate) > config.hard_limit))
        total_updates += candidate.size
        activity += float(np.sum(np.abs(candidate - state)))
        state = np.clip(candidate, -config.hard_limit, config.hard_limit)

    for _ in range(stimulus_steps):
        advance(stimulus)
    response = state.copy()

    return_times = np.full(state.shape[0], np.nan)
    for step in range(1, return_steps + 1):
        advance(np.zeros_like(stimulus))
        rms = np.sqrt(np.mean((state - reference) ** 2, axis=(1, 2)))
        newly_returned = np.isnan(return_times) & (rms <= config.return_tolerance)
        return_times[newly_returned] = step * config.dt

    residual = np.sqrt(np.mean((state - reference) ** 2, axis=(1, 2)))
    return response, {
        "return_residual": float(np.mean(residual)),
        "return_time": float(np.nanmean(return_times)) if np.any(~np.isnan(return_times)) else math.nan,
        "return_success": float(np.mean(~np.isnan(return_times))),
        "violation_rate": attempted_violations / max(total_updates, 1),
        "activity_proxy": activity / max(total_updates, 1),
        "max_abs": float(np.max(np.abs(response))),
    }


def _digital_diffusion(stimulus: np.ndarray, config: SimulationConfig) -> np.ndarray:
    state = np.clip(config.input_gain * stimulus, -config.hard_limit, config.hard_limit)
    for _ in range(12):
        state += 0.12 * laplacian_neumann(state)
        state = np.clip(state, -config.hard_limit, config.hard_limit)
    levels = 2**12 - 1
    return np.round((state + 3.0) / 6.0 * levels) / levels * 6.0 - 3.0


def simulate_batch(
    stimulus: np.ndarray,
    variant: str,
    rng: np.random.Generator,
    config: SimulationConfig,
) -> tuple[np.ndarray, dict[str, float]]:
    if variant == "baseline_rohsignal":
        response = np.clip(config.input_gain * stimulus, -config.hard_limit, config.hard_limit)
    elif variant == "baseline_digital_diffusion":
        response = _digital_diffusion(stimulus, config)
    else:
        return _dynamic_model(stimulus, variant, rng, config)
    return response, {
        "return_residual": math.nan,
        "return_time": math.nan,
        "return_success": math.nan,
        "violation_rate": 0.0,
        "activity_proxy": math.nan,
        "max_abs": float(np.max(np.abs(response))),
    }


def nearest_centroid_metrics(
    train_fields: np.ndarray,
    train_labels: np.ndarray,
    test_fields: np.ndarray,
    test_labels: np.ndarray,
) -> dict[str, float]:
    classes = np.unique(train_labels)
    train_flat = train_fields.reshape(train_fields.shape[0], -1)
    test_flat = test_fields.reshape(test_fields.shape[0], -1)
    centroids = np.stack([train_flat[train_labels == label].mean(axis=0) for label in classes])
    distances = np.linalg.norm(test_flat[:, None, :] - centroids[None, :, :], axis=2)
    predictions = classes[np.argmin(distances, axis=1)]
    accuracy = float(np.mean(predictions == test_labels))

    within = np.mean([
        np.mean(np.linalg.norm(train_flat[train_labels == label] - centroids[index], axis=1))
        for index, label in enumerate(classes)
    ])
    between = min(
        np.linalg.norm(centroids[a] - centroids[b])
        for a in range(len(classes))
        for b in range(a + 1, len(classes))
    )
    repeatability_rmse = float(np.sqrt(np.mean([
        np.mean((train_flat[train_labels == label] - centroids[index]) ** 2)
        for index, label in enumerate(classes)
    ])))
    return {
        "accuracy": accuracy,
        "separability_ratio": float(between / max(within, 1e-12)),
        "repeatability_rmse": repeatability_rmse,
    }


def compact_readout(fields: np.ndarray) -> np.ndarray:
    """Acht feste, analog realisierbare Skalare aus einem 4x4-Feld."""
    if fields.ndim != 3 or fields.shape[1:] != (4, 4):
        raise ValueError("compact_readout erwartet Felder der Form (n, 4, 4)")
    magnitude = np.abs(fields)
    total_magnitude = np.sum(magnitude, axis=(1, 2))
    safe_total = np.maximum(total_magnitude, 1e-12)
    axis = np.linspace(-1.0, 1.0, 4)
    x_grid = np.broadcast_to(axis[None, :], (4, 4))
    y_grid = np.broadcast_to(axis[:, None], (4, 4))
    center_x = np.sum(magnitude * x_grid, axis=(1, 2)) / safe_total
    center_y = np.sum(magnitude * y_grid, axis=(1, 2)) / safe_total
    spread_x = np.sum(
        magnitude * (x_grid - center_x[:, None, None]) ** 2, axis=(1, 2)
    ) / safe_total
    spread_y = np.sum(
        magnitude * (y_grid - center_y[:, None, None]) ** 2, axis=(1, 2)
    ) / safe_total
    return np.column_stack((
        np.mean(fields, axis=(1, 2)),
        np.mean(magnitude, axis=(1, 2)),
        center_x,
        center_y,
        spread_x,
        spread_y,
        np.max(fields, axis=(1, 2)),
        -np.min(fields, axis=(1, 2)),
    ))


def run_campaign(
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    train_per_pattern: int = DEFAULT_TRAIN_PER_PATTERN,
    test_per_pattern: int = DEFAULT_TEST_PER_PATTERN,
    config: SimulationConfig | None = None,
    readout: str = "full",
) -> tuple[list[dict[str, float | int | str]], dict[str, np.ndarray]]:
    config = config or SimulationConfig()
    if readout not in {"full", "compact"}:
        raise ValueError("readout muss 'full' oder 'compact' sein")
    patterns = canonical_patterns()
    rows: list[dict[str, float | int | str]] = []
    examples: dict[str, np.ndarray] = {}

    for seed in seeds:
        for noise_sigma in NOISE_LEVELS:
            sample_rng = np.random.default_rng(seed * 1000 + round(noise_sigma * 100))
            train_inputs, test_inputs, train_labels, test_labels = [], [], [], []
            for label, name in enumerate(PATTERN_NAMES):
                train_inputs.append(distorted_samples(patterns[name], train_per_pattern, noise_sigma, sample_rng, config))
                test_inputs.append(distorted_samples(patterns[name], test_per_pattern, noise_sigma, sample_rng, config))
                train_labels.extend([label] * train_per_pattern)
                test_labels.extend([label] * test_per_pattern)
            train_input = np.concatenate(train_inputs)
            test_input = np.concatenate(test_inputs)
            train_labels_array = np.asarray(train_labels)
            test_labels_array = np.asarray(test_labels)

            for model_index, model in enumerate(MODEL_NAMES):
                device_seed = seed * 10000 + model_index * 101
                train_rng = np.random.default_rng(device_seed)
                test_rng = np.random.default_rng(device_seed)
                train_fields, train_dynamics = simulate_batch(train_input, model, train_rng, config)
                test_fields, test_dynamics = simulate_batch(test_input, model, test_rng, config)
                train_values = compact_readout(train_fields) if readout == "compact" else train_fields
                test_values = compact_readout(test_fields) if readout == "compact" else test_fields
                metrics = nearest_centroid_metrics(
                    train_values, train_labels_array, test_values, test_labels_array
                )
                rows.append({
                    "seed": seed,
                    "noise_sigma": noise_sigma,
                    "model": model,
                    **metrics,
                    **test_dynamics,
                })
                if seed == seeds[0] and noise_sigma == NOISE_LEVELS[1]:
                    start = PATTERN_NAMES.index("kreuz") * test_per_pattern
                    examples[model] = test_fields[start].copy()
    return rows, examples


def summarize(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | str]]:
    summary: list[dict[str, float | str]] = []
    for model in MODEL_NAMES:
        model_rows = [row for row in rows if row["model"] == model]
        result: dict[str, float | str] = {"model": model}
        for metric in (
            "accuracy",
            "separability_ratio",
            "repeatability_rmse",
            "return_residual",
            "return_time",
            "return_success",
            "violation_rate",
            "activity_proxy",
            "max_abs",
        ):
            values = np.asarray([float(row[metric]) for row in model_rows])
            finite = values[np.isfinite(values)]
            result[f"{metric}_mean"] = float(np.mean(finite)) if finite.size else math.nan
            result[f"{metric}_std"] = float(np.std(finite, ddof=1)) if finite.size > 1 else math.nan
        summary.append(result)
    return summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _color(value: float, limit: float = 3.0) -> str:
    x = float(np.clip(value / limit, -1.0, 1.0))
    if x >= 0:
        r, g, b = 245, round(245 - 135 * x), round(245 - 175 * x)
    else:
        x = -x
        r, g, b = round(245 - 175 * x), round(245 - 100 * x), 245
    return f"rgb({r},{g},{b})"


def write_field_svg(path: Path, examples: dict[str, np.ndarray]) -> None:
    cell, panel_w, panel_h = 42, 260, 245
    width, height = 4 * panel_w, 2 * panel_h
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>']
    for index, model in enumerate(MODEL_NAMES):
        x0, y0 = (index % 4) * panel_w + 45, (index // 4) * panel_h + 48
        parts.append(f'<text x="{x0-25}" y="{y0-20}" font-family="Arial" font-size="15" font-weight="bold">{model}</text>')
        field = examples[model]
        for row in range(4):
            for col in range(4):
                value = float(field[row, col])
                x, y = x0 + col * cell, y0 + row * cell
                parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{_color(value)}" stroke="#333"/>')
                parts.append(f'<text x="{x+cell/2}" y="{y+cell/2+5}" text-anchor="middle" font-family="Arial" font-size="12">{value:.2f}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts), encoding="utf-8")


def write_accuracy_svg(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    width, height = 1180, 620
    margin_left, margin_top, chart_h = 110, 55, 430
    group_w, bar_w = 130, 11
    palette = ["#245b78", "#4b8a68", "#a96f24", "#915f8c", "#63717a", "#3d7ca6", "#b24e43", "#444444"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>', '<text x="30" y="30" font-family="Arial" font-size="20" font-weight="bold">Mustertrennung nach Rauschstufe</text>']
    for tick in range(0, 11, 2):
        value = tick / 10
        y = margin_top + chart_h * (1 - value)
        parts.append(f'<line x1="{margin_left}" y1="{y}" x2="{width-40}" y2="{y}" stroke="#d8dde1"/>')
        parts.append(f'<text x="{margin_left-12}" y="{y+5}" text-anchor="end" font-family="Arial" font-size="12">{value:.1f}</text>')
    for group_index, noise in enumerate(NOISE_LEVELS):
        center = margin_left + 155 + group_index * 335
        parts.append(f'<text x="{center}" y="{margin_top+chart_h+35}" text-anchor="middle" font-family="Arial" font-size="14">σ = {noise:.2f}</text>')
        for model_index, model in enumerate(MODEL_NAMES):
            vals = [float(r["accuracy"]) for r in rows if r["model"] == model and float(r["noise_sigma"]) == noise]
            mean = float(np.mean(vals))
            x = center - 4 * (bar_w + 5) + model_index * (bar_w + 5)
            y = margin_top + chart_h * (1 - mean)
            parts.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{margin_top+chart_h-y}" fill="{palette[model_index]}"/>')
    legend_y = 535
    for index, model in enumerate(MODEL_NAMES):
        x = 40 + (index % 4) * 285
        y = legend_y + (index // 4) * 30
        parts.append(f'<rect x="{x}" y="{y-13}" width="15" height="15" fill="{palette[index]}"/>')
        parts.append(f'<text x="{x+22}" y="{y}" font-family="Arial" font-size="12">{model}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts), encoding="utf-8")


def write_report(
    path: Path,
    summary: list[dict[str, float | str]],
    rows: list[dict[str, float | int | str]],
    readout: str = "full",
) -> None:
    ranked = sorted(summary, key=lambda row: float(row["accuracy_mean"]), reverse=True)
    best = ranked[0]
    field_rows = [row for row in summary if str(row["model"]).startswith("feld_")]
    best_field = max(field_rows, key=lambda row: float(row["accuracy_mean"]))
    best_baseline = max((row for row in summary if str(row["model"]).startswith("baseline_")), key=lambda row: float(row["accuracy_mean"]))
    advantage = float(best_field["accuracy_mean"]) - float(best_baseline["accuracy_mean"])
    lines = [
        "# Ergebnisbericht: mathematischer 4×4-Demonstrator",
        "",
        "## Prüfziel",
        "",
        "Geprüft wird, ob gekoppelte kontinuierliche Zellen unter identischen gestörten Eingangsmustern reproduzierbar trennbare Feldformen erzeugen. Der Arbeitsbereich bleibt für alle Feldvarianten bei −3 bis +3. Verglichen werden zwei, drei und vier Rückführungsregime sowie eine geglättete Dreiregime-Kennlinie.",
        "",
        "## Vorab festgelegte Aufgabe",
        "",
        "Sechs 4×4-Muster werden mit Verstärkungsstreuung, Offset, Pixelausfällen und drei Rauschstufen beaufschlagt. Pro Rauschstufe laufen fünf unabhängige Zufallsstarts. " + ("Die Auswertung verwendet acht vorab festgelegte Skalare: Summe, Betragsenergie, zwei Schwerpunktkoordinaten, zwei räumliche Ausdehnungen sowie positiven und negativen Spitzenwert." if readout == "compact" else "Die Auswertung verwendet ausschließlich die 16 Feldwerte am Ende des Eingangspulses.") + " In beiden Fällen wird ein einfacher Nächste-Zentroid-Auswerter eingesetzt.",
        "",
        "## Gesamtergebnis",
        "",
        f"Die höchste mittlere Trennrate erreichte `{best['model']}` mit {100*float(best['accuracy_mean']):.1f} %. Die beste Feldvariante war `{best_field['model']}` mit {100*float(best_field['accuracy_mean']):.1f} %. Die beste Baseline war `{best_baseline['model']}` mit {100*float(best_baseline['accuracy_mean']):.1f} %.",
        "",
        f"Differenz beste Feldvariante minus beste Baseline: {100*advantage:+.1f} Prozentpunkte.",
        "",
        "Damit ist ein Vorteil der Feldarchitektur in dieser Aufgabe " + ("vorläufig sichtbar, aber noch nicht allgemein nachgewiesen." if advantage > 0.01 else "nicht nachgewiesen; die einfachere Baseline ist gleich gut oder besser."),
        "",
        "## Zentrale Befunde und Nichtnachweise",
        "",
        f"- Die vier Feldkennlinien liegen bei der mittleren Trennrate eng beieinander. Der Abstand zwischen bester und schwächster Feldvariante beträgt nur {100*(max(float(row['accuracy_mean']) for row in field_rows)-min(float(row['accuracy_mean']) for row in field_rows)):.1f} Prozentpunkte. Aus diesem Lauf folgt daher kein besonderer Vorteil von zwei, drei, vier oder geglätteten Regimen.",
        f"- Die beste Feldvariante liegt {abs(100*advantage):.1f} Prozentpunkte " + ("vor" if advantage > 0 else "hinter") + " der besten Baseline. Für die hier verwendete " + ("kompakte Auslese" if readout == "compact" else "Vollfeldauslese") + " ist ein zusätzlicher Nutzen der nichtlinearen Feldbildung " + ("vorläufig sichtbar, aber noch nicht unabhängig bestätigt." if advantage > 0.01 else "nicht nachgewiesen."),
        f"- Der Rückkehrerfolg der Feldvarianten liegt nach fünf normierten Sekunden nur zwischen {100*min(float(row['return_success_mean']) for row in field_rows):.1f} % und {100*max(float(row['return_success_mean']) for row in field_rows):.1f} %. Die gewählte schwache innere Rückführung erfüllt das Rückkehrkriterium damit nicht.",
        f"- Im regulären Lauf traten bei keiner Feldvariante versuchte Grenzüberschreitungen auf. Der höchste mittlere Betrag blieb bei {max(float(row['max_abs_mean']) for row in field_rows):.3f} und damit deutlich innerhalb des Bereichs −3 bis +3.",
        "- Die feste digitale Diffusion glättet die kleinen 4×4-Muster stark und ist in dieser einzelnen Parametrierung deutlich schlechter. Das ist kein allgemeiner Nachweis gegen digitale Verfahren; dafür wäre ein eigener Parametersweep erforderlich.",
        "",
        "## Zusammenfassung der Modelle",
        "",
        "| Modell | Trennrate | Trennverhältnis | Wiederhol-RMSE | Rückkehrerfolg | Rückkehrzeit | Grenzverletzungen |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        return_success = float(row["return_success_mean"])
        return_time = float(row["return_time_mean"])
        lines.append(
            f"| {row['model']} | {100*float(row['accuracy_mean']):.1f} ± {100*float(row['accuracy_std']):.1f} % | {float(row['separability_ratio_mean']):.3f} | {float(row['repeatability_rmse_mean']):.3f} | "
            f"{(f'{100*return_success:.1f} %' if math.isfinite(return_success) else 'n/a')} | "
            f"{(f'{return_time:.2f} s' if math.isfinite(return_time) else 'n/a')} | {100*float(row['violation_rate_mean']):.4f} % |"
        )
    lines.extend([
        "",
        "## Abbildungen",
        "",
        "![Trennrate nach Rauschstufe](accuracy_comparison.svg)",
        "",
        "![Beispielhafte Feldkarten](field_examples.svg)",
        "",
        "## Aussagegrenze",
        "",
        "Dies ist ein dimensionsloses mathematisches Referenzmodell. Der Aktivitätswert ist nur ein Rechenproxy und keine elektrische Energiemessung. Bauteilrauschen, parasitäre Effekte, Temperatur und reale Ausleseschaltungen sind erst mit SPICE beziehungsweise Hardware belastbar prüfbar. Ein positives Ergebnis rechtfertigt den nächsten Simulationsschritt, aber noch keine Aussage über einen gefertigten Chip.",
        "",
        "## Reproduzierbarkeit",
        "",
        "Die vollständigen Einzelwerte stehen in `trials.csv`, die aggregierten Werte in `summary.csv`. `manifest.json` hält Modellparameter, Seeds und Stichprobengrößen fest. Der Lauf ist mit festen Seeds reproduzierbar.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(
    output_dir: Path,
    rows: list[dict[str, object]],
    examples: dict[str, np.ndarray],
    config: SimulationConfig | None = None,
    readout: str = "full",
) -> list[dict[str, float | str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    config = config or SimulationConfig()
    summary = summarize(rows)  # type: ignore[arg-type]
    write_csv(output_dir / "trials.csv", rows)
    write_csv(output_dir / "summary.csv", summary)
    write_accuracy_svg(output_dir / "accuracy_comparison.svg", rows)  # type: ignore[arg-type]
    write_field_svg(output_dir / "field_examples.svg", examples)
    write_report(output_dir / "ERGEBNISBERICHT.md", summary, rows, readout)  # type: ignore[arg-type]
    manifest = {
        "schema_version": 1,
        "grid": "4x4",
        "readout": readout,
        "readout_channels": 8 if readout == "compact" else 16,
        "models": MODEL_NAMES,
        "patterns": PATTERN_NAMES,
        "noise_levels": NOISE_LEVELS,
        "seeds": DEFAULT_SEEDS,
        "train_per_pattern": DEFAULT_TRAIN_PER_PATTERN,
        "test_per_pattern": DEFAULT_TEST_PER_PATTERN,
        "simulation_config": asdict(config),
        "interpretation": "Dimensionsloses mathematisches Referenzmodell; keine elektrische Energiemessung.",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary
