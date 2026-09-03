"""Vorregistrierter zeitlich-räumlicher Vergleich für das 4x4-Referenzmodell."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import hashlib
import json
import math

import numpy as np

from .feldchip_simulation import (
    DEFAULT_SEEDS,
    DEFAULT_TEST_PER_PATTERN,
    DEFAULT_TRAIN_PER_PATTERN,
    MODEL_NAMES,
    NOISE_LEVELS,
    SimulationConfig,
    compact_readout,
    laplacian_neumann,
    nearest_centroid_metrics,
    return_gain,
    write_accuracy_svg,
    write_csv,
)


SEQUENCE_NAMES = (
    "punkt_links_rechts",
    "punkt_rechts_links",
    "punkt_oben_unten",
    "punkt_unten_oben",
    "pulse_kreuzen",
    "pulse_ueberlagern",
    "gradient_aufbau",
    "gradient_abbau",
    "stoerung_mitte_nachlauf",
    "stoerung_rand_nachlauf",
)
SEQUENCE_STEPS = 80


def canonical_sequences(steps: int = SEQUENCE_STEPS) -> dict[str, np.ndarray]:
    """Erzeugt die zehn vorregistrierten idealen 4x4-Sequenzen."""
    if steps < 8:
        raise ValueError("Eine Sequenz benötigt mindestens acht Schritte")
    result = {name: np.zeros((steps, 4, 4), dtype=float) for name in SEQUENCE_NAMES}
    phase = np.linspace(0.0, 3.0, steps)

    for index, position in enumerate(np.rint(phase).astype(int)):
        result["punkt_links_rechts"][index, 1, position] = 1.0
        result["punkt_rechts_links"][index, 2, 3 - position] = 1.0
        result["punkt_oben_unten"][index, position, 1] = 1.0
        result["punkt_unten_oben"][index, 3 - position, 2] = 1.0

        result["pulse_kreuzen"][index, 1, position] += 0.8
        result["pulse_kreuzen"][index, position, 2] -= 0.8
        result["pulse_ueberlagern"][index, 2, position] += 0.8
        result["pulse_ueberlagern"][index, 2, 3 - position] += 0.8

    gradient = np.tile(np.linspace(-1.0, 1.0, 4), (4, 1))
    ramp = np.linspace(0.0, 1.0, steps)
    result["gradient_aufbau"] = ramp[:, None, None] * gradient
    result["gradient_abbau"] = ramp[::-1, None, None] * gradient

    pulse_start, pulse_end = steps // 8, steps // 4
    result["stoerung_mitte_nachlauf"][pulse_start:pulse_end, 1:3, 1:3] = 0.8
    result["stoerung_rand_nachlauf"][pulse_start:pulse_end, 0, 0] = 1.0
    return result


def distorted_sequences(
    sequence: np.ndarray,
    count: int,
    noise_sigma: float,
    rng: np.random.Generator,
    config: SimulationConfig,
) -> np.ndarray:
    samples = np.broadcast_to(sequence, (count,) + sequence.shape).copy()
    gain = rng.normal(1.0, 0.12, size=(count, 1, 1, 1))
    bias = rng.normal(0.0, 0.08, size=(count, 1, 1, 1))
    samples = gain * samples + bias
    samples += rng.normal(0.0, noise_sigma, size=samples.shape)
    dropout = rng.random(samples.shape) < config.dropout_probability
    samples[dropout] = 0.0
    return np.clip(samples, -1.5, 1.5)


def _quantize(values: np.ndarray, limit: float) -> np.ndarray:
    levels = 2**12 - 1
    return np.round((values + limit) / (2.0 * limit) * levels) / levels * (2.0 * limit) - limit


def simulate_temporal_batch(
    inputs: np.ndarray,
    model: str,
    rng: np.random.Generator,
    config: SimulationConfig,
) -> tuple[np.ndarray, dict[str, float]]:
    """Wendet ein Modell schrittweise an und gibt den gesamten Verlauf zurück."""
    if inputs.ndim != 4 or inputs.shape[2:] != (4, 4):
        raise ValueError("inputs muss die Form (n, zeit, 4, 4) besitzen")
    count, steps = inputs.shape[:2]
    output = np.empty_like(inputs)

    if model == "baseline_rohsignal":
        output[:] = np.clip(config.input_gain * inputs, -config.hard_limit, config.hard_limit)
        return output, {"violation_rate": 0.0, "activity_proxy": math.nan, "max_abs": float(np.max(np.abs(output)))}

    state = np.zeros((count, 4, 4), dtype=float)
    attempted_violations = 0
    activity = 0.0

    if model == "baseline_digital_diffusion":
        alpha, spatial = 0.35, 0.12
        for step in range(steps):
            target = np.clip(config.input_gain * inputs[:, step], -config.hard_limit, config.hard_limit)
            state += alpha * (target - state) + spatial * laplacian_neumann(state)
            state = _quantize(np.clip(state, -config.hard_limit, config.hard_limit), config.hard_limit)
            output[:, step] = state
        return output, {"violation_rate": 0.0, "activity_proxy": math.nan, "max_abs": float(np.max(np.abs(output)))}

    device_shape = (1, 4, 4)
    reference = rng.normal(0.0, config.offset_sigma, size=device_shape)
    mismatch = rng.normal(1.0, config.mismatch_sigma, size=device_shape)
    coupling = 0.0 if model == "baseline_ungekoppelt" else config.coupling
    constant_return = model in {"baseline_ungekoppelt", "baseline_linear_rc"}

    for step in range(steps):
        delta = state - reference
        gain = 0.40 if constant_return else return_gain(np.abs(delta), model, config)
        excess = np.maximum(np.abs(state) - config.soft_limit_start, 0.0)
        soft_limit = config.soft_limit_gain * np.sign(state) * excess**3
        dynamic_noise = rng.normal(0.0, config.dynamic_noise_scale, size=state.shape)
        derivative = (
            config.input_gain * inputs[:, step]
            + coupling * laplacian_neumann(state)
            - mismatch * gain * delta
            - soft_limit
            + dynamic_noise
        )
        candidate = state + config.dt * derivative
        attempted_violations += int(np.count_nonzero(np.abs(candidate) > config.hard_limit))
        activity += float(np.sum(np.abs(candidate - state)))
        state = np.clip(candidate, -config.hard_limit, config.hard_limit)
        output[:, step] = state

    updates = count * steps * 16
    return output, {
        "violation_rate": attempted_violations / max(updates, 1),
        "activity_proxy": activity / max(updates, 1),
        "max_abs": float(np.max(np.abs(output))),
    }


def temporal_readout(fields: np.ndarray) -> np.ndarray:
    """Verdichtet acht Momentanmerkmale auf Mittelwert und lineare Steigung."""
    if fields.ndim != 4 or fields.shape[2:] != (4, 4):
        raise ValueError("fields muss die Form (n, zeit, 4, 4) besitzen")
    count, steps = fields.shape[:2]
    channels = compact_readout(fields.reshape(count * steps, 4, 4)).reshape(count, steps, 8)
    time = np.linspace(-1.0, 1.0, steps)
    slopes = np.sum(channels * time[None, :, None], axis=1) / np.sum(time**2)
    return np.concatenate((np.mean(channels, axis=1), slopes), axis=1)


def run_temporal_campaign(
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    train_per_sequence: int = DEFAULT_TRAIN_PER_PATTERN,
    test_per_sequence: int = DEFAULT_TEST_PER_PATTERN,
    config: SimulationConfig | None = None,
) -> list[dict[str, float | int | str]]:
    config = config or SimulationConfig()
    sequences = canonical_sequences()
    rows: list[dict[str, float | int | str]] = []

    for seed in seeds:
        for noise_sigma in NOISE_LEVELS:
            sample_rng = np.random.default_rng(seed * 1000 + round(noise_sigma * 100))
            train_parts, test_parts, train_labels, test_labels = [], [], [], []
            for label, name in enumerate(SEQUENCE_NAMES):
                train_parts.append(distorted_sequences(sequences[name], train_per_sequence, noise_sigma, sample_rng, config))
                test_parts.append(distorted_sequences(sequences[name], test_per_sequence, noise_sigma, sample_rng, config))
                train_labels.extend([label] * train_per_sequence)
                test_labels.extend([label] * test_per_sequence)
            train_input, test_input = np.concatenate(train_parts), np.concatenate(test_parts)
            train_label_array, test_label_array = np.asarray(train_labels), np.asarray(test_labels)

            for model_index, model in enumerate(MODEL_NAMES):
                device_seed = seed * 10000 + model_index * 101
                train_fields, _ = simulate_temporal_batch(train_input, model, np.random.default_rng(device_seed), config)
                test_fields, dynamics = simulate_temporal_batch(test_input, model, np.random.default_rng(device_seed), config)
                metrics = nearest_centroid_metrics(
                    temporal_readout(train_fields), train_label_array,
                    temporal_readout(test_fields), test_label_array,
                )
                rows.append({"seed": seed, "noise_sigma": noise_sigma, "model": model, **metrics, **dynamics})
    return rows


def summarize_temporal(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | str]]:
    summary: list[dict[str, float | str]] = []
    for model in MODEL_NAMES:
        selected = [row for row in rows if row["model"] == model]
        item: dict[str, float | str] = {"model": model}
        for metric in ("accuracy", "separability_ratio", "repeatability_rmse", "violation_rate", "activity_proxy", "max_abs"):
            values = np.asarray([float(row[metric]) for row in selected])
            finite = values[np.isfinite(values)]
            item[f"{metric}_mean"] = float(np.mean(finite)) if finite.size else math.nan
            item[f"{metric}_std"] = float(np.std(finite, ddof=1)) if finite.size > 1 else math.nan
        summary.append(item)
    return summary


def paired_result(rows: list[dict[str, float | int | str]], summary: list[dict[str, float | str]]) -> dict[str, object]:
    best_field = max((row for row in summary if str(row["model"]).startswith("feld_")), key=lambda row: float(row["accuracy_mean"]))
    best_baseline = max((row for row in summary if str(row["model"]).startswith("baseline_")), key=lambda row: float(row["accuracy_mean"]))
    def values(model: str) -> dict[tuple[int, float], float]:
        return {(int(row["seed"]), float(row["noise_sigma"])): float(row["accuracy"]) for row in rows if row["model"] == model}
    field_values, baseline_values = values(str(best_field["model"])), values(str(best_baseline["model"]))
    differences = np.asarray([field_values[key] - baseline_values[key] for key in sorted(field_values)])
    mean = float(np.mean(differences))
    sem = float(np.std(differences, ddof=1) / np.sqrt(differences.size))
    low, high = mean - 1.96 * sem, mean + 1.96 * sem
    return {
        "best_field": best_field["model"], "best_baseline": best_baseline["model"],
        "difference": mean, "ci95_low": low, "ci95_high": high,
        "comparisons": int(differences.size), "success": bool(mean > 0.02 and low > 0.0),
    }


def write_temporal_outputs(output_dir: Path, rows: list[dict[str, object]], config: SimulationConfig | None = None) -> list[dict[str, float | str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    config = config or SimulationConfig()
    summary = summarize_temporal(rows)  # type: ignore[arg-type]
    paired = paired_result(rows, summary)  # type: ignore[arg-type]
    write_csv(output_dir / "trials.csv", rows)
    write_csv(output_dir / "summary.csv", summary)
    write_accuracy_svg(output_dir / "accuracy_comparison.svg", rows)  # type: ignore[arg-type]
    summary_hash = hashlib.sha256((output_dir / "summary.csv").read_bytes()).hexdigest().upper()
    trials_hash = hashlib.sha256((output_dir / "trials.csv").read_bytes()).hexdigest().upper()
    manifest = {
        "schema_version": 1, "experiment": "vorregistrierter_zeitlich_raeumlicher_hauptversuch",
        "grid": "4x4", "sequence_steps": SEQUENCE_STEPS, "readout_channels": 16,
        "models": MODEL_NAMES, "sequences": SEQUENCE_NAMES, "noise_levels": NOISE_LEVELS,
        "seeds": DEFAULT_SEEDS, "train_per_sequence": DEFAULT_TRAIN_PER_PATTERN,
        "test_per_sequence": DEFAULT_TEST_PER_PATTERN, "simulation_config": asdict(config),
        "success_rule": "Differenz > 0.02 und untere gepaarte approximative 95-%-Grenze > 0",
        "interpretation": "Dimensionsloses mathematisches Referenzmodell; keine elektrische Energiemessung.",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Ergebnisbericht: zeitlich-räumlicher Hauptversuch", "", "## Prüfziel", "",
        "Geprüft wird die vorregistrierte Frage, ob ein gekoppeltes `4×4`-Feld zehn zeitlich-räumliche Sequenzklassen unter derselben kompakten 16-Kanal-Auslese besser trennt als die beste Baseline.",
        "", "## Ergebnis", "",
        f"Beste Feldvariante: `{paired['best_field']}`. Beste Baseline: `{paired['best_baseline']}`.", "",
        f"Gepaarte Differenz: {100*float(paired['difference']):+.1f} Prozentpunkte; approximatives 95-%-Intervall {100*float(paired['ci95_low']):+.1f} bis {100*float(paired['ci95_high']):+.1f} Prozentpunkte.", "",
        ("Beide vorregistrierten Bedingungen sind erfüllt. Ein Vorteil ist in dieser Simulation vorläufig sichtbar." if paired["success"] else "Mindestens eine vorregistrierte Bedingung ist nicht erfüllt. Ein Vorteil ist in dieser Aufgabe nicht nachgewiesen."),
        "", "Die Auswahl der jeweils besten Variante war vorregistriert, enthält aber einen explorativen Auswahlanteil.",
        "", "Das ungekoppelte dynamische Array liegt in allen drei Rauschstufen vor den gekoppelten Feldvarianten. Die zeitliche Zustandsbildung ist damit in dieser Aufgabe nützlich, die zusätzliche räumliche Kopplung in der festgelegten Parametrierung jedoch nicht. Daraus folgt keine allgemeine Aussage über andere Kopplungstopologien oder Ausleseverfahren.",
        "", "## Modellübersicht", "", "| Modell | Trennrate | Trennverhältnis | Wiederhol-RMSE | Maximalbetrag |", "|---|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(f"| {row['model']} | {100*float(row['accuracy_mean']):.1f} ± {100*float(row['accuracy_std']):.1f} % | {float(row['separability_ratio_mean']):.3f} | {float(row['repeatability_rmse_mean']):.3f} | {float(row['max_abs_mean']):.3f} |")
    lines.extend([
        "", "## Abbildung", "", "![Trennrate nach Rauschstufe](accuracy_comparison.svg)",
        "", "## Aussagegrenze", "",
        "Das Ergebnis gilt nur für die festgelegten Sequenzen, Störungen, Modelle und die feste Auslese. Fertigbarkeit und elektrische Größen sind damit nicht geprüft.",
        "", "## Reproduzierbarkeit", "",
        "Die CSV-Dateien werden mit festen Seeds deterministisch erzeugt. Zwei vollständige Läufe wurden zusätzlich bitgenau verglichen.",
        "", f"- `summary.csv`: SHA-256 `{summary_hash}`",
        f"- `trials.csv`: SHA-256 `{trials_hash}`", "",
    ])
    (output_dir / "ERGEBNISBERICHT.md").write_text("\n".join(lines), encoding="utf-8")
    return summary
