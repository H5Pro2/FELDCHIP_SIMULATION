# Forschungsplan

## Zweck

Das Projekt untersucht, welche Zustands- oder Kopplungsdynamik gegenüber einem
ungekoppelten dynamischen Array einen konstruktiven Nutzen für einen möglichen
Sensor-Front-End-Chip erzeugen könnte. Die bisher geprüfte positive,
symmetrische Nachbarschaftskopplung wird nicht als Vorteilskandidat
weitergeführt.

Alle Aussagen bleiben auf die jeweils simulierte Aufgabe begrenzt.

## Ausgangsbefund

- Die vier Rückführungskennlinien erzeugen nahezu gleiche Trennraten.
- Die beste Feldvariante liegt 5,4 Prozentpunkte hinter der Rohsignal-Baseline.
- Die aktuelle innere Rückführung erreicht den Referenzbereich zu langsam.
- Im regulären Lauf treten keine Grenzüberschreitungen auf.

Die Regimezahl wird nicht weiter optimiert. Die langsame Rückkehr wird als
separater technischer Parameterbefund geführt und nicht mit der
Klassifikationsleistung vermischt.

## Abgeschlossener Versuch: kompakte Auslese

### Hypothese

Geprüft wurde, ob eine gekoppelte Feldvorverarbeitung bei begrenzter
Auslesebandbreite nützlicher ist als bei vollständiger Digitalisierung aller 16
Zellwerte.

### Vorab festgelegte Merkmale

Jedes `4×4`-Feld wird auf genau acht Skalare reduziert:

1. vorzeichenbehafteter Mittelwert,
2. mittlerer Betrag als Aktivitätsmaß,
3. horizontaler Betragsschwerpunkt,
4. vertikaler Betragsschwerpunkt,
5. horizontale räumliche Ausdehnung,
6. vertikale räumliche Ausdehnung,
7. positiver Spitzenwert,
8. Betrag des negativen Spitzenwerts.

Die Definitionen werden identisch auf alle Feldmodelle und Baselines angewendet.
Sie werden nach dem Lauf nicht verändert.

### Konstant gehalten

- Arbeitsbereich `−3…+3`,
- sämtliche Modellparameter und Kennlinien,
- sechs Eingangsmuster,
- drei Rauschstufen,
- fünf Seeds,
- Trainings- und Teststichproben,
- Nächste-Zentroid-Auswertung.

### Primäre Messgröße

Mittlere Mustertrennung über alle Seeds und Rauschstufen. Zusätzlich werden
Trennverhältnis und Wiederhol-RMSE berichtet.

### Entscheidungskriterium

Ein Nutzen der Feldbildung ist in dieser Aufgabe nur dann vorläufig sichtbar,
wenn die beste Feldvariante die beste identisch ausgelesene Baseline um mehr als
zwei Prozentpunkte übertrifft. Andernfalls bleibt der Nutzen nicht nachgewiesen.

Der beobachtete Vorsprung von `0,8` Prozentpunkten und das gepaarte Intervall von
`−0,8` bis `+2,3` Prozentpunkten erfüllen das Entscheidungskriterium nicht.

## Abgeschlossener Hauptversuch: zeitlich-räumliche Dynamik

Die Forschungsfrage wird auf wandernde, überlagerte, zeitlich integrierte und
kurze Eingangsmuster mit Nachlauf verschoben. Sequenzen, gemeinsame Auslese und
Erfolgskriterium stehen vor Ausführung in `TEMPORALER_VERSUCHSPLAN.md`.

Der unveränderte Lauf ergab `85,3 %` für die beste Feldvariante und `89,7 %`
für die beste Baseline. Die gepaarte Differenz von `−4,5` Prozentpunkten mit
einem approximativen 95-%-Intervall von `−5,5` bis `−3,5` Prozentpunkten
verfehlt beide Erfolgskriterien. In dieser Aufgabe ist ein Nutzen des
zeitlichen Zustands sichtbar, aber kein zusätzlicher Nutzen der räumlichen
Kopplung.

## Separater Rückführungsversuch

Die Rückführung wurde als technische Pflichtprüfung unabhängig von der
Sequenztrennung untersucht.
Dabei werden keine Musterkennzahlen zur Auswahl der Parameter verwendet.
Primäre Größe ist der Anteil der Zustände, die innerhalb der festgelegten Zeit
zum Referenzbereich zurückkehren.

Parameterraum, Anfangsauslenkungen, Grenzwerte und numerische Bestätigung wurden
vor dem Lauf in `RUECKFUEHRUNG_VORREGISTRIERUNG.md` festgelegt. Zehn von 87
Kandidaten erfüllen die Hauptkriterien; alle drei nach Rangfolge ausgewählten
Kandidaten bestehen auch die Zeitschrittprüfung. Der bestplatzierte Kandidat ist
damit technisch zugelassen, aber noch nicht als Verarbeitungsarchitektur
ausgewählt.

## Architektur-Neuausrichtung

Die allgemeinere Architektursuche prüft getrennt gerichtete oder anisotrope
Kopplung, hemmende Kopplungsanteile, mehrere Zeitskalen, lokale Adaptation und
ereignisbasierte Auslese. Das methodische Vorgehen ist in
`ARCHITEKTUR_NEUAUSRICHTUNG.md` festgelegt. Größere Arrays folgen erst, wenn ein
Mechanismus auf `4×4` einen vorab definierten Vorteilskandidaten liefert.

Der erste Mechanismus ist gerichtete beziehungsweise reziprok anisotrope
Kopplung auf Basis der bestätigten konstanten Rückführung `1,6`. Kandidatenraum,
technische Zulassung, Entwicklungsdaten und Auswahlregel sind vor Ausführung in
`ANISOTROPE_KOPPLUNG_VORREGISTRIERUNG.md` festgelegt.

Der ausgeführte Lauf lässt alle 26 Modelle technisch zu, aber kein neues Modell
erfüllt die explorative Auswahlregel. Die beste gerichtete Variante liegt
`2,18` Prozentpunkte und die beste reziprok anisotrope Variante `2,27`
Prozentpunkte unter der ungekoppelten Pflichtbaseline. Für diesen Mechanismus
wird daher kein Bestätigungslauf angelegt.

Als nächster explorativer Mechanismus werden mehrere lokale Zeitskalen ohne
räumliche Kopplung geprüft. Die bestätigte konstante Rückführung bleibt die
Ein-Zustands-Pflichtbaseline. Modellraum, technische Zulassung, zwei Aufgaben
und Auswahlregel sind in `MEHRERE_ZEITSKALEN_VORREGISTRIERUNG.md` vorab
festgelegt.

Der ausgeführte Lauf lässt 19 von 28 Modellen technisch zu und wählt gemäß der
vorregistrierten Regel `zwei_zustaende_l1.2_s2_a0.5` als explorativen Kandidaten
aus. Der Gesamtvorsprung von `2,38` Prozentpunkten entsteht überwiegend in der
Zeitskalenaufgabe; die Kontinuitätsaufgabe bleibt leicht positiv. Vor jeder
Bestätigung ist ein neuer Plan mit frischen Seeds erforderlich.

Der Bestätigungsplan unter
`BESTAETIGUNG_ZEITSKALEN_VORREGISTRIERUNG.md` fror Kandidat,
Ein-Zustands-Baseline, beide Aufgaben, fünf neue Seeds und ein kombiniertes
Effekt-, Intervall- und Erhaltungskriterium vor der Ausführung ein.

Der ausgeführte Bestätigungslauf ergibt einen positiven mittleren Unterschied
von `1,18` Prozentpunkten mit einem approximativen 95-%-Intervall von `+0,15`
bis `+2,21` Punkten. Aufgaben- und Rauschmittel bleiben nichtnegativ, aber die
vorregistrierte Mindestgröße von mehr als `2,0` Punkten wird verfehlt. Der
explorative Vorteil ist damit nicht bestätigt.

Der konkrete Zwei-Zustands-Kandidat wird nicht nachoptimiert und nicht erneut
bestätigend geprüft. Als neuer explorativer Mechanismus folgt lokale begrenzte
Adaptation ohne räumliche Kopplung. Modellraum, technische Zulassung, drei
Aufgaben, neue Seeds und Auswahlregel sind in
`ADAPTATION_VORREGISTRIERUNG.md` festgelegt.

## Übergang zu SPICE

Eine SPICE-Einzelzelle ist erst begründet, wenn Rückführbarkeit nachgewiesen ist
und mindestens ein Mechanismus einen klaren, reproduzierbaren Kandidaten
liefert. Bis dahin bleiben elektrische Energie, reale Bauteilstreuung,
Temperaturverhalten und Fertigbarkeit ungeprüft.
