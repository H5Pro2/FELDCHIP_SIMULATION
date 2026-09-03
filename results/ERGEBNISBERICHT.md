# Ergebnisbericht: mathematischer 4×4-Demonstrator

## Prüfziel

Geprüft wird, ob gekoppelte kontinuierliche Zellen unter identischen gestörten Eingangsmustern reproduzierbar trennbare Feldformen erzeugen. Der Arbeitsbereich bleibt für alle Feldvarianten bei −3 bis +3. Verglichen werden zwei, drei und vier Rückführungsregime sowie eine geglättete Dreiregime-Kennlinie.

## Vorab festgelegte Aufgabe

Sechs 4×4-Muster werden mit Verstärkungsstreuung, Offset, Pixelausfällen und drei Rauschstufen beaufschlagt. Pro Rauschstufe laufen fünf unabhängige Zufallsstarts. Die Auswertung verwendet ausschließlich die 16 Feldwerte am Ende des Eingangspulses und einen einfachen Nächste-Zentroid-Auswerter.

## Gesamtergebnis

Die höchste mittlere Trennrate erreichte `baseline_rohsignal` mit 92.3 %. Die beste Feldvariante war `feld_glatt` mit 86.9 %. Die beste Baseline war `baseline_rohsignal` mit 92.3 %.

Differenz beste Feldvariante minus beste Baseline: -5.4 Prozentpunkte.

Damit ist ein Vorteil der Feldarchitektur in dieser Aufgabe nicht nachgewiesen; die einfachere Baseline ist gleich gut oder besser.

## Zentrale Befunde und Nichtnachweise

- Die vier Feldkennlinien liegen bei der mittleren Trennrate eng beieinander. Der Abstand zwischen bester und schwächster Feldvariante beträgt nur 0.3 Prozentpunkte. Aus diesem Lauf folgt daher kein besonderer Vorteil von zwei, drei, vier oder geglätteten Regimen.
- Die beste Feldvariante liegt 5.4 Prozentpunkte hinter der besten Baseline. Für die hier verwendete Vollfeldauslese ist ein zusätzlicher Nutzen der nichtlinearen Feldbildung nicht nachgewiesen.
- Der Rückkehrerfolg der Feldvarianten liegt nach fünf normierten Sekunden nur zwischen 3.9 % und 5.4 %. Die gewählte schwache innere Rückführung erfüllt das Rückkehrkriterium damit nicht.
- Im regulären Lauf traten bei keiner Feldvariante versuchte Grenzüberschreitungen auf. Der höchste mittlere Betrag blieb bei 2.003 und damit deutlich innerhalb des Bereichs −3 bis +3.
- Die feste digitale Diffusion glättet die kleinen 4×4-Muster stark und ist in dieser einzelnen Parametrierung deutlich schlechter. Das ist kein allgemeiner Nachweis gegen digitale Verfahren; dafür wäre ein eigener Parametersweep erforderlich.

## Zusammenfassung der Modelle

| Modell | Trennrate | Trennverhältnis | Wiederhol-RMSE | Rückkehrerfolg | Rückkehrzeit | Grenzverletzungen |
|---|---:|---:|---:|---:|---:|---:|
| feld_2_regime | 86.7 ± 9.0 % | 1.083 | 0.418 | 3.9 % | 4.01 s | 0.0000 % |
| feld_3_regime | 86.7 ± 8.7 % | 1.088 | 0.383 | 3.9 % | 3.98 s | 0.0000 % |
| feld_4_regime | 86.6 ± 9.3 % | 1.063 | 0.381 | 5.4 % | 3.96 s | 0.0000 % |
| feld_glatt | 86.9 ± 8.9 % | 1.063 | 0.408 | 4.0 % | 3.99 s | 0.0000 % |
| baseline_ungekoppelt | 92.2 ± 8.1 % | 1.261 | 0.624 | 0.9 % | 4.34 s | 0.0000 % |
| baseline_linear_rc | 87.7 ± 9.1 % | 1.056 | 0.375 | 37.4 % | 3.73 s | 0.0000 % |
| baseline_digital_diffusion | 48.2 ± 6.8 % | 0.382 | 0.157 | n/a | n/a | 0.0000 % |
| baseline_rohsignal | 92.3 ± 8.0 % | 1.261 | 0.450 | n/a | n/a | 0.0000 % |

## Abbildungen

![Trennrate nach Rauschstufe](accuracy_comparison.svg)

![Beispielhafte Feldkarten](field_examples.svg)

## Aussagegrenze

Dies ist ein dimensionsloses mathematisches Referenzmodell. Der Aktivitätswert ist nur ein Rechenproxy und keine elektrische Energiemessung. Bauteilrauschen, parasitäre Effekte, Temperatur und reale Ausleseschaltungen sind erst mit SPICE beziehungsweise Hardware belastbar prüfbar. Ein positives Ergebnis rechtfertigt den nächsten Simulationsschritt, aber noch keine Aussage über einen gefertigten Chip.

## Reproduzierbarkeit

Die vollständigen Einzelwerte stehen in `trials.csv`, die aggregierten Werte in `summary.csv`. `manifest.json` hält Modellparameter, Seeds und Stichprobengrößen fest. Der Lauf ist mit festen Seeds reproduzierbar.
