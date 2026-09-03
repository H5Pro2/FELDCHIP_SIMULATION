# Ergebnisbericht: ereignisbasierte zeitliche Auslese

## Ergebnis

Kein Kandidat erfüllt die vorregistrierte Auswahlregel. Die untersuchte Delta-Modulation mit Endakkumulatoren liefert keinen Kandidaten für einen unabhängigen Bestätigungslauf.

Alle Ausleseverfahren erhielten dieselben Feldverläufe und lieferten jeweils `16` Werte. Sämtliche `12` vorregistrierten Ereignisvarianten wurden ausgewertet.

## Stärkster Ereignisbefund

Die stärkste beobachtete Ereignisvariante ist `ereignis_t0.05_l1.6` mit Schwelle `0.05` und Leckrate `1.6`. Sie ist keine ausgewählte Bestätigungsvariante.

Die Gesamttrennrate beträgt `72.64 %` für die bisherige Auslese, `69.38 %` für die normierte Kontrolle und `57.56 %` für die Ereignisvariante.

Gegenüber der bisherigen Auslese beträgt die gepaarte Differenz `-15.08` Prozentpunkte mit einem approximativen 95-%-Intervall von `-18.38` bis `-11.77` Punkten.

Gegenüber der normierten Kontrolle beträgt sie `-11.82` Punkte mit einem Intervall von `-14.81` bis `-8.83` Punkten.

Die mittlere Ereignisaktivität liegt bei `86.56` Ereignissen je Sequenz. Dieser Wert ist nur ein Aktivitätsproxy und keine Energieangabe.

## Aufgabenmittel

| Aufgabe | Bisherige Auslese | Normierte Kontrolle | Ereignisvariante |
|---|---:|---:|---:|
| Kontinuität | 93.19 % | 89.91 % | 75.97 % |
| Zeitskalen | 44.86 % | 42.41 % | 37.96 % |
| Adaptation | 79.86 % | 75.83 % | 58.75 % |

## Entscheidungsregel

| Vorregistrierte Bedingung | Schlechtester Wert | Erfüllt |
|---|---:|:---:|
| Gesamtdifferenz gegenüber beiden Kontrollen größer als `2,0` Punkte | -15.08 | nein |
| Kein negatives Aufgabenmittel gegenüber beiden Kontrollen | -21.11 | nein |
| Kein negatives Rauschmittel gegenüber beiden Kontrollen | -19.07 | nein |

Die Ereignisvariante verliert bei allen drei Aufgaben deutlich. Der Befund spricht gegen diese konkrete Endakkumulator-Auslese; er ist keine allgemeine Aussage gegen ereignisbasierte Verfahren.

## Abbildung

![Aktueller Ereignisauslese-Vergleich](current_comparison.svg)

## Reproduzierbarkeit

Zwei vollständige Ausführungen erzeugten alle zentralen Dateien bitgenau identisch.

Nach der Ausführung wurden ausschließlich Bericht und Vergleichsgrafik ergänzt. Feldverläufe, Messdaten, Kandidatenvergleich und Auswahlentscheidung blieben unverändert.

- `task_trials.csv`: SHA-256 `E95185A85A2EC8EC97E04C4D5C7E1BA98ACDA633420D3F994C5C5089D828260A`
- `comparisons.csv`: SHA-256 `AA4BB4114AADB4F4901529CAC5876FA83591B7EC72AA220D84C1AE53AEDC2FB7`
- `manifest.json`: SHA-256 `0FC4378943CDB34A77D4C07C17D381242899D9E96E844FCAE6E4C50205937C2A`

## Aussagegrenze

Das Ergebnis gilt nur für die vorregistrierte Delta-Modulation, Endakkumulation, Aufgaben und Simulationsbedingungen. Es bewertet weder andere Ereigniscodes noch eine konkrete Schaltung, elektrische Energie oder Fertigbarkeit.
