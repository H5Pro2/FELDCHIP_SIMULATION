"""Vorregistrierte Exploration mehrerer lokaler Zeitskalen ohne Kopplung."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math

import numpy as np

from .anisotropic_experiment import DEVELOPMENT_SEEDS
from .feldchip_simulation import NOISE_LEVELS, SimulationConfig, nearest_centroid_metrics
from .return_experiment import CORNER_CONFIGS, initial_displacements
from .temporal_experiment import SEQUENCE_NAMES, canonical_sequences, distorted_sequences, temporal_readout


TASK_NAMES = ("kontinuitaet", "zeitskalen")
TIMESCALE_SEQUENCE_NAMES = (
    "pulsabstand_kurz", "pulsabstand_lang", "impuls_frueh", "impuls_spaet",
    "impuls_kurz_stark", "impuls_lang_schwach", "wechsel_schnell",
    "wechsel_langsam", "gradient_aufbau", "gradient_abbau",
)


@dataclass(frozen=True)
class TimescaleCandidate:
    name: str
    slow_rate: float
    fast_rate: float
    fast_weight: float
    state_count: int

    @property
    def rate_ratio(self) -> float:
        return self.fast_rate / self.slow_rate


def timescale_candidates() -> tuple[TimescaleCandidate, ...]:
    candidates = [TimescaleCandidate("baseline_ein_zustand", 1.6, 1.6, 1.0, 1)]
    for slow in (0.8, 1.0, 1.2):
        for fast in (2.0, 3.2, 4.8):
            for weight in (0.25, 0.50, 0.75):
                candidates.append(TimescaleCandidate(
                    f"zwei_zustaende_l{slow:g}_s{fast:g}_a{weight:g}",
                    slow, fast, weight, 2,
                ))
    return tuple(candidates)


def canonical_timescale_sequences(steps: int = 80) -> dict[str, np.ndarray]:
    sequences = {name: np.zeros((steps, 4, 4), dtype=float) for name in TIMESCALE_SEQUENCE_NAMES}
    center = (1, 1)
    for start in (12, 22):
        sequences["pulsabstand_kurz"][start:start + 5, center[0], center[1]] = 1.0
    for start in (8, 50):
        sequences["pulsabstand_lang"][start:start + 5, center[0], center[1]] = 1.0
    sequences["impuls_frueh"][8:18, 0, 3] = 1.0
    sequences["impuls_spaet"][58:68, 0, 3] = 1.0
    sequences["impuls_kurz_stark"][24:32, 2, 2] = 1.0
    sequences["impuls_lang_schwach"][20:36, 2, 2] = 0.5
    checker = np.fromfunction(lambda row, col: (-1.0) ** (row + col), (4, 4))
    for step in range(steps):
        sequences["wechsel_schnell"][step] = (1.0 if (step // 4) % 2 == 0 else -1.0) * 0.35 * checker
        sequences["wechsel_langsam"][step] = (1.0 if (step // 16) % 2 == 0 else -1.0) * 0.35 * checker
    gradient = np.tile(np.linspace(-1.0, 1.0, 4), (4, 1))
    ramp = np.linspace(0.0, 1.0, steps)
    sequences["gradient_aufbau"] = ramp[:, None, None] * gradient
    sequences["gradient_abbau"] = ramp[::-1, None, None] * gradient
    return sequences


def _internal_displacements(state_count: int) -> np.ndarray:
    base, _ = initial_displacements()
    if state_count == 1:
        return base[:, None, :, :]
    common = np.stack((base, base), axis=1)
    opposing = np.stack((base, -base), axis=1)
    return np.concatenate((common, opposing))


def simulate_technical_return(
    candidate: TimescaleCandidate,
    corner: str,
    seed: int,
    dt: float,
    dynamic_noise: bool,
) -> dict[str, float | int | str]:
    offset_sigma, mismatch_sigma, noise_sigma = CORNER_CONFIGS[corner]
    if not dynamic_noise:
        noise_sigma = 0.0
    rng = np.random.default_rng(seed * 1013 + (0 if corner == "nominal" else 1))
    channels = candidate.state_count
    reference = rng.normal(0.0, offset_sigma, size=(1, channels, 4, 4))
    mismatch = rng.normal(1.0, mismatch_sigma, size=(1, channels, 4, 4))
    state = np.clip(reference + _internal_displacements(channels), -3.0, 3.0)
    rates = np.asarray([candidate.fast_rate] if channels == 1 else [candidate.slow_rate, candidate.fast_rate])[None, :, None, None]
    steps, hold_steps = round(6.0 / dt), round(0.5 / dt)
    history = np.empty((state.shape[0], steps), dtype=bool)
    attempted_violations = 0
    for step in range(steps):
        delta = state - reference
        excess = np.maximum(np.abs(state) - 2.65, 0.0)
        derivative = (
            -mismatch * rates * delta
            - 2.5 * np.sign(state) * excess**3
            + rng.normal(0.0, noise_sigma, size=state.shape)
        )
        proposed = state + dt * derivative
        attempted_violations += int(np.count_nonzero(np.abs(proposed) > 3.0))
        state = np.clip(proposed, -3.0, 3.0)
        history[:, step] = np.sqrt(np.mean((state - reference) ** 2, axis=(1, 2, 3))) <= 0.05
    residual = np.sqrt(np.mean((state - reference) ** 2, axis=(1, 2, 3)))
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
        "model": candidate.name, "corner": corner, "seed": seed, "dt": dt,
        "dynamic_noise": int(dynamic_noise), "return_rate": float(np.mean(returned)),
        "settling_time_p95": float(np.nanquantile(settling, 0.95)) if np.any(returned) else math.nan,
        "residual_p95": float(np.quantile(residual, 0.95)),
        "reexit_rate": float(np.mean(reexited)), "attempted_violations": attempted_violations,
    }


def run_technical_screen() -> list[dict[str, float | int | str]]:
    return [
        simulate_technical_return(candidate, corner, seed, dt, dynamic_noise)
        for candidate in timescale_candidates()
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
    candidate: TimescaleCandidate,
    rng: np.random.Generator,
    config: SimulationConfig,
) -> np.ndarray:
    count, steps = inputs.shape[:2]
    channels = candidate.state_count
    state = np.zeros((channels, count, 4, 4), dtype=float)
    output = np.empty_like(inputs)
    reference = rng.normal(0.0, config.offset_sigma, size=(2, 1, 4, 4))[:channels]
    mismatch = rng.normal(1.0, config.mismatch_sigma, size=(2, 1, 4, 4))[:channels]
    rates = np.asarray([candidate.fast_rate] if channels == 1 else [candidate.slow_rate, candidate.fast_rate])[:, None, None, None]
    for step in range(steps):
        delta = state - reference
        excess = np.maximum(np.abs(state) - config.soft_limit_start, 0.0)
        derivative = (
            config.input_gain * inputs[:, step][None, :, :, :]
            - mismatch * rates * delta
            - config.soft_limit_gain * np.sign(state) * excess**3
            + rng.normal(0.0, config.dynamic_noise_scale, size=(2, count, 4, 4))[:channels]
        )
        state = np.clip(state + config.dt * derivative, -config.hard_limit, config.hard_limit)
        output[:, step] = state[0] if channels == 1 else (
            (1.0 - candidate.fast_weight) * state[0] + candidate.fast_weight * state[1]
        )
    return output


def _task_sequences(task: str) -> tuple[tuple[str, ...], dict[str, np.ndarray]]:
    if task == "kontinuitaet":
        return SEQUENCE_NAMES, canonical_sequences()
    if task == "zeitskalen":
        return TIMESCALE_SEQUENCE_NAMES, canonical_timescale_sequences()
    raise ValueError(f"Unbekannte Aufgabe: {task}")


def run_exploratory_campaign(
    technical_rows: list[dict[str, float | int | str]],
    config: SimulationConfig | None = None,
) -> list[dict[str, float | int | str]]:
    config = config or SimulationConfig()
    admitted = [candidate for candidate in timescale_candidates() if technical_passes(technical_rows, candidate.name)]
    rows: list[dict[str, float | int | str]] = []
    for task_index, task in enumerate(TASK_NAMES):
        names, sequences = _task_sequences(task)
        for seed in DEVELOPMENT_SEEDS:
            for noise_sigma in NOISE_LEVELS:
                sample_rng = np.random.default_rng(task_index * 1_000_000 + seed * 1000 + round(noise_sigma * 100))
                train_parts, test_parts, train_labels, test_labels = [], [], [], []
                for label, name in enumerate(names):
                    train_parts.append(distorted_sequences(sequences[name], 12, noise_sigma, sample_rng, config))
                    test_parts.append(distorted_sequences(sequences[name], 24, noise_sigma, sample_rng, config))
                    train_labels.extend([label] * 12)
                    test_labels.extend([label] * 24)
                train_input, test_input = np.concatenate(train_parts), np.concatenate(test_parts)
                train_label_array, test_label_array = np.asarray(train_labels), np.asarray(test_labels)
                device_seed = task_index * 1_000_000 + seed * 10000 + round(noise_sigma * 100)
                for candidate in admitted:
                    train_fields = simulate_temporal_candidate(train_input, candidate, np.random.default_rng(device_seed), config)
                    test_fields = simulate_temporal_candidate(test_input, candidate, np.random.default_rng(device_seed), config)
                    metrics = nearest_centroid_metrics(
                        temporal_readout(train_fields), train_label_array,
                        temporal_readout(test_fields), test_label_array,
                    )
                    rows.append({
                        "task": task, "seed": seed, "noise_sigma": noise_sigma,
                        "model": candidate.name, **metrics,
                    })
    return rows


def exploratory_comparisons(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | str]]:
    baseline = {
        (str(row["task"]), int(row["seed"]), float(row["noise_sigma"])): float(row["accuracy"])
        for row in rows if row["model"] == "baseline_ein_zustand"
    }
    results: list[dict[str, float | str]] = []
    for candidate in timescale_candidates()[1:]:
        selected = [row for row in rows if row["model"] == candidate.name]
        if not selected:
            continue
        differences = np.asarray([
            float(row["accuracy"]) - baseline[(str(row["task"]), int(row["seed"]), float(row["noise_sigma"]))]
            for row in selected
        ])
        task_means = {
            task: float(np.mean([difference for difference, row in zip(differences, selected) if row["task"] == task]))
            for task in TASK_NAMES
        }
        noise_means = {
            noise: float(np.mean([difference for difference, row in zip(differences, selected) if float(row["noise_sigma"]) == noise]))
            for noise in NOISE_LEVELS
        }
        sem = float(np.std(differences, ddof=1) / np.sqrt(differences.size))
        mean = float(np.mean(differences))
        results.append({
            "model": candidate.name, "mean_accuracy": float(np.mean([float(row["accuracy"]) for row in selected])),
            "advantage": mean, "ci95_low": mean - 1.96 * sem, "ci95_high": mean + 1.96 * sem,
            "advantage_kontinuitaet": task_means["kontinuitaet"],
            "advantage_zeitskalen": task_means["zeitskalen"],
            "advantage_noise_015": noise_means[0.15], "advantage_noise_035": noise_means[0.35],
            "advantage_noise_055": noise_means[0.55], "rate_ratio": candidate.rate_ratio,
            "slow_weight": 1.0 - candidate.fast_weight,
        })
    return results


def select_candidate(comparisons: list[dict[str, float | str]]) -> str | None:
    eligible = [row for row in comparisons if float(row["advantage"]) > 0.02 and all(
        float(row[key]) >= 0.0 for key in (
            "advantage_kontinuitaet", "advantage_zeitskalen", "advantage_noise_015",
            "advantage_noise_035", "advantage_noise_055",
        )
    )]
    eligible.sort(key=lambda row: (
        -float(row["advantage"]), float(row["rate_ratio"]),
        -float(row["slow_weight"]), str(row["model"]),
    ))
    return str(eligible[0]["model"]) if eligible else None


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
    comparisons = exploratory_comparisons(task_rows)
    selected = select_candidate(comparisons)
    _write_csv(output_dir / "technical_screen.csv", technical_rows)
    _write_csv(output_dir / "task_trials.csv", task_rows)
    _write_csv(output_dir / "comparisons.csv", comparisons)  # type: ignore[arg-type]
    admitted = [candidate.name for candidate in timescale_candidates() if technical_passes(technical_rows, candidate.name)]
    manifest = {
        "schema_version": 1, "experiment": "exploration_mehrere_lokale_zeitskalen",
        "development_seeds": DEVELOPMENT_SEEDS, "noise_levels": NOISE_LEVELS,
        "tasks": TASK_NAMES, "models": [asdict(candidate) for candidate in timescale_candidates()],
        "technically_admitted": admitted, "selected_confirmation_candidate": selected,
        "interpretation": "Explorative Auswahl; kein bestätigender Nachweis.",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Ergebnisbericht: mehrere lokale Zeitskalen", "", "## Technische Zulassung", "",
        f"Von 28 Modellen sind `{len(admitted)}` technisch zugelassen.", "",
        "## Explorative Auswahl", "",
        (f"`{selected}` wurde als Kandidat für einen späteren Bestätigungslauf ausgewählt." if selected else "Kein Modell erfüllt die vorregistrierte Auswahlregel."),
        "", "Das Ergebnis ist explorativ und bestätigt keinen Verarbeitungsvorteil.", "",
    ]
    (output_dir / "ERGEBNISBERICHT.md").write_text("\n".join(lines), encoding="utf-8")
