# Vorregistrierung: gerichtete und anisotrope Kopplung

## Forschungsstatus und Ziel

Die bisherige positive, symmetrische Vierer-Nachbarschaftskopplung hat in der
vorregistrierten zeitlich-räumlichen Aufgabe keinen Vorteil gegenüber dem
ungekoppelten dynamischen Array gezeigt. Die technische Rückführungsprüfung hat
dagegen eine konstante Rückführung mit Verstärkung `1,6` als stabilen
Referenzkandidaten bestätigt.

Dieser explorative Versuch prüft als ersten neuen Architekturmechanismus, ob
gerichtete oder reziprok anisotrope Kopplung einen Kandidaten für einen späteren
unabhängigen Bestätigungslauf liefert. Der Lauf selbst bestätigt keinen
Verarbeitungsvorteil.

## Fest eingefrorene Rückführung

Alle Modelle verwenden:

- konstante Rückführungsverstärkung `1,6`,
- Kopplung ausschließlich auf der Abweichung vom individuellen Referenzfeld,
- Arbeitsbereich `−3…+3`,
- dieselbe Softbegrenzung, Zellstreuung und Rauschdefinition wie die bisherigen
  Referenzmodelle.

Nichtlineare Rückführungskennlinien werden in diesem Versuch nicht verwendet.

## Kopplungsgleichung

Für die Abweichung `d` vom Referenzfeld wird die Kopplung als gewichtete Summe
der vier Nachbardifferenzen definiert:

`K(d) = w_o(d_o−d) + w_u(d_u−d) + w_l(d_l−d) + w_r(d_r−d)`

An den Rändern gelten reflexive Randbedingungen. Die vier Gewichte werden vor
dem Lauf festgelegt und bleiben während einer Sequenz konstant.

## Vorab festgelegter Kandidatenraum

Der Vergleich enthält genau `26` Modelle:

- ungekoppelte Pflichtbaseline: alle Gewichte `0`,
- isotroper Kontrollfall: alle Gewichte `0,34`,
- acht reziprok anisotrope Varianten:
  - dominante Achse horizontal oder vertikal,
  - dominantes Gewicht `0,34` oder `0,68`,
  - transversales Gewicht `0` oder `0,17`,
- sechzehn gerichtete Varianten:
  - Vorzugsrichtung oben, unten, links oder rechts,
  - Vorzugsgewicht `0,34` oder `0,68`,
  - Gegengewicht `0` oder `0,17`,
  - beide transversalen Gewichte fest `0,17`.

Es werden nach dem Lauf keine zusätzlichen Gewichte ergänzt.

## Phase A: technische Zulassung

Jedes der 26 Modelle wird vor der Aufgabenbewertung mit den 18 Anfangsfeldern
der Rückführungsprüfung, beiden Streuungsecken und den Entwicklungsseeds `101`,
`131`, `167` geprüft. Jeder Lauf dauert `6,0` Sekunden. Pro Kombination laufen
ein Robustheitstest mit dem Rauschen der jeweiligen Streuungsecke bei
`dt = 0,02` sowie zwei rauschfreie Läufe bei `dt = 0,02` und `dt = 0,01` für
die numerische Prüfung.

Ein Modell ist technisch zulässig, wenn für jede Ecke-Seed-Kombination:

1. im verrauschten Robustheitslauf und bei beiden rauschfreien Zeitschritten
   alle Anfangsfelder dauerhaft zurückkehren,
2. die schlechteste 95-%-Einschwingzeit höchstens `5,0` Sekunden beträgt,
3. der schlechteste 95-%-Restfehler höchstens `0,05` beträgt,
4. keine erneuten Toleranzaustritte und keine Grenzüberschreitungen auftreten,
5. die t95-Differenz zwischen den Zeitschritten höchstens `0,10` Sekunden und
   die Restfehlerdifferenz höchstens `0,005` beträgt.

Nicht zugelassene Modelle werden in Phase B nicht bewertet.

## Phase B: explorative zeitlich-räumliche Aufgabe

Verwendet werden unverändert die zehn Sequenzklassen des vorregistrierten
zeitlich-räumlichen Versuchs: vier wandernde Einzelpunkte, kreuzende und
überlagerte Pulse, Aufbau und Abbau eines Gradienten sowie kurze Störungen in
Mitte und Rand mit Nachlauf.

- Entwicklungsseeds: `101`, `131`, `167`
- Rauschstufen: `0,15`, `0,35`, `0,55`
- Training: `12` Sequenzen je Klasse
- Test: `24` Sequenzen je Klasse
- Auslese: dieselben acht Momentanmerkmale, jeweils zeitlicher Mittelwert und
  lineare Steigung, insgesamt `16` Werte
- Auswerter: Nächste-Zentroid-Verfahren

Eingänge, Referenzoffset, Zellstreuung und dynamisches Rauschen werden innerhalb
jeder Seed-Rausch-Kombination für alle Modelle identisch erzeugt.

## Explorative Kandidatenauswahl

Für jedes technisch zugelassene anisotrope oder gerichtete Modell wird die
gepaarte Differenz zur ungekoppelten Pflichtbaseline über die neun
Seed-Rausch-Kombinationen berechnet.

Höchstens ein Modell wird für einen späteren Bestätigungslauf ausgewählt. Dafür
muss es

1. die ungekoppelte Baseline im Gesamtmittel um mehr als `2,0` Prozentpunkte
   übertreffen und
2. in keiner der drei Rauschstufen im Mittel unter der Baseline liegen.

Erfüllen mehrere Modelle diese Bedingungen, gewinnt die größte mittlere
Differenz. Bei Gleichstand folgen geringere Summe der Kopplungsgewichte,
reziproke vor gerichteter Kopplung und schließlich der Modellname. Erfüllt kein
Modell beide Bedingungen, endet die Exploration ohne Bestätigungskandidaten.

Der isotrope Kontrollfall kann keinen neuen Kandidaten stellen. Für das
ausgewählte Modell werden Effektstreuung und ein approximatives gepaartes
95-%-Intervall berichtet, aber nicht als bestätigender Nachweis interpretiert.

## Späterer Bestätigungslauf

Ein ausgewählter Kandidat darf erst nach einer neuen Vorregistrierung mit neuen
Seeds geprüft werden. Dieser spätere Lauf muss mindestens dieselbe ungekoppelte
Baseline, identische Ein- und Ausgabebedingungen sowie ein vorab festgelegtes
Intervallkriterium enthalten.

## Aussagegrenze

Der Versuch ist eine begrenzte Mechanismensuche in einem dimensionslosen
`4×4`-Modell. Ein explorativer Kandidat belegt weder einen allgemeinen Vorteil
noch elektrische Realisierbarkeit, Energiebedarf oder Fertigbarkeit.
