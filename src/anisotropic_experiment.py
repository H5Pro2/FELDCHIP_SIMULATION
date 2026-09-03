"""Vorregistrierte Exploration gerichteter und anisotroper Kopplung."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import hashlib
import json
import math

import numpy as np

from .feldchip_simulation import NOISE_LEVELS, SimulationConfig, nearest_centroid_metrics
from .return_experiment import CORNER_CONFIGS, initial_displacements
from .temporal_experiment import SEQUENCE_NAMES, canonical_sequences, distorted_sequences, temporal_readout


DEVELOPMENT_SEEDS = (101, 131, 167)


@dataclass(frozen=True)
class CouplingCandidate:
    name: str
    family: str
    up: float
    down: float
    left: float
    right: float

    @property
    def weight_sum(self) -> float:
        return self.up + self.down + self.left + self.right


def coupling_candidates() -> tuple[CouplingCandidate, ...]:
    candidates = [
        CouplingCandidate("baseline_ungekoppelt", "baseline", 0.0, 0.0, 0.0, 0.0),
        CouplingCandidate("kontrolle_isotrop_0.34", "isotrop", 0.34, 0.34, 0.34, 0.34),
    ]
    for axis in ("horizontal", "vertikal"):
        for dominant in (0.34, 0.68):
            for transverse in (0.0, 0.17):
                if axis == "horizontal":
                    weights = (transverse, transverse, dominant, dominant)
                else:
                    weights = (dominant, dominant, transverse, transverse)
                candidates.append(CouplingCandidate(
                    f"anisotrop_{axis}_d{dominant:g}_t{transverse:g}", "anisotrop", *weights
                ))
    directions = {
        "oben": ("up", "down"), "unten": ("down", "up"),
        "links": ("left", "right"), "rechts": ("right", "left"),
    }
    for direction, (preferred, opposite) in directions.items():
        for dominant in (0.34, 0.68):
            for reverse in (0.0, 0.17):
                weights = {"up": 0.17, "down": 0.17, "left": 0.17, "right": 0.17}
                weights[preferred] = dominant
                weights[opposite] = reverse
                candidates.append(CouplingCandidate(
                    f"gerichtet_{direction}_d{dominant:g}_g{reverse:g}", "gerichtet",
                    weights["up"], weights["down"], weights["left"], weights["right"],
                ))
    return tuple(candidates)


def weighted_coupling(values: np.ndarray, candidate: CouplingCandidate) -> np.ndarray:
    padded = np.pad(values, ((0, 0), (1, 1), (1, 1)), mode="edge")
    return (
        candidate.up * (padded[:, :-2, 1:-1] - values)
        + candidate.down * (padded[:, 2:, 1:-1] - values)
        + candidate.left * (padded[:, 1:-1, :-2] - values)
        + candidate.right * (padded[:, 1:-1, 2:] - values)
    )


def simulate_technical_return(
    candidate: CouplingCandidate,
    corner: str,
    seed: int,
    dt: float,
    dynamic_noise: bool,
) -> dict[str, float | int | str]:
    offset_sigma, mismatch_sigma, noise_sigma = CORNER_CONFIGS[corner]
    if not dynamic_noise:
        noise_sigma = 0.0
    rng = np.random.default_rng(seed * 1009 + (0 if corner == "nominal" else 1))
    reference = rng.normal(0.0, offset_sigma, size=(1, 4, 4))
    mismatch = rng.normal(1.0, mismatch_sigma, size=(1, 4, 4))
    displacements, _ = initial_displacements()
    state = np.clip(reference + displacements, -3.0, 3.0)
    steps, hold_steps = round(6.0 / dt), round(0.5 / dt)
    history = np.empty((state.shape[0], steps), dtype=bool)
    attempted_violations = 0

    for step in range(steps):
        delta = state - reference
        excess = np.maximum(np.abs(state) - 2.65, 0.0)
        derivative = (
            weighted_coupling(delta, candidate)
            - mismatch * 1.6 * delta
            - 2.5 * np.sign(state) * excess**3
            + rng.normal(0.0, noise_sigma, size=state.shape)
        )
        proposed = state + dt * derivative
        attempted_violations += int(np.count_nonzero(np.abs(proposed) > 3.0))
        state = np.clip(proposed, -3.0, 3.0)
        history[:, step] = np.sqrt(np.mean((state - reference) ** 2, axis=(1, 2))) <= 0.05

    residual = np.sqrt(np.mean((state - reference) ** 2, axis=(1, 2)))
    returned = np.all(history[:, -hold_steps:], axis=1)
    settling = np.full(state.shape[0], np.nan)
    reexited = np.zeros(state.shape[0], dtype=bool)
    for index, trace in enumerate(history):
        outside = np.flatnonzero(~trace)
        if returned[index]:
            settling[index] = (int(outside[-1]) + 1 if outside.size else 0) * dt
        first_inside = np.flatnonzero(trace)
        if first_inside.size:
            reexited[index] = bool(np.any(~trace[first_inside[0]:]))
    return {
        "model": candidate.name, "family": candidate.family, "corner": corner,
        "seed": seed, "dt": dt, "dynamic_noise": int(dynamic_noise),
        "return_rate": float(np.mean(returned)),
        "settling_time_p95": float(np.nanquantile(settling, 0.95)) if np.any(returned) else math.nan,
        "residual_p95": float(np.quantile(residual, 0.95)),
        "reexit_rate": float(np.mean(reexited)),
        "attempted_violations": attempted_violations,
    }


def run_technical_screen() -> list[dict[str, float | int | str]]:
    return [
        simulate_technical_return(candidate, corner, seed, dt, dynamic_noise)
        for candidate in coupling_candidates()
        for corner in CORNER_CONFIGS
        for seed in DEVELOPMENT_SEEDS
        for dt, dynamic_noise in ((0.02, True), (0.02, False), (0.01, False))
    ]


def technical_passes(rows: list[dict[str, float | int | str]], model: str) -> bool:
    selected = [row for row in rows if row["model"] == model]
    grouped: dict[tuple[str, int], list[dict[str, float | int | str]]] = {}
    for row in selected:
        grouped.setdefault((str(row["corner"]), int(row["seed"])), []).append(row)
    if len(grouped) != len(CORNER_CONFIGS) * len(DEVELOPMENT_SEEDS):
        return False
    for group in grouped.values():
        robust = [row for row in group if int(row["dynamic_noise"]) == 1]
        numerical = {float(row["dt"]): row for row in group if int(row["dynamic_noise"]) == 0}
        if len(robust) != 1 or set(numerical) != {0.01, 0.02}:
            return False
        fine, coarse = numerical[0.01], numerical[0.02]
        for row in (robust[0], fine, coarse):
            if not (
                float(row["return_rate"]) == 1.0
                and float(row["settling_time_p95"]) <= 5.0
                and float(row["residual_p95"]) <= 0.05
                and float(row["reexit_rate"]) == 0.0
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
    candidate: CouplingCandidate,
    rng: np.random.Generator,
    config: SimulationConfig,
) -> np.ndarray:
    count, steps = inputs.shape[:2]
    state = np.zeros((count, 4, 4), dtype=float)
    output = np.empty_like(inputs)
    reference = rng.normal(0.0, config.offset_sigma, size=(1, 4, 4))
    mismatch = rng.normal(1.0, config.mismatch_sigma, size=(1, 4, 4))
    for step in range(steps):
        delta = state - reference
        excess = np.maximum(np.abs(state) - config.soft_limit_start, 0.0)
        derivative = (
            config.input_gain * inputs[:, step]
            + weighted_coupling(delta, candidate)
            - mismatch * 1.6 * delta
            - config.soft_limit_gain * np.sign(state) * excess**3
            + rng.normal(0.0, config.dynamic_noise_scale, size=state.shape)
        )
        state = np.clip(state + config.dt * derivative, -config.hard_limit, config.hard_limit)
        output[:, step] = state
    return output


def run_exploratory_campaign(
    technical_rows: list[dict[str, float | int | str]],
    config: SimulationConfig | None = None,
) -> list[dict[str, float | int | str]]:
    config = config or SimulationConfig()
    sequences = canonical_sequences()
    admitted = [candidate for candidate in coupling_candidates() if technical_passes(technical_rows, candidate.name)]
    rows: list[dict[str, float | int | str]] = []
    for seed in DEVELOPMENT_SEEDS:
        for noise_sigma in NOISE_LEVELS:
            sample_rng = np.random.default_rng(seed * 1000 + round(noise_sigma * 100))
            train_parts, test_parts, train_labels, test_labels = [], [], [], []
            for label, name in enumerate(SEQUENCE_NAMES):
                train_parts.append(distorted_sequences(sequences[name], 12, noise_sigma, sample_rng, config))
                test_parts.append(distorted_sequences(sequences[name], 24, noise_sigma, sample_rng, config))
                train_labels.extend([label] * 12)
                test_labels.extend([label] * 24)
            train_input, test_input = np.concatenate(train_parts), np.concatenate(test_parts)
            train_label_array, test_label_array = np.asarray(train_labels), np.asarray(test_labels)
            device_seed = seed * 10000 + round(noise_sigma * 100)
            for candidate in admitted:
                train_fields = simulate_temporal_candidate(train_input, candidate, np.random.default_rng(device_seed), config)
                test_fields = simulate_temporal_candidate(test_input, candidate, np.random.default_rng(device_seed), config)
                metrics = nearest_centroid_metrics(
                    temporal_readout(train_fields), train_label_array,
                    temporal_readout(test_fields), test_label_array,
                )
                rows.append({
                    "seed": seed, "noise_sigma": noise_sigma, "model": candidate.name,
                    "family": candidate.family, **metrics,
                })
    return rows


def exploratory_comparisons(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | str]]:
    baseline = {
        (int(row["seed"]), float(row["noise_sigma"])): float(row["accuracy"])
        for row in rows if row["model"] == "baseline_ungekoppelt"
    }
    comparisons: list[dict[str, float | str]] = []
    for candidate in coupling_candidates():
        if candidate.family in {"baseline", "isotrop"}:
            continue
        selected = [row for row in rows if row["model"] == candidate.name]
        if not selected:
            continue
        differences = np.asarray([
            float(row["accuracy"]) - baseline[(int(row["seed"]), float(row["noise_sigma"]))]
            for row in selected
        ])
        by_noise = [
            float(np.mean([difference for difference, row in zip(differences, selected) if float(row["noise_sigma"]) == noise]))
            for noise in NOISE_LEVELS
        ]
        sem = float(np.std(differences, ddof=1) / np.sqrt(differences.size))
        comparisons.append({
            "model": candidate.name, "family": candidate.family,
            "mean_accuracy": float(np.mean([float(row["accuracy"]) for row in selected])),
            "advantage": float(np.mean(differences)),
            "ci95_low": float(np.mean(differences) - 1.96 * sem),
            "ci95_high": float(np.mean(differences) + 1.96 * sem),
            "advantage_noise_015": by_noise[0], "advantage_noise_035": by_noise[1],
            "advantage_noise_055": by_noise[2], "weight_sum": candidate.weight_sum,
        })
    return comparisons


def select_candidate(comparisons: list[dict[str, float | str]]) -> str | None:
    eligible = [row for row in comparisons if float(row["advantage"]) > 0.02 and all(
        float(row[key]) >= 0.0 for key in ("advantage_noise_015", "advantage_noise_035", "advantage_noise_055")
    )]
    family_order = {"anisotrop": 0, "gerichtet": 1}
    eligible.sort(key=lambda row: (
        -float(row["advantage"]), float(row["weight_sum"]),
        family_order[str(row["family"])], str(row["model"]),
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
    comparisons: list[dict[str, float | str]],
) -> None:
    means = {
        model: float(np.mean([float(row["accuracy"]) for row in task_rows if row["model"] == model]))
        for model in ("baseline_ungekoppelt", "kontrolle_isotrop_0.34")
    }
    best_anisotropic = max(
        (row for row in comparisons if row["family"] == "anisotrop"),
        key=lambda row: float(row["advantage"]),
    )
    best_directional = max(
        (row for row in comparisons if row["family"] == "gerichtet"),
        key=lambda row: float(row["advantage"]),
    )
    entries = (
        ("Ungekoppelte Baseline", means["baseline_ungekoppelt"], "#2f5964"),
        ("Isotroper Kontrollfall", means["kontrolle_isotrop_0.34"], "#8b6f47"),
        ("Beste Anisotropie", float(best_anisotropic["mean_accuracy"]), "#537a4b"),
        ("Beste gerichtete Kopplung", float(best_directional["mean_accuracy"]), "#8a4f63"),
    )
    width, height = 920, 500
    chart_left, chart_top, chart_height = 100, 70, 315
    lower, upper = 0.75, 1.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="40" y="36" font-family="Arial" font-size="21" font-weight="bold">Aktueller Architekturvergleich</text>',
    ]
    for tick in (0.75, 0.80, 0.85, 0.90, 0.95, 1.00):
        y = chart_top + chart_height * (upper - tick) / (upper - lower)
        parts.append(f'<line x1="{chart_left}" y1="{y:.1f}" x2="880" y2="{y:.1f}" stroke="#d7dcdf"/>')
        parts.append(f'<text x="88" y="{y+5:.1f}" text-anchor="end" font-family="Arial" font-size="12">{100*tick:.0f} %</text>')
    for index, (label, value, color) in enumerate(entries):
        x = 145 + index * 185
        y = chart_top + chart_height * (upper - value) / (upper - lower)
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="92" height="{chart_top+chart_height-y:.1f}" fill="{color}"/>')
        parts.append(f'<text x="{x+46}" y="{y-10:.1f}" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold">{100*value:.2f} %</text>')
        for line, word in enumerate(label.split()):
            parts.append(f'<text x="{x+46}" y="{415+line*17}" text-anchor="middle" font-family="Arial" font-size="12">{word}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts), encoding="utf-8")


def write_outputs(
    output_dir: Path,
    technical_rows: list[dict[str, float | int | str]],
    task_rows: list[dict[str, float | int | str]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    comparisons = exploratory_comparisons(task_rows)
    selected = select_candidate(comparisons)
    _write_csv(output_dir / "technical_screen.csv", technical_rows)
    _write_csv(output_dir / "task_trials.csv", task_rows)
    _write_csv(output_dir / "comparisons.csv", comparisons)  # type: ignore[arg-type]
    write_current_comparison_svg(output_dir / "current_comparison.svg", task_rows, comparisons)
    admitted = [candidate.name for candidate in coupling_candidates() if technical_passes(technical_rows, candidate.name)]
    manifest = {
        "schema_version": 1, "experiment": "exploration_gerichtete_anisotrope_kopplung",
        "development_seeds": DEVELOPMENT_SEEDS, "noise_levels": NOISE_LEVELS,
        "models": [asdict(candidate) for candidate in coupling_candidates()],
        "technically_admitted": admitted, "selected_confirmation_candidate": selected,
        "interpretation": "Explorative Auswahl; kein bestätigender Nachweis.",
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    hashes = {
        name: hashlib.sha256((output_dir / name).read_bytes()).hexdigest().upper()
        for name in ("technical_screen.csv", "task_trials.csv", "comparisons.csv", "manifest.json")
    }
    baseline_rows = [row for row in task_rows if row["model"] == "baseline_ungekoppelt"]
    isotropic_rows = [row for row in task_rows if row["model"] == "kontrolle_isotrop_0.34"]
    baseline_accuracy = float(np.mean([float(row["accuracy"]) for row in baseline_rows]))
    isotropic_accuracy = float(np.mean([float(row["accuracy"]) for row in isotropic_rows]))
    best_by_family = {
        family: max((row for row in comparisons if row["family"] == family), key=lambda row: float(row["advantage"]))
        for family in ("anisotrop", "gerichtet")
    }
    technical_max_settling = max(float(row["settling_time_p95"]) for row in technical_rows)
    technical_max_residual = max(float(row["residual_p95"]) for row in technical_rows)
    violations = sum(int(row["attempted_violations"]) for row in technical_rows)
    lines = [
        "# Ergebnisbericht: gerichtete und anisotrope Kopplung", "",
        "## Technische Zulassung", "",
        f"Von 26 Modellen sind `{len(admitted)}` technisch zugelassen. Die schlechteste 95-%-Einschwingzeit beträgt `{technical_max_settling:.3f} s`, der größte 95-%-Restfehler `{technical_max_residual:.5f}`. Insgesamt traten `{violations}` versuchte Grenzüberschreitungen auf.", "",
        "## Explorative Auswahl", "",
        (f"Nach der vorregistrierten Regel wurde `{selected}` als Kandidat für einen späteren Bestätigungslauf ausgewählt." if selected else "Kein Modell erfüllt die vorregistrierten Bedingungen für einen späteren Bestätigungslauf."),
        "", f"Die ungekoppelte Pflichtbaseline erreicht `{100*baseline_accuracy:.2f} %`. Der isotrope Kontrollfall erreicht `{100*isotropic_accuracy:.2f} %` und liegt damit `{100*(isotropic_accuracy-baseline_accuracy):+.2f}` Prozentpunkte relativ zur Baseline.",
        "", "| Familie | bestes Modell | Trennrate | Differenz zur Baseline | approximatives 95-%-Intervall |", "|---|---|---:|---:|---:|",
    ]
    for family in ("anisotrop", "gerichtet"):
        row = best_by_family[family]
        lines.append(
            f"| {family} | `{row['model']}` | {100*float(row['mean_accuracy']):.2f} % | "
            f"{100*float(row['advantage']):+.2f} Punkte | {100*float(row['ci95_low']):+.2f} bis {100*float(row['ci95_high']):+.2f} Punkte |"
        )
    lines.extend([
        "", "Auch die jeweils besten neuen Modelle liegen bei jeder einzelnen Rauschstufe im Mittel unter der Baseline. Der Mechanismus liefert in diesem festgelegten Aufgaben- und Ausleseschema daher kein Signal für einen Bestätigungslauf.",
        "", "## Abbildung", "", "![Aktueller Architekturvergleich](current_comparison.svg)",
        "", "## Reproduzierbarkeit", "",
        "Zwei vollständige Ausführungen erzeugten die zentralen Dateien bitgenau identisch.", "",
        f"- `technical_screen.csv`: SHA-256 `{hashes['technical_screen.csv']}`",
        f"- `task_trials.csv`: SHA-256 `{hashes['task_trials.csv']}`",
        f"- `comparisons.csv`: SHA-256 `{hashes['comparisons.csv']}`",
        f"- `manifest.json`: SHA-256 `{hashes['manifest.json']}`",
        "", "## Aussagegrenze", "",
        "Das Ergebnis ist explorativ und gilt nur für den festgelegten Kandidatenraum, die zehn Sequenzklassen und die gemeinsame Auslese. Es bestätigt keinen allgemeinen Verarbeitungsvorteil und macht keine Aussage über elektrische Realisierbarkeit.", "",
    ])
    (output_dir / "ERGEBNISBERICHT.md").write_text("\n".join(lines), encoding="utf-8")
