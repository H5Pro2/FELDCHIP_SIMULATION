# Pausenbeschluss und funktionale Neubewertung

**Version:** 1.0

**Datum:** 3. September 2026

**Status:** Gesamtprojekt formell pausiert, nicht endgültig geschlossen

## 1. Beschluss

Das Projekt `FELDCHIP_SIMULATION` wird nach Abschluss aller derzeit ohne reale
Hardware möglichen Arbeitsschritte formell pausiert.

- **Phase I ist abgeschlossen.** Für keinen der geprüften zusätzlichen
  Mechanismen wurde unter den festgelegten Bedingungen ein bestätigter Vorteil
  nachgewiesen.
- **Phase II ist methodisch vorbereitet.** Architektur, H1-Auswahl,
  Messprotokoll und Datenschnittstelle sind definiert. Ohne reale Messdaten ist
  die Hypothese nicht ausführbar.
- **Das Gesamtprojekt ist pausiert.** Es beginnen keine weiteren Simulationen,
  Parametersuchen, Modellvarianten oder synthetischen Kontaktversuche.

Die Pause bewahrt Ergebnisse, negative Befunde und Protokolle. Sie ist keine
Behauptung, dass jede denkbare Feldchip-Architektur unmöglich sei. Ebenso ist
sie keine Freigabe, die bisher nicht bestätigten Ansätze später ohne neue
physikalische Begründung fortzusetzen.

## 2. Was die Untersuchung tatsächlich gezeigt hat

Im dimensionslosen `4×4`-Modell sind begrenzte kontinuierliche Zustände,
zeitliche Nachwirkung und kontrollierte Rückkehr numerisch darstellbar. Eine
stabile Rückführung wurde für den geprüften Referenzkandidaten erreicht.

Die ungekoppelte Ein-Zustands-Dynamik mit Mittelwert-/Steigungs-Auslese bleibt
die belastbare technische Referenz. Gegen diese Referenz ergaben die
untersuchten Erweiterungen keinen bestätigten Zusatznutzen:

- positive symmetrische, gerichtete und reziprok anisotrope räumliche
  Kopplung verschlechterte die geprüften Aufgaben,
- zusätzliche lokale Zeitskalen erzeugten nur einen kleinen, unter der
  vorregistrierten Mindestwirkung liegenden Bestätigungseffekt,
- lokale begrenzte Adaptation blieb unter der Mindestwirkung und war nicht
  über alle Rauschstufen robust,
- die geprüfte Delta-Ereignisauslese verlor deutlich mehr zeitliche
  Information als die Mittelwert-/Steigungs-Auslesen,
- eine höhere Zahl nichtlinearer Bereiche ergab keinen tragfähigen Vorteil.

Diese Befunde gelten für die dokumentierten Modelle, Aufgaben, Baselines und
Ausleseverfahren. Sie dürfen nicht als allgemeiner Unmöglichkeitsnachweis
verallgemeinert werden.

## 3. Welche ursprünglichen Deutungen nicht getragen werden

### 3.1 Der Bereich `−3…+3` ist kein eigener Rechenvorteil

Ein kontinuierlicher Bereich kann Zwischenwerte darstellen. Seine bloße
Breite erzeugt jedoch weder zusätzliche Messgenauigkeit noch automatisch mehr
nutzbare Information. Die reale Auflösung hängt von Sensorrauschen,
Kalibrierung, Dynamikbereich, Wandlerauflösung und Auslese ab.

`−3…+3` ist deshalb als **normierter Zustandsbereich mit Begrenzungsreserve**
zu lesen, nicht als Ersatz für binäre Logik und nicht als Beleg einer
höherwertigen Chipberechnung.

### 3.2 Feldbildung ist nicht automatisch nützliche Verarbeitung

Dass sich aus lokalen Zuständen eine räumliche Form darstellen lässt, beweist
noch keinen funktionalen Nutzen. In den geprüften Aufgaben vermischte die
räumliche Kopplung relevante lokale Unterschiede und verschlechterte das
Ergebnis gegenüber dem ungekoppelten Array.

Eine sichtbare Feldform darf daher nicht mit Informationsgewinn gleichgesetzt
werden. Ihr Nutzen müsste an einer physikalischen Aufgabe mit fairer Baseline
und festem Übertragungsbudget gemessen werden.

### 3.3 Mehr Dynamik ist nicht automatisch bessere Funktion

Ein zweiter Zustand, Adaptation oder eine Ereigniscodierung erhöht zunächst
nur die Architekturkomplexität. Die Versuche zeigten kleine, nicht bestätigte
Effekte oder klare Nachteile. Zusätzliche Dynamik ist erst gerechtfertigt,
wenn eine konkrete physikalische Ursache genau diesen Mechanismus benötigt.

### 3.4 Stabile Rückkehr ist eine Pflichtbedingung, kein Nutzennachweis

Die nachgewiesene numerische Rückführung zeigt, dass ein begrenzter Zustand im
Modell kontrolliert zum Referenzwert zurückkehren kann. Sie belegt nicht, dass
die Zustandsbildung eine Aufgabe besser löst, auf Hardware übertragbar ist
oder einen wirtschaftlichen Vorteil besitzt.

### 3.5 Klassifikationsleistung war nicht die passende Hauptdeutung

Die Phase-I-Aufgaben waren geeignet, behauptete Verarbeitungsvorteile zu
prüfen. Sie begründen aber keine allgemeine Funktion des Feldchips. Der
tragfähigere Prüfgegenstand ist eine reale physikalische Repräsentation
zwischen Sensor und Prozessor, bewertet etwa durch Rekonstruktionsfehler,
Rückkehr, Robustheit und übertragene Datenmenge.

## 4. Korrigierte funktionale Interpretation

Der Feldchip wird im weiteren Projekt ausschließlich als möglicher
**sensorischer Zustandskonditionierer** interpretiert:

1. Ein Sensoradapter überführt kalibrierte physikalische Eingänge in lokale,
   begrenzte Zustandsabweichungen.
2. Jede Zelle führt einen messbaren lokalen Zustand mit definierter
   Nachwirkung und kontrollierter Rückkehr.
3. Die räumliche Anordnung bildet eine Zustandsfläche. Eine vorteilhafte
   Wechselwirkung zwischen Zellen ist nicht nachgewiesen und wird nicht
   vorausgesetzt.
4. Die Prozessorebene erhält nur vorab festgelegte Zustandsmerkmale; lokale
   Verläufe dürfen innerhalb der sensorischen Ebene verbleiben.
5. Ein technischer Nutzen liegt nur vor, wenn diese Verdichtung bei gleichem
   Informationsziel messbar besser oder aufwandsärmer ist als Rohdaten und die
   ungekoppelte Referenz.

Der Begriff **Feld** bezeichnet damit zunächst die verteilte Darstellung
kontinuierlicher lokaler Zustände. Er behauptet weder ein besonderes
physikalisches Wechselwirkungsfeld noch eine eigenständige allgemeine
Rechenfunktion.

## 5. Offene, aber zulässige Hypothese

H1 bleibt als einzige ausgewählte Operationalisierung bestehen: Eine real
messbare Restabweichung nach einem Konditionierungsreiz könnte die Antwort auf
einen identischen Folgereiz reproduzierbar verändern und anschließend
abklingen.

Ein positiver H1-Befund würde ausschließlich eine begrenzte dissipative
Kontextnachwirkung der geprüften Sensorfläche belegen. Er würde noch keinen
Vorteil einer Chiparchitektur beweisen. Dafür wären anschließend eine separat
vorregistrierte Zustandsabbildung und faire Hardware- oder
Messkettenvergleiche erforderlich.

## 6. Nicht belegte Aussagen

Der bisherige Projektstand belegt nicht:

- einen allgemeinen Rechen- oder Verarbeitungsvorteil,
- einen Vorteil des Wertebereichs `−3…+3` gegenüber anderen Skalierungen,
- einen Nutzen räumlicher Kopplung,
- eine Überlegenheit gegenüber analoger oder digitaler Signalverarbeitung,
- geringeren Energiebedarf,
- Fertigbarkeit, Skalierbarkeit oder Langzeitstabilität eines Chips,
- die Übertragbarkeit der Simulation auf Druck, Audio oder Bild ohne reale
  sensorspezifische Kennwerte,
- nichttechnische oder allgemein selbstentstehende Eigenschaften.

Diese Punkte dürfen in externen Darstellungen nur als offene Prüffragen, nicht
als Projektergebnisse bezeichnet werden.

## 7. Voraussetzungen für eine Wiederaufnahme

Eine Wiederaufnahme ist nur zulässig, wenn mindestens Folgendes real vorliegt:

- eine dokumentierte `4×4`-Sensorfläche mit getrenntem Rohzugriff auf alle
  Zellen,
- eine synchron erfasste, kalibrierte Referenzkraft,
- reale Paar-Dateien nach dem Vertrag in `measurement_interface/`,
- vollständige Metadaten zu Sensor, Aufbau, ADC, Abtastrate,
  Kontaktgeometrie, Position, Neigung, Prüflast und Versuchsreihenfolge,
- ausreichende Daten zur Bestimmung von Arbeitsbereich, Relaxationszeit,
  Beobachtungsdauer und Messunsicherheit.

Nach Eingang dieser Voraussetzungen wird zuerst ausschließlich die vorhandene
Messschnittstelle angewendet. Erst bei bestandener Struktur- und
Messfreigabe darf eine getrennte H1-Validierungsserie vorbereitet werden.

## 8. Während der Pause ausgeschlossene Arbeiten

Bis zur formellen Wiederaufnahme werden nicht durchgeführt:

- neue abstrakte Mechanismen oder Parametersweeps,
- Nachoptimierung abgeschlossener Varianten,
- synthetische Ersatzdaten für fehlende reale Messungen,
- eine Modellvorregistrierung ohne physikalische Kennwerte,
- SPICE- oder Chipauslegung auf Grundlage der dimensionslosen Simulation,
- Aussagen zu Energie, Fertigung oder industriellem Nutzen ohne Messung.

Korrekturen an Dokumentation, Reproduzierbarkeit oder Datenschnittstelle
bleiben zulässig, sofern sie keine neue Ergebnisinterpretation nach Datenlage
einführen.

## 9. Wiederaufnahmeentscheidung

Die Bereitstellung von Hardware oder Rohdaten startet das Projekt nicht
automatisch. Nach Validierung der Eingänge ist ein eigener versionierter
Wiederaufnahmebeschluss erforderlich. Er benennt den realen Aufbau, friert die
numerischen H1-Wartezeiten und Unsicherheitsgrenzen ein und legt die getrennte
Messserie fest.
