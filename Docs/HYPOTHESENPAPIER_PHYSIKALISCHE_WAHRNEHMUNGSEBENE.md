# Hypothesenpapier: physikalische Wahrnehmungsebene

**Projekt:** FELDCHIP_SIMULATION

**Status:** Kandidatenbildung vor Auswahl und Vorregistrierung

**Geltungsbereich:** technische Sensor-zu-Zustand-Abbildung

## 1. Ziel

Eine physikalische Wahrnehmungsebene ist hier eine technisch definierte
Zwischenschicht zwischen Sensor und Prozessor. Sie soll einen realen
physikalischen Verlauf lokal in einen begrenzten, rückführbaren Zustand
überführen und nur wenige messrelevante Größen weitergeben.

Gesucht wird kein allgemeiner Rechenvorteil. Eine tragfähige Hypothese muss
begründen, warum eine bestimmte physikalische Ursache bereits nahe am Sensor
verdichtet werden sollte. Sie muss außerdem gegen Rohdatenerfassung und gegen
die bisherige Referenz aus ungekoppelter Ein-Zustands-Dynamik mit
Mittelwert-/Steigungs-Auslese prüfbar sein.

Dieses Papier beschreibt genau drei Anwendungsszenarien. Es wählt noch keines
davon aus und enthält weder Simulation noch Parametersuche.

## 2. Gemeinsame Randbedingungen

- Der lokale Arbeitsbereich bleibt normiert auf `−3…+3`.
- Jeder Zustand besitzt einen kontrollierten Rückführungspunkt.
- Die Prozessorebene erhält weniger Werte als eine vollständige zeitaufgelöste
  Rohdatenerfassung.
- Ein Vergleich verwendet identische Sensorereignisse, Störungen, Zeitfenster
  und Ausgangsbandbreiten.
- Klassifikationsrate darf berichtet werden, ist aber keine primäre
  Erfolgsgröße.
- Ein Vorteil gilt erst nach einer getrennten Vorregistrierung und einem
  unabhängigen Bestätigungslauf als bestätigt.

## 3. Szenario A: lokaler Kontaktimpuls in einer Drucksensorfläche

### 3.1 Reale Eingangsgröße

Eingang ist die zeitabhängige Kraft beziehungsweise Druckänderung eines
piezoresistiven, kapazitiven oder piezoelektrischen `4×4`-Sensorfeldes.
Relevant sind Kontaktbeginn, Belastungsanstieg, Entlastung und die durch
Material und Kontaktmechanik verursachte Relaxation.

### 3.2 Gewünschter lokaler Zustand

Jede Zelle bildet eine vorzeichenbehaftete Auslenkung relativ zu ihrem
kalibrierten Ruhewert. Ein schneller Anteil repräsentiert den Kontaktimpuls;
die kontrollierte Rückführung bildet das Abklingen nach der Belastung ab. Die
Zeitkonstante wäre nicht frei zu suchen, sondern aus gemessener Sensor- und
Materialrelaxation abzuleiten.

### 3.3 Reduzierte Übergabe

Vorgesehen sind höchstens sechs Werte pro Messfenster:

- Gesamtkraft beziehungsweise Betragsenergie,
- zwei Koordinaten des Druckschwerpunkts,
- Kontaktfläche,
- maximale Anstiegsrate,
- Relaxationszeit oder Restzustand nach festem Zeitabstand.

### 3.4 Vermuteter Vorteil

Eine Rohdatenlösung müsste alle 16 Kanäle während des gesamten Kontakts mit
ausreichender Rate digitalisieren. Die bestehende Referenz verdichtet zwar den
Feldverlauf, trennt aber Kontaktimpuls und physikalische Relaxation nicht
explizit. Die Hypothese lautet, dass eine aus der realen Relaxationskennlinie
abgeleitete lokale Zustandsbildung die Zahl der ADC-Abtastungen und
übertragenen Werte reduziert, ohne Impuls- und Entlastungsinformation zu
verlieren.

### 3.5 Messbare Erfolgsgröße

Primär: normierter Fehler der rekonstruierten Kraft-Zeit-Fläche bei festem
Ausgabebudget. Zusätzlich werden Kontaktlatenz, Relaxationszeitfehler und
benötigte ADC-Abtastungen je Kontakt berichtet.

### 3.6 Falsifikation

Die Hypothese ist falsifiziert, wenn Rohdaten oder Referenzarchitektur bei
gleichem Ausgabebudget einen höchstens gleich großen Rekonstruktionsfehler und
keine höhere Latenz erreichen oder wenn die Zustandsbildung die Zahl der
erforderlichen ADC-Abtastungen nicht senkt.

## 4. Szenario B: thermischer Fluss und bewegter Wärmeeintrag

### 4.1 Reale Eingangsgröße

Eingang ist die lokale Temperatur- oder Wärmestromänderung eines
Thermopile-, Widerstands- oder Diodenfeldes. Relevant sind Beginn, Richtung und
Dauer eines bewegten Wärmeeintrags bei langsam veränderlichem Hintergrund.

### 4.2 Gewünschter lokaler Zustand

Jede Zelle bildet die thermische Abweichung von einem kontrollierten
Referenzwert. Der Zustand soll der gemessenen thermischen Zeitkonstante des
Sensorelements folgen und nach Ende des Wärmeeintrags reproduzierbar
zurückkehren. Eine mögliche Nachbarschaftswirkung wäre nur zulässig, wenn sie
aus real gemessener Wärmeleitung des Trägers abgeleitet wird.

### 4.3 Reduzierte Übergabe

Vorgesehen sind höchstens sechs Werte pro Messfenster:

- gesamte thermische Abweichung,
- zwei Koordinaten des thermischen Schwerpunkts,
- zwei Komponenten der Bewegungsrichtung,
- zeitlich integrierte Wärmedosis.

### 4.4 Vermuteter Vorteil

Rohdaten erfordern eine wiederholte Digitalisierung aller Sensoren, um
Hintergrunddrift, Bewegungsrichtung und Wärmedosis nachträglich zu bestimmen.
Die Referenzarchitektur nutzt eine allgemeine Rückführung, aber keine aus dem
realen Wärmefluss abgeleitete Zustandsgröße. Die Hypothese lautet, dass eine
physikalisch kalibrierte thermische Zustandsbildung die notwendige Abtastrate
senkt und Wärmedosis sowie Bewegungsrichtung bei Drift stabiler erhält.

### 4.5 Messbare Erfolgsgröße

Primär: Fehler der Wärmedosis bei festem Übertragungsbudget. Zusätzlich werden
Schwerpunkt-RMSE, Richtungsfehler, Driftfehler und übertragene Werte pro Sekunde
gemessen.

### 4.6 Falsifikation

Die Hypothese ist falsifiziert, wenn die thermische Eigendynamik des Sensors
bereits dieselbe Verdichtung liefert, wenn die Referenzarchitektur bei gleichem
Budget Wärmedosis und Richtung mindestens gleich genau bestimmt oder wenn
Drift die lokale Zustandsabbildung stärker verfälscht als die Rohdatenlösung.

## 5. Szenario C: lokale Schwingungsphase in einem Resonanzsensorfeld

### 5.1 Reale Eingangsgröße

Eingang ist die zeitabhängige Spannung eines `4×4`-Feldes aus piezoelektrischen
oder mikromechanischen Schwingungssensoren. Relevant sind Amplitude,
Phasenlage, Ankunftszeit und Dämpfung einer mechanischen Welle in einem vorab
festgelegten Frequenzband.

### 5.2 Gewünschter lokaler Zustand

Jede Zelle bildet einen begrenzten phasenempfindlichen Resonanzzustand, dessen
Mittenfrequenz und Dämpfung aus der gemessenen mechanischen Übertragungsfunktion
abgeleitet werden. Der Zustand kehrt ohne Eingang zum Referenzpunkt zurück. Er
ist damit kein frei abgestimmter zweiter Zustand, sondern eine Abbildung einer
konkreten Resonanz des Sensors oder Trägers.

### 5.3 Reduzierte Übergabe

Vorgesehen sind höchstens sechs Werte pro Messfenster:

- Gesamtenergie im festgelegten Frequenzband,
- zwei Komponenten der geschätzten Ausbreitungsrichtung,
- räumliche Phasenkohärenz,
- dominante Frequenz,
- Abklingrate.

### 5.4 Vermuteter Vorteil

Eine Rohdatenlösung muss alle 16 Kanäle deutlich oberhalb der relevanten
Frequenz abtasten und Phasenbeziehungen digital berechnen. Die bisherige
Mittelwert-/Steigungs-Auslese erhält schnelle Phasenlagen nur unzureichend. Die
Hypothese lautet, dass sensornahe resonante Zustände die für Richtung und
Dämpfung erforderliche Phaseninformation mit erheblich geringerer
Ausgabebandbreite bereitstellen.

### 5.5 Messbare Erfolgsgröße

Primär: mittlerer absoluter Winkelfehler der Ausbreitungsrichtung bei festem
Ausgabebudget. Zusätzlich werden Phasenfehler, Frequenzfehler,
Erkennungslatenz und erforderliche ADC-Abtastungen je Ereignis gemessen.

### 5.6 Falsifikation

Die Hypothese ist falsifiziert, wenn Rohdaten oder Referenzarchitektur bei
gleichem Ausgabebudget einen höchstens gleich großen Richtungsfehler erreichen,
wenn Bauteilstreuung die Phasenkohärenz unbrauchbar macht oder wenn die
erforderliche sensornahe Abtastrate gegenüber der Rohdatenlösung nicht sinkt.

## 6. Auswahlverfahren für den nächsten Abschnitt

Die Auswahl erfolgt erst nach diesem Papier in einem getrennten, versionierten
Beschluss. Genau ein Szenario darf ausgewählt werden. Es muss vor einer
Modellierung folgende Bedingungen erfüllen:

1. Die physikalische Ursache ist durch Messdaten oder ein belastbares
   Bauteilmodell quantifizierbar.
2. Sensor, Störgrößen und Referenzverfahren sind praktisch beschaffbar oder
   reproduzierbar nachbildbar.
3. Die primäre Erfolgsgröße kann ohne Klassifikationsmodell gemessen werden.
4. Ausgangsbandbreite, Latenz und Zahl der ADC-Abtastungen können für alle
   Verfahren gleich oder transparent vergleichbar festgelegt werden.
5. Der Falsifikationsfall kann mit vertretbarem Versuchsaufwand erreicht
   werden.

Vor der Auswahl werden keine Simulationswerte erzeugt. Nach der Auswahl werden
zunächst reale Kennwerte beziehungsweise belastbare Bauteilparameter erhoben,
dann ein einzelner Versuchsplan vorregistriert und erst anschließend ein Modell
implementiert.

## 7. Aussagegrenze

Alle drei Szenarien sind prüfbare Arbeitshypothesen. Das Papier behauptet weder
einen Energie- noch einen Verarbeitungs- oder Fertigungsvorteil. Es legt nur
fest, welche physikalischen Ursachen, reduzierten Größen und Gegenbelege eine
spätere Untersuchung tragen müssten.
