# Arbeitspaket: Architektur-Neuausrichtung

## Ausgangspunkt

Drei vorregistrierte Simulationsabschnitte zeigen reproduzierbar kontrollierte
Zustands- und Feldverläufe, aber keinen nachgewiesenen Vorteil der bisher
getesteten positiven, symmetrischen Vierer-Nachbarschaftskopplung. Im
zeitlich-räumlichen Hauptversuch liegt das ungekoppelte dynamische Array mit
`89,7 %` vor der besten gekoppelten Variante mit `85,3 %`. Das gepaarte
95-%-Intervall der Differenz liegt mit `−5,5` bis `−3,5` Prozentpunkten
vollständig gegen die gekoppelte Variante.

Dieser Befund beendet den bisherigen Auslegungskandidaten für die untersuchte
Aufgabe. Er widerlegt nicht jede mögliche Feld- oder Zustandsarchitektur.

## Neue Leitfrage

Welche Zustands- oder Kopplungsdynamik kann gegenüber einem ungekoppelten
dynamischen Array einen konstruktiven, reproduzierbaren Nutzen für ein
mögliches Sensor-Front-End erzeugen?

## Zu prüfende Mechanismen

Die folgenden Mechanismen sind getrennte Hypothesen und werden nicht gemeinsam
in ein unübersichtliches Gesamtmodell eingebaut:

1. gerichtete oder anisotrope Kopplung,
2. hemmende beziehungsweise negative Kopplungsanteile,
3. zwei oder mehrere lokale Zeitskalen,
4. lokale, begrenzte Adaptation,
5. ereignisbasierte zeitliche Auslese.

Eine Vergrößerung über `4×4` wird erst geprüft, wenn mindestens ein Mechanismus
auf `4×4` einen vorab festgelegten Vorteilskandidaten liefert.

## Methodisches Vorgehen

### Phase A: technischer Eignungstest

Jeder Mechanismus wird zunächst nur auf Bereichseinhaltung, numerische
Stabilität, Reproduzierbarkeit und Rückführbarkeit geprüft. Instabile oder nur
durch Grenzbegrenzung funktionierende Varianten werden nicht zur
Leistungsprüfung zugelassen.

### Phase B: explorative Mechanismensuche

Je Mechanismus wird ein begrenztes, vorab dokumentiertes Parameterraster auf
einem getrennten Entwicklungsdatensatz untersucht. Ziel ist die Auswahl
höchstens eines Kandidaten je Mechanismus, nicht der Nachweis eines Vorteils.

### Phase C: vorregistrierter Bestätigungslauf

Ausgewählte Kandidaten werden mit eingefrorenen Parametern auf neuen Seeds und
gegen mindestens das ungekoppelte dynamische Array geprüft. Aufgabe, Auslese,
Stichprobe und Erfolgsschwelle werden vor dem Lauf committed. Erst dieser Lauf
kann einen Vorteil vorläufig bestätigen.

## Vergleichsregeln

- Das ungekoppelte dynamische Array bleibt Pflichtbaseline.
- Eingänge, Störungen, Ausgabebudget und Auswerter sind innerhalb eines
  Vergleichs identisch.
- Rückführungsparameter werden nicht anhand der Klassifikationsrate gewählt.
- Ergebnisse werden einschließlich negativer und neutraler Befunde berichtet.
- Eine nachträgliche Auswahl der günstigsten Aufgabe gilt nur als explorativ.
- Elektrische Energie und Fertigbarkeit bleiben bis SPICE beziehungsweise
  Hardware ungeprüft.

## Nächster Schritt

Die technische Rückführung wurde gemäß
`RUECKFUEHRUNG_VORREGISTRIERUNG.md` geprüft. Drei Kandidaten sind technisch
bestätigt; daraus folgt noch keine Auswahl eines Verarbeitungsmechanismus. Als
nächster Schritt wird für den ersten Architekturmechanismus ein eigener
explorativer Versuchsplan erstellt. Dieser Plan liegt nun unter
`ANISOTROPE_KOPPLUNG_VORREGISTRIERUNG.md` vor und wurde ausgeführt. Alle
Varianten sind technisch stabil, aber keine erfüllt die Auswahlregel. Der
Mechanismus wird für diese Aufgabe ohne Bestätigungslauf abgeschlossen. Ein
weiterer Mechanismus benötigt erneut einen eigenen vorregistrierten Plan.

Der nächste Mechanismus sind mehrere lokale Zeitskalen ohne räumliche Kopplung.
Der explorative Plan liegt unter `MEHRERE_ZEITSKALEN_VORREGISTRIERUNG.md` vor;
der Lauf wurde ausgeführt und liefert genau einen Kandidaten für einen späteren
unabhängigen Bestätigungslauf. Dieser ist unter
`BESTAETIGUNG_ZEITSKALEN_VORREGISTRIERUNG.md` vorregistriert worden.

Der Bestätigungslauf wurde ausgeführt. Der Effekt bleibt positiv, verfehlt aber
die vorregistrierte Mindestgröße. Mehrere lokale Zeitskalen sind damit für die
geprüften Aufgaben kein bestätigter Vorteilskandidat. Das Kriterium wird nicht
nachträglich abgesenkt.

Als nächster getrennt vorregistrierter Mechanismus folgt lokale begrenzte
Adaptation ohne räumliche Kopplung. Der Plan liegt unter
`ADAPTATION_VORREGISTRIERUNG.md` und bildete die Grundlage des Ergebnislaufs.

Der Lauf wurde anschließend ohne Kandidaten abgeschlossen. Die stärkste
zugelassene Variante verfehlt mit `+1,02` Prozentpunkten die Mindestwirkung und
verletzt zusätzlich die Rauschrobustheitsbedingung. Eine unabhängige
Bestätigung dieses Mechanismus ist damit nicht vorgesehen.
