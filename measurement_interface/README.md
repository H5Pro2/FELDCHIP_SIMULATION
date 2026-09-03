# Datenschnittstelle für reale Drucksensor-Vorversuche

## Status

Diese Schnittstelle nimmt ausschließlich reale Messungen gemäß
`Docs/MESS_UND_PARAMETRISIERUNGSPROTOKOLL_DRUCKSENSORFLAECHE.md` entgegen. Sie
erzeugt keine Messwerte, keine Kontaktverläufe und keine Modellparameter.

Bis zu einem versionierten Messfreigabebericht ist nur die Phase `pretest`
zulässig. Hauptmessung und Validierungsserie benötigen eine spätere
Schemafreigabe.

## Dateien je Kontaktversuch

Jeder Kontaktversuch besteht aus genau zwei gleich benannten Dateien:

```text
<trial_id>.csv
<trial_id>.metadata.json
```

`trial_id` muss in Dateinamen und Metadaten identisch sein. Ein vollständiger
Messsatz enthält zusätzlich die unveränderten Kalibrierunterlagen der
Referenzkraftmesszelle und des Messaufbaus.

## CSV-Vertrag

Die Datei ist UTF-8-kodiert, verwendet Komma als Spaltentrenner und Punkt als
Dezimalzeichen. Die Spaltenreihenfolge ist verbindlich:

```text
time_s,force_N,cell_00,cell_01,cell_02,cell_03,cell_10,cell_11,cell_12,cell_13,cell_20,cell_21,cell_22,cell_23,cell_30,cell_31,cell_32,cell_33,supply_V,temperature_C
```

Die Datei `raw_contact_header.csv` enthält nur diese Kopfzeile und ist kein
Messdatensatz.

Regeln:

- alle 20 Spalten sind in jeder Zeile erforderlich,
- alle Werte müssen endliche Dezimalzahlen sein,
- `time_s` muss streng steigen,
- `supply_V` muss größer als null sein,
- mindestens zwei Messzeilen sind erforderlich,
- die aus `time_s` bestimmte Median-Abtastrate darf höchstens `5 %` von der
  Metadatenrate abweichen,
- eine einzelne Zeitlücke darf höchstens zwei nominale Abtastintervalle
  betragen.

Kleine negative Werte von `force_N` werden nicht strukturell verworfen, weil
sie aus Nullpunktunsicherheit der Referenzkraftmesszelle entstehen können.

## Metadatenvertrag

Das verbindliche JSON-Schema liegt unter
`measurement_metadata.schema.json`. Pflichtangaben sind:

- eindeutige Versuch-, Sensor- und Aufbaukennung,
- Kennung der vorab gespeicherten Randomisierung,
- Hersteller, Modell, Seriennummer und Sensorklasse,
- Kennungen von Referenzkraftmesszelle, Aktor und ADC,
- Kalibrierkennung der Referenzkraftmesszelle,
- ADC-Auflösung und nominelle Abtastrate,
- Kontaktgeometrie und physikalische Position,
- Zeilen- und Spaltenposition im `4×4`-Feld,
- Neigung in beiden Achsen,
- Prüflast und Versuchsreihenfolge,
- UTC-Zeitpunkt und Bedienerkennung.

Freitextnotizen sind zulässig, ersetzen aber keine Pflichtangabe.

## Validierung

Die Prüfung ist rein lesend:

```powershell
python validate_measurement_data.py `
  path\to\trial_id.csv `
  path\to\trial_id.metadata.json
```

Bei Erfolg werden Zeilenzahl, Dauer, beobachtete Abtastrate, Zeitlücke,
Wertebereiche und SHA-256-Prüfsummen ausgegeben. Es werden keine Dateien
verändert oder erzeugt.

Eine bestandene Schnittstellenprüfung ist keine Messfreigabe. Physikalische
Kennwerte, Unsicherheiten und Abbruchkriterien werden erst im Vorversuch
ausgewertet.
