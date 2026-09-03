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

Der vorregistrierte Adaptationslauf wurde ausgeführt. `22` von `24` Varianten
sind technisch zugelassen, aber keine erfüllt die Auswahlregel. Der stärkste
zugelassene Befund beträgt `+1,02` Prozentpunkte und unterschreitet die
Mindestwirkung; zudem ist sein Mittel bei Rauschstufe `0,35` negativ. Der
Mechanismus endet deshalb ohne Kandidaten für einen Bestätigungslauf.

Als nächster klar getrennter Mechanismus wird die Auslese statt der lokalen
Dynamik variiert. `EREIGNISAUSLESE_VORREGISTRIERUNG.md` friert zwei
16-Werte-Kontrollen, zwölf Ereignisvarianten, drei bestehende Aufgaben, neue
Seeds und eine konservative Auswahl gegen beide Kontrollen ein.

Der Lauf wurde ohne Kandidaten abgeschlossen. Die stärkste Ereignisvariante
liegt `15,08` Prozentpunkte hinter der bisherigen und `11,82` Punkte hinter der
normierten Kontrolle. Die konkrete Delta-Modulation mit Endakkumulatoren wird
deshalb nicht bestätigt und nicht innerhalb dieses Parameterraums nachoptimiert.

## Abschluss der Suchphase

Die aktuelle mechanismenorientierte Suchphase ist abgeschlossen. Im geprüften
dimensionslosen `4×4`-Modell ist die ungekoppelte Ein-Zustands-Dynamik mit
Mittelwert-/Steigungs-Auslese die belastbare Referenz. Rückführung und
numerische Stabilität sind technisch erreichbar; für die geprüften
Erweiterungen wurde kein bestätigter Zusatznutzen nachgewiesen.

Eine neue Phase wird nicht durch weitere Kombinationen bereits untersuchter
Parameter eröffnet. Voraussetzung ist eine vorab formulierte Hypothese, die
entweder eine konkrete physikalische Ursache oder einen klar abgegrenzten
Anwendungsbedarf mit messbarem Erfolgskriterium adressiert.

Das erste Hypothesenpapier liegt unter
`Docs/HYPOTHESENPAPIER_PHYSIKALISCHE_WAHRNEHMUNGSEBENE.md`. Es beschreibt drei
prüfbare Szenarien, trifft aber noch keine Auswahl. Auswahl, Vorregistrierung
und Modellierung bleiben getrennte nachfolgende Schritte.

Mit `Docs/AUSWAHLBESCHLUSS_001_DRUCKSENSORFLAECHE.md` wurde Szenario A als
einziger erster Anwendungsabschnitt ausgewählt. Der Beschluss enthält noch kein
Modell. Vor jeder Modellierung folgt ein getrennt versioniertes Mess- und
Parametrisierungsprotokoll.

Dieses Protokoll liegt nun unter
`Docs/MESS_UND_PARAMETRISIERUNGSPROTOKOLL_DRUCKSENSORFLAECHE.md`. Es legt eine
piezoresistive Polymer-Sensorfläche, reale Kontaktfolgen, Störgrößen,
Relaxationskennwerte, sechs Übergabewerte, Pflichtbaselines und den Fehler der
Kraft-Zeit-Fläche als primäre Erfolgsgröße fest. Messwerte und Modellparameter
liegen noch nicht vor.

Unter `measurement_interface/` sind CSV-Vertrag, Metadatenschema und eine
Kopfzeilenvorlage für reale Vorversuche festgelegt. Der lesende Validator
`validate_measurement_data.py` prüft nur Datenintegrität und Prüfsummen. Er
erzeugt weder Messwerte noch Modellparameter. Bis reale Daten vorliegen, bleibt
der Abschnitt ohne Mess- und Modellfreigabe pausiert.

## Phase II: kontinuierliche sensorische Zustandsfläche

Der versionierte Architekturrahmen liegt unter
`Docs/ARCHITEKTURPAPIER_PHASE_II_KONTINUIERLICHE_SENSORISCHE_ZUSTANDSFLAECHE.md`.
Er trennt Sensoradapter, lokale Zustandsfläche, reduzierte Prozessschnittstelle
und optionalen Umweltpfad. Die alte Drucksensorlinie bleibt bis zu realen Daten
pausiert und ist nur eine mögliche spätere Eingangsquelle.

Von den drei getrennten Architekturhypothesen wurde H1, die
vorzustandsabhängige dissipative Reaktion, im versionierten
`Docs/AUSWAHLBESCHLUSS_002_H1_VORZUSTANDSABHAENGIGE_DISSIPATIVE_REAKTION.md`
als erste Operationalisierung ausgewählt. Der Beschluss definiert Vorzustand,
identische Folgereize, Wartezeiten, Reaktionsdifferenz, Unsicherheitsgrenze und
Falsifikation. Er erteilt keine Modell- oder Simulationsfreigabe. Die reale
Drucksensorfläche bleibt die erste mögliche Quelle und bis zu realen Daten
pausiert.

## Übergang zu SPICE

Eine SPICE-Einzelzelle ist erst begründet, wenn Rückführbarkeit nachgewiesen ist
und mindestens ein Mechanismus einen klaren, reproduzierbaren Kandidaten
liefert. Bis dahin bleiben elektrische Energie, reale Bauteilstreuung,
Temperaturverhalten und Fertigbarkeit ungeprüft.
