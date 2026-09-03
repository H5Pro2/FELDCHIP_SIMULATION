# Feldbasierter Wahrnehmungschip

## Eine Konzeptarchitektur für räumliche Zustandsabbildung im kontinuierlichen Arbeitsbereich von −3 bis +3

**Whitepaper · Version 1.0 · September 2026**

## Kurzfassung

Dieses Whitepaper beschreibt eine Chiparchitektur, bei der sensorische oder
technisch kodierte Eingänge nicht vorrangig in binäre Zwischenzustände
übersetzt werden. Stattdessen erzeugen gekoppelte physikalische Regionen eine
räumlich und zeitlich verteilte Feldform. Jeder lokale Feldwert bleibt in einem
normierten kontinuierlichen Arbeitsbereich von `−3` bis `+3`. Nach Wegfall des
Eingangs wird das Feld kontrolliert zu einem definierten Referenzpunkt
zurückgeführt.

Der Chip soll keine symbolischen Zustände dauerhaft speichern. Seine Funktion
ist die gegenwartsbezogene Abbildung eines Eingangs in eine messbare
Feldgeometrie. Der Begriff „Wahrnehmung“ wird daher technisch verwendet: Er
bezeichnet eine reproduzierbare physikalische Transformation von Eingangsmustern
in unterscheidbare interne Feldformen. Weitergehende funktionale Deutungen sind
für das technische Konzept nicht erforderlich.

Die Literatur zeigt deutliche Berührungspunkte mit Cellular Nonlinear Networks,
Reaktions-Diffusions-Chips, In-Sensor-Computing, physikalischem
Reservoir-Computing, ereignisbasierten Sensoren und gekoppelten
Oszillatornetzwerken. Keine dieser Richtungen entspricht jedoch vollständig
der hier formulierten Kombination aus kontinuierlichem symmetrischem
Arbeitsraum, räumlicher Feldabbildung, expliziter Nicht-Speicherfunktion,
feldförmiger Auslese und kontrollierter Rückführung. Das Konzept ist
mathematisch formulierbar und als kleiner Mixed-Signal-Demonstrator
grundsätzlich realisierbar. Ein industrieller Nutzen muss an einer eng
definierten Sensoraufgabe gegen digitale und klassische analoge Baselines
nachgewiesen werden.

## 1. Ausgangsfrage

Digitale Prozessoren verwenden robuste binäre Zustandsklassen. Diese
Abstraktion ermöglicht exakte Logik, allgemeine Programmierbarkeit und hohe
Fehlertoleranz. Räumlich verteilte Signale werden dafür jedoch gewöhnlich
abgetastet, quantisiert, gespeichert und durch aufeinanderfolgende
Rechenoperationen verarbeitet.

Die Ausgangsfrage dieses Whitepapers lautet:

> Kann ein Chip einen sensorischen oder technisch kodierten Eingang direkt als
> räumliche Feldform abbilden, deren lokale Werte kontinuierlich zwischen −3
> und +3 liegen und die nach der Auswertung kontrolliert auf einen
> Referenzpunkt zurückkehrt?

Die konzeptionelle Antwort ist ja. Die erforderlichen Grundmechanismen –
kontinuierliche Zustände, lokale Kopplung, Sättigung, Relaxation und räumliche
Auslese – sind aus Analog-, Sensor- und Halbleitertechnik bekannt. Die offene
Forschungsfrage ist, ob ihre konkrete Kombination eine nützliche und messbar
effiziente Wahrnehmungsfunktion ergibt.

## 2. Technische Definition

### 2.1 Wahrnehmung als Zustandsabbildung

Für dieses Konzept bezeichnet Wahrnehmung ausschließlich:

> Die reproduzierbare Transformation eines gegenwärtigen Eingangsmusters in
> eine räumlich verteilte, messbare interne Feldform.

Eine technische Feldwahrnehmung ist gegeben, wenn:

- ein Eingang die interne Feldverteilung kausal verändert,
- verschiedene Eingänge unterscheidbare Feldformen erzeugen,
- gleiche Eingänge innerhalb festgelegter Toleranzen vergleichbare Feldformen
  hervorbringen,
- relevante räumliche oder zeitliche Eigenschaften am Ausgang messbar sind,
- das System nach Ende des Eingangs definiert zum Referenzzustand zurückkehrt.

### 2.2 Keine dauerhafte Speicherung

Die Feldform ist ein vorübergehender Betriebszustand. Kapazitäten, Hysterese
und endliche Relaxationszeiten können kurzfristige Nachläufe verursachen. Diese
werden zunächst als Bauelementdynamik behandelt, nicht als eigenständige
Speicherfunktion. Für zeitabhängige Anwendungen darf die Relaxationsbahn
ausgewertet werden; danach muss die kontrollierte Rückführung einen
reproduzierbaren Ausgangszustand wiederherstellen.

### 2.3 Der Arbeitsbereich −3 bis +3

Der lokale Zustand ist eine kontinuierliche Größe:

```text
u(x, y, t) ∈ [−3, +3]
```

Die Werte bilden keine siebenwertige Logik. Zwischenwerte sind ausdrücklich
zulässig. Die Zahlen sind normierte technische Grenzwerte und können in einer
Realisierung beispielsweise Spannungen, Strömen, Ladungsdichten,
Polarisationsgraden, Phasenlagen oder Leitwerten zugeordnet werden.

Der größere Darstellungsraum kann bei gleicher absoluter physikalischer
Unterscheidungsschwelle `Δ` mehr unterscheidbare Pegel bereitstellen. Näherungsweise
gilt `N ≈ 6/Δ + 1` für `−3…+3`, gegenüber `N ≈ 2/Δ + 1` für `−1…+1`. Der
Gewinn beträgt damit ungefähr den Faktor drei, sofern Rauschen, Linearität und
Ausleseelektronik die gleiche Schrittweite tatsächlich erhalten. Bei einer
festen Anzahl digitaler Auslesecodes entsteht dagegen keine zusätzliche
Auflösung; dann verteilen sich dieselben Codes lediglich über einen größeren
Bereich. Der beanspruchte Darstellungsgewinn setzt deshalb einen entsprechend
nutzbaren physikalischen Dynamikbereich voraus.

#### 2.3.1 Funktionale Begründung der Grenze

Die Zahl `3` wird in diesem Konzept nicht als Naturkonstante verstanden. Sie
bezeichnet eine normierte Entwurfsgrenze, durch die auf jeder Seite des
Rückführungspunkts drei funktional unterscheidbare Intensitätsregime abgebildet
werden können. Mit `a = |u-r|` lassen sie sich zunächst wie folgt definieren:

1. **Sensitiver Bereich (`0 ≤ a < 1`):** Kleine Eingangsunterschiede sollen mit
   hoher Empfindlichkeit erhalten bleiben. Die Rückführung ist vergleichsweise
   schwach.
2. **Integrationsbereich (`1 ≤ a < 2`):** Stärkere oder überlagerte Eingänge
   können gekoppelte und nichtlineare Feldmuster ausbilden. Die Rückführung
   nimmt zu.
3. **Sättigungs- und Schutzbereich (`2 ≤ a ≤ 3`):** Große Auslenkungen werden
   begrenzt. Eine starke Rückführung verhindert, dass das Feld seinen
   vorgesehenen Arbeitsraum dauerhaft verlässt.

Eine mögliche mathematische Umsetzung ist eine zustandsabhängige
Rückführungsstärke:

```text
∂u/∂t = F_Eingang + D∇²u − k(|u−r|)(u−r) + η

k₁ < k₂ < k₃
```

Dabei gelten `k₁`, `k₂` und `k₃` in den drei genannten Bereichen. Der Übergang
kann stufig oder, zur Vermeidung harter Schaltgrenzen, kontinuierlich geglättet
ausgeführt werden.

#### 2.3.2 Warum zusätzliche Bereiche nicht automatisch nützen

Eine Erweiterung auf `−4…+4`, `−5…+5` oder größere Zahlenbereiche erzeugt für
sich genommen weder eine neue Feldfunktion noch zusätzliche Information. Ohne
ein weiteres physikalisch unterscheidbares Verhaltensregime wäre sie lediglich
eine andere Skalierung. Zusätzliche Bereiche würden zugleich höhere
Anforderungen an Dynamikbereich, Rauschabstand, Bauteiltoleranzen, Kalibrierung
und gegebenenfalls Energiebedarf stellen. Bei unveränderter digitaler
Auslesebreite könnte sich sogar die Auflösung pro normierter Einheit
verschlechtern.

Der Bereich `−3…+3` ist deshalb als kleinster symmetrischer Funktionsraum
motiviert, der die Folge **Wahrnehmung, Integration und Begrenzung** auf beiden
Seiten eines kontrollierten Rückführungspunkts ausdrückt. Zusätzliche
Information soll vorrangig durch räumliche Feldform, Verteilungsbreite,
Gradienten, zeitliche Entwicklung und gekoppelte Muster entstehen, nicht durch
eine unbegründete Verlängerung der Zustandsachse.

Diese Begründung bleibt eine prüfbare Entwurfsannahme. Ob drei Regime gegenüber
zwei, vier oder einer vollständig glatten Kennlinie technisch optimal sind,
muss anhand von Informationsgehalt, Robustheit, Energiebedarf und
Realisierungsaufwand experimentell verglichen werden.

Die Information liegt nicht nur im lokalen Pegel, sondern in der gesamten
Feldform `U(t) = {u(x,y,t)}`. Dadurch können Lage, Richtung, Ausdehnung,
Symmetrie, Gradient, Amplitude, Phase oder Veränderung eines Eingangsmusters
physikalisch abgebildet werden.

## 3. Funktionsprinzip

Die minimale Signalkette lautet:

```text
Sensor oder Datenwandler
→ gekoppelte Feldregionen
→ dynamische Feldform in [−3,+3]
→ räumliche und zeitliche Auslese
→ kontrollierte Rückführung zum Referenzfeld
```

Der Eingangswandler überführt Licht, Druck, Schall, Temperatur,
elektromagnetische Größen, chemische Konzentrationen oder digital vorbereitete
Daten in eine räumliche Anregung. Die gekoppelte Struktur entwickelt daraus
selbsttätig eine Feldform. Ein Auslesearray misst die vollständige Verteilung
oder daraus abgeleitete Merkmale. Eine Rückführungsstruktur stellt anschließend
den definierten Ausgangszustand wieder her.

Mögliche Ausgaben sind:

- eine vollständige zweidimensionale Feldkarte,
- Schwerpunkt, Ausdehnung und Orientierung,
- Gradienten, Kanten und lokale Kontraste,
- Symmetrie-, Phasen- oder Kohärenzmaße,
- zeitliche Änderungsraten,
- Abstand zum Referenzfeld,
- Ereignis- oder Klassifikationssignale für nachgelagerte Elektronik.

## 4. Mathematisches Grundmodell

Eine skalare Felddynamik kann durch folgende Gleichung beschrieben werden:

```text
∂u/∂t = D·Δu + K[u] + G(I) − λ(u−r) − ∂V_B(u)/∂u + η
```

Dabei bezeichnet `u(x,y,t)` den lokalen Feldwert, `I(x,y,t)` den aktuellen
Eingang, `D·Δu` die lokale räumliche Kopplung, `K[u]` weitere gerichtete oder
nichtlokale Kopplungen und `G(I)` die Eingangswandlung. Der Term `λ(u−r)` führt
das Feld zum Referenzwert `r` zurück. `V_B` begrenzt den Arbeitsbereich und `η`
fasst Rauschen sowie Bauteilstreuung zusammen.

Ein mögliches mathematisches Begrenzungspotential im offenen Intervall lautet:

```text
V_B(u) = β / (9 − u²)
```

Eine reale Schaltung muss dieses Potential nicht wörtlich implementieren.
Sättigung, Clamping oder eine nichtlineare Materialantwort können dieselbe
begrenzende Funktion erfüllen.

Ohne Eingang und ohne weitere Anregung reduziert sich die Dynamik
näherungsweise auf:

```text
∂u/∂t = −λ(u−r)
u(t) = r + [u(t₀)−r]·exp[−λ(t−t₀)]
```

Damit ist die Rückführungszeit über `λ` kontrollierbar. Statt eines skalaren
Punkts kann ein räumlich strukturiertes Referenzfeld `R(x,y)` verwendet werden.
So lassen sich Nullstellung, Vorspannung oder eine anwendungsspezifische
Grundgeometrie definieren.

Eine feldförmige Ausgabe kann durch gewichtete räumliche Funktionale entstehen:

```text
y_j(t) = ∬ w_j(x,y) · Φ[u, ∇u, ∂u/∂t] dxdy
```

Diese Form erlaubt sowohl direkte Feldkarten als auch kompakte Merkmalsausgaben.

## 5. Technologische Berührungspunkte

Der Ausgangspunkt dieses Konzepts war die eigenständige Überlegung, binäre
Zwischenrepräsentationen für bestimmte Wahrnehmungsaufgaben durch eine
begrenzte dynamische Feldform zu ergänzen. Ein anschließender Vergleich mit dem
Stand der Forschung zeigt, dass wesentliche Teilmechanismen bereits in mehreren
Disziplinen untersucht wurden. Diese Berührungspunkte stützen die prinzipielle
Machbarkeit, begründen aber keine Aussage über Priorität oder Schutzfähigkeit.

### 5.1 Cellular Neural beziehungsweise Nonlinear Networks

Chua und Yang beschrieben 1988 zweidimensionale Netze aus lokal gekoppelten,
kontinuierlichen nichtlinearen Zellen. Die Netzdynamik kann räumliche Muster
parallel entwickeln und in stabile Zustände überführen. Spätere analoge
CMOS-Implementierungen wurden für Bildverarbeitung und räumliche Dynamik
eingesetzt.

Der direkte Berührungspunkt liegt in den kontinuierlichen lokalen Zuständen,
der Nachbarschaftskopplung und der selbsttätigen Entwicklung eines globalen
Musters. Das vorliegende Konzept ergänzt eine explizite sensorische
Wahrnehmungsdefinition, den normierten Bereich `−3…+3`, die feldförmige
Auslese und eine kontrollierte Rückführung ohne vorausgesetzte dauerhafte
Speicherung.

### 5.2 Reaktions-Diffusions-Chips

Analoge CMOS-Reaktions-Diffusions-Schaltungen bilden lokale Reaktion und
räumliche Diffusion direkt in Hardware nach. Gefertigte Versuchschips zeigen,
dass komplexe räumliche Muster durch physikalische Dynamik entstehen können,
ohne jeden inneren Übergang digital zu berechnen.

Dies ist dem Prinzip der selbsttätigen Feldbildung besonders nahe. Der
Unterschied besteht darin, dass Reaktions-Diffusions-Chips typischerweise eine
spezifische Modellgleichung emulieren, während der Wahrnehmungschip eine
anwendungsbezogene, begrenzte und rückgeführte Eingangsabbildung anstrebt.

### 5.3 In-Sensor-Computing

In-Sensor-Computing verlagert Rechenoperationen direkt in Sensorarrays. So
wurden programmierbare Silizium-Fotodiodennetze demonstriert, die analoge
Bildfilter bereits in der Sensorebene ausführen. Der gemeinsame Ansatz ist die
Reduktion von Datenbewegung zwischen Erfassung und Verarbeitung.

Viele dieser Systeme implementieren jedoch vorab definierte Operationen wie
Multiply-Accumulate oder Faltung. Der hier beschriebene Chip nutzt dagegen die
gekoppelte Feldform selbst als primäre interne Darstellung.

### 5.4 Ereignisbasierte und neuromorphe Sensoren

Dynamische Bildsensoren reagieren lokal und asynchron auf Helligkeitsänderungen,
statt vollständige Bildfolgen mit fester Taktrate auszugeben. Dies zeigt, dass
gegenwartsbezogene, kontinuierliche Sensordynamik und kontrollierte lokale
Rückstellung in integrierter Hardware praktisch nutzbar sind.

Solche Sensoren geben üblicherweise adressierte Ereignisse aus. Sie bilden
nicht notwendigerweise ein räumlich gekoppeltes internes Feld. Für den
Wahrnehmungschip liefern sie dennoch wichtige Vorbilder für lokale
Eingangswandlung, geringe Latenz und ereignisorientierte Auslese.

### 5.5 Physikalisches Reservoir-Computing

Physikalische Reservoirs nutzen die nichtlineare Dynamik eines Materials oder
Netzwerks, um Eingänge in einen hochdimensionalen Zustandsraum abzubilden.
Memristive, photonische, mechanische und elektronische Demonstratoren belegen
die technische Breite dieses Ansatzes.

Der zentrale Unterschied liegt im Umgang mit der Zeitabhängigkeit:
Reservoir-Computing nutzt häufig eine ausklingende Abhängigkeit von früheren
Eingängen. Beim hier vorgeschlagenen Chip ist eine solche Nachwirkung nur eine
kontrollierte Übergangsdynamik; anschließend soll das Referenzfeld gezielt
wiederhergestellt werden.

### 5.6 Gekoppelte Oszillator- und Ising-Chips

Große Arrays gekoppelter Ringoszillatoren zeigen, dass ein integriertes System
durch lokale Wechselwirkungen schnell in globale Phasenmuster relaxieren kann.
Ein publizierter 1.968-Knoten-Chip demonstrierte die Skalierbarkeit dieses
Prinzips für Optimierungsaufgaben.

Der Wahrnehmungschip verfolgt keine Ising-Optimierung. Relevant ist hier der
Nachweis, dass eine globale physikalische Konfiguration auf einem Chip
kontrolliert entstehen, gemessen und für eine technische Aufgabe genutzt
werden kann.

## 6. Eigenständige Kombination

| Merkmal | Bestehende Berührungspunkte | Schwerpunkt dieses Whitepapers |
|---|---|---|
| Interner Zustand | Analoge Pegel, Zellzustände, Phasen oder Leitwerte | Kontinuierliche räumliche Feldform |
| Arbeitsbereich | Technologiespezifisch, häufig normiert | Explizit symmetrisch und begrenzt auf `−3…+3` |
| Eingang | Bild, Zeitreihe, Bias oder Optimierungsproblem | Sensorfeld oder räumlich kodierte technische Daten |
| Verarbeitung | Faltung, Relaxation, Reservoir- oder Netzwerkdynamik | Selbsttätige Bildung einer Wahrnehmungsfeldform |
| Ausgabe | Ereignis, Klasse, Optimierungslösung oder Skalar | Feldkarte und/oder räumlich-zeitliche Merkmale |
| Zeitverhalten | Teilweise persistierend oder mit kurzzeitiger Nachwirkung | Definierte Übergangsdynamik mit kontrollierter Rückführung |
| Ziel | Rechnen, Erkennen, Optimieren oder Speichern | Gegenwartsbezogene Zustandsabbildung ohne Speicheranspruch |

Die mögliche Eigenständigkeit liegt somit nicht in einem einzelnen
Bauelement und nicht allein in der Skalierung `−3…+3`. Sie liegt in der
Systemdefinition und im Zusammenspiel von Eingangswandlung, gekoppeltem Feld,
symmetrischer Begrenzung, räumlicher Auslese und definiertem Reset. Ob diese
Kombination gegenüber dem Stand der Technik neu oder schutzfähig ist, kann nur
eine gesonderte Patent- und Anspruchsrecherche klären.

## 7. Funktionale Architektur

Eine erste Architektur kann monolithisch oder als Mixed-Signal-System
realisiert werden. Das Konzept setzt keine bestimmte Packaging-Technik voraus.

Erforderliche Funktionsblöcke sind:

- **Eingangswandler:** Überführung physikalischer oder digital vorbereiteter
  Signale in lokale Anregungen.
- **Feldarray:** Gekoppelte kontinuierliche Zellen mit einstellbarer lokaler
  und gegebenenfalls nichtlokaler Wechselwirkung.
- **Begrenzung:** Sicherung des zulässigen Bereichs von `−3` bis `+3`.
- **Rückführung:** Regelbare Relaxation auf `r = 0` oder ein programmierbares
  Referenzfeld `R(x,y)`.
- **Auslesearray:** Messung lokaler Werte, Gradienten, Phasen oder
  Integralfunktionen.
- **Digitale Schnittstelle:** Konfiguration, Kalibrierung, Diagnose und
  Weitergabe der Ergebnisse.

Als Substrate kommen zunächst resistiv-kapazitive CMOS-Netze, gekoppelte
Oszillatoren oder ferroelektrische und memristive Bauelemente infrage. Eine
Materialentscheidung vor der Festlegung der Zielaufgabe wäre verfrüht. Der
erste Demonstrator sollte mit gut charakterisierbarer Mixed-Signal-Technik
arbeiten, damit die Systemhypothese unabhängig von neuartigen Materialien
geprüft werden kann.

## 8. Anwendungspotenzial

### 8.1 Raumfahrt, Robotik und autonome Systeme

Ein Feldarray könnte mehrere räumlich verteilte Sensoren zu einer gemeinsamen
Momentaufnahme koppeln. Denkbare Aufgaben sind Annäherungs- und
Kollisionsfelder, Oberflächenbelastungen, Magnetfeldverteilungen, thermische
Gradienten oder lokale Anomalien. Interessant wäre insbesondere ein
energiebegrenzter Betrieb mit schneller Ereignisausgabe und nachgelagerter
digitaler Verifikation.

### 8.2 Bild- und Bewegungssensorik

Optische Eingänge könnten unmittelbar Kanten, Bewegungsrichtungen,
Kontrastinseln, Symmetrien oder Schwerpunkte als Feldgeometrie ausprägen. Das
Ziel wäre keine vollständige Ersetzung digitaler Bildverarbeitung, sondern eine
frühe physikalische Verdichtung relevanter Strukturen.

### 8.3 Taktile und strukturelle Sensorflächen

Druck-, Dehnungs- oder Vibrationsarrays besitzen bereits eine natürliche
räumliche Topologie. Ein gekoppeltes Feld könnte Kontaktflächen, Lastpfade,
Rissausbreitung oder ungewöhnliche Schwingungsmuster direkt abbilden.

### 8.4 Elektromagnetische und akustische Felder

Phasen- und Amplitudenbeziehungen mehrerer Antennen oder Mikrofone könnten in
eine interne Feldform überführt werden. Daraus ließen sich Richtung,
Kohärenz, Interferenz oder lokale Störquellen ableiten.

### 8.5 Technisch kodierte Daten

Auch nichtphysikalische Daten können verarbeitet werden, wenn sie über einen
Wandler räumlich angeordnet werden. Der Chip erkennt dabei nicht automatisch
deren semantische Bedeutung. Er verarbeitet ausschließlich die Geometrie und
Dynamik der angebotenen Darstellung.

## 9. Potenzielle Vorteile

Für geeignete Aufgaben sind folgende Vorteile prüfbar:

- parallele physikalische Wechselwirkung vieler lokaler Eingänge,
- geringe Latenz bis zu einer verwertbaren Feldform,
- reduzierter Daten- und Speicherverkehr,
- direkte Verarbeitung räumlich verteilter Sensorsignale,
- robuste Wiederholbarkeit durch definierte Begrenzung und Rückführung,
- ereignisorientierte Ausgabe statt permanenter Vollfelddigitalisierung,
- mögliche Energieeinsparung bei eng passenden Aufgaben.

Diese Punkte sind Forschungsziele und keine bereits belegten
Leistungsversprechen. Die Gesamtbilanz muss Eingangswandlung, Feldentwicklung,
Stabilisierung, Auslese, Analog-Digital-Wandlung, Kalibrierung und
Fehlerbehandlung umfassen.

## 10. Wissenschaftliche und technische Machbarkeit

**Mathematisch:** Das Konzept ist mit gekoppelten Differentialgleichungen,
nichtlinearen Netzwerken und beschränkten dynamischen Systemen direkt
modellierbar.

**Experimentell:** Ein kleines resistiv-kapazitives oder Mixed-Signal-Array mit
lokaler Kopplung, einstellbarer Sättigung, räumlicher Auslese und geregeltem
Reset ist mit heutiger Labortechnik grundsätzlich aufbaubar.

**Halbleitertechnisch:** Eine Integration ist plausibel, erfordert jedoch eine
sorgfältige Beherrschung von Bauteilstreuung, Temperaturdrift,
Kopplungsparasiten, Rauschen und Ausleseaufwand.

**Industriell:** Noch nicht belegt ist, ob der Ansatz bei einer konkreten
Anwendung Energie, Latenz, Baufläche oder Robustheit gegenüber etablierten
Sensorprozessoren verbessert. Der Nutzen kann nur durch einen vollständigen
End-to-End-Benchmark nachgewiesen werden.

Die zentrale Unsicherheit lautet nicht, ob irgendeine Feldform erzeugt werden
kann. Entscheidend ist, ob eine nützliche Eingangseigenschaft reproduzierbar,
kontrollierbar und insgesamt günstiger abgebildet wird als mit einem einfachen
Analogfilter oder einer digitalen Verarbeitungskette.

## 11. Prüfbare Hypothesen und Messgrößen

Ein erster Demonstrator sollte folgende Hypothesen testen:

- **H1:** Verschiedene räumliche Eingänge erzeugen statistisch trennbare
  Feldformen.
- **H2:** Wiederholte gleiche Eingänge erzeugen innerhalb einer festgelegten
  Toleranz vergleichbare Feldformen.
- **H3:** Alle lokalen Zustände bleiben unter spezifizierten Störungen im
  Bereich `−3…+3`.
- **H4:** Nach Entfernen des Eingangs erreicht das Feld den Rückführungspunkt
  innerhalb einer spezifizierten Zeit und Genauigkeit.
- **H5:** Die gekoppelte Feldform enthält für die Zielaufgabe mehr nutzbare
  Information als ungekoppelte analoge Sensorkanäle.
- **H6:** Energie und Latenz des Gesamtsystems sind für die Zielaufgabe günstiger
  als bei festgelegten Vergleichssystemen.
- **H7:** Unter gleichen Randbedingungen erreicht die Drei-Regime-Kennlinie ein
  günstigeres Verhältnis aus unterscheidbaren Feldformen, Robustheit,
  Energiebedarf und Kalibrierungsaufwand als Zwei-, Vier-Regime- oder vollständig
  glatte Vergleichskennlinien.

Zu messen sind Feldform, Trennbarkeit, Wiederholbarkeit, Grenzverletzungen,
Rückführungszeit, Rückführungsfehler, Temperatur- und Rauschabhängigkeit,
Kalibrierungsaufwand, Latenz und Energie vom Eingang bis zur verwertbaren
Ausgabe.

Pflichtbaselines sind ein digitaler Sensorprozessor, ein klassischer
Analogfilter, ein ungekoppeltes Sensorarray und ein einfaches
resistiv-kapazitives Netzwerk. Das Konzept bietet für eine konkrete Anwendung
keinen eigenständigen Nutzen, wenn eine einfachere Baseline dieselben Merkmale
mit gleicher oder besserer Effizienz erzeugt oder die Auslese den möglichen
Vorteil aufzehrt.

## 12. Vorgeschlagenes Entwicklungsprogramm

### Phase 1: Mathematischer Demonstrator

Simulation eines zweidimensionalen Feldes mit 16×16 oder 32×32 gekoppelten
Regionen, kontinuierlichen Zuständen in `−3…+3`, räumlichen Eingaben,
Bauteilstreuung, Rauschen und einstellbarem Rückführungspunkt. Zwei-, Drei- und
Vier-Regime-Ausführungen sowie eine vollständig glatte Kennlinie werden unter
gleichen Randbedingungen verglichen.

### Phase 2: Baselinevergleich

Vergleich gegen digitale Faltung, klassische Analogfilter, ungekoppelte
Sensorkanäle und resistiv-kapazitive Netze anhand derselben Eingaben und
Ausgabemetriken.

### Phase 3: Labordemonstrator

Aufbau eines kleinen diskreten oder integrierten Mixed-Signal-Arrays. Primäres
Ziel ist der Nachweis stabiler Feldformen und einer reproduzierbaren
Rückführung, nicht die sofortige Optimierung der Leistungsaufnahme.

### Phase 4: Anwendungsspezifischer Prototyp

Integration mit genau einer räumlichen Sensoraufgabe, beispielsweise einer
taktilen Fläche, einem Mikrofonarray oder einem optischen Kontrastfeld.

### Phase 5: Halbleitermapping und Skalierung

Erst nach erfolgreichem Funktionsnachweis werden CMOS-, ferroelektrische,
spintronische, photonische, oszillatorische oder memristive Implementierungen
anhand messbarer Anforderungen verglichen.

## 13. Vorschlag für eine industrielle Kooperation

Für einen Industriepartner wäre ein begrenztes Vorprojekt sinnvoll, das nicht
mit einer vollständigen Chipentwicklung beginnt. Ein gemeinsames Team aus
Mixed-Signal-Design, Sensorik, nichtlinearer Dynamik und Systembenchmarking
könnte innerhalb eines klar definierten Programms:

- eine Zielanwendung und verbindliche Baselines festlegen,
- das mathematische Modell und die Rückführungsregel simulieren,
- einen kleinen elektrischen Demonstrator aufbauen,
- Nutzen und Grenzen anhand offener Messgrößen dokumentieren,
- auf dieser Grundlage über eine ASIC- oder Spezialmaterial-Implementierung
  entscheiden.

Ein positives Ergebnis wäre nicht zwingend ein universeller neuer Prozessor.
Bereits ein energieeffizienter Sensor-Front-End-Baustein für eine klar
abgegrenzte Aufgabe könnte industriell relevant sein.

## 14. Schlussfolgerung

Ein feldbasierter Wahrnehmungschip ist eine wissenschaftlich plausible
Spezialarchitektur. Sein interner Zustand ist keine binäre Bitfolge und keine
dauerhaft gespeicherte Klasse, sondern eine vorübergehende räumliche Feldform
innerhalb des kontinuierlichen Bereichs von `−3` bis `+3`. Ein kontrollierter
Rückführungspunkt stellt nach jedem Vorgang einen definierten Ausgangszustand
wieder her.

Die Forschung zu gekoppelten analogen Zellnetzen, Reaktions-Diffusions-Chips,
In-Sensor-Computing, ereignisbasierten Sensoren, physikalischen Reservoirs und
Oszillatorarrays zeigt, dass die benötigten Teilmechanismen real sind. Der
offene Beitrag dieses Konzepts liegt in ihrer gezielten Kombination für eine
gegenwartsbezogene Feldwahrnehmung mit expliziter Begrenzung und Rückführung.

Der nächste belastbare Schritt ist ein falsifizierbarer mathematischer und
elektrischer Demonstrator mit vollständigem Baselinevergleich. Erst dieser
Nachweis kann zeigen, ob aus der plausiblen Idee eine wirtschaftlich relevante
Chipfunktion wird. Das Whitepaper beschreibt keine fertige Hardware, keinen
belegten Leistungsvorteil und erhebt keine Aussage über Patentierbarkeit oder
historische Priorität.

## Literatur

- Chua, L. O.; Yang, L.: “Cellular Neural Networks: Theory.” *IEEE
   Transactions on Circuits and Systems*, 35(10), 1257–1272, 1988.
   DOI: https://doi.org/10.1109/31.7600
- Asai, T.: “Analog reaction-diffusion chip and its application.” *Oyo
   Buturi*, 72(10), 1286–1290, 2003.
   DOI: https://doi.org/10.11470/oubutsu.72.10_1286
- Lichtsteiner, P.; Posch, C.; Delbrück, T.: “A 128×128 120 dB 15 μs
   Latency Asynchronous Temporal Contrast Vision Sensor.” *IEEE Journal of
   Solid-State Circuits*, 43(2), 566–576, 2008.
   DOI: https://doi.org/10.1109/JSSC.2007.914337
- Jang, H. et al.: “In-sensor optoelectronic computing using
   electrostatically doped silicon.” *Nature Electronics*, 5, 519–525, 2022.
   DOI: https://doi.org/10.1038/s41928-022-00819-6
- Moy, W. et al.: “A 1,968-node coupled ring oscillator circuit for
   combinatorial optimization problem solving.” *Nature Electronics*, 5,
   310–317, 2022. DOI: https://doi.org/10.1038/s41928-022-00749-3
- Choi, S. et al.: “3D-integrated multilayered physical reservoir array for
   learning and forecasting time-series information.” *Nature
   Communications*, 15, 2044, 2024.
   DOI: https://doi.org/10.1038/s41467-024-46323-7
- Liang, X. et al.: “Physical reservoir computing with emerging
   electronics.” *Nature Electronics*, 7, 193–206, 2024.
   DOI: https://doi.org/10.1038/s41928-024-01133-z
