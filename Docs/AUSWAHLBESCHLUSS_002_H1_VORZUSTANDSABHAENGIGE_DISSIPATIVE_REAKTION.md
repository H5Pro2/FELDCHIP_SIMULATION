# Auswahlbeschluss 002: H1 - vorzustandsabhängige dissipative Reaktion

**Version:** 1.0

**Datum:** 3. September 2026

**Status:** beschlossen, nicht zur Modellierung freigegeben

**Grundlage:**
`ARCHITEKTURPAPIER_PHASE_II_KONTINUIERLICHE_SENSORISCHE_ZUSTANDSFLAECHE.md`

## 1. Auswahl

Als erste Operationalisierung der kontinuierlichen sensorischen Zustandsfläche
wird genau eine Architekturhypothese ausgewählt:

> **H1: Ein messbarer physikalischer Vorzustand verändert die Reaktion auf
> einen identischen Folgereiz reproduzierbar; anschließend kehrt das System
> kontrolliert zum Referenzzustand zurück.**

Der Beschluss wählt eine zu prüfende physikalische Beziehung aus. Er legt noch
keine Zustandsgleichung, Kennlinie, Modellparameter oder Schaltungsform fest.
Er erlaubt weder Simulationen noch synthetische Kontaktversuche.

## 2. Begründung und Abgrenzung

H1 prüft die elementare zeitliche Eigenschaft der Architektur, bevor mehrere
Sensorquellen oder ein Aktorpfad eingeführt werden. Vorzustand, Folgereiz,
Reaktionsdifferenz und Rückkehr sind an einer einzelnen realen Sensorquelle
direkt messbar.

H2 bleibt zurückgestellt, weil dafür mindestens zwei synchronisierte und
getrennt charakterisierte Sensorquellen erforderlich wären. H3 bleibt
zurückgestellt, weil zusätzlich Aktorik, Sicherheitsgrenzen und eine faire
Regelungsbaseline benötigt würden.

Die Auswahl von H1 ist keine Annahme, dass der Effekt existiert oder technisch
nützlich ist. Beides muss getrennt nachgewiesen werden.

## 3. Physikalischer Vorzustand

Der Vorzustand ist eine **direkt messbare Restabweichung einer realen
Sensorfläche nach einem definierten Konditionierungsreiz**. Er darf nicht aus
einem später angepassten Modell oder aus einer Klassenbezeichnung abgeleitet
werden.

Für jede Zelle `i` gilt vor dem Folgereiz die baselinebereinigte Abweichung
`p_i = s_i(t_pre) - b_i`. Dabei ist `s_i` das kalibrierte Rohsignal und `b_i`
der vor der Versuchsserie bestimmte Referenzwert. Zusätzlich werden Betrag
und räumliche Verteilung des Vektors `p = (p_00, ..., p_33)` gespeichert.

Zwei Arten des Vorzustands werden verglichen:

1. **Referenzzustand R:** Alle Zellen erfüllen das bestehende
   Rückkehrkriterium. Danach folgt eine zusätzliche Wartezeit von einer
   Sekunde.
2. **Dissipativer Vorzustand P:** Ein festgelegter Konditionierungsreiz wurde
   beendet; der Folgereiz beginnt nach einer definierten kurzen oder langen
   Wartezeit, obwohl eine messbare Restabweichung bestehen darf.

Temperatur, Versorgung, Kontaktposition und mechanischer Aufbau müssen für R
und P innerhalb ihrer vorab kalibrierten Toleranzen liegen. Anderenfalls ist
der Paarvergleich technisch ungültig.

## 4. Konditionierungs- und Folgereiz

Als erste mögliche reale Quelle bleibt die vorbereitete piezoresistive
`4×4`-Drucksensorfläche vorgesehen. Der Konditionierungsreiz und der
anschließende Folgereiz verwenden:

- dieselbe zentrale Einzelzellgeometrie,
- dieselbe Position und Neigung,
- `50 %` des gemessenen gemeinsamen Kraftarbeitsbereichs,
- dieselbe nominelle Anstiegs- und Abfallsrate,
- dieselbe Haltezeit,
- dieselbe gemessene Umgebungstoleranz.

Maßgeblich ist die Referenzkraft, nicht der Aktorsollwert. Zwei Folgereize
gelten nur dann als identisch, wenn ihre gemessenen Spitzenkräfte um höchstens
`2 %`, ihre Kraft-Zeit-Flächen um höchstens `2 %` und ihre Kontaktzeiten um
höchstens `2 %` voneinander abweichen. Die Positionsabweichung darf höchstens
ein Zehntel des Zellabstands betragen. Engere Grenzen aus der späteren
Messunsicherheitsanalyse haben Vorrang.

Ein ungültiges Paar wird mit Grund dokumentiert und nicht ersetzt. Die
Versuchsreihenfolge wird vor Beginn gespeichert und innerhalb jedes Blocks
randomisiert.

## 5. Festgelegte Wartezeiten

Die dominante physikalische Relaxationszeit `tau_relax` und die erforderliche
Beobachtungsdauer müssen aus dem bereits geforderten realen Vorversuch
stammen. Erst danach werden folgende Wartebedingungen gebildet:

- **kurz:** `w_kurz = 1 × tau_relax`,
- **lang:** `w_lang = 3 × tau_relax`,
- **Referenz:** vollständige Erfüllung des Rückkehrkriteriums plus eine
  Sekunde.

Die numerischen Zeiten werden nach dem Vorversuch, aber vor Aufnahme einer
getrennten H1-Validierungsserie versioniert eingefroren. Sie dürfen nicht aus
dem beobachteten H1-Effekt optimiert werden. Ist `tau_relax` nicht mit
ausreichender Güte und Unsicherheit bestimmbar, erhält H1 keine Messfreigabe.

## 6. Messgrößen der Reaktionsdifferenz

Für jeden Folgereiz wird aus den baselinebereinigten, kalibrierten
Zellsignalen die räumlich summierte Reaktionsfläche bestimmt:

`A_S = Integral über W [Summe_i |s_i(t) - b_i|] dt`.

Das feste Beobachtungsfenster `W` beginnt am Kontaktbeginn und endet nach der
im Vorversuch festgelegten Beobachtungsdauer. Die **primäre
Reaktionsdifferenz** ist die gepaarte relative Differenz

`D_A = (A_S,P - A_S,R) / A_S,R`

zwischen einem Folgereiz aus Vorzustand P und seinem kraftangepassten
Referenzreiz aus R.

Sekundär werden vorab dieselben Paare verglichen hinsichtlich:

- maximaler räumlich summierter Reaktion,
- Anfangssteigung nach Kontaktbeginn,
- Reaktionsfläche nach Kontaktende,
- zellweiser normierter Musterdifferenz,
- Zeit bis zur erneuten dauerhaften Rückkehr.

Diese Größen beschreiben die physikalische Sensorreaktion. Eine spätere
Zustandsfläche darf erst nach Messfreigabe daraus abgeleitet werden.

## 7. Unsicherheitsgrenze

Für `D_A` wird eine erweiterte Messunsicherheit `U_D` mit ungefähr `95 %`
Überdeckungswahrscheinlichkeit bestimmt. Sie muss mindestens Beiträge aus
Referenzkraft, Zeitbasis, ADC-Auflösung, Kalibrierung, Nullpunktdrift,
Reizangleichung und Wiederholungsstreuung enthalten.

Die kleinste relevante Reaktionsdifferenz wird vor der H1-Validierungsserie
festgelegt als:

`delta_min = max(0,05; U_D)`.

Damit gilt weder ein Effekt unter `5 %` noch ein Effekt innerhalb der
erweiterten Messunsicherheit als belastbare vorzustandsabhängige Reaktion. Für
die gepaarten `D_A`-Werte wird zusätzlich ein zweiseitiges `95-%`-
Konfidenzintervall berichtet. Stichprobenzahl und Auswertungsverfahren werden
in einer späteren Messvorregistrierung festgelegt, nicht in diesem
Auswahlbeschluss.

## 8. Rückkehr- und Dissipationsbedingung

Eine für H1 geeignete Reaktion muss neben der Differenz folgende Bedingungen
erfüllen:

1. Nach jedem Reiz wird das bestehende dauerhafte Rückkehrkriterium erreicht.
2. Die Restabweichung vor dem Folgereiz ist bei `w_lang` kleiner als bei
   `w_kurz`.
3. Der Betrag der primären Reaktionsdifferenz nimmt von `w_kurz` zu `w_lang`
   ab.
4. Im Referenzzustand treten weder fortlaufende Drift noch selbstverstärkende
   Ausschläge auf.

Diese Bedingungen prüfen eine begrenzte, abklingende Vorgeschichte. Eine
dauerhafte Veränderung, unkontrollierte Aufschaukelung oder fehlende Rückkehr
erfüllt H1 nicht.

## 9. Entscheidungs- und Falsifikationsregel

H1 erhält nur dann Unterstützung für eine spätere Modellvorregistrierung,
wenn bei `w_kurz` das gesamte zweiseitige `95-%`-Konfidenzintervall von `D_A`
entweder oberhalb `+delta_min` oder unterhalb `-delta_min` liegt und zugleich
alle Rückkehr- und Dissipationsbedingungen erfüllt sind.

H1 gilt für die geprüfte Sensorquelle und den festgelegten Arbeitsbereich als
falsifiziert, wenn mindestens einer dieser Fälle eintritt:

- das gesamte Konfidenzintervall bei `w_kurz` liegt innerhalb
  `[-delta_min, +delta_min]`,
- die Richtung der gepaarten Differenz ist unter identischen Bedingungen
  nicht reproduzierbar,
- die Reaktionsdifferenz nimmt mit längerer Wartezeit nicht ab,
- das dauerhafte Rückkehrkriterium wird nicht zuverlässig erreicht.

Schneidet das Konfidenzintervall eine Entscheidungsgrenze, ist das Ergebnis
unbestimmt und kein positiver Befund. Eine Wiederholung wäre nur nach einem
getrennten, vorab begründeten Beschluss zulässig.

Lassen sich identische Folgereize nicht innerhalb der festgelegten Toleranzen
herstellen oder messtechnisch unterscheiden, ist der Versuch technisch
ungültig. Dieser Fall beendet die Freigabe, falsifiziert H1 aber nicht.

## 10. Daten- und Modellgrenze

Die Drucksensorlinie bleibt bis zum Eingang realer Hardware oder echter
Paar-Dateien gemäß `measurement_interface/` pausiert. Zuerst werden
ausschließlich Datenintegrität, Kalibrierbarkeit, Relaxationszeit,
Beobachtungsdauer und Messunsicherheit geprüft.

Ohne diese realen Kennwerte beginnen keine Modellierung, keine Simulation,
keine synthetische Datenerzeugung und keine Parametersuche. Auch bei einem
positiven physikalischen H1-Befund wäre eine Zustandsgleichung erst Gegenstand
einer neuen, getrennt versionierten Modellvorregistrierung.
