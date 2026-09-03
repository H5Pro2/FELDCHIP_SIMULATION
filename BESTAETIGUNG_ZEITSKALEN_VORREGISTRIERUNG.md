# Vorregistrierung: Bestätigung lokaler Zeitskalen

## Ziel und Status

Die explorative Zeitskalenuntersuchung wählte genau einen Kandidaten aus:
`zwei_zustaende_l1.2_s2_a0.5`. Dieser Lauf prüft mit neuen Seeds, ob dessen
Vorsprung gegenüber der Ein-Zustands-Baseline reproduzierbar ist.

Es findet keine weitere Modellauswahl oder Parameteroptimierung statt. Der Lauf
wird erst nach einem Commit dieser Vorregistrierung und des zugehörigen Codes
ausgeführt.

## Eingefrorene Modelle

### Pflichtbaseline

- ein lokaler Zustand je Zelle,
- konstante Rückführungsrate `1,6`,
- keine räumliche Kopplung.

### Bestätigungskandidat

- zwei lokale Zustände je Zelle,
- langsame Rückführungsrate `1,2`,
- schnelle Rückführungsrate `2,0`,
- Ausgangsmischung `0,5` langsam und `0,5` schnell,
- keine räumliche Kopplung.

Arbeitsbereich, Eingangsverstärkung, Softbegrenzung, Störmodell und kompakte
16-Werte-Auslese bleiben gegenüber der Exploration unverändert.

## Neue Seeds

Der Bestätigungslauf verwendet ausschließlich `211`, `241`, `277`, `313`,
`349`. Diese Seeds wurden weder in der explorativen Zeitskalensuche noch in den
vorherigen Hauptversuchen verwendet.

## Technische Pflichtprüfung

Beide Modelle werden mit den neuen Seeds, beiden Streuungsecken und denselben
internen Anfangsauslenkungen wie in der Exploration geprüft. Beim
Zwei-Zustands-Modell gehören die gegenläufigen internen Auslenkungen dazu.

Pro Kombination laufen ein verrauschter Robustheitslauf bei `dt = 0,02` und
rauschfreie Läufe bei `dt = 0,02` sowie `dt = 0,01`. Dauer, Toleranz,
Einschwinggrenze, Restfehlergrenze und Zeitschrittkriterien bleiben unverändert.

Die Aufgabenbewertung findet nur statt, wenn beide Modelle sämtliche
technischen Kriterien erfüllen. Andernfalls endet der Bestätigungslauf mit
einem technischen Negativbefund.

## Eingefrorene Aufgaben

Es werden exakt die beiden explorativen Aufgaben wiederverwendet:

1. die zehn Klassen der räumlich-zeitlichen Kontinuitätsaufgabe,
2. die zehn Klassen der lokalen Zeitskalenaufgabe.

Sequenzen und Klassen werden nicht verändert. Pro Aufgabe gelten:

- Rauschstufen `0,15`, `0,35`, `0,55`,
- `12` Trainingssequenzen je Klasse,
- `24` Testsequenzen je Klasse,
- identische Eingänge und Zufallsbedingungen für beide Modelle,
- dieselben acht Momentanmerkmale mit Mittelwert und linearer Steigung,
- Nächste-Zentroid-Auswertung.

Damit entstehen `30` gepaarte Aufgabe-Seed-Rausch-Differenzen.

## Primäre Auswertung

Für jede der 30 Kombinationen wird die Trennratendifferenz
`Zwei-Zustands-Kandidat minus Ein-Zustands-Baseline` gebildet. Berichtet werden
Mittelwert, Standardfehler und das approximative gepaarte 95-%-Intervall
`Mittelwert ± 1,96 × Standardfehler`.

## Bestätigungskriterium

Der explorative Hinweis gilt in diesem Modell nur dann als bestätigt, wenn
sämtliche Bedingungen erfüllt sind:

1. mittlere Gesamtdifferenz größer als `2,0` Prozentpunkte,
2. untere Grenze des gepaarten 95-%-Intervalls größer als null,
3. mittlere Differenz in jeder der beiden Aufgaben mindestens null,
4. mittlere Differenz bei jeder der drei Rauschstufen mindestens null.

Werden nicht alle Bedingungen erfüllt, gilt der Vorteil als nicht bestätigt.
Grenzwerte, Aufgaben und Auswertung werden nach dem Lauf nicht geändert.

## Aussagegrenze

Eine statistische Bestätigung würde ausschließlich für diese zwei Modelle,
Aufgaben und Simulationsbedingungen gelten. Der zusätzliche lokale Zustand
erhöht den Schaltungsaufwand. Fläche, elektrische Energie, Bauteilmodelle und
Fertigbarkeit bleiben bis zu getrennten SPICE- und Hardwareprüfungen offen.

