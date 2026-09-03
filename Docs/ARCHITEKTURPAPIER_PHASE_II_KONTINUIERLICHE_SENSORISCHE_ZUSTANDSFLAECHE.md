# Architekturpapier Phase II: kontinuierliche sensorische Zustandsfläche

**Version:** 1.0

**Datum:** 3. September 2026

**Status:** Architekturrahmen vor Auswahl einer Operationalisierung

## 1. Zweck

Phase II untersucht eine technisch definierte Ebene zwischen Sensorik und
Prozessor. Diese Ebene nimmt kontinuierliche physikalische Eingänge auf, führt
lokale begrenzte Zustände, bildet zeitliche Nachwirkung und kontrollierte
Rückkehr ab und stellt wenige zustandsbezogene Messgrößen bereit.

Ziel ist weder eine höhere Klassifikationsrate noch ein allgemeiner
Rechenvorteil. Das Architekturpapier legt Begriffe, Systemgrenzen,
Schnittstellen und Beobachtungskriterien fest. Es wählt noch keine einzelne
Architekturhypothese aus und enthält keine Simulation oder Parametersuche.

Die Ergebnisse der abgeschlossenen Mechanismensuche bleiben gültig. Die
ungekoppelte Ein-Zustands-Dynamik mit Mittelwert-/Steigungs-Auslese ist die
technische Referenz. Abgeschlossene Kopplungs-, Mehrzustands-, Adaptations- und
Ereignisauslesevarianten werden nicht erneut geöffnet.

## 2. Systemgrenze

Die Architektur besteht aus vier getrennten Bereichen:

```text
physikalische Quelle
        |
        v
Sensor + modalspezifischer Adapter
        |
        v
kontinuierliche lokale Zustandsfläche
        |
        v
reduzierte Prozessschnittstelle ---> Prozessorebene
        ^                                  |
        |                                  v
begrenzte Steuerbefehle             optionaler Aktor
        |                                  |
        +---------- Umweltpfad <-----------+
```

### 2.1 Sensorquellen

Eine Sensorquelle wandelt eine reale Größe in ein elektrisches oder bereits
digitalisiertes Rohsignal um. Beispiele sind Druck, Schallfeld oder optische
Intensität. Sensorkennlinie, Bandbreite, Rauschen, Drift und räumliche
Anordnung gehören zur Sensorbeschreibung und werden nicht der Zustandsfläche
zugeschrieben.

### 2.2 Modalspezifischer Adapter

Der Adapter ordnet Rohkanäle räumlichen Zellen zu, versieht sie mit einer
gemeinsamen Zeitbasis und überführt ihre physikalischen Einheiten in einen
normierten Antrieb. Kalibrierung, Antialiasing, Offsetkorrektur und bekannte
Gültigkeitsgrenzen liegen in diesem Bereich.

Der Adapter darf keine nicht dokumentierte Klassifikation oder semantische
Vorentscheidung durchführen. Jede Transformation muss auf messbaren
Sensoreigenschaften beruhen.

### 2.3 Zustandsfläche

Die Zustandsfläche besteht aus adressierbaren lokalen Zellen. Eine Zelle führt
mindestens einen kontinuierlichen Hauptzustand und einen definierten
Referenzzustand. Räumliche Beziehungen sind Teil der Geometrie, begründen aber
noch keine Kopplung. Eine Kopplung wäre nur als eigene Hypothese mit
physikalischer Ursache zulässig.

### 2.4 Prozessorebene

Die Prozessorebene erhält ausschließlich die freigegebenen reduzierten
Zustandsgrößen und technische Statusangaben. Sie darf Rohdaten parallel
erfassen, wenn dies für einen Vergleich erforderlich ist. Die Rohdatenleitung
gehört dann zur Messbaseline und nicht zum behaupteten Funktionsumfang der
Zustandsfläche.

### 2.5 Aktor und Umweltpfad

Ein optionaler Aktor verändert die reale Umgebung. Seine Wirkung darf die
Zustandsfläche nur über eine erneut gemessene Sensorgröße erreichen. Dieser
Umweltpfad ist von direkten Steuerbefehlen an die Zustandsfläche getrennt und
wird mit eigener Latenz, Verstärkung und Begrenzung beschrieben.

## 3. Interne Zustandsgrößen

### 3.1 Lokaler Hauptzustand

Der lokale Hauptzustand `x_i(t)` einer Zelle `i` ist eine normierte technische
Repräsentation der sensorbezogenen Abweichung. Er ist kein gespeicherter
Rohwert und kein symbolisches Etikett. Sein zulässiger Bereich bleibt
konzeptionell auf `−3…+3` begrenzt.

Die Vorzeichen und Beträge erhalten erst durch den jeweiligen Sensoradapter
eine physikalische Bedeutung. Bei einem Drucksensor kann das Vorzeichen etwa
Belastung und Entlastungsabweichung unterscheiden; bei einem Audiosignal kann
es eine vorzeichenbehaftete Bandamplitude darstellen.

### 3.2 Referenzzustand

`r_i(t)` bezeichnet den technisch bestimmten Ruhezustand einer Zelle. Er wird
aus Kalibrierung oder einer ausdrücklich freigegebenen langsamen
Referenznachführung abgeleitet. Eine Änderung von `r_i` während einer
Messsequenz ist standardmäßig ausgeschlossen.

Der Referenzzustand darf nicht nachträglich so verschoben werden, dass ein
unerwünschtes Versuchsergebnis verschwindet. Zeitpunkt, Ursache und Betrag
jeder Referenzänderung müssen protokollierbar sein.

### 3.3 Persistenz

Persistenz ist die messbare Fortdauer einer Zustandsabweichung nach Änderung
oder Ende des auslösenden Eingangs. Sie wird durch Dauer, Verlauf und
Abhängigkeit vom Vorzustand beschrieben. Persistenz ist nur dann funktional,
wenn sie reproduzierbar, begrenzt und für eine festgelegte physikalische
Messgröße relevant ist.

### 3.4 Rückkehr

Rückkehr ist die dauerhafte Annäherung von `x_i(t)` an `r_i(t)`, nachdem der
relevante Eingang beendet wurde. Sie wird durch Toleranzband, Rückkehrquote,
Einschwingzeit, Restfehler und erneuten Toleranzaustritt bestimmt.

Ein bloßes kurzzeitiges Durchqueren des Toleranzbands gilt nicht als Rückkehr.
Ein Zustand, der ohne Eingang dauerhaft anwächst oder außerhalb seines
Arbeitsbereichs verbleibt, ist technisch unzulässig.

### 3.5 Technische Qualitätsgrößen

Zusätzlich zum Hauptzustand darf jede Zelle lokale technische Flags führen,
beispielsweise Sättigung, ungültige Kalibrierung oder Ausfall. Diese Angaben
werden nicht als zusätzlicher physikalischer Zustand interpretiert.

## 4. Zeitverhalten

### 4.1 Kurze Reaktion

Ein kurzer Reiz soll eine begrenzte Zustandsauslenkung erzeugen, wenn seine
Dauer oder Flankensteilheit innerhalb der freigegebenen Sensorbandbreite liegt.
Zu messen sind Ansprechlatenz, Spitzenwert, Impulsfläche und Rückkehrzeit.

Reize unterhalb der nachgewiesenen Sensorauflösung dürfen keine belastbare
Zustandsaussage begründen. Reize oberhalb des Arbeitsbereichs müssen als
Sättigung markiert werden.

### 4.2 Kontextnachwirkung

Kontextnachwirkung bezeichnet ausschließlich den Einfluss eines definierten
physischen Vorzustands auf die Reaktion eines späteren, identischen Reizes.
Beispiele sind Materialrelaxation, thermische Vorbelastung oder ein noch nicht
abgeklungener Sensorzustand.

Eine Kontextwirkung ist nur zulässig, wenn Ausgangszustand, Zwischenzeit und
Folgereaktion messbar sind. Ohne dokumentierten Vorzustand wird eine
Reaktionsänderung als Störung oder Drift behandelt.

### 4.3 Dauerreiz

Bei einem Dauerreiz muss der Zustand entweder einen stabilen Arbeitspunkt
erreichen oder einer vorab festgelegten, physikalisch begründeten Kennlinie
folgen. Langsames unbegrenztes Wandern ist unzulässig. Creep oder Drift dürfen
nur als Sensorphänomen geführt werden, wenn sie separat messbar sind.

### 4.4 Verhinderung unkontrollierter Aufschaukelung

Jede spätere Operationalisierung muss vor einer Aufgabenbewertung nachweisen:

- begrenzte Zustände für den gesamten zulässigen Eingangsbereich,
- dissipative Rückkehr ohne Eingang,
- keine dauerhafte positive Selbsterregung,
- definierte Reaktion bei Sättigung und Sensorausfall,
- Stabilität unter maximaler erlaubter Rückkopplung und Verzögerung,
- robuste Zeitschritt- beziehungsweise Abtastratenprüfung.

Sättigung allein gilt nicht als Stabilitätsnachweis. Ein begrenzter, aber
dauerhaft an einer Grenze haftender Zustand kann technisch unzulässig sein.

## 5. Prinzip der Sensorintegration

Die Zustandsfläche ist nicht ohne Adapter universell. Jede Eingangsart benötigt
eine eigene, messbare Abbildung.

### 5.1 Druck

Ein Druckadapter kann kalibrierte Kraft- oder Widerstandsabweichungen auf lokale
Zellen abbilden. Materialrelaxation, Hysterese und mechanisches Übersprechen
müssen aus realen Messungen stammen. Die bestehende Drucksensorlinie bleibt bis
zum Eingang realer Hardware oder Rohdaten pausiert.

### 5.2 Audio

Ein Audioadapter kann Mikrofonkanäle oder physikalisch definierte Frequenzbänder
räumlichen Zellen zuordnen. Bandbegrenzung, Phase, Abtastrate und
Antialiasing gehören zum Adapter. Das Architekturpapier behauptet weder eine
bestimmte Filterbank noch eine hardwareseitige Realisierung.

### 5.3 Bild

Ein Bildadapter kann Pixelgruppen, Helligkeitsabweichungen oder optisch
definierte lokale Kontraste auf Zellen abbilden. Belichtung, Bildrate,
Farbraum und optische Verzerrung müssen vor einer Zustandsdeutung festgelegt
werden. Eine semantische Objekterkennung gehört nicht zur Zustandsfläche.

### 5.4 Gemeinsame Integrationsregeln

Für jede Eingangsart sind vor einer Operationalisierung festzulegen:

1. physikalische Einheit und Kalibrierkette,
2. räumliche Zuordnung und Zeitbasis,
3. Arbeitsbereich und Auflösung,
4. bekannte Störungen und Ausfallzustände,
5. Abbildung auf Vorzeichen und Betrag des lokalen Zustands,
6. Rohdaten- und Referenzbaseline.

Unterschiedliche Eingänge dürfen nur dann in einer gemeinsamen Fläche
zusammengeführt werden, wenn ihre Zeit- und Raumbezüge technisch definiert
sind. Eine bloße Normierung auf denselben Zahlenbereich genügt nicht.

## 6. Prozessschnittstelle

### 6.1 Zulässige Ausgabeklassen

Pro Beobachtungsfenster darf die Prozessorebene höchstens acht numerische
Zustandsgrößen erhalten:

1. vorzeichenbehaftetes Zustandsmittel,
2. gesamte Betragsauslenkung,
3. x-Koordinate des Zustandsschwerpunkts,
4. y-Koordinate des Zustandsschwerpunkts,
5. räumliche Ausdehnung in x-Richtung,
6. räumliche Ausdehnung in y-Richtung,
7. zeitliche Änderungs- oder Rückkehrgröße,
8. technischer Gültigkeits- und Sättigungswert.

Eine einzelne Operationalisierung muss vorab eine Teilmenge festlegen und darf
das Ausgabebudget nicht nach Ergebnislage erweitern. Die Drucksensorlinie
behält unabhängig davon ihr bereits festgelegtes Sechs-Werte-Paket.

### 6.2 Lokal verbleibende Information

Nicht regulär an die Prozessorebene übertragen werden:

- vollständige Zeitreihen aller Zellzustände,
- interne Rückführungs- und Begrenzungssignale,
- lokale Zwischenwerte eines Adapters,
- nicht freigegebene Kalibrierwerte,
- nachträglich erzeugte Klassen- oder Bedeutungslabels.

Für wissenschaftliche Vergleichsmessungen dürfen diese Größen protokolliert
werden. Sie zählen dann als Diagnose- beziehungsweise Rohdatenbaseline und
nicht als reguläre reduzierte Schnittstelle.

## 7. Rückkopplung

### 7.1 Zulässige Steuersignale

Die Prozessorebene darf nur folgende begrenzte und protokollierte Befehle an
die Zustandsfläche senden:

- explizite Rücksetzung zum Referenzzustand zwischen Messfenstern,
- Freigabe einer langsamen Referenzkalibrierung ohne relevanten Eingang,
- Auswahl eines vorab kalibrierten Messbereichs,
- Maskierung nachweislich defekter Zellen,
- Start und Ende eines Beobachtungsfensters.

Jeder Befehl besitzt einen bekannten Wertebereich, einen Zeitpunkt und eine
technische Wirkung. Während eines eingefrorenen Validierungslaufs werden diese
Befehle nicht adaptiv aus dem Ergebnis verändert.

### 7.2 Umweltvermittelte Rückkopplung

Ein Aktor darf die Umwelt beeinflussen. Die daraus entstehende Wirkung wird
erneut über Sensoren aufgenommen. Für diesen Kreis sind Aktorgrenzen,
Totzeiten, Abbruchzustände und eine unabhängige Sicherheitsbegrenzung
erforderlich.

### 7.3 Ausgeschlossene Rückkopplungen

Ausgeschlossen sind:

- beliebiges Schreiben interner Zellzustände durch die Prozessorebene,
- Rückführung von Klassenlabels oder nachträglichen Zielwerten in die Fläche,
- positive Rückkopplung ohne feste Verstärkungs- und Zustandsgrenze,
- verdeckte Parameteränderung während Messung oder Validierung,
- direkter Aktor-zu-Zustand-Pfad unter Umgehung des Sensors,
- autonome Referenzverschiebung bei unbekanntem Eingang.

## 8. Beobachtungskriterien

Die Architektur wird nicht allein anhand einer Klassifikationsrate bewertet.
Mindestens folgende technische Merkmale sind für jede Operationalisierung zu
definieren.

### 8.1 Zustandsstabilität

- Anteil der Zeit innerhalb des zulässigen Bereichs,
- Abstand zu den Zustandsgrenzen,
- stationäre Streuung bei konstantem Eingang,
- Abhängigkeit von Bauteil-, Sensor- und Abtaststreuung.

### 8.2 Erholung nach Störung

- dauerhafte Rückkehrquote,
- 50-%- und 95-%-Rückkehrzeit,
- Restfehler nach festem Zeitabstand,
- erneuter Austritt aus dem Toleranzband,
- Verhalten nach Sättigung oder Kanalausfall.

### 8.3 Gleicher Reiz bei unterschiedlichen Vorzuständen

Ein identischer, kalibrierter Reiz wird mindestens aus dem Referenzzustand und
aus einem definierten Vorzustand angewendet. Gemessen werden Differenzen in
Latenz, Spitzenwert, Zustandsfläche und Rückkehr.

Eine brauchbare Kontextnachwirkung muss größer als Messunsicherheit und
Wiederholungsstreuung sein, innerhalb ihrer vorgesehenen Zeit abklingen und
eine vorab benannte physikalische Zielgröße besser erhalten. Eine bloße
Abhängigkeit von der Versuchshistorie genügt nicht.

### 8.4 Bindung mehrerer Eingänge

Bindung bezeichnet hier nur eine messbare gemeinsame Zustandsantwort auf zwei
oder mehr zeitlich und räumlich definierte Eingänge. Geprüft werden getrennte
Eingänge `A` und `B`, ihre Kombination `AB` sowie zeitlich versetzte
Kontrollen.

Zu berichten sind:

- Rekonstruktionsfehler der gemeinsamen physikalischen Zielgröße,
- Empfindlichkeit gegenüber relativem Zeitversatz,
- räumlicher Schwerpunkt- und Ausdehnungsfehler,
- Abweichung der kombinierten Antwort von einer vorab definierten linearen
  Überlagerung,
- Verlust gegenüber vollständigen Rohdaten bei gleichem Ausgabebudget.

Eine nichtlineare Abweichung allein gilt nicht als nützliche Bindung.

### 8.5 Informationsreduktion

- Zahl übertragener Werte pro Zeit oder Ereignis,
- Verhältnis lokaler Zustandswerte zu Ausgabewerten,
- Fehler der physikalischen Zielgröße bei festem Ausgabebudget,
- Latenz bis zur verfügbaren reduzierten Ausgabe,
- notwendige ADC-Abtastungen und interne Aktualisierungen.

ADC-Anzahl und Zustandsaktivität sind Aufwandsgrößen, aber keine direkten
Energieangaben.

### 8.6 Reproduzierbarkeit

- gepaarte Wiederholungen derselben Eingänge,
- neue, getrennte Validierungsreihen,
- dokumentierte Kalibrier- und Gerätezustände,
- Prüfsummen aller Roh- und Ergebnisdateien,
- vorab festgelegte Ausschluss- und Falsifikationsregeln.

## 9. Kandidaten für die spätere Einzelentscheidung

Das Papier stellt drei voneinander getrennte Architekturhypothesen bereit. Es
wählt keine davon aus.

### H1: vorzustandsabhängige dissipative Reaktion

Ein physikalisch definierter Vorzustand verändert die Antwort auf denselben
Folgereiz reproduzierbar, während die Fläche anschließend sicher zum
Referenzzustand zurückkehrt. Ein möglicher Nutzen müsste sich in geringerem
Rekonstruktionsfehler oder geringerer Ausgabebandbreite zeigen.

### H2: zeitlich-räumliche Bindung mehrerer Sensorquellen

Zwei kalibrierte Eingänge mit gemeinsamem Raum- und Zeitbezug erzeugen eine
reduzierte Zustandsbeschreibung, die ihre gemeinsame physikalische Zielgröße
besser erhält als getrennte reduzierte Ausgaben. Vollständige Rohdaten bleiben
Pflichtbaseline.

### H3: umweltvermittelte Zustandsregelung

Eine begrenzte Aktorwirkung verändert die Umwelt und wird über den Sensorpfad
erneut aufgenommen. Die Hypothese wäre nur tragfähig, wenn Stabilität,
Totzeiten, Sicherheitsgrenzen und ein messbarer Nutzen gegenüber einer
prozessorseitigen Regelung vorab festgelegt werden können.

Die spätere Projektentscheidung darf genau eine dieser Hypothesen auswählen.
Erst danach werden Messaufgabe, Baselines, Falsifikationsfall und mögliche
Modellierung getrennt vorregistriert.

## 10. Aussagegrenzen

Dieses Papier beschreibt eine technische Sensor-zu-Zustand-Architektur. Es
schreibt der Fläche keine nichttechnischen oder allgemein
selbstentstehenden Eigenschaften zu.

Nicht nachgewiesen oder behauptet werden:

- ein allgemeiner Verarbeitungs- oder Klassifikationsvorteil,
- ein allgemeines selbstorganisierendes Systemverhalten,
- geringere elektrische Energie oder Chipfläche,
- analoge, digitale oder Mixed-Signal-Fertigbarkeit,
- Robustheit außerhalb konkret geprüfter Sensor- und Störbereiche,
- Übertragbarkeit eines Ergebnisses zwischen Druck, Audio und Bild,
- ein Vorteil gegenüber Rohdaten ohne gleiches Ausgabebudget und faire
  Baselines.

Hardware-Realisierbarkeit, Energie, Temperaturverhalten, Fertigungsstreuung und
Sicherheit benötigen jeweils getrennte Evidenz. Eine stabile mathematische
Zustandsfläche allein ist dafür kein Nachweis.

## 11. Verhältnis zur pausierten Drucksensorlinie

Die Drucksensorfläche bleibt als mögliche spätere Sensorquelle erhalten. Ihre
Messschnittstelle und ihr Messprotokoll bleiben unverändert. Ohne reale
Hardware oder reale Paar-Dateien werden dort weder Vorversuch noch Modell
freigegeben.

Die Drucksensorlinie definiert nicht die Phase-II-Architektur. Umgekehrt hebt
das Architekturpapier den physischen Datenbedarf der Drucksensorlinie nicht
auf.

## 12. Nächster zulässiger Schritt

Nach Veröffentlichung dieses Papiers folgt ein getrennter versionierter
Auswahlbeschluss für genau eine der Hypothesen H1 bis H3. Vor diesem Beschluss
werden keine neuen Modelle, Simulationen, Parameterbereiche oder
Aufgabenresultate erzeugt.
