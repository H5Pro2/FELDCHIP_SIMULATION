"""Vorregistrierter Bestätigungslauf für den explorativen Zeitskalenkandidaten."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import csv
import json

import numpy as np

from .feldchip_simulation import NOISE_LEVELS, SimulationConfig, nearest_centroid_metrics
from .multiscale_experiment import (
    TASK_NAMES,
    TIMESCALE_SEQUENCE_NAMES,
    TimescaleCandidate,
    canonical_timescale_sequences,
    simulate_technical_return,
    simulate_temporal_candidate,
)
from .return_experiment import CORNER_CONFIGS
from .temporal_experiment import SEQUENCE_NAMES, canonical_sequences, distorted_sequences, temporal_readout


CONFIRMATION_SEEDS = (211, 241, 277, 313, 349)
BASELINE = TimescaleCandidate("baseline_ein_zustand", 1.6, 1.6, 1.0, 1)
CANDIDATE = TimescaleCandidate("zwei_zustaende_l1.2_s2_a0.5", 1.2, 2.0, 0.5, 2)
CONFIRMATION_MODELS = (BASELINE, CANDIDATE)


def run_technical_confirmation() -> list[dict[str, float | int | str]]:
    return [
        simulate_technical_return(model, corner, seed, dt, dynamic_noise)
        for model in CONFIRMATION_MODELS
        for corner in CORNER_CONFIGS
        for seed in CONFIRMATION_SEEDS
        for dt, dynamic_noise in ((0.02, True), (0.02, False), (0.01, False))
    ]


def _technical_passes_confirmation(
    rows: list[dict[str, float | int | str]],
    model: str,
) -> bool:
    # Die Prüflogik ist identisch; nur die Seed-Anzahl wird lokal kontrolliert.
    selected = [row for row in rows if row["model"] == model]
    grouped: dict[tuple[str, int], list[dict[str, float | int | str]]] = {}
    for row in selected:
        grouped.setdefault((str(row["corner"]), int(row["seed"])), []).append(row)
    if len(grouped) != len(CORNER_CONFIGS) * len(CONFIRMATION_SEEDS):
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


def technical_confirmation_passes(rows: list[dict[str, float | int | str]]) -> bool:
    return all(_technical_passes_confirmation(rows, model.name) for model in CONFIRMATION_MODELS)


def _task_sequences(task: str) -> tuple[tuple[str, ...], dict[str, np.ndarray]]:
    if task == "kontinuitaet":
        return SEQUENCE_NAMES, canonical_sequences()
    if task == "zeitskalen":
        return TIMESCALE_SEQUENCE_NAMES, canonical_timescale_sequences()
    raise ValueError(f"Unbekannte Aufgabe: {task}")


def run_confirmation_campaign(
    technical_rows: list[dict[str, float | int | str]],
    config: SimulationConfig | None = None,
) -> list[dict[str, float | int | str]]:
    if not technical_confirmation_passes(technical_rows):
        return []
    config = config or SimulationConfig()
    rows: list[dict[str, float | int | str]] = []
    for task_index, task in enumerate(TASK_NAMES):
        names, sequences = _task_sequences(task)
        for seed in CONFIRMATION_SEEDS:
            for noise_sigma in NOISE_LEVELS:
                sample_rng = np.random.default_rng(10_000_000 + task_index * 1_000_000 + seed * 1000 + round(noise_sigma * 100))
                train_parts, test_parts, train_labels, test_labels = [], [], [], []
                for label, name in enumerate(names):
                    train_parts.append(distorted_sequences(sequences[name], 12, noise_sigma, sample_rng, config))
                    test_parts.append(distorted_sequences(sequences[name], 24, noise_sigma, sample_rng, config))
                    train_labels.extend([label] * 12)
                    test_labels.extend([label] * 24)
                train_input, test_input = np.concatenate(train_parts), np.concatenate(test_parts)
                train_label_array, test_label_array = np.asarray(train_labels), np.asarray(test_labels)
                device_seed = 10_000_000 + task_index * 1_000_000 + seed * 10000 + round(noise_sigma * 100)
                for model in CONFIRMATION_MODELS:
                    train_fields = simulate_temporal_candidate(train_input, model, np.random.default_rng(device_seed), config)
                    test_fields = simulate_temporal_candidate(test_input, model, np.random.default_rng(device_seed), config)
                    metrics = nearest_centroid_metrics(
                        temporal_readout(train_fields), train_label_array,
                        temporal_readout(test_fields), test_label_array,
                    )
                    rows.append({
                        "task": task, "seed": seed, "noise_sigma": noise_sigma,
                        "model": model.name, **metrics,
                    })
    return rows


def confirmation_metrics(rows: list[dict[str, float | int | str]]) -> dict[str, float | bool]:
    baseline = {
        (str(row["task"]), int(row["seed"]), float(row["noise_sigma"])): float(row["accuracy"])
        for row in rows if row["model"] == BASELINE.name
    }
    selected = [row for row in rows if row["model"] == CANDIDATE.name]
    differences = np.asarray([
        float(row["accuracy"]) - baseline[(str(row["task"]), int(row["seed"]), float(row["noise_sigma"]))]
        for row in selected
    ])
    if differences.size != len(TASK_NAMES) * len(CONFIRMATION_SEEDS) * len(NOISE_LEVELS):
        raise ValueError("Bestätigungsdaten sind unvollständig")
    mean = float(np.mean(differences))
    sem = float(np.std(differences, ddof=1) / np.sqrt(differences.size))
    task_means = {
        task: float(np.mean([difference for difference, row in zip(differences, selected) if row["task"] == task]))
        for task in TASK_NAMES
    }
    noise_means = {
        noise: float(np.mean([difference for difference, row in zip(differences, selected) if float(row["noise_sigma"]) == noise]))
        for noise in NOISE_LEVELS
    }
    low, high = mean - 1.96 * sem, mean + 1.96 * sem
    success = bool(
        mean > 0.02 and low > 0.0
        and all(value >= 0.0 for value in task_means.values())
        and all(value >= 0.0 for value in noise_means.values())
    )
    return {
        "advantage": mean, "standard_error": sem, "ci95_low": low, "ci95_high": high,
        "advantage_kontinuitaet": task_means["kontinuitaet"],
        "advantage_zeitskalen": task_means["zeitskalen"],
        "advantage_noise_015": noise_means[0.15], "advantage_noise_035": noise_means[0.35],
        "advantage_noise_055": noise_means[0.55], "success": success,
    }


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    output_dir: Path,
    technical_rows: list[dict[str, float | int | str]],
    task_rows: list[dict[str, float | int | str]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    technical_success = technical_confirmation_passes(technical_rows)
    _write_csv(output_dir / "technical_screen.csv", technical_rows)
    _write_csv(output_dir / "task_trials.csv", task_rows)
    metrics = confirmation_metrics(task_rows) if task_rows else None
    manifest = {
        "schema_version": 1, "experiment": "bestaetigung_mehrere_lokale_zeitskalen",
        "confirmation_seeds": CONFIRMATION_SEEDS, "noise_levels": NOISE_LEVELS,
        "tasks": TASK_NAMES, "baseline": asdict(BASELINE), "candidate": asdict(CANDIDATE),
        "technical_success": technical_success, "confirmation_metrics": metrics,
        "success_rule": "Vorsprung > 0.02, CI-Untergrenze > 0, Aufgaben- und Rauschmittel >= 0",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not technical_success:
        conclusion = "Die technische Pflichtprüfung ist fehlgeschlagen; die Aufgabenbewertung wurde nicht ausgeführt."
    elif metrics and bool(metrics["success"]):
        conclusion = "Alle vorregistrierten Bedingungen sind erfüllt. Der simulierte Vorteil ist für diese Aufgabe bestätigt."
    else:
        conclusion = "Mindestens eine vorregistrierte Bedingung ist nicht erfüllt. Der explorative Vorteil ist nicht bestätigt."
    lines = [
        "# Ergebnisbericht: Bestätigung lokaler Zeitskalen", "", "## Ergebnis", "",
        conclusion, "", "Dieser Bericht bezieht sich ausschließlich auf den vorregistrierten Kandidaten und die Ein-Zustands-Baseline.", "",
    ]
    (output_dir / "ERGEBNISBERICHT.md").write_text("\n".join(lines), encoding="utf-8")
