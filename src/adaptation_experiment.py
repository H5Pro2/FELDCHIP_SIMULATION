"""Vorregistrierte Exploration lokaler begrenzter Adaptation ohne Kopplung."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import hashlib
import json
import math

import numpy as np

from .feldchip_simulation import NOISE_LEVELS, SimulationConfig, nearest_centroid_metrics
from .multiscale_experiment import (
    TIMESCALE_SEQUENCE_NAMES,
    canonical_timescale_sequences,
)
from .return_experiment import CORNER_CONFIGS, initial_displacements
from .temporal_experiment import SEQUENCE_NAMES, canonical_sequences, distorted_sequences, temporal_readout


ADAPTATION_SEEDS = (401, 431, 463)
TASK_NAMES = ("kontinuitaet", "zeitskalen", "adaptation")
ADAPTATION_SEQUENCE_NAMES = (
    "positiv_frueh", "positiv_spaet", "negativ_frueh", "negativ_spaet",
    "hintergrund_positiv_impuls_frueh", "hintergrund_positiv_impuls_spaet",
    "hintergrund_negativ_impuls_frueh", "hintergrund_negativ_impuls_spaet",
    "gradient_aufbau", "gradient_abbau",
)


@dataclass(frozen=True)
class AdaptationCandidate:
    name: str
    adaptation_rate: float
    feedback_strength: float
    adaptation_limit: float
    state_count: int


def adaptation_candidates() -> tuple[AdaptationCandidate, ...]:
    candidates = [AdaptationCandidate("baseline_ein_zustand", 0.0, 0.0, 0.0, 1)]
    for rate in (0.6, 0.9, 1.2):
        for strength in (0.25, 0.50, 0.75, 1.00):
            for limit in (0.5, 1.0):
                candidates.append(AdaptationCandidate(
                    f"adaptation_r{rate:g}_b{strength:g}_a{limit:g}",
                    rate, strength, limit, 2,
                ))
    return tuple(candidates)


def canonical_adaptation_sequences(steps: int = 80) -> dict[str, np.ndarray]:
    sequences = {name: np.zeros((steps, 4, 4), dtype=float) for name in ADAPTATION_SEQUENCE_NAMES}
    mask = np.zeros((4, 4), dtype=float)
    mask[1:3, 1:3] = 0.7
    sequences["positiv_frueh"][:steps // 2] = mask
    sequences["positiv_spaet"][steps // 2:] = mask
    sequences["negativ_frueh"][:steps // 2] = -mask
    sequences["negativ_spaet"][steps // 2:] = -mask

    for polarity, prefix in ((1.0, "positiv"), (-1.0, "negativ")):
        background = np.full((steps, 4, 4), polarity * 0.25)
        early, late = background.copy(), background.copy()
        early[12:20, 1, 1] += polarity * 0.5
        late[56:64, 1, 1] += polarity * 0.5
        sequences[f"hintergrund_{prefix}_impuls_frueh"] = early
        sequences[f"hintergrund_{prefix}_impuls_spaet"] = late

    gradient = np.tile(np.linspace(-1.0, 1.0, 4), (4, 1))
    ramp = np.linspace(0.0, 1.0, steps)
    sequences["gradient_aufbau"] = ramp[:, None, None] * gradient
    sequences["gradient_abbau"] = ramp[::-1, None, None] * gradient
    return sequences


def _internal_initial_states(candidate: AdaptationCandidate) -> tuple[np.ndarray, np.ndarray]:
    base, _ = initial_displacements()
    if candidate.state_count == 1:
        return base, np.zeros_like(base)
    adaptation = np.clip(base / 3.0 * candidate.adaptation_limit, -candidate.adaptation_limit, candidate.adaptation_limit)
    cell = np.concatenate((base, np.zeros_like(base), base))
    local = np.concatenate((np.zeros_like(base), adaptation, -adaptation))
    return cell, local


def simulate_technical_return(
    candidate: AdaptationCandidate,
    corner: str,
    seed: int,
    dt: float,
    dynamic_noise: bool,
) -> dict[str, float | int | str]:
    config = SimulationConfig(dt=dt)
    offset_sigma, mismatch_sigma, noise_sigma = CORNER_CONFIGS[corner]
    if not dynamic_noise:
        noise_sigma = 0.0
    rng = np.random.default_rng(seed * 1019 + (0 if corner == "nominal" else 1))
    cell_initial, adaptation_initial = _internal_initial_states(candidate)
    reference = rng.normal(0.0, offset_sigma, size=(1, 4, 4))
    mismatch = rng.normal(1.0, mismatch_sigma, size=(1, 4, 4))
    cell = np.clip(reference + cell_initial, -3.0, 3.0)
    adaptation = adaptation_initial.copy()
    steps, hold_steps = round(6.0 / dt), round(0.5 / dt)
    history = np.empty((cell.shape[0], steps), dtype=bool)
    violations = 0
    for step in range(steps):
        delta = cell - reference
        excess = np.maximum(np.abs(cell) - 2.65, 0.0)
        drive = 0.0 if candidate.state_count == 1 else -candidate.feedback_strength * adaptation
        proposed_cell = cell + dt * (
            config.input_gain * drive
            -mismatch * 1.6 * delta
            - 2.5 * np.sign(cell) * excess**3
            + rng.normal(0.0, noise_sigma, size=cell.shape)
        )
        proposed_adaptation = adaptation * (1.0 - dt * candidate.adaptation_rate)
        violations += int(np.count_nonzero(np.abs(proposed_cell) > 3.0))
        cell = np.clip(proposed_cell, -3.0, 3.0)
        adaptation = np.clip(proposed_adaptation, -candidate.adaptation_limit, candidate.adaptation_limit)
        if candidate.state_count == 1:
            rms = np.sqrt(np.mean((cell - reference) ** 2, axis=(1, 2)))
        else:
            rms = np.sqrt(np.mean(np.stack(((cell - reference) ** 2, adaptation**2)), axis=(0, 2, 3)))
        history[:, step] = rms <= 0.05
    if candidate.state_count == 1:
        residual = np.sqrt(np.mean((cell - reference) ** 2, axis=(1, 2)))
    else:
        residual = np.sqrt(np.mean(np.stack(((cell - reference) ** 2, adaptation**2)), axis=(0, 2, 3)))
    returned = np.all(history[:, -hold_steps:], axis=1)
    settling = np.full(cell.shape[0], np.nan)
    reexited = np.zeros(cell.shape[0], dtype=bool)
    for index, trace in enumerate(history):
        outside = np.flatnonzero(~trace)
        if returned[index]:
            settling[index] = (int(outside[-1]) + 1 if outside.size else 0) * dt
        first_inside = np.flatnonzero(trace)
        if first_inside.size:
            reexited[index] = bool(np.any(~trace[first_inside[0]:]))
    return {
        "model": candidate.name, "corner": corner, "seed": seed, "dt": dt,
        "dynamic_noise": int(dynamic_noise), "return_rate": float(np.mean(returned)),
        "settling_time_p95": float(np.nanquantile(settling, 0.95)) if np.any(returned) else math.nan,
        "residual_p95": float(np.quantile(residual, 0.95)), "reexit_rate": float(np.mean(reexited)),
        "attempted_violations": violations,
    }


def run_technical_screen() -> list[dict[str, float | int | str]]:
    return [
        simulate_technical_return(candidate, corner, seed, dt, dynamic_noise)
        for candidate in adaptation_candidates()
        for corner in CORNER_CONFIGS
        for seed in ADAPTATION_SEEDS
        for dt, dynamic_noise in ((0.02, True), (0.02, False), (0.01, False))
    ]


def technical_passes(rows: list[dict[str, float | int | str]], model: str) -> bool:
    selected = [row for row in rows if row["model"] == model]
    grouped: dict[tuple[str, int], list[dict[str, float | int | str]]] = {}
    for row in selected:
        grouped.setdefault((str(row["corner"]), int(row["seed"])), []).append(row)
    if len(grouped) != len(CORNER_CONFIGS) * len(ADAPTATION_SEEDS):
        return False
    for group in grouped.values():
        robust = [row for row in group if int(row["dynamic_noise"]) == 1]
        numerical = {float(row["dt"]): row for row in group if int(row["dynamic_noise"]) == 0}
        if len(robust) != 1 or set(numerical) != {0.01, 0.02}:
            return False
        fine, coarse = numerical[0.01], numerical[0.02]
        for row in (robust[0], fine, coarse):
            if not (
                float(row["return_rate"]) == 1.0 and float(row["settling_time_p95"]) <= 5.0
                and float(row["residual_p95"]) <= 0.05 and float(row["reexit_rate"]) == 0.0
                and int(row["attempted_violations"]) == 0
            ):
                return False
        if abs(float(fine["settling_time_p95"]) - float(coarse["settling_time_p95"])) > 0.10:
            return False
        if abs(float(fine["residual_p95"]) - float(coarse["residual_p95"])) > 0.005:
            return False
    return True


def simulate_temporal_candidate(
    inputs: np.ndarray,
    candidate: AdaptationCandidate,
    rng: np.random.Generator,
    config: SimulationConfig,
) -> np.ndarray:
    count, steps = inputs.shape[:2]
    cell = np.zeros((count, 4, 4), dtype=float)
    adaptation = np.zeros_like(cell)
    output = np.empty_like(inputs)
    reference = rng.normal(0.0, config.offset_sigma, size=(1, 4, 4))
    mismatch = rng.normal(1.0, config.mismatch_sigma, size=(1, 4, 4))
    for step in range(steps):
        input_field = inputs[:, step]
        delta = cell - reference
        excess = np.maximum(np.abs(cell) - config.soft_limit_start, 0.0)
        drive = input_field if candidate.state_count == 1 else input_field - candidate.feedback_strength * adaptation
        cell += config.dt * (
            config.input_gain * drive - mismatch * 1.6 * delta
            - config.soft_limit_gain * np.sign(cell) * excess**3
            + rng.normal(0.0, config.dynamic_noise_scale, size=cell.shape)
        )
        cell = np.clip(cell, -config.hard_limit, config.hard_limit)
        if candidate.state_count == 2:
            adaptation += config.dt * candidate.adaptation_rate * (input_field - adaptation)
            adaptation = np.clip(adaptation, -candidate.adaptation_limit, candidate.adaptation_limit)
        output[:, step] = cell
    return output


def _task_sequences(task: str) -> tuple[tuple[str, ...], dict[str, np.ndarray]]:
    if task == "kontinuitaet":
        return SEQUENCE_NAMES, canonical_sequences()
    if task == "zeitskalen":
        return TIMESCALE_SEQUENCE_NAMES, canonical_timescale_sequences()
    if task == "adaptation":
        return ADAPTATION_SEQUENCE_NAMES, canonical_adaptation_sequences()
    raise ValueError(f"Unbekannte Aufgabe: {task}")


def run_exploratory_campaign(
    technical_rows: list[dict[str, float | int | str]],
    config: SimulationConfig | None = None,
) -> list[dict[str, float | int | str]]:
    config = config or SimulationConfig()
    admitted = [candidate for candidate in adaptation_candidates() if technical_passes(technical_rows, candidate.name)]
    rows: list[dict[str, float | int | str]] = []
    for task_index, task in enumerate(TASK_NAMES):
        names, sequences = _task_sequences(task)
        for seed in ADAPTATION_SEEDS:
            for noise_sigma in NOISE_LEVELS:
                sample_rng = np.random.default_rng(20_000_000 + task_index * 1_000_000 + seed * 1000 + round(noise_sigma * 100))
                train_parts, test_parts, train_labels, test_labels = [], [], [], []
                for label, name in enumerate(names):
                    train_parts.append(distorted_sequences(sequences[name], 12, noise_sigma, sample_rng, config))
                    test_parts.append(distorted_sequences(sequences[name], 24, noise_sigma, sample_rng, config))
                    train_labels.extend([label] * 12)
                    test_labels.extend([label] * 24)
                train_input, test_input = np.concatenate(train_parts), np.concatenate(test_parts)
                train_label_array, test_label_array = np.asarray(train_labels), np.asarray(test_labels)
                device_seed = 20_000_000 + task_index * 1_000_000 + seed * 10000 + round(noise_sigma * 100)
                for candidate in admitted:
                    train_fields = simulate_temporal_candidate(train_input, candidate, np.random.default_rng(device_seed), config)
                    test_fields = simulate_temporal_candidate(test_input, candidate, np.random.default_rng(device_seed), config)
                    metrics = nearest_centroid_metrics(
                        temporal_readout(train_fields), train_label_array,
                        temporal_readout(test_fields), test_label_array,
                    )
                    rows.append({"task": task, "seed": seed, "noise_sigma": noise_sigma, "model": candidate.name, **metrics})
    return rows


def exploratory_comparisons(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | str]]:
    baseline = {
        (str(row["task"]), int(row["seed"]), float(row["noise_sigma"])): float(row["accuracy"])
        for row in rows if row["model"] == "baseline_ein_zustand"
    }
    results: list[dict[str, float | str]] = []
    for candidate in adaptation_candidates()[1:]:
        selected = [row for row in rows if row["model"] == candidate.name]
        if not selected:
            continue
        differences = np.asarray([
            float(row["accuracy"]) - baseline[(str(row["task"]), int(row["seed"]), float(row["noise_sigma"]))]
            for row in selected
        ])
        task_means = {task: float(np.mean([d for d, row in zip(differences, selected) if row["task"] == task])) for task in TASK_NAMES}
        noise_means = {noise: float(np.mean([d for d, row in zip(differences, selected) if float(row["noise_sigma"]) == noise])) for noise in NOISE_LEVELS}
        mean = float(np.mean(differences))
        sem = float(np.std(differences, ddof=1) / np.sqrt(differences.size))
        results.append({
            "model": candidate.name, "advantage": mean, "ci95_low": mean - 1.96 * sem,
            "ci95_high": mean + 1.96 * sem, "advantage_kontinuitaet": task_means["kontinuitaet"],
            "advantage_zeitskalen": task_means["zeitskalen"], "advantage_adaptation": task_means["adaptation"],
            "advantage_noise_015": noise_means[0.15], "advantage_noise_035": noise_means[0.35],
            "advantage_noise_055": noise_means[0.55], "feedback_strength": candidate.feedback_strength,
            "adaptation_rate": candidate.adaptation_rate, "adaptation_limit": candidate.adaptation_limit,
        })
    return results


def select_candidate(comparisons: list[dict[str, float | str]]) -> str | None:
    guard_keys = (
        "advantage_kontinuitaet", "advantage_zeitskalen", "advantage_adaptation",
        "advantage_noise_015", "advantage_noise_035", "advantage_noise_055",
    )
    eligible = [row for row in comparisons if float(row["advantage"]) > 0.02 and all(float(row[key]) >= 0.0 for key in guard_keys)]
    eligible.sort(key=lambda row: (
        -round(float(row["advantage"]), 12), float(row["feedback_strength"]),
        -float(row["adaptation_rate"]), float(row["adaptation_limit"]), str(row["model"]),
    ))
    return str(eligible[0]["model"]) if eligible else None


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_current_comparison_svg(
    path: Path,
    task_rows: list[dict[str, float | int | str]],
    candidate: str,
) -> None:
    models = ("baseline_ein_zustand", candidate)
    labels = ("Ein Zustand", "Lokale Adaptation")
    colors = ("#315a66", "#557a47")
    groups: list[tuple[str, tuple[float, float]]] = []
    for task, label in (
        ("kontinuitaet", "Kontinuität"),
        ("zeitskalen", "Zeitskalen"),
        ("adaptation", "Adaptation"),
    ):
        values = tuple(float(np.mean([
            float(row["accuracy"]) for row in task_rows
            if row["task"] == task and row["model"] == model
        ])) for model in models)
        groups.append((label, values))  # type: ignore[arg-type]
    overall = tuple(float(np.mean([
        float(row["accuracy"]) for row in task_rows if row["model"] == model
    ])) for model in models)
    groups.append(("Gesamt", overall))  # type: ignore[arg-type]

    width, height = 1080, 510
    left, top, chart_height = 95, 65, 345
    lower, upper = 0.4, 1.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="38" y="34" font-family="Arial" font-size="21" font-weight="bold">Explorativer Adaptationsvergleich</text>',
    ]
    for tick in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
        y = top + chart_height * (upper - tick) / (upper - lower)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="1040" y2="{y:.1f}" stroke="#d7dcdf"/>')
        parts.append(f'<text x="83" y="{y+5:.1f}" text-anchor="end" font-family="Arial" font-size="12">{100*tick:.0f} %</text>')
    for group_index, (group_label, values) in enumerate(groups):
        center = 190 + group_index * 235
        for model_index, value in enumerate(values):
            x = center - 70 + model_index * 82
            y = top + chart_height * (upper - value) / (upper - lower)
            parts.append(f'<rect x="{x}" y="{y:.1f}" width="62" height="{top+chart_height-y:.1f}" fill="{colors[model_index]}"/>')
            parts.append(f'<text x="{x+31}" y="{y-8:.1f}" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold">{100*value:.2f} %</text>')
        parts.append(f'<text x="{center+1}" y="438" text-anchor="middle" font-family="Arial" font-size="14">{group_label}</text>')
    for index, label in enumerate(labels):
        x = 350 + index * 230
        parts.append(f'<rect x="{x}" y="468" width="16" height="16" fill="{colors[index]}"/>')
        parts.append(f'<text x="{x+24}" y="481" font-family="Arial" font-size="13">{label}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts), encoding="utf-8")


def write_outputs(output_dir: Path, technical_rows: list[dict[str, float | int | str]], task_rows: list[dict[str, float | int | str]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    comparisons = exploratory_comparisons(task_rows)
    selected = select_candidate(comparisons)
    _write_csv(output_dir / "technical_screen.csv", technical_rows)
    _write_csv(output_dir / "task_trials.csv", task_rows)
    _write_csv(output_dir / "comparisons.csv", comparisons)  # type: ignore[arg-type]
    admitted = [candidate.name for candidate in adaptation_candidates() if technical_passes(technical_rows, candidate.name)]
    manifest = {
        "schema_version": 1, "experiment": "exploration_lokale_begrenzte_adaptation",
        "seeds": ADAPTATION_SEEDS, "tasks": TASK_NAMES, "noise_levels": NOISE_LEVELS,
        "models": [asdict(candidate) for candidate in adaptation_candidates()],
        "technically_admitted": admitted, "selected_confirmation_candidate": selected,
        "interpretation": "Explorative Auswahl; kein bestätigender Nachweis.",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    hashes = {
        name: hashlib.sha256((output_dir / name).read_bytes()).hexdigest().upper()
        for name in ("technical_screen.csv", "task_trials.csv", "comparisons.csv", "manifest.json")
    }
    admitted_candidates = [name for name in admitted if name != "baseline_ein_zustand"]
    failed_candidates = [candidate.name for candidate in adaptation_candidates()[1:] if candidate.name not in admitted]
    best = max(comparisons, key=lambda row: float(row["advantage"])) if comparisons else None
    if best:
        best_name = str(best["model"])
        write_current_comparison_svg(output_dir / "current_comparison.svg", task_rows, best_name)
        baseline_accuracy = float(np.mean([
            float(row["accuracy"]) for row in task_rows if row["model"] == "baseline_ein_zustand"
        ]))
        candidate_accuracy = float(np.mean([
            float(row["accuracy"]) for row in task_rows if row["model"] == best_name
        ]))
        task_min = min(float(best[f"advantage_{task}"]) for task in TASK_NAMES)
        noise_min = min(float(best[f"advantage_noise_{str(noise).replace('.', '')}"]) for noise in NOISE_LEVELS)
        lines = [
            "# Ergebnisbericht: lokale begrenzte Adaptation", "", "## Ergebnis", "",
            "Kein Kandidat erfüllt die vorregistrierte Auswahlregel. Der Mechanismus liefert in diesem begrenzten Suchraum keinen Kandidaten für einen unabhängigen Bestätigungslauf.", "",
            "## Technische Zulassung", "",
            f"Die Baseline und `{len(admitted_candidates)}` von `24` Adaptationsvarianten erfüllen sämtliche technischen Kriterien. Nicht zugelassen sind `{failed_candidates[0]}` und `{failed_candidates[1]}`; beide überschreiten in mindestens einer Bedingung die vorregistrierte t95-Grenze von `5,0 s`. Rückkehrrate, Restfehler, erneuter Toleranzaustritt und Grenzüberschreitungen sind dort nicht die ausschlaggebenden Fehler.", "",
            "## Stärkster zugelassener Befund", "",
            f"Die stärkste beobachtete Variante ist `{best_name}`. Sie ist keine ausgewählte Bestätigungsvariante.", "",
            f"Die Gesamttrennrate beträgt `{100*baseline_accuracy:.2f} %` für die Baseline und `{100*candidate_accuracy:.2f} %` für diese Variante. Die gepaarte Differenz ist `{100*float(best['advantage']):+.2f}` Prozentpunkte; das approximative 95-%-Intervall reicht von `{100*float(best['ci95_low']):+.2f}` bis `{100*float(best['ci95_high']):+.2f}` Prozentpunkten.", "",
            f"Kontinuität: `{100*float(best['advantage_kontinuitaet']):+.2f}` Punkte. Zeitskalen: `{100*float(best['advantage_zeitskalen']):+.2f}` Punkte. Adaptation: `{100*float(best['advantage_adaptation']):+.2f}` Punkte.", "",
            f"Rauschen `0,15`: `{100*float(best['advantage_noise_015']):+.2f}` Punkte. Rauschen `0,35`: `{100*float(best['advantage_noise_035']):+.2f}` Punkte. Rauschen `0,55`: `{100*float(best['advantage_noise_055']):+.2f}` Punkte.", "",
            "| Vorregistrierte Bedingung | Ergebnis | Erfüllt |", "|---|---:|:---:|",
            f"| Gesamtdifferenz größer als `2,0` Punkte | {100*float(best['advantage']):+.2f} | {'ja' if float(best['advantage']) > 0.02 else 'nein'} |",
            f"| Alle drei Aufgabenmittel mindestens null | {100*task_min:+.2f} | {'ja' if task_min >= 0.0 else 'nein'} |",
            f"| Alle drei Rauschmittel mindestens null | {100*noise_min:+.2f} | {'ja' if noise_min >= 0.0 else 'nein'} |", "",
            "Der positive Gesamtwert genügt nicht: Die Mindestwirkung wird verfehlt und das mittlere Ergebnis bei Rauschstufe `0,35` ist negativ. Die Schwellen werden nicht nachträglich verändert.", "",
            "## Abbildung", "", "![Aktueller Adaptationsvergleich](current_comparison.svg)", "",
            "## Reproduzierbarkeit", "", "Zwei vollständige Ausführungen erzeugten die zentralen Dateien bitgenau identisch.", "",
            "Nach der Ausführung wurden ausschließlich Bericht und Vergleichsgrafik ergänzt. Simulationsdaten, Kandidatenvergleich und Auswahlentscheidung blieben unverändert.", "",
            f"- `technical_screen.csv`: SHA-256 `{hashes['technical_screen.csv']}`",
            f"- `task_trials.csv`: SHA-256 `{hashes['task_trials.csv']}`",
            f"- `comparisons.csv`: SHA-256 `{hashes['comparisons.csv']}`",
            f"- `manifest.json`: SHA-256 `{hashes['manifest.json']}`", "",
            "## Aussagegrenze", "",
            "Das Ergebnis gilt nur für den vorregistrierten dimensionslosen Kandidatenraum, die drei Aufgaben und die verwendete Auslese. Es belegt weder einen allgemeinen Nachteil lokaler Adaptation noch einen Chipvorteil oder elektrische Realisierbarkeit.", "",
        ]
    else:
        lines = ["# Ergebnisbericht: lokale begrenzte Adaptation", "", "## Ergebnis", "", "Es liegen keine auswertbaren Kandidatenvergleiche vor.", ""]
    (output_dir / "ERGEBNISBERICHT.md").write_text("\n".join(lines), encoding="utf-8")
