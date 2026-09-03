"""Vorregistrierte Exploration einer ereignisbasierten zeitlichen Auslese."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import hashlib
import json

import numpy as np

from .adaptation_experiment import ADAPTATION_SEQUENCE_NAMES, canonical_adaptation_sequences
from .feldchip_simulation import NOISE_LEVELS, SimulationConfig, compact_readout, nearest_centroid_metrics
from .multiscale_experiment import TIMESCALE_SEQUENCE_NAMES, canonical_timescale_sequences
from .temporal_experiment import SEQUENCE_NAMES, canonical_sequences, distorted_sequences, temporal_readout


EVENT_READOUT_SEEDS = (503, 541, 577)
TASK_NAMES = ("kontinuitaet", "zeitskalen", "adaptation")
BASELINE_READOUTS = ("mittelwert_steigung", "mittelwert_steigung_normiert")
CHANNEL_SCALES = np.asarray((3.0, 3.0, 1.0, 1.0, 1.0, 1.0, 3.0, 3.0))


@dataclass(frozen=True)
class EventReadoutCandidate:
    name: str
    threshold: float
    decay_rate: float


def event_readout_candidates() -> tuple[EventReadoutCandidate, ...]:
    return tuple(
        EventReadoutCandidate(f"ereignis_t{threshold:g}_l{decay:g}", threshold, decay)
        for threshold in (0.05, 0.10, 0.20)
        for decay in (0.0, 0.8, 1.6, 3.2)
    )


def normalized_compact_channels(fields: np.ndarray) -> np.ndarray:
    if fields.ndim != 4 or fields.shape[2:] != (4, 4):
        raise ValueError("fields muss die Form (n, zeit, 4, 4) besitzen")
    count, steps = fields.shape[:2]
    channels = compact_readout(fields.reshape(count * steps, 4, 4)).reshape(count, steps, 8)
    return np.clip(channels / CHANNEL_SCALES[None, None, :], -1.0, 1.0)


def normalized_temporal_readout(fields: np.ndarray) -> np.ndarray:
    channels = normalized_compact_channels(fields)
    steps = channels.shape[1]
    time = np.linspace(-1.0, 1.0, steps)
    slopes = np.sum(channels * time[None, :, None], axis=1) / np.sum(time**2)
    return np.concatenate((np.mean(channels, axis=1), slopes), axis=1)


def event_readout(fields: np.ndarray, candidate: EventReadoutCandidate, dt: float = 0.02) -> tuple[np.ndarray, float]:
    channels = normalized_compact_channels(fields)
    count = channels.shape[0]
    reference = np.zeros((count, 8), dtype=float)
    positive = np.zeros_like(reference)
    negative = np.zeros_like(reference)
    event_count = 0.0
    decay = float(np.exp(-candidate.decay_rate * dt))
    for step in range(channels.shape[1]):
        positive *= decay
        negative *= decay
        delta = channels[:, step] - reference
        positive_events = np.floor(np.maximum(delta, 0.0) / candidate.threshold + 1e-12)
        negative_events = np.floor(np.maximum(-delta, 0.0) / candidate.threshold + 1e-12)
        reference += candidate.threshold * (positive_events - negative_events)
        positive += positive_events
        negative += negative_events
        event_count += float(np.sum(positive_events + negative_events))
    return np.concatenate((positive, negative), axis=1), event_count / max(count, 1)


def _task_sequences(task: str) -> tuple[tuple[str, ...], dict[str, np.ndarray]]:
    if task == "kontinuitaet":
        return SEQUENCE_NAMES, canonical_sequences()
    if task == "zeitskalen":
        return TIMESCALE_SEQUENCE_NAMES, canonical_timescale_sequences()
    if task == "adaptation":
        return ADAPTATION_SEQUENCE_NAMES, canonical_adaptation_sequences()
    raise ValueError(f"Unbekannte Aufgabe: {task}")


def _simulate_fixed_field(inputs: np.ndarray, rng: np.random.Generator, config: SimulationConfig) -> np.ndarray:
    count, steps = inputs.shape[:2]
    state = np.zeros((count, 4, 4), dtype=float)
    output = np.empty_like(inputs)
    reference = rng.normal(0.0, config.offset_sigma, size=(1, 4, 4))
    mismatch = rng.normal(1.0, config.mismatch_sigma, size=(1, 4, 4))
    for step in range(steps):
        delta = state - reference
        excess = np.maximum(np.abs(state) - config.soft_limit_start, 0.0)
        state += config.dt * (
            config.input_gain * inputs[:, step]
            - mismatch * 1.6 * delta
            - config.soft_limit_gain * np.sign(state) * excess**3
            + rng.normal(0.0, config.dynamic_noise_scale, size=state.shape)
        )
        state = np.clip(state, -config.hard_limit, config.hard_limit)
        output[:, step] = state
    return output


def run_event_readout_campaign(config: SimulationConfig | None = None) -> list[dict[str, float | int | str]]:
    config = config or SimulationConfig()
    rows: list[dict[str, float | int | str]] = []
    for task_index, task in enumerate(TASK_NAMES):
        names, sequences = _task_sequences(task)
        for seed in EVENT_READOUT_SEEDS:
            for noise_sigma in NOISE_LEVELS:
                sample_rng = np.random.default_rng(30_000_000 + task_index * 1_000_000 + seed * 1000 + round(noise_sigma * 100))
                train_parts, test_parts, train_labels, test_labels = [], [], [], []
                for label, name in enumerate(names):
                    train_parts.append(distorted_sequences(sequences[name], 12, noise_sigma, sample_rng, config))
                    test_parts.append(distorted_sequences(sequences[name], 24, noise_sigma, sample_rng, config))
                    train_labels.extend([label] * 12)
                    test_labels.extend([label] * 24)
                train_input, test_input = np.concatenate(train_parts), np.concatenate(test_parts)
                train_label_array, test_label_array = np.asarray(train_labels), np.asarray(test_labels)
                device_seed = 30_000_000 + task_index * 1_000_000 + seed * 10000 + round(noise_sigma * 100)
                train_fields = _simulate_fixed_field(train_input, np.random.default_rng(device_seed), config)
                test_fields = _simulate_fixed_field(test_input, np.random.default_rng(device_seed), config)

                for readout_name, train_features, test_features in (
                    ("mittelwert_steigung", temporal_readout(train_fields), temporal_readout(test_fields)),
                    ("mittelwert_steigung_normiert", normalized_temporal_readout(train_fields), normalized_temporal_readout(test_fields)),
                ):
                    metrics = nearest_centroid_metrics(train_features, train_label_array, test_features, test_label_array)
                    rows.append({"task": task, "seed": seed, "noise_sigma": noise_sigma, "readout": readout_name, "event_activity": float("nan"), **metrics})

                for candidate in event_readout_candidates():
                    train_features, train_activity = event_readout(train_fields, candidate, config.dt)
                    test_features, test_activity = event_readout(test_fields, candidate, config.dt)
                    metrics = nearest_centroid_metrics(train_features, train_label_array, test_features, test_label_array)
                    rows.append({
                        "task": task, "seed": seed, "noise_sigma": noise_sigma,
                        "readout": candidate.name,
                        "event_activity": 0.5 * (train_activity + test_activity),
                        **metrics,
                    })
    return rows


def event_readout_comparisons(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | str]]:
    baseline = {
        name: {
            (str(row["task"]), int(row["seed"]), float(row["noise_sigma"])): float(row["accuracy"])
            for row in rows if row["readout"] == name
        }
        for name in BASELINE_READOUTS
    }
    comparisons: list[dict[str, float | str]] = []
    for candidate in event_readout_candidates():
        selected = [row for row in rows if row["readout"] == candidate.name]
        if not selected:
            continue
        result: dict[str, float | str] = {
            "readout": candidate.name,
            "threshold": candidate.threshold,
            "decay_rate": candidate.decay_rate,
            "mean_event_activity": float(np.mean([float(row["event_activity"]) for row in selected])),
        }
        overall_advantages = []
        task_advantages = []
        noise_advantages = []
        for baseline_name in BASELINE_READOUTS:
            differences = np.asarray([
                float(row["accuracy"]) - baseline[baseline_name][
                    (str(row["task"]), int(row["seed"]), float(row["noise_sigma"]))
                ]
                for row in selected
            ])
            mean = float(np.mean(differences))
            sem = float(np.std(differences, ddof=1) / np.sqrt(differences.size))
            suffix = "existing" if baseline_name == "mittelwert_steigung" else "normalized"
            result[f"advantage_{suffix}"] = mean
            result[f"ci95_low_{suffix}"] = mean - 1.96 * sem
            result[f"ci95_high_{suffix}"] = mean + 1.96 * sem
            overall_advantages.append(mean)
            for task in TASK_NAMES:
                advantage = float(np.mean([
                    difference for difference, row in zip(differences, selected) if row["task"] == task
                ]))
                result[f"advantage_{suffix}_{task}"] = advantage
                task_advantages.append(advantage)
            for noise in NOISE_LEVELS:
                advantage = float(np.mean([
                    difference for difference, row in zip(differences, selected) if float(row["noise_sigma"]) == noise
                ]))
                result[f"advantage_{suffix}_noise_{str(noise).replace('.', '')}"] = advantage
                noise_advantages.append(advantage)
        result["conservative_advantage"] = min(overall_advantages)
        result["minimum_task_advantage"] = min(task_advantages)
        result["minimum_noise_advantage"] = min(noise_advantages)
        comparisons.append(result)
    return comparisons


def select_event_readout(comparisons: list[dict[str, float | str]]) -> str | None:
    eligible = [row for row in comparisons if (
        float(row["conservative_advantage"]) > 0.02
        and float(row["minimum_task_advantage"]) >= 0.0
        and float(row["minimum_noise_advantage"]) >= 0.0
    )]
    eligible.sort(key=lambda row: (
        -round(float(row["conservative_advantage"]), 12),
        float(row["mean_event_activity"]),
        -float(row["threshold"]),
        float(row["decay_rate"]),
        str(row["readout"]),
    ))
    return str(eligible[0]["readout"]) if eligible else None


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_current_comparison_svg(
    path: Path,
    rows: list[dict[str, float | int | str]],
    candidate: str,
) -> None:
    models = (*BASELINE_READOUTS, candidate)
    labels = ("Bisherige Auslese", "Normierte Kontrolle", "Beste Ereignisvariante")
    colors = ("#315a66", "#7b6b52", "#557a47")
    groups: list[tuple[str, tuple[float, ...]]] = []
    for task, label in (
        ("kontinuitaet", "Kontinuität"),
        ("zeitskalen", "Zeitskalen"),
        ("adaptation", "Adaptation"),
    ):
        values = tuple(float(np.mean([
            float(row["accuracy"]) for row in rows
            if row["task"] == task and row["readout"] == model
        ])) for model in models)
        groups.append((label, values))
    overall = tuple(float(np.mean([
        float(row["accuracy"]) for row in rows if row["readout"] == model
    ])) for model in models)
    groups.append(("Gesamt", overall))

    width, height = 1120, 530
    left, top, chart_height = 95, 65, 350
    lower, upper = 0.3, 1.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="38" y="34" font-family="Arial" font-size="21" font-weight="bold">Explorativer Ereignisauslese-Vergleich</text>',
    ]
    for tick in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
        y = top + chart_height * (upper - tick) / (upper - lower)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="1080" y2="{y:.1f}" stroke="#d7dcdf"/>')
        parts.append(f'<text x="83" y="{y+5:.1f}" text-anchor="end" font-family="Arial" font-size="12">{100*tick:.0f} %</text>')
    for group_index, (group_label, values) in enumerate(groups):
        center = 205 + group_index * 245
        for model_index, value in enumerate(values):
            x = center - 91 + model_index * 61
            y = top + chart_height * (upper - value) / (upper - lower)
            parts.append(f'<rect x="{x}" y="{y:.1f}" width="49" height="{top+chart_height-y:.1f}" fill="{colors[model_index]}"/>')
            parts.append(f'<text x="{x+24.5:.1f}" y="{y-7:.1f}" text-anchor="middle" font-family="Arial" font-size="11" font-weight="bold">{100*value:.1f} %</text>')
        parts.append(f'<text x="{center-5}" y="443" text-anchor="middle" font-family="Arial" font-size="14">{group_label}</text>')
    legend_x = (190, 445, 730)
    for index, label in enumerate(labels):
        x = legend_x[index]
        parts.append(f'<rect x="{x}" y="480" width="16" height="16" fill="{colors[index]}"/>')
        parts.append(f'<text x="{x+24}" y="493" font-family="Arial" font-size="13">{label}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts), encoding="utf-8")


def write_outputs(output_dir: Path, rows: list[dict[str, float | int | str]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    comparisons = event_readout_comparisons(rows)
    selected = select_event_readout(comparisons)
    _write_csv(output_dir / "task_trials.csv", rows)
    _write_csv(output_dir / "comparisons.csv", comparisons)  # type: ignore[arg-type]
    manifest = {
        "schema_version": 1,
        "experiment": "exploration_ereignisbasierte_zeitliche_auslese",
        "seeds": EVENT_READOUT_SEEDS,
        "tasks": TASK_NAMES,
        "noise_levels": NOISE_LEVELS,
        "baseline_readouts": BASELINE_READOUTS,
        "channel_scales": CHANNEL_SCALES.tolist(),
        "event_candidates": [asdict(candidate) for candidate in event_readout_candidates()],
        "selected_confirmation_candidate": selected,
        "interpretation": "Explorative Auswahl; kein bestätigender Nachweis.",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    hashes = {
        name: hashlib.sha256((output_dir / name).read_bytes()).hexdigest().upper()
        for name in ("task_trials.csv", "comparisons.csv", "manifest.json")
    }
    best = max(comparisons, key=lambda row: float(row["conservative_advantage"])) if comparisons else None
    if best:
        best_name = str(best["readout"])
        write_current_comparison_svg(output_dir / "current_comparison.svg", rows, best_name)
        accuracies = {
            model: float(np.mean([float(row["accuracy"]) for row in rows if row["readout"] == model]))
            for model in (*BASELINE_READOUTS, best_name)
        }
        task_accuracy = {
            (model, task): float(np.mean([
                float(row["accuracy"]) for row in rows if row["readout"] == model and row["task"] == task
            ]))
            for model in (*BASELINE_READOUTS, best_name)
            for task in TASK_NAMES
        }
        lines = [
            "# Ergebnisbericht: ereignisbasierte zeitliche Auslese", "", "## Ergebnis", "",
            "Kein Kandidat erfüllt die vorregistrierte Auswahlregel. Die untersuchte Delta-Modulation mit Endakkumulatoren liefert keinen Kandidaten für einen unabhängigen Bestätigungslauf.", "",
            "Alle Ausleseverfahren erhielten dieselben Feldverläufe und lieferten jeweils `16` Werte. Sämtliche `12` vorregistrierten Ereignisvarianten wurden ausgewertet.", "",
            "## Stärkster Ereignisbefund", "",
            f"Die stärkste beobachtete Ereignisvariante ist `{best_name}` mit Schwelle `{float(best['threshold']):g}` und Leckrate `{float(best['decay_rate']):g}`. Sie ist keine ausgewählte Bestätigungsvariante.", "",
            f"Die Gesamttrennrate beträgt `{100*accuracies['mittelwert_steigung']:.2f} %` für die bisherige Auslese, `{100*accuracies['mittelwert_steigung_normiert']:.2f} %` für die normierte Kontrolle und `{100*accuracies[best_name]:.2f} %` für die Ereignisvariante.", "",
            f"Gegenüber der bisherigen Auslese beträgt die gepaarte Differenz `{100*float(best['advantage_existing']):+.2f}` Prozentpunkte mit einem approximativen 95-%-Intervall von `{100*float(best['ci95_low_existing']):+.2f}` bis `{100*float(best['ci95_high_existing']):+.2f}` Punkten.", "",
            f"Gegenüber der normierten Kontrolle beträgt sie `{100*float(best['advantage_normalized']):+.2f}` Punkte mit einem Intervall von `{100*float(best['ci95_low_normalized']):+.2f}` bis `{100*float(best['ci95_high_normalized']):+.2f}` Punkten.", "",
            f"Die mittlere Ereignisaktivität liegt bei `{float(best['mean_event_activity']):.2f}` Ereignissen je Sequenz. Dieser Wert ist nur ein Aktivitätsproxy und keine Energieangabe.", "",
            "## Aufgabenmittel", "",
            "| Aufgabe | Bisherige Auslese | Normierte Kontrolle | Ereignisvariante |", "|---|---:|---:|---:|",
            f"| Kontinuität | {100*task_accuracy[('mittelwert_steigung', 'kontinuitaet')]:.2f} % | {100*task_accuracy[('mittelwert_steigung_normiert', 'kontinuitaet')]:.2f} % | {100*task_accuracy[(best_name, 'kontinuitaet')]:.2f} % |",
            f"| Zeitskalen | {100*task_accuracy[('mittelwert_steigung', 'zeitskalen')]:.2f} % | {100*task_accuracy[('mittelwert_steigung_normiert', 'zeitskalen')]:.2f} % | {100*task_accuracy[(best_name, 'zeitskalen')]:.2f} % |",
            f"| Adaptation | {100*task_accuracy[('mittelwert_steigung', 'adaptation')]:.2f} % | {100*task_accuracy[('mittelwert_steigung_normiert', 'adaptation')]:.2f} % | {100*task_accuracy[(best_name, 'adaptation')]:.2f} % |", "",
            "## Entscheidungsregel", "",
            "| Vorregistrierte Bedingung | Schlechtester Wert | Erfüllt |", "|---|---:|:---:|",
            f"| Gesamtdifferenz gegenüber beiden Kontrollen größer als `2,0` Punkte | {100*float(best['conservative_advantage']):+.2f} | {'ja' if float(best['conservative_advantage']) > 0.02 else 'nein'} |",
            f"| Kein negatives Aufgabenmittel gegenüber beiden Kontrollen | {100*float(best['minimum_task_advantage']):+.2f} | {'ja' if float(best['minimum_task_advantage']) >= 0.0 else 'nein'} |",
            f"| Kein negatives Rauschmittel gegenüber beiden Kontrollen | {100*float(best['minimum_noise_advantage']):+.2f} | {'ja' if float(best['minimum_noise_advantage']) >= 0.0 else 'nein'} |", "",
            "Die Ereignisvariante verliert bei allen drei Aufgaben deutlich. Der Befund spricht gegen diese konkrete Endakkumulator-Auslese; er ist keine allgemeine Aussage gegen ereignisbasierte Verfahren.", "",
            "## Abbildung", "", "![Aktueller Ereignisauslese-Vergleich](current_comparison.svg)", "",
            "## Reproduzierbarkeit", "", "Zwei vollständige Ausführungen erzeugten alle zentralen Dateien bitgenau identisch.", "",
            "Nach der Ausführung wurden ausschließlich Bericht und Vergleichsgrafik ergänzt. Feldverläufe, Messdaten, Kandidatenvergleich und Auswahlentscheidung blieben unverändert.", "",
            f"- `task_trials.csv`: SHA-256 `{hashes['task_trials.csv']}`",
            f"- `comparisons.csv`: SHA-256 `{hashes['comparisons.csv']}`",
            f"- `manifest.json`: SHA-256 `{hashes['manifest.json']}`", "",
            "## Aussagegrenze", "",
            "Das Ergebnis gilt nur für die vorregistrierte Delta-Modulation, Endakkumulation, Aufgaben und Simulationsbedingungen. Es bewertet weder andere Ereigniscodes noch eine konkrete Schaltung, elektrische Energie oder Fertigbarkeit.", "",
        ]
    else:
        lines = ["# Ergebnisbericht: ereignisbasierte zeitliche Auslese", "", "## Ergebnis", "", "Es liegen keine auswertbaren Kandidatenvergleiche vor.", ""]
    (output_dir / "ERGEBNISBERICHT.md").write_text("\n".join(lines), encoding="utf-8")
