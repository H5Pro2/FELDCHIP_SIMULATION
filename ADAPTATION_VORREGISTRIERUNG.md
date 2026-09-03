# Vorregistrierung: lokale begrenzte Adaptation

## Ausgangspunkt und Ziel

Räumliche Kopplung lieferte keinen Vorteil. Mehrere lokale Zeitskalen zeigten
einen kleinen positiven Effekt, verfehlten im unabhängigen Bestätigungslauf
aber die vorab festgelegte Mindestgröße. Der konkrete Zwei-Zustands-Kandidat
wird nicht weiter optimiert.

Dieser explorative Versuch prüft als neuen Mechanismus eine lokale begrenzte
Adaptation ohne räumliche Kopplung. Ziel ist höchstens ein Kandidat für einen
späteren unabhängigen Bestätigungslauf.

## Modell

Die Ein-Zustands-Pflichtbaseline bleibt unverändert:

`dx/dt = Eingang − 1,6(x−r) − Softbegrenzung + Rauschen`.

Das Adaptationsmodell ergänzt je Zelle einen lokalen Zustand `a`:

`da/dt = λ_a(Eingang−a)`

`dx/dt = g(Eingang−βa) − 1,6(x−r) − Softbegrenzung + Rauschen`.

Der Adaptationszustand wird symmetrisch auf `−A…+A` begrenzt. Es gibt keine
Nachbarschaftsterme. Ausgegeben wird nur `x`; damit bleiben `4×4` Feldwerte und
die kompakte 16-Werte-Auslese unverändert. Mehr interne Zustände führen nicht
zu mehr externen Ausgabewerten.

## Kandidatenraum

Verglichen werden eine Pflichtbaseline und genau `24` Adaptationskandidaten:

- Adaptationsrate `λ_a`: `0,6`, `0,9`, `1,2`,
- Rückwirkungsstärke `β`: `0,25`, `0,50`, `0,75`, `1,00`,
- Adaptationsgrenze `A`: `0,5`, `1,0`.

Zellrückführung `1,6`, Eingangsverstärkung, Softbegrenzung und Arbeitsbereich
`−3…+3` sind eingefroren. Nach dem Lauf werden keine Parameter ergänzt.

## Entwicklungsseeds

Verwendet werden ausschließlich `401`, `431`, `463`. Diese Seeds kamen in
keinem bisherigen Haupt-, Explorations- oder Bestätigungslauf vor.

## Phase A: technische Zulassung

Die Baseline wird mit den bekannten 18 Zellenauslenkungen geprüft. Für jeden
Adaptationskandidaten werden `54` interne Anfangskonfigurationen verwendet:

1. Zelle ausgelenkt, Adaptation null,
2. Zelle am Referenzwert, Adaptation ausgelenkt,
3. Zelle und Adaptation gegenläufig ausgelenkt.

Die Adaptationsauslenkung wird auf die jeweilige Grenze `A` skaliert. RMS-
Abstand und Rückkehr beziehen sich auf alle internen Zustände.

Mit beiden Streuungsecken laufen je Kombination ein verrauschter
Robustheitstest bei `dt = 0,02` sowie rauschfreie Tests bei `dt = 0,02` und
`dt = 0,01`. Dauer `6,0 s`, Toleranz `0,05`, t95-Grenze `5,0 s`,
Restfehlergrenze `0,05`, Verbot erneuter Toleranzaustritte und
Zeitschrittgrenzen `0,10 s` beziehungsweise `0,005` bleiben unverändert.

Nur technisch zugelassene Modelle gelangen in Phase B.

## Phase B: drei Aufgaben

### Kontinuität

Die zehn Klassen der bisherigen räumlich-zeitlichen Kontinuitätsaufgabe werden
unverändert wiederverwendet.

### Zeitskalen

Die zehn energiegleichen Klassen der bisherigen lokalen Zeitskalenaufgabe
werden unverändert wiederverwendet.

### Adaptation

Zehn deterministische Klassen bilden fünf energiegleiche Paare:

1. positives räumliches Feld in der ersten oder zweiten Sequenzhälfte,
2. negatives räumliches Feld in der ersten oder zweiten Sequenzhälfte,
3. positiver Hintergrund mit frühem oder spätem lokalem Zusatzimpuls,
4. negativer Hintergrund mit frühem oder spätem lokalem Zusatzimpuls,
5. Aufbau oder Abbau eines räumlichen Gradienten.

Innerhalb jedes Paares sind räumliche Form und integrierte Betragsenergie
gleich; unterschieden wird ausschließlich der zeitliche Verlauf.

### Gemeinsame Bedingungen

- Rauschstufen `0,15`, `0,35`, `0,55`,
- `12` Trainings- und `24` Testsequenzen je Klasse,
- identische Eingänge und Zufallsbedingungen für alle Modelle,
- acht Momentanmerkmale mit Mittelwert und linearer Steigung,
- insgesamt `16` Ausgabewerte,
- Nächste-Zentroid-Auswertung.

## Explorative Auswahlregel

Für jeden zugelassenen Kandidaten wird die gepaarte Differenz zur Baseline über
die drei Aufgaben, drei Seeds und drei Rauschstufen berechnet.

Höchstens ein Kandidat wird ausgewählt. Er muss:

1. im Gesamtmittel mehr als `2,0` Prozentpunkte vor der Baseline liegen,
2. auf keiner der drei Aufgaben im Mittel unter der Baseline liegen,
3. bei keiner Rauschstufe im Mittel unter der Baseline liegen.

Bei mehreren Kandidaten gewinnt die größte Gesamtdifferenz. Beobachtete
Differenzen gelten nach Rundung auf `12` Dezimalstellen als gleich. Danach
folgen geringere Rückwirkungsstärke, höhere Adaptationsrate, kleinere
Adaptationsgrenze und schließlich der Modellname.

Ein Intervall wird berichtet, ist wegen der explorativen Auswahl aber kein
Bestätigungsnachweis. Erfüllt kein Modell alle Bedingungen, endet der
Mechanismus ohne Kandidaten.

## Aussagegrenze

Der Versuch prüft eine begrenzte dimensionslose Modellfamilie. Ein zusätzlicher
Adaptationszustand erhöht möglichen Schaltungsaufwand. Fläche, Energie,
Bauteilverhalten und Fertigbarkeit sind damit nicht bewertet.
