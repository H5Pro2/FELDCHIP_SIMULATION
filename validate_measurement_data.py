from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import sys
from typing import Any


CELL_COLUMNS = tuple(f"cell_{row}{column}" for row in range(4) for column in range(4))
REQUIRED_COLUMNS = ("time_s", "force_N", *CELL_COLUMNS, "supply_V", "temperature_C")


class ValidationError(ValueError):
    pass


def _reject_unknown(container: dict[str, Any], allowed: set[str], path: str) -> None:
    unknown = set(container) - allowed
    if unknown:
        raise ValidationError(f"{path} enthält unbekannte Felder: {', '.join(sorted(unknown))}")


def _require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{path} muss ein JSON-Objekt sein")
    return value


def _require_string(container: dict[str, Any], key: str, path: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path}.{key} muss eine nichtleere Zeichenfolge sein")
    return value


def _require_number(container: dict[str, Any], key: str, path: str) -> float:
    value = container.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise ValidationError(f"{path}.{key} muss eine endliche Zahl sein")
    return float(value)


def _require_integer(container: dict[str, Any], key: str, path: str) -> int:
    value = container.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{path}.{key} muss eine Ganzzahl sein")
    return value


def validate_metadata(path: Path, csv_path: Path) -> dict[str, Any]:
    try:
        metadata = _require_object(json.loads(path.read_text(encoding="utf-8")), "metadata")
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"Metadaten sind nicht lesbar: {error}") from error

    if metadata.get("schema_version") != "1.0":
        raise ValidationError("metadata.schema_version muss '1.0' sein")
    if metadata.get("phase") != "pretest":
        raise ValidationError("metadata.phase muss vor der Messfreigabe 'pretest' sein")
    _reject_unknown(
        metadata,
        {
            "schema_version", "phase", "trial_id", "randomization_id", "sensor",
            "setup", "acquisition", "contact", "recording",
        },
        "metadata",
    )
    trial_id = _require_string(metadata, "trial_id", "metadata")
    randomization_id = _require_string(metadata, "randomization_id", "metadata")
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", trial_id) is None:
        raise ValidationError("metadata.trial_id enthält unzulässige Zeichen")
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", randomization_id) is None:
        raise ValidationError("metadata.randomization_id enthält unzulässige Zeichen")
    if csv_path.stem != trial_id or path.name != f"{trial_id}.metadata.json":
        raise ValidationError("trial_id muss mit beiden Dateinamen übereinstimmen")

    sensor = _require_object(metadata.get("sensor"), "metadata.sensor")
    _reject_unknown(
        sensor,
        {"sensor_id", "manufacturer", "model", "serial_number", "sensor_class", "array_shape"},
        "metadata.sensor",
    )
    for key in ("sensor_id", "manufacturer", "model", "serial_number"):
        _require_string(sensor, key, "metadata.sensor")
    if sensor.get("sensor_class") != "piezoresistive_polymer":
        raise ValidationError("metadata.sensor.sensor_class muss 'piezoresistive_polymer' sein")
    if sensor.get("array_shape") != [4, 4]:
        raise ValidationError("metadata.sensor.array_shape muss [4, 4] sein")

    setup = _require_object(metadata.get("setup"), "metadata.setup")
    _reject_unknown(
        setup,
        {"setup_id", "reference_force_sensor_id", "reference_force_calibration_id", "actuator_id", "adc_id"},
        "metadata.setup",
    )
    for key in (
        "setup_id", "reference_force_sensor_id", "reference_force_calibration_id",
        "actuator_id", "adc_id",
    ):
        _require_string(setup, key, "metadata.setup")

    acquisition = _require_object(metadata.get("acquisition"), "metadata.acquisition")
    _reject_unknown(acquisition, {"adc_resolution_bits", "sample_rate_hz"}, "metadata.acquisition")
    adc_bits = _require_integer(acquisition, "adc_resolution_bits", "metadata.acquisition")
    sample_rate = _require_number(acquisition, "sample_rate_hz", "metadata.acquisition")
    if not 1 <= adc_bits <= 32:
        raise ValidationError("metadata.acquisition.adc_resolution_bits muss zwischen 1 und 32 liegen")
    if sample_rate <= 0.0:
        raise ValidationError("metadata.acquisition.sample_rate_hz muss größer als null sein")

    contact = _require_object(metadata.get("contact"), "metadata.contact")
    _reject_unknown(
        contact,
        {"geometry", "position", "tilt_deg", "target_load_N", "sequence_index"},
        "metadata.contact",
    )
    if contact.get("geometry") not in {"single_cell", "central_2x2"}:
        raise ValidationError("metadata.contact.geometry ist nicht zugelassen")
    position = _require_object(contact.get("position"), "metadata.contact.position")
    _reject_unknown(position, {"row", "column", "x_mm", "y_mm"}, "metadata.contact.position")
    row = _require_integer(position, "row", "metadata.contact.position")
    column = _require_integer(position, "column", "metadata.contact.position")
    _require_number(position, "x_mm", "metadata.contact.position")
    _require_number(position, "y_mm", "metadata.contact.position")
    if not 0 <= row <= 3 or not 0 <= column <= 3:
        raise ValidationError("Zeilen- und Spaltenposition müssen zwischen 0 und 3 liegen")
    tilt = _require_object(contact.get("tilt_deg"), "metadata.contact.tilt_deg")
    _reject_unknown(tilt, {"x", "y"}, "metadata.contact.tilt_deg")
    _require_number(tilt, "x", "metadata.contact.tilt_deg")
    _require_number(tilt, "y", "metadata.contact.tilt_deg")
    if _require_number(contact, "target_load_N", "metadata.contact") <= 0.0:
        raise ValidationError("metadata.contact.target_load_N muss größer als null sein")
    if _require_integer(contact, "sequence_index", "metadata.contact") < 1:
        raise ValidationError("metadata.contact.sequence_index muss mindestens 1 sein")

    recording = _require_object(metadata.get("recording"), "metadata.recording")
    _reject_unknown(recording, {"timestamp_utc", "operator_id", "notes"}, "metadata.recording")
    timestamp = _require_string(recording, "timestamp_utc", "metadata.recording")
    _require_string(recording, "operator_id", "metadata.recording")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValidationError("metadata.recording.timestamp_utc ist kein ISO-8601-Zeitpunkt") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValidationError("metadata.recording.timestamp_utc muss eine Zeitzone enthalten")
    if parsed.utcoffset().total_seconds() != 0.0:
        raise ValidationError("metadata.recording.timestamp_utc muss in UTC angegeben sein")
    if "notes" in recording and not isinstance(recording["notes"], str):
        raise ValidationError("metadata.recording.notes muss eine Zeichenfolge sein")

    return metadata


def validate_csv(path: Path, nominal_sample_rate: float) -> dict[str, Any]:
    minima = {column: math.inf for column in REQUIRED_COLUMNS[1:]}
    maxima = {column: -math.inf for column in REQUIRED_COLUMNS[1:]}
    times: list[float] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != REQUIRED_COLUMNS:
                raise ValidationError("CSV-Kopfzeile oder Spaltenreihenfolge ist ungültig")
            for line_number, row in enumerate(reader, start=2):
                if None in row or any(value is None or value.strip() == "" for value in row.values()):
                    raise ValidationError(f"CSV-Zeile {line_number} ist unvollständig")
                numeric: dict[str, float] = {}
                for column in REQUIRED_COLUMNS:
                    try:
                        numeric[column] = float(row[column])
                    except ValueError as error:
                        raise ValidationError(f"CSV-Zeile {line_number}, {column}: keine Dezimalzahl") from error
                    if not math.isfinite(numeric[column]):
                        raise ValidationError(f"CSV-Zeile {line_number}, {column}: Wert ist nicht endlich")
                if times and numeric["time_s"] <= times[-1]:
                    raise ValidationError(f"CSV-Zeile {line_number}: time_s steigt nicht streng")
                if numeric["supply_V"] <= 0.0:
                    raise ValidationError(f"CSV-Zeile {line_number}: supply_V muss größer als null sein")
                times.append(numeric["time_s"])
                for column in REQUIRED_COLUMNS[1:]:
                    minima[column] = min(minima[column], numeric[column])
                    maxima[column] = max(maxima[column], numeric[column])
    except OSError as error:
        raise ValidationError(f"CSV ist nicht lesbar: {error}") from error

    if len(times) < 2:
        raise ValidationError("CSV muss mindestens zwei Messzeilen enthalten")
    intervals = [later - earlier for earlier, later in zip(times, times[1:])]
    median_interval = statistics.median(intervals)
    observed_rate = 1.0 / median_interval
    relative_rate_error = abs(observed_rate - nominal_sample_rate) / nominal_sample_rate
    if relative_rate_error > 0.05:
        raise ValidationError("Beobachtete Median-Abtastrate weicht mehr als 5 % von den Metadaten ab")
    if max(intervals) > 2.0 / nominal_sample_rate:
        raise ValidationError("Mindestens eine Zeitlücke überschreitet zwei nominale Abtastintervalle")

    return {
        "row_count": len(times),
        "start_time_s": times[0],
        "end_time_s": times[-1],
        "duration_s": times[-1] - times[0],
        "observed_sample_rate_hz": observed_rate,
        "relative_sample_rate_error": relative_rate_error,
        "maximum_time_gap_s": max(intervals),
        "ranges": {
            column: {"minimum": minima[column], "maximum": maxima[column]}
            for column in REQUIRED_COLUMNS[1:]
        },
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser(description="Prüft reale Drucksensor-Vorversuchsdaten ohne Auswertung.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("metadata_path", type=Path)
    args = parser.parse_args()
    try:
        metadata = validate_metadata(args.metadata_path, args.csv_path)
        csv_summary = validate_csv(args.csv_path, float(metadata["acquisition"]["sample_rate_hz"]))
        result = {
            "valid": True,
            "trial_id": metadata["trial_id"],
            "csv_sha256": sha256(args.csv_path),
            "metadata_sha256": sha256(args.metadata_path),
            **csv_summary,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except ValidationError as error:
        print(f"Ungültiger Messdatensatz: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
