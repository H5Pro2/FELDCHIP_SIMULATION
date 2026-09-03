# FELDCHIP_SIMULATION

Reproduzierbares mathematisches Referenzmodell für einen hypothetischen
feldbasierten Sensorprozessor. Ein gekoppeltes `4×4`-Zellfeld bildet räumliche
Eingangssignale in kontinuierliche Zustände im normierten Arbeitsbereich
`−3…+3` ab und kehrt nach dem Eingangspuls zu einem Referenzfeld zurück.

Der Projektname **Wahrnehmungschip** bezeichnet in den begleitenden Papieren
ausschließlich diese technisch messbare Sensor-zu-Feld-Abbildung.

## Forschungsstatus

Das Repository enthält eine prüfbare Arbeitshypothese und einen ersten
Referenzversuch. Es enthält keinen fertigen Schaltplan, keinen gefertigten Chip
und keinen nachgewiesenen Energie- oder Leistungsvorteil.

Der erste Lauf vergleicht bei identischem Arbeitsbereich:

- zwei Rückführungsregime,
- drei Rückführungsregime,
- vier Rückführungsregime,
- eine geglättete Dreiregime-Kennlinie,
- ein ungekoppeltes dynamisches Sensorarray,
- ein lineares RC-Diffusionsnetz,
- digitale Diffusion mit 12-Bit-Quantisierung,
- das unverarbeitete Rohsignal.

## Aktueller Befund

Über sechs Eingangsmuster, drei Rauschstufen und fünf feste Zufallsstarts
erreichte die beste Feldvariante `86,9 %` Mustertrennung. Die Rohsignal-Baseline
erreichte `92,3 %`. Die Feldvarianten lagen nur `0,3` Prozentpunkte auseinander.

Damit gilt für die untersuchte Vollfeldauslese:

- reproduzierbar unterscheidbare Feldformen: **beobachtet**,
- Einhaltung des Bereichs `−3…+3`: **beobachtet**,
- besonderer Vorteil einer Regimezahl: **nicht nachgewiesen**,
- Vorteil gegenüber der besten Baseline: **nicht nachgewiesen**,
- ausreichend schnelle Rückführung: **mit der aktuellen Parametrierung nicht erreicht**.

Die Ergebnisse dürfen nicht auf andere Aufgaben oder eine reale Schaltung
übertragen werden, ohne diese gesondert zu prüfen.

![Trennraten der Modelle](results/accuracy_comparison.svg)

![Beispielhafte 4x4-Feldkarten](results/field_examples.svg)

## Reproduzieren

Voraussetzung ist Python 3.11 oder neuer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run_experiment.py
```

Der Hauptlauf erzeugt `120` aggregierte Modellläufe. Seine beiden zentralen
CSV-Dateien wurden in zwei vollständigen Wiederholungen bitgenau identisch
erzeugt.

## Ergebnisse

- [`ERGEBNISBERICHT.md`](results/ERGEBNISBERICHT.md): Befunde und Grenzen
- [`summary.csv`](results/summary.csv): aggregierte Kennzahlen
- [`trials.csv`](results/trials.csv): alle Seeds und Rauschstufen
- [`manifest.json`](results/manifest.json): vollständige Versuchsparameter
- [`accuracy_comparison.svg`](results/accuracy_comparison.svg): Modellvergleich
- [`field_examples.svg`](results/field_examples.svg): beispielhafte Feldkarten

## Projektstruktur

```text
Docs/                         Konzept- und Konstruktionspapiere
src/feldchip_simulation.py    Modell, Baselines und Auswertung
tests/test_simulation.py      mathematische und reproduktive Tests
run_experiment.py             ausführbarer Referenzversuch
results/                      Manifest, Rohwerte, Bericht und Diagramme
FORSCHUNGSPLAN.md             vorab festgelegte nächste Untersuchung
```

## Wissenschaftliche Grenze

Das Modell prüft dimensionslose Dynamik, Trennbarkeit, Reproduzierbarkeit,
Rückführung und Bereichseinhaltung. Es ersetzt weder eine SPICE-Simulation mit
realistischen Bauteilmodellen noch Messungen an physischer Hardware. Der
Aktivitätswert ist keine elektrische Energiemessung.

Neue Varianten werden nur dann als Fortschritt gewertet, wenn sie eine vorher
festgelegte Messgröße gegenüber denselben Baselines verbessern. Negative und
neutrale Ergebnisse bleiben Bestandteil der Dokumentation.

Der nächste Versuch verändert die Felddynamik nicht. Er reduziert jedes Feld
vor der Auswertung auf acht feste Skalare und prüft damit eine begrenzte
Auslesebandbreite. Die langsame Rückkehr wird davon getrennt untersucht.

Dieser kompakte Versuch wurde inzwischen ausgeführt. Die beste Feldvariante
erreichte `63,2 %`, die beste identisch ausgelesene Baseline `62,4 %`. Der
Vorsprung von `0,8` Prozentpunkten liegt unter der vorab festgelegten Schwelle
und ist daher kein bestätigter Vorteil. Der vollständige Bericht liegt unter
[`results_compact/ERGEBNISBERICHT.md`](results_compact/ERGEBNISBERICHT.md).
