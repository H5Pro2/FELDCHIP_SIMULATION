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

Die technische Rückführung ist gemäß `RUECKFUEHRUNG_VORREGISTRIERUNG.md`
vorregistriert und wird als Nächstes geprüft. Danach wird für den ersten
Architekturmechanismus ein eigener explorativer Versuchsplan erstellt. Ohne
diese Vorregistrierungen wird kein neuer Parametersweep ausgeführt.
