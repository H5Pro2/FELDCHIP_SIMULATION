# FELDCHIP_SIMULATION

Reproduzierbares mathematisches `4×4`-Referenzmodell für einen hypothetischen
feldbasierten Sensorprozessor im normierten Arbeitsbereich `−3…+3`. Der
Projektname **Wahrnehmungschip** bezeichnet ausschließlich eine technisch
messbare Sensor-zu-Feld-Abbildung.

Das Repository enthält Simulationsmodelle, Vorregistrierungen und vollständige
Ergebnisdaten. Es enthält keinen gefertigten Chip und keinen nachgewiesenen
Energie-, Leistungs- oder Verarbeitungsvorteil.

## Aktueller Stand

- Eine zuverlässige Rückführung ist im Modell technisch nachgewiesen. Der
  Referenzkandidat verwendet konstante Rückführung `1,6` und koppelt die
  Abweichung vom Referenzfeld.
- Positive symmetrische Nachbarschaftskopplung zeigte weder bei statischen noch
  bei zeitlich-räumlichen Aufgaben einen Vorteil gegenüber den Baselines.
- Alle 26 gerichteten und anisotropen Varianten waren technisch stabil. Keine
  erfüllte die vorregistrierte Auswahlregel für einen Bestätigungslauf.
- Die ungekoppelte dynamische Baseline bleibt der stärkste Kandidat der zuletzt
  untersuchten Aufgabe.

![Aktueller Architekturvergleich](results_anisotropic/current_comparison.svg)

Der Mechanismus „gerichtete beziehungsweise anisotrope Kopplung“ ist für diese
Aufgabe abgeschlossen. Ein weiterer Architekturmechanismus benötigt eine neue
Vorregistrierung. Der aktuelle Forschungsrahmen steht in
[`ARCHITEKTUR_NEUAUSRICHTUNG.md`](ARCHITEKTUR_NEUAUSRICHTUNG.md).

## Reproduzieren

Voraussetzung ist Python 3.11 oder neuer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run_experiment.py
python run_compact_readout.py
python run_temporal_experiment.py
python run_return_experiment.py
python run_anisotropic_experiment.py
```

Die veröffentlichten Hauptläufe wurden jeweils vollständig wiederholt. Die
zugehörigen Berichte enthalten die bitgenau verglichenen SHA-256-Prüfsummen.

## Dokumentation

| Abschnitt | Vorregistrierung oder Plan | Ergebnis |
|---|---|---|
| Statische Referenz und kompakte Auslese | [`FORSCHUNGSPLAN.md`](FORSCHUNGSPLAN.md) | [`results/`](results/), [`results_compact/`](results_compact/) |
| Zeitlich-räumlicher Hauptversuch | [`TEMPORALER_VERSUCHSPLAN.md`](TEMPORALER_VERSUCHSPLAN.md) | [`results_temporal/`](results_temporal/) |
| Technische Rückführung | [`RUECKFUEHRUNG_VORREGISTRIERUNG.md`](RUECKFUEHRUNG_VORREGISTRIERUNG.md) | [`results_return/`](results_return/) |
| Gerichtete und anisotrope Kopplung | [`ANISOTROPE_KOPPLUNG_VORREGISTRIERUNG.md`](ANISOTROPE_KOPPLUNG_VORREGISTRIERUNG.md) | [`results_anisotropic/`](results_anisotropic/) |

Konzept- und Konstruktionspapiere liegen unter [`Docs/`](Docs/).

## Wissenschaftliche Grenze

Alle Aussagen gelten nur für die jeweils vorregistrierten dimensionslosen
Modelle, Aufgaben und Ausleseverfahren. SPICE-Modelle, reale Bauteilstreuung,
Temperaturverhalten, elektrische Energie und Fertigbarkeit erfordern getrennte
Untersuchungen. Negative und neutrale Ergebnisse bleiben dokumentiert.
