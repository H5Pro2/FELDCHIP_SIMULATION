# Vorregistrierung: mehrere lokale Zeitskalen

## Ziel

Die bisherigen Versuche zeigen einen Nutzen lokaler zeitlicher Zustandsbildung,
aber keinen Vorteil der geprüften räumlichen Kopplungen. Dieser explorative
Versuch prüft deshalb Zwei-Zustands-Zellen mit unterschiedlichen lokalen
Zeitskalen und vollständig ohne räumliche Kopplung.

Ein positives exploratives Ergebnis wäre nur die Begründung für einen späteren
Bestätigungslauf mit neuen Seeds.

## Referenz und Modellschnitt

Die Pflichtbaseline besitzt pro Zelle einen Zustand mit konstanter
Rückführungsverstärkung `1,6`. Jeder neue Kandidat besitzt pro Zelle einen
langsamen und einen schnellen Zustand:

`dx_i/dt = Eingang − λ_i(x_i−r_i) − Softbegrenzung + Rauschen`

Der ausgegebene Feldwert ist

`y = α x_schnell + (1−α) x_langsam`.

Es gibt keine Nachbarschaftsterme. Beide internen Zustände bleiben einzeln auf
`−3…+3` begrenzt. Die Mischung ist konvex und vergrößert den Ausgangsbereich
nicht. Alle Modelle verwenden dieselbe Eingangsverstärkung und dieselbe
kompakte 16-Werte-Auslese wie der zeitlich-räumliche Hauptversuch.

## Kandidatenraum

Der Vergleich enthält die Ein-Zustands-Pflichtbaseline und genau `27`
Zwei-Zustands-Kandidaten:

- langsame Rückführungsrate `λ_langsam`: `0,8`, `1,0`, `1,2`,
- schnelle Rückführungsrate `λ_schnell`: `2,0`, `3,2`, `4,8`,
- Gewicht des schnellen Zustands `α`: `0,25`, `0,50`, `0,75`.

Nach dem Lauf werden keine Raten oder Mischgewichte ergänzt.

## Phase A: technische Zulassung

Verwendet werden beide Streuungsecken und die Entwicklungsseeds `101`, `131`,
`167`. Die Baseline wird mit den 18 bekannten Anfangsauslenkungen geprüft. Bei
Zwei-Zustands-Kandidaten werden zusätzlich 18 gegenläufige Anfangszustände
geprüft, sodass sich interne Auslenkungen nicht nur im Ausgang aufheben können.

Pro Kombination laufen:

- ein verrauschter Robustheitslauf bei `dt = 0,02`,
- ein rauschfreier Lauf bei `dt = 0,02`,
- ein rauschfreier Lauf bei `dt = 0,01`.

Jeder Lauf dauert `6,0` Sekunden. RMS-Abstand und Rückkehrkriterium beziehen
sich auf sämtliche internen Zustände, nicht nur auf den gemischten Ausgang.

Ein Modell ist nur zulässig, wenn in jeder Ecke-Seed-Kombination:

1. alle internen Zustände dauerhaft zurückkehren,
2. das schlechteste 95-%-Quantil der Einschwingzeit höchstens `5,0` Sekunden
   beträgt,
3. das schlechteste 95-%-Quantil des Restfehlers höchstens `0,05` beträgt,
4. keine erneuten Toleranzaustritte und keine Grenzüberschreitungen auftreten,
5. die t95-Differenz zwischen den rauschfreien Zeitschritten höchstens `0,10`
   Sekunden und die Restfehlerdifferenz höchstens `0,005` beträgt.

Nicht zugelassene Kandidaten gelangen nicht in Phase B.

## Phase B: zwei explorative Aufgaben

### Aufgabe 1: räumlich-zeitliche Kontinuität

Unverändert werden die zehn Sequenzklassen des bisherigen zeitlich-räumlichen
Hauptversuchs verwendet.

### Aufgabe 2: lokale Zeitskalen

Zehn neue Sequenzklassen bilden fünf kontrollierte Paare:

1. zwei Pulse mit kurzem oder langem Abstand,
2. gleicher Impuls früh oder spät in der Sequenz,
3. kurzer starker oder langer schwacher Impuls mit gleicher Eingangssumme,
4. schneller oder langsamer Polaritätswechsel mit gleicher Betragsenergie,
5. Aufbau oder Abbau eines Gradienten mit gleicher Betragsenergie.

Innerhalb jedes Paares ist die räumliche Form gleich. Die zeitlichen Profile
sind deterministisch und besitzen paarweise dieselbe integrierte
Betragsenergie.

### Gemeinsame Bedingungen

- Entwicklungsseeds: `101`, `131`, `167`,
- Rauschstufen: `0,15`, `0,35`, `0,55`,
- Training: `12` Sequenzen je Klasse,
- Test: `24` Sequenzen je Klasse,
- Auslese: acht Momentanmerkmale, jeweils zeitlicher Mittelwert und lineare
  Steigung, insgesamt `16` Werte,
- Auswerter: Nächste-Zentroid-Verfahren.

Eingänge und Zufallsbedingungen sind innerhalb jeder Aufgabe-Seed-Rausch-
Kombination für alle Modelle identisch.

## Explorative Auswahlregel

Für jeden technisch zugelassenen Zwei-Zustands-Kandidaten wird die gepaarte
Differenz zur Ein-Zustands-Pflichtbaseline über beide Aufgaben und alle
Seed-Rausch-Kombinationen berechnet.

Höchstens ein Kandidat wird ausgewählt. Er muss:

1. im Gesamtmittel mehr als `2,0` Prozentpunkte vor der Baseline liegen,
2. auf keiner der beiden Aufgaben im Mittel unter der Baseline liegen,
3. bei keiner der drei Rauschstufen im Mittel unter der Baseline liegen.

Bei mehreren Kandidaten gewinnt die größte Gesamtdifferenz. Bei Gleichstand
folgen das kleinere Verhältnis `λ_schnell/λ_langsam`, das größere Gewicht des
langsamen Zustands und schließlich der Modellname.

Für den ausgewählten Kandidaten werden ein approximatives gepaartes
95-%-Intervall und die Einzelwerte beider Aufgaben berichtet. Diese Größen sind
explorativ und kein bestätigender Nachweis.

## Aussagegrenze

Der Versuch vergleicht eine begrenzte Familie dimensionsloser
Zwei-Zustands-Modelle. Zusätzlicher interner Zustand bedeutet zusätzlichen
Schaltungsaufwand, dessen Fläche und Energie hier nicht bewertet werden. Ein
Kandidat müsste in einem neuen vorregistrierten Lauf und später elektrisch
geprüft werden.

