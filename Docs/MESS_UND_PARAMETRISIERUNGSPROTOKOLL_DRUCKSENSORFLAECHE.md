# Mess- und Parametrisierungsprotokoll: Drucksensorfläche

**Version:** 1.0

**Datum:** 3. September 2026

**Status:** vor Messbeginn festgelegt

**Grundlage:** `AUSWAHLBESCHLUSS_001_DRUCKSENSORFLAECHE.md`

## 1. Zweck und Abgrenzung

Dieses Protokoll legt fest, welche physikalischen Kennwerte vor einer
Modellierung der Drucksensorfläche erhoben werden müssen. Es erzeugt selbst
kein mathematisches Modell und erlaubt keinen Parametersweep.

Ziel ist die Prüfung, ob ein reales Sensorfeld eine reproduzierbare lokale
Kontakt- und Relaxationsdynamik besitzt, die eine sensornahe Verdichtung auf
höchstens sechs Werte pro Kontakt sachlich begründet.

## 2. Festgelegte Sensorklasse

Verwendet wird ein passives `4×4`-Feld aus **piezoresistiven
Polymer-Verbundsensoren**. Jede der 16 Zellen muss separat analog auslesbar
sein. Die bevorzugte Bauform ist eine flexible Drucksensorfolie mit
identischer Zellgeometrie und gemeinsamem Trägermaterial.

Diese Sensorklasse wird gewählt, weil sie:

- statische und zeitlich veränderliche Kontaktkräfte abbilden kann,
- eine messbare materialbedingte Relaxation und Hysterese erwarten lässt,
- ohne räumliche Kopplungsannahme als 16 lokale Kanäle betrieben werden kann,
- mit langsamer mechanischer Belastung und üblicher Mehrkanalmesstechnik
  charakterisierbar ist.

Ein konkretes Bauteil wird erst zugelassen, wenn Datenblatt oder Vorprüfung
separaten Rohzugriff auf alle Zellen, einen nicht gesättigten Arbeitsbereich
und wiederholbare Kontakte erlauben. Herstellerinterne Signalverarbeitung
darf nicht zwischen Sensorelement und Rohdatenerfassung liegen.

## 3. Erforderlicher Messaufbau

Der Aufbau besteht mindestens aus:

- einem kraftgeregelten linearen Aktor,
- einer kalibrierten Referenzkraftmesszelle in der Kraftachse,
- austauschbaren starren Eindringkörpern für Einzelzelle und `2×2`-Fläche,
- synchroner Rohdatenerfassung aller 16 Sensorspannungen,
- Messung von Versorgungsspannung und Sensortemperatur,
- einer mechanischen Führung für reproduzierbare Position und Neigung,
- einer Zeitbasis für Referenzkraft und Sensorkanäle.

Die Referenzkraftmesszelle ist die Messwahrheit für Kraft und Kraft-Zeit-Fläche.
Ihre Messunsicherheit, Nullpunktdrift, Auflösung und Abtastrate werden vor dem
ersten Sensorversuch protokolliert.

Die Rohabtastrate wird so gewählt, dass die kürzeste im Vorversuch gemessene
10-90-%-Anstiegs- oder Abfallzeit durch mindestens 20 Abtastwerte beschrieben
wird. Referenzkraft und 16 Sensorkanäle werden zeitsynchron erfasst.

## 4. Kalibrierung und Arbeitsbereich

Vor der Kennwertmessung werden folgende Größen bestimmt:

1. Nullsignal und Standardabweichung jeder unbelasteten Zelle,
2. monotone statische Kennlinie jeder Zelle,
3. Beginn messbarer Reaktion,
4. Beginn von Sättigung oder nichtmonotonem Verhalten,
5. elektrische Kanalverstärkung und Versorgungsempfindlichkeit,
6. mechanisches Übersprechen zu direkten Nachbarzellen.

Als kalibrierter Arbeitsbereich `F_cal` gilt nur der gemeinsame Kraftbereich,
in dem alle 16 Zellen monoton reagieren und keine Zelle sättigt. Die drei
Prüflasten werden anschließend auf `20 %`, `50 %` und `80 %` dieses Bereichs
festgelegt. Der spätere normierte Zustand `−3…+3` darf erst aus diesen
gemessenen Grenzen abgeleitet werden.

## 5. Definition der Kontakt- und Entlastungsereignisse

### 5.1 Ruhezustand

Ein Versuch beginnt erst, wenn die Referenzkraft unter `1 %` von `F_cal` liegt
und jeder Sensorkanal für mindestens eine Sekunde innerhalb seiner
Nulltoleranz bleibt. Die Nulltoleranz ist das Maximum aus dreifacher
Standardabweichung des Nullsignals und `1 %` der jeweiligen Kanalspanne.

### 5.2 Kontaktbeginn

Kontaktbeginn `t_on` ist der erste Zeitpunkt, an dem die Referenzkraft `5 %`
der jeweiligen Prüflast überschreitet und mindestens 50 ms darüber bleibt.

### 5.3 Belastungsanstieg

Die Kraft wird kontrolliert bis zur Prüflast erhöht. Gemessen werden mindestens
drei Anstiegsraten: die im Vorversuch zuverlässig regelbare Nennrate sowie
deren Faktor `0,5` und `2,0`. Die tatsächlich gemessene Kraftkurve, nicht der
Sollwert des Aktors, ist maßgeblich.

### 5.4 Haltephase

Die Prüflast wird innerhalb von `±2 %` gehalten. Im Vorversuch beträgt die
Haltezeit 60 Sekunden. Für die Hauptmessung wird sie vorab auf mindestens das
Fünffache der im Vorversuch bestimmten dominanten Relaxationszeit festgelegt,
jedoch nicht nach einzelnen Versuchsergebnissen verändert.

### 5.5 Entlastungsbeginn und Kontaktende

Entlastungsbeginn ist der erste geregelte Kraftabfall aus der Haltephase.
Kontaktende `t_off` ist der erste Zeitpunkt, an dem die Referenzkraft wieder
unter `5 %` der Prüflast fällt und mindestens 50 ms darunter bleibt.

### 5.6 Rückkehr

Nach `t_off` wird ohne Kontakt weitergemessen. Die Rückkehrzeit endet, sobald
alle 16 Kanäle für mindestens eine Sekunde dauerhaft innerhalb ihrer
Nulltoleranz liegen. Wird dieses Kriterium innerhalb der festgelegten
Beobachtungsdauer nicht erreicht, wird der Versuch als nicht zurückgeführt
markiert; der Wert wird nicht abgeschnitten oder ersetzt.

## 6. Kontaktgeometrien und Wiederholungen

Die nominale Messreihe enthält:

- Einzelzellkontakt im Zentrum,
- Einzelzellkontakt am Rand,
- Einzelzellkontakt in einer Ecke,
- flächigen Kontakt über ein zentrales `2×2`-Gebiet.

Jede Geometrie wird bei allen drei Prüflasten und der Nennrate zehnmal
wiederholt. Die Reihenfolge wird vor Messbeginn zufällig festgelegt und
gespeichert. Zwischen Wiederholungen muss das Rückkehrkriterium erfüllt sein.

Zusätzlich werden bei mittlerer Prüflast und zentralem Kontakt je zehn
Wiederholungen der langsamen und schnellen Anstiegsrate durchgeführt.

## 7. Störgrößen

Folgende Einflüsse werden getrennt von der nominalen Reihe untersucht:

- Sensortemperatur: Labortemperatur sowie `−5 K` und `+5 K`, soweit innerhalb
  der Bauteilgrenzen,
- Versorgungsspannung: Nennwert sowie `−2 %` und `+2 %`,
- Eindringkörperposition: Sollposition sowie Verschiebung um ein Viertel des
  Zellabstands in zwei Achsrichtungen,
- Neigung: senkrechter Kontakt sowie `5°` in zwei Achsrichtungen,
- mechanische Vorgeschichte: erster Kontakt und zehn unmittelbar
  aufeinanderfolgende Kontakte,
- Langzeitnullpunkt: unbelastete Aufzeichnung vor und nach jeder Messserie.

Es wird zunächst jeweils nur eine Störgröße gegenüber der nominalen Bedingung
verändert. Kombinierte Ecken werden erst in einem späteren, getrennt
vorregistrierten Versuch zugelassen, falls das Einzelstörgrößenbild dies
begründet.

## 8. Zu messende physikalische Kennwerte

Für jede Zelle und für die Summe des Feldes werden bestimmt:

1. statische Empfindlichkeit und Nichtlinearität über `F_cal`,
2. 10-%, 50-%- und 90-%-Anstiegszeit,
3. relative Signaländerung während der Haltephase,
4. dominante Relaxationszeit und Güte ihrer Beschreibung,
5. 10-%, 50-%- und 90-%-Abfallzeit,
6. Restabweichung nach festen Zeiten relativ zu `t_off`,
7. dauerhafte Rückkehrzeit zur Nulltoleranz,
8. normierte Hysteresefläche aus Belastung und Entlastung,
9. Wiederholungsstreuung innerhalb einer Bedingung,
10. Zell-zu-Zell-Streuung,
11. mechanisches Übersprechen zu Nachbarzellen,
12. Temperatur-, Versorgungs- und Nullpunktkoeffizienten.

Zeitkonstanten werden nicht aus nur einem Einzelkontakt übernommen. Berichtet
werden Verteilung, Median, 5-%- und 95-%-Quantil sowie die Abhängigkeit von
Kraft, Position und Störgrößen.

## 9. Höchstens sechs Übergabewerte

Die physikalische Wahrnehmungsebene darf je abgeschlossenem Kontakt genau die
folgenden sechs Werte an die Prozessorebene übergeben:

1. Kontaktbeginn `t_on`,
2. Kontaktende `t_off`,
3. geschätzte Kraft-Zeit-Fläche `J_F`,
4. x-Koordinate des kraftgewichteten Kontaktschwerpunkts,
5. y-Koordinate des kraftgewichteten Kontaktschwerpunkts,
6. effektive Kontaktfläche.

Interne Zellzustände, Rohspannungen und Zwischenwerte zählen nicht als
Übergabewerte und dürfen nicht zusätzlich übertragen werden. Kennwerte zur
Relaxation dienen der Konstruktion und Rückführung der lokalen Ebene; sie
erweitern das Sechs-Werte-Paket nicht.

## 10. Rohdatenbaseline und Referenzvergleich

### 10.1 Rohdatenbaseline

Die Rohdatenbaseline digitalisiert alle 16 Zellen mit der festgelegten
Rohabtastrate. Jede Zelle wird mit ihrer gemessenen statischen Kennlinie in
Kraft umgerechnet. Die Gesamtkräfte werden über die Zeit integriert. Auch
diese Baseline darf nach interner Verarbeitung nur dieselben sechs Werte je
Kontakt übertragen.

Die Anzahl interner ADC-Abtastungen wird separat gezählt. Sie verändert das
gemeinsame Übertragungsbudget nicht, wird aber als Aufwandsgröße berichtet.

### 10.2 Bestehende Referenzarchitektur

Zusätzlich bleibt die ungekoppelte Ein-Zustands-Dynamik mit kontrollierter
Rückführung und Mittelwert-/Steigungs-Auslese Pflichtvergleich. Ihre Parameter
dürfen erst aus den gemessenen Kennwerten auf physikalische Einheiten abgebildet
werden. Die bisherige dimensionslose Parametrierung wird nicht ungeprüft
übernommen.

### 10.3 Messwahrheit

`J_ref` ist das numerische Zeitintegral der synchron gemessenen
Referenzkraft zwischen `t_on` und `t_off`. Die anschließende Sensorrückkehr
gehört nicht zur tatsächlich anliegenden Kontaktkraft. Ort und Kontaktfläche
werden aus dokumentierter Aktorposition und Eindringkörpergeometrie bestimmt,
nicht aus den Sensorwerten selbst.

## 11. Primäre Erfolgsgröße

Die primäre Erfolgsgröße ist der **Rekonstruktionsfehler der
Kraft-Zeit-Fläche bei festem Übertragungsbudget von sechs Werten je Kontakt**.

Für Kontakt `k` gilt:

`e_k = |J_hat,k − J_ref,k| / max(|J_ref,k|, J_min)`.

`J_min` ist die Kraft-Zeit-Fläche des kleinsten regulären Prüfeingangs und wird
vor Auswertung der Hauptmessung festgeschrieben. Berichtet werden Median,
95-%-Quantil und Maximum von `e_k` für jede Architektur sowie gepaarte
Differenzen auf denselben Kontakten.

Ein späterer Erfolgsschwellenwert wird vor der Modellvalidierung aus der
Messunsicherheit der Referenzkraft und dem praktisch zulässigen Fehler
abgeleitet. Er darf nicht anhand der beobachteten Architekturdifferenzen
gewählt werden.

## 12. Sekundäre Größen

Sekundär werden gemessen:

- Fehler von `t_on` und `t_off`,
- Schwerpunktfehler in Einheiten des Zellabstands,
- Fehler der effektiven Kontaktfläche,
- Zahl interner ADC-Abtastungen je Kontakt,
- Verarbeitungslatenz bis zum vollständigen Sechs-Werte-Paket,
- Rückkehrquote und Rückkehrzeit,
- Robustheit der sechs Werte gegenüber jeder einzelnen Störgröße.

Elektrische Energie wird nur angegeben, wenn Strom und Spannung real gemessen
werden. Die ADC-Anzahl oder Zustandsaktivität wird nicht als Energieersatz
bezeichnet.

## 13. Datenaufteilung und Nachvollziehbarkeit

Die Vorversuche dienen ausschließlich der Bestimmung von Arbeitsbereich,
Abtastrate, Beobachtungsdauer und physikalischen Kennwerten. Die später zur
Modellprüfung verwendeten Kontakte werden als getrennte Validierungsserie mit
neuer Reihenfolge aufgenommen.

Für jede Messdatei werden gespeichert:

- Sensor- und Aufbaukennung,
- Datum, Temperatur und Versorgung,
- Kontaktgeometrie, Position, Neigung und Sollbedingung,
- Rohkanäle, Referenzkraft und Zeitbasis,
- Kalibrierstand und Softwareversion,
- SHA-256-Prüfsumme.

Rohdaten werden nicht überschrieben. Ausschlüsse sind nur aufgrund vorab
definierter Gerätefehler zulässig und werden mit Grund dokumentiert.

## 14. Abbruch vor Modellierung

Der Abschnitt endet ohne Modell, wenn mindestens einer der folgenden Fälle
eintritt:

1. Die Sensorzellen besitzen keinen gemeinsamen monotonen Arbeitsbereich.
2. Relaxation oder Rückkehr ist gegenüber Nullrauschen und
   Wiederholungsstreuung nicht reproduzierbar trennbar.
3. Die Richtung der Relaxation wechselt innerhalb identischer Bedingungen
   unkontrolliert.
4. Mechanisches Übersprechen verhindert eine belastbare Zuordnung von Ort und
   Fläche.
5. Die sechs Übergabewerte lassen sich gegenüber der Rohdatenbaseline nicht
   mit einer messbaren Reduktion interner Abtastungen begründen.
6. Referenzkraft oder Aktor sind nicht genau genug, um den primären Fehler mit
   ausreichender Unsicherheit zu bestimmen.

## 15. Freigabe für eine spätere Modellvorregistrierung

Eine Modellvorregistrierung ist erst zulässig, wenn:

- alle Pflichtkennwerte mit Unsicherheiten vorliegen,
- Arbeitsbereich und Rückkehrkriterium experimentell bestimmt sind,
- genau eine aus den Messdaten begründete Zustandsgleichung gewählt wurde,
- die sechs Übergabewerte und beide Pflichtvergleiche unverändert bleiben,
- Erfolgsschwelle und Falsifikationsregel vor dem Validierungslauf feststehen.

Bis zu dieser Freigabe werden keine synthetischen Kontaktdaten, keine
Modellvarianten und keine Parametersweeps erzeugt.
