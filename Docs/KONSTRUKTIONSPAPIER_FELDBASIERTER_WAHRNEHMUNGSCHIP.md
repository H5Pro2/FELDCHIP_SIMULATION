# Technisches Architektur- und Konstruktionskonzept für einen feldbasierten Wahrnehmungschip

## Schaltungsmodell, Demonstratorarchitektur und Validierungsplan für einen kontinuierlichen Arbeitsbereich von −3 bis +3

**Dokumenttyp:** Technisches Konstruktionskonzept<br>
**Version:** 1.0<br>
**Stand:** September 2026<br>
**Status:** Forschungs- und Entwicklungsgrundlage, kein fertigungstauglicher Schaltplan

---

## Kurzfassung

Dieses Dokument überführt das Konzept eines feldbasierten Wahrnehmungschips in
eine technisch prüfbare Architektur. Der Chip soll gegenwärtige sensorische oder
technisch kodierte Eingangsmuster nicht ausschließlich in binäre
Zwischenzustände übersetzen. Stattdessen erzeugt ein Array gekoppelter
physikalischer Zellen eine kontinuierliche, räumlich verteilte Feldform. Jeder
lokale Zustand wird auf den normierten Bereich von `−3` bis `+3` begrenzt. Nach
der Auswertung führt eine kontrollierte Rückführungsdynamik das Array zu einem
definierten Referenzfeld zurück.

Als erste Realisierung wird ein Mixed-Signal-System vorgeschlagen. Das
eigentliche Feld entsteht analog in einem resistiv-kapazitiven Zellarray. Eine
digitale Randstruktur konfiguriert Kopplung, Verstärkung, Referenzwert und
Messablauf. Die drei Intensitätsregime pro Polarität werden durch eine
zustandsabhängige Rückführungskennlinie umgesetzt: empfindliche Wahrnehmung bei
kleiner Auslenkung, Integration im mittleren Bereich sowie starke Begrenzung und
Rückführung im äußeren Bereich.

Das Papier beschreibt eine einzelne Feldzelle, die Kopplung im Array,
Eingangs- und Ausleseschaltungen, eine mathematische Stabilitätsbedingung, einen
diskreten `4×4`- beziehungsweise `8×8`-Demonstrator und den Übergang zu einem
integrierten Testchip. Alle Leistungsangaben bleiben Zielgrößen. Ein technischer
Vorteil gegenüber Analogfiltern oder digitaler Sensorverarbeitung muss durch
Messungen nachgewiesen werden.

## 1. Zweck und Abgrenzung

Ziel dieses Dokuments ist eine Konstruktion, mit der folgende Systemhypothese
experimentell geprüft werden kann:

> Ein gekoppeltes physikalisches Zellarray kann unterschiedliche räumliche
> Eingänge reproduzierbar in unterscheidbare, vorübergehende Feldformen
> transformieren und danach kontrolliert zu einem Referenzzustand zurückkehren.

Der Begriff Wahrnehmung wird ausschließlich technisch verwendet. Er bezeichnet
die kausale und reproduzierbare Abbildung eines Eingangsmusters in eine intern
messbare Feldform. Eine semantische Eigeninterpretation wird weder vorausgesetzt
noch behauptet.

Das Dokument ist noch kein ASIC-Freigabedatensatz. Nicht enthalten sind ein
festgelegter Halbleiterprozess, vollständige Transistordimensionierungen,
verifizierte Layoutregeln, Maskendaten, qualifizierte Zuverlässigkeitswerte oder
gemessene Leistungsversprechen. Diese Angaben können erst nach Simulation und
Demonstratorvalidierung sinnvoll festgelegt werden.

## 2. Technische Systemanforderungen

Ein erster Demonstrator muss mindestens folgende Anforderungen erfüllen:

1. Jede Feldzelle besitzt einen kontinuierlichen, messbaren Zustand.
2. Der normierte Zustand bleibt innerhalb von `−3 ≤ u_i ≤ +3`.
3. Positive und negative Zustände werden ohne negative Versorgungsspannung
   darstellbar.
4. Benachbarte Zellen beeinflussen sich mit einstellbarer Kopplungsstärke.
5. Die Rückführung zum Referenzwert wird mit wachsender Auslenkung stärker.
6. Sensorische oder künstlich erzeugte Eingangsmuster können lokal eingespeist
   werden.
7. Lokale Zustände sowie globale Feldmerkmale sind auslesbar.
8. Rauschen, Bauteilstreuung, Temperatur und Grenzverletzungen werden gemessen.
9. Das System erreicht nach Ende des Eingangs innerhalb einer spezifizierten
   Zeit wieder das Referenzfeld.
10. Ein Vergleich mit einfacheren analogen und digitalen Baselines ist möglich.

## 3. Zustandsvariable und physikalische Kodierung

### 3.1 Normierter Feldzustand

Für jede Zelle `i` wird eine dimensionslose Zustandsvariable definiert:

```text
u_i(t) ∈ [−3,+3]
```

Die Zahl `3` ist keine physikalische Naturkonstante. Sie bezeichnet die Grenze
eines normierten Arbeitsraums mit drei funktionalen Intensitätsregimen pro
Polarität. Die physikalische Realisierung kann Spannung, Strom, Ladung,
Leitwert, Polarisation oder Phase verwenden.

### 3.2 Differentielle Spannungskodierung

Für einen CMOS- oder Leiterplattendemonstrator wird eine differentielle
Spannungskodierung empfohlen:

```text
u_i = (V_i+ − V_i−) / V_U
```

`V_U` bezeichnet die Spannungsdifferenz pro normierter Einheit. Bei
`V_U = 0,4 V` entspricht der Gesamtbereich `−3…+3` einer differentiellen
Spannung von `−1,2 V…+1,2 V`. Beide Leitungen können um eine positive
Gleichtaktspannung geführt werden, beispielsweise um `V_CM = 1,65 V` bei einer
Versorgung von `3,3 V`.

Eine einfachere erste Leiterplattenversion darf alternativ einen einzelnen
Zellknoten um `V_CM` verwenden:

```text
u_i = (V_i − V_CM) / V_U
```

Die differentielle Variante ist für eine spätere Integration günstiger, weil
sie Versorgungsschwankungen, Gleichtaktstörungen und Offsetfehler besser
unterdrücken kann.

### 3.3 Darstellungsbereich und effektive Auflösung

Bei gleicher absoluter physikalischer Unterscheidungsschwelle `Δ` gilt
näherungsweise:

```text
N_±3 ≈ 6/Δ + 1
N_±1 ≈ 2/Δ + 1
```

Damit kann der Bereich `−3…+3` ungefähr dreimal so viele unterscheidbare Pegel
wie `−1…+1` bereitstellen, sofern Rauschen, Linearität und Ausleseelektronik die
gleiche absolute Schrittweite erhalten. Bei fester ADC-Bitbreite entsteht dieser
Gewinn nicht automatisch. Die effektive Auflösung ist deshalb über Signal-
Rausch-Abstand, Nichtlinearität und wiederholbare Pegeltrennung zu bestimmen.

## 4. Schaltungsmodell einer Feldzelle

### 4.1 Dynamische Grundgleichung

Eine Feldzelle wird als kontinuierlicher Integrator mit Eingang, Kopplung,
Rückführung und Begrenzung beschrieben:

```text
C_i · dV_i/dt = I_i,ein
                + Σ_j g_ij(V_j − V_i)
                − I_R(V_i − V_r)
                − I_B(V_i)
                + I_i,stör
```

In normierter Form:

```text
du_i/dt = s_i(t)
          + Σ_j d_ij(u_j − u_i)
          − k(|u_i−r_i|)(u_i−r_i)
          − b(u_i)
          + η_i(t)
```

Dabei sind:

- `C_i`: Zustandskapazität,
- `s_i(t)`: lokaler Eingang,
- `d_ij`: Kopplung zwischen Zellen,
- `r_i`: lokaler Rückführungspunkt,
- `k(a)`: auslenkungsabhängige Rückführungsstärke,
- `b(u)`: weiche oder harte Bereichsbegrenzung,
- `η_i(t)`: Rauschen und nicht modellierte Störungen.

### 4.2 Funktionale Schaltungsblöcke

Eine Zelle benötigt folgende Schaltungsblöcke:

1. **Eingangswandler:** Wandelt Sensorstrom oder Eingangsspannung in einen
   begrenzten Anregungsstrom.
2. **Zustandsintegrator:** Ein Kondensator bildet den momentanen lokalen Zustand.
3. **Kopplungszweige:** Widerstände oder Transkonduktanzstufen verbinden die
   Zelle mit Nachbarn.
4. **Rückführungsverstärker:** Erzeugt einen Strom in Richtung des
   Referenzwertes.
5. **Begrenzungsstufe:** Verhindert dauerhaftes Überschreiten des Arbeitsraums.
6. **Auslesepuffer:** Entkoppelt Messsystem und Feldzelle.
7. **Konfigurationsregister:** Legt Verstärkungen, Referenz und Messmodus fest.

### 4.3 Zustandskapazität

Der Kondensator ist ein dynamisches Zustandsbauelement, aber kein vorgesehener
Langzeitspeicher. Seine Zeitkonstante bestimmt zusammen mit Rückführung und
Kopplung die Feldgeschwindigkeit.

Für einen Leiterplattendemonstrator sind zunächst `10 nF…1 µF` sinnvoll, weil
damit Zeitkonstanten im gut messbaren Millisekunden- bis Sekundenbereich erzeugt
werden können. Ein integrierter Testchip würde deutlich kleinere Kapazitäten
verwenden und entsprechend mit kleineren Strömen oder höheren
Geschwindigkeiten arbeiten. Konkrete ASIC-Werte hängen vom Prozess ab.

## 5. Drei Intensitätsregime und Rückführung

### 5.1 Funktionale Einteilung

Mit der Auslenkung

```text
a_i = |u_i − r_i|
```

werden drei Bereiche definiert:

1. **Sensitiver Bereich (`0 ≤ a < 1`):** Kleine Eingangsunterschiede bleiben
   sichtbar; die Rückführung ist schwach.
2. **Integrationsbereich (`1 ≤ a < 2`):** Überlagerte Eingänge und Kopplung
   können ausgeprägte Feldmuster bilden; die Rückführung nimmt zu.
3. **Sättigungs- und Schutzbereich (`2 ≤ a ≤ 3`):** Große Auslenkungen werden
   stark zurückgeführt und begrenzt.

### 5.2 Geglättete Rückführungskennlinie

Harte Komparatorschwellen können Umschaltstörungen und Oszillationen erzeugen.
Für den Regelbetrieb wird daher eine geglättete Kennlinie empfohlen:

```text
k(a) = k_1
       + (k_2−k_1)·σ((a−1)/w)
       + (k_3−k_2)·σ((a−2)/w)

σ(z) = 1/(1+e^(−z))
k_1 < k_2 < k_3
```

`w` bestimmt die Breite der Übergänge. Auf einer Leiterplatte kann die Kennlinie
mit Operationsverstärkern, Dioden, Transistorpaaren oder spannungsgesteuerten
Transkonduktanzverstärkern angenähert werden. In CMOS kann sie durch mehrere
parallel gewichtete Differenzpaare oder eine programmierbare
Transkonduktanzstufe entstehen.

### 5.3 Bereichsbegrenzung

Die Rückführung allein garantiert bei extremen Störungen noch keine harte
Grenze. Deshalb wird zusätzlich eine Schutzbegrenzung vorgesehen:

- weiches Clamping kurz vor `|u| = 3`,
- Strombegrenzung im Eingangspfad,
- optionaler harter Schutzkomparator außerhalb des normalen Arbeitsbereichs,
- digitales Fehlerflag bei jeder Grenzverletzung.

Die normale Feldfunktion soll in der weichen Kennlinie arbeiten. Der harte
Schutz ist ausschließlich eine Fehlersicherung.

### 5.4 Programmierbarer Referenzpunkt

Der Standardwert ist

```text
r_i = 0
```

Für Kalibrierung, Vorspannung oder anwendungsspezifische Referenzfelder kann
`r_i` programmierbar sein. Ein räumlich strukturiertes Referenzfeld
`R = {r_i}` ist technisch möglich, muss aber explizit geladen werden und darf
nicht mit einer selbstständig entstehenden Bedeutung verwechselt werden.

## 6. Kopplung und selbsttätige Feldbildung

### 6.1 Lokale Nachbarschaft

Ein zweidimensionales Array verwendet zunächst eine Vierer-Nachbarschaft:

```text
N_i = {oben, unten, links, rechts}
```

Der Kopplungsstrom lautet:

```text
I_i,kopplung = Σ_j g_ij(V_j − V_i)
```

Diese passive beziehungsweise transkonduktive Differenzkopplung entspricht
einer räumlichen Glättung. Diagonale oder weiter entfernte Verbindungen können
später ergänzt werden, wenn eine konkrete Aufgabe sie erfordert.

### 6.2 Einstellbare Kopplung

Für den Demonstrator sollten mindestens vier Kopplungsstufen verfügbar sein:

- aus,
- schwach,
- mittel,
- stark.

Die Einstellung kann mit Widerstandsnetzwerken, Analogschaltern oder digital
programmierbaren Transkonduktanzstufen erfolgen. Symmetrische Kopplungen
`g_ij = g_ji ≥ 0` vereinfachen den Stabilitätsnachweis. Gerichtete und negative
Kopplungen sind forschungsrelevant, erhöhen aber das Risiko instabiler
Oszillationen und gehören nicht in den ersten Funktionsnachweis.

### 6.3 Randbedingungen

Für die Arrayränder sind drei Betriebsarten sinnvoll:

1. **Reflektierend:** Kein Kopplungsstrom über den Rand.
2. **Festes Randfeld:** Randzellen koppeln zusätzlich an einen Referenzwert.
3. **Periodisch:** Gegenüberliegende Ränder werden verbunden, hauptsächlich für
   Simulationen.

Der Hardwaredemonstrator sollte reflektierende Ränder als Standard verwenden.

### 6.4 Stabilitätsbedingung

Für linearisierte positive Kopplungen kann das Array geschrieben werden als:

```text
C·du/dt = s(t) − L_g·u − K_r·(u−r)
```

`L_g` ist die gewichtete Graph-Laplace-Matrix. Sind alle Kapazitäten positiv,
alle symmetrischen Kopplungen nichtnegativ und die Rückführungskoeffizienten
positiv, ist das ungestörte Referenzfeld lokal asymptotisch stabil. Die
nichtlineare Begrenzung muss diese Eigenschaft im äußeren Bereich erhalten.

Der Nachweis ist für jede konkrete Schaltung durch Kleinsignalanalyse,
Transientensimulation und Monte-Carlo-Analyse zu wiederholen.

## 7. Eingangswandler

### 7.1 Allgemeine Schnittstelle

Jeder Eingang wird auf einen begrenzten Zellstrom abgebildet:

```text
I_i,ein = G_s(S_i − S_0)
```

`S_i` ist das lokale Sensorsignal, `S_0` dessen Referenz und `G_s` die
programmierbare Eingangsempfindlichkeit. Der Eingangspfad muss bipolar wirken
können, auch wenn die Versorgung unipolar ist. Dies gelingt durch differentielle
Strompfade um einen Biasstrom.

### 7.2 Geeignete Sensoren

Für erste Demonstratoren eignen sich:

- Fotodioden oder LED-/Fototransistorfelder,
- Druck- und Dehnungssensoren,
- Mikrofon- oder Ultraschallkanäle,
- Hall-Sensoren,
- künstlich erzeugte Spannungs- und Strommuster aus einem DAC-Array.

Für den reinen Schaltungsnachweis ist ein DAC-Array vorzuziehen. Es erzeugt
definierte, wiederholbare Eingangsmuster und trennt Feldfehler von
Sensorabweichungen. Die Sensorintegration folgt erst nach erfolgreicher
Grundvalidierung.

### 7.3 Eingangsbegrenzung

Der maximale Eingangsstrom muss so begrenzt werden, dass eine einzelne Zelle das
Array nicht dauerhaft in die Schutzbegrenzung zwingt. Übersteuerung wird als
eigener Messzustand markiert. Dadurch kann zwischen regulärer Feldbildung und
einem Fehlerfall unterschieden werden.

## 8. Auslesearchitektur

### 8.1 Vollständige Feldkarte

Für Forschung und Kalibrierung muss jede Zellspannung auslesbar sein. Ein
Analogmultiplexer verbindet die Zellen nacheinander mit einem ADC. Ein
Sample-and-Hold ist erforderlich, wenn die Feldform während der vollständigen
Abtastung eingefroren werden soll.

Alternativ kann die zeitliche Entwicklung kontinuierlich fortlaufen. Dann müssen
Abtastreihenfolge und Zeitstempel bei der Rekonstruktion berücksichtigt werden.

### 8.2 Analoge Merkmalsausgabe

Für einen späteren energieeffizienten Betrieb müssen nicht zwingend alle
Zellwerte digitalisiert werden. Analoge Summiernetze können beispielsweise
folgende Größen erzeugen:

```text
M_0 = Σ_i u_i
M_x = Σ_i x_i·u_i
M_y = Σ_i y_i·u_i
E_2 = Σ_i (u_i−r_i)²
```

Damit lassen sich Gesamtauslenkung, Schwerpunkt, Richtung und Feldenergie
abschätzen. Weitere Ausgänge können Gradienten, Symmetrie, lokale Maxima oder
zeitliche Änderungsraten erfassen.

### 8.3 Digitale Auslese

Für den Demonstrator ist ein ADC mit mindestens zwölf nominellen Bit sinnvoll.
Entscheidend ist jedoch nicht die Nennbitzahl, sondern die effektive Zahl
rauscharmer Bits im vollständigen Signalpfad. Die Messsoftware speichert:

- Rohwerte jeder Zelle,
- Zeitstempel,
- Konfigurationsparameter,
- Temperatur,
- Grenz- und Übersteuerungsflags,
- Referenz- und Kalibrierdaten.

## 9. Digitale Steuer- und Kalibrierschicht

Die digitale Elektronik führt keine vollständige Feldsimulation aus. Sie
übernimmt ausschließlich Konfiguration, Ablaufsteuerung, Auslese und Diagnose.

Erforderliche Register sind:

- Eingangsempfindlichkeit pro Kanal oder Kanalgruppe,
- Kopplungsstufe,
- Rückführungsparameter `k_1`, `k_2`, `k_3`,
- Übergangsbreite `w`,
- Referenzwert `r_i`,
- Auslesemodus und Abtastrate,
- Kalibriertrimmwerte,
- Schutz- und Fehlergrenzen.

Ein Mikrocontroller oder FPGA reicht für den ersten Demonstrator aus. Die
Regelung der schnellen Felddynamik bleibt analog; andernfalls würde das zentrale
Prinzip lediglich digital emuliert.

## 10. Vorgeschlagener Hardwaredemonstrator

### 10.1 Entwicklungsstufe A: Einzelzelle

Zunächst wird eine einzige Zelle aufgebaut. Zu prüfen sind:

- lineare Eingangsempfindlichkeit im inneren Bereich,
- Übergänge zwischen den drei Rückführungsregimen,
- Rückführungszeit nach einem Eingangspuls,
- Begrenzung nahe `−3` und `+3`,
- Rauschen, Offset und Temperaturdrift.

### 10.2 Entwicklungsstufe B: Gekoppelte Linie

Eine Linie aus vier bis acht Zellen prüft räumliche Ausbreitung und Stabilität.
Ein lokaler Puls muss eine reproduzierbare Verteilung erzeugen, deren Breite und
Abklingzeit von Kopplung und Rückführung abhängen.

### 10.3 Entwicklungsstufe C: Zweidimensionales Array

Der erste vollständige Demonstrator umfasst `4×4` Zellen. Nach erfolgreichem
Nachweis folgt ein `8×8`-Array. Größere Arrays sind erst sinnvoll, wenn
Stabilität, Auslese und Kalibrierung beherrscht werden.

Empfohlene Ausgangsparameter für die Leiterplatte:

| Parameter | Startbereich | Zweck |
|---|---:|---|
| Versorgung | 3,3 V oder 5 V | kompatibel mit Mess- und Steuertechnik |
| Gleichtaktwert | halbe Versorgung | symmetrische Auslenkung |
| Zustandskapazität | 10 nF…1 µF | gut messbare Felddynamik |
| Kopplungswiderstand | 100 kΩ…10 MΩ | einstellbare räumliche Zeitkonstante |
| Rückführungszeit | 1 ms…1 s | sichtbare und messbare Relaxation |
| Arraygröße | 4×4, danach 8×8 | schrittweise Komplexität |
| ADC | nominell mindestens 12 Bit | Rohfeldmessung und Kalibrierung |
| Temperaturmessung | mindestens ein Sensor je Platine | Driftzuordnung |

Diese Werte sind keine abschließenden Dimensionierungen. Sie müssen durch
SPICE-Simulation, verfügbare Operationsverstärker, Biasströme und gewünschte
Zeitkonstanten konkretisiert werden.

### 10.4 Funktionsblöcke der Demonstratorplatine

Die Platine umfasst:

1. Feldarray mit zugänglichen Testpunkten,
2. programmierbares Eingangsmuster aus DACs,
3. Analogmultiplexer und ADC,
4. Mikrocontroller oder FPGA,
5. Spannungsreferenz und rauscharme Versorgung,
6. Temperatur- und Strommessung,
7. USB- oder Ethernet-Schnittstelle,
8. Schutzschaltung und unabhängigen Abschaltpfad.

## 11. Simulations- und Entwurfsablauf

### 11.1 Mathematische Simulation

Vor dem Schaltungsaufbau wird ein `16×16`- oder `32×32`-Modell simuliert. Zu
variieren sind:

- Zwei-, Drei- und Vier-Regime-Kennlinien,
- vollständig glatte Rückführung ohne feste Zonen,
- Kopplungsstärke und Nachbarschaft,
- Rauschen und Offset,
- Bauteilstreuung,
- Eingangsamplitude und -geometrie,
- Rückführungspunkt,
- Randbedingungen.

### 11.2 SPICE-Simulation

Die Einzelzelle und anschließend kleine Zellverbände werden transistor- oder
operationsverstärkerbasiert simuliert. Erforderlich sind:

- DC-Arbeitspunktanalyse,
- AC- und Schleifenstabilitätsanalyse,
- Transientenanalyse,
- Rauschsimulation,
- Temperatur-Sweeps,
- Monte-Carlo-Analyse der Bauteilstreuung,
- Übersteuerungs- und Einschaltanalyse.

### 11.3 Übergang zur Leiterplatte

Erst wenn Einzelzelle und Viererzellenverband in SPICE stabil sind, wird die
Platine gefertigt. Testpunkte an jedem Zellknoten sind für die erste Version
wichtiger als maximale Packungsdichte.

## 12. Messplan und Falsifikationskriterien

### 12.1 Eingangsmuster

Mindestens folgende Muster werden verwendet:

- Einzelpunkt,
- Linie horizontal und vertikal,
- zwei getrennte Punkte,
- symmetrisches Kreuz,
- kontinuierlicher Gradient,
- wandernder Punkt,
- zufälliges Muster mit definierter Statistik,
- Übersteuerungsmuster.

### 12.2 Messgrößen

Zu erfassen sind:

- Feldkarte über der Zeit,
- Trennbarkeit verschiedener Eingangsmuster,
- Wiederholbarkeit gleicher Eingänge,
- räumliche Ausbreitungsbreite,
- Rückführungszeit und Restfehler,
- Häufigkeit und Dauer von Grenzverletzungen,
- Rauschleistung und effektive Auflösung,
- Temperatur- und Versorgungsempfindlichkeit,
- Energie pro Wahrnehmungsvorgang,
- Ausleselatenz und Datenmenge,
- Kalibrierungsaufwand.

### 12.3 Vergleichssysteme

Verbindliche Baselines sind:

- ungekoppeltes analoges Sensorarray,
- klassisches RC- oder Analogfilter,
- digitale Faltung beziehungsweise digitale Diffusion,
- einfaches lineares resistiv-kapazitives Netz ohne Drei-Regime-Rückführung.

Alle Systeme erhalten dieselben Eingangsmuster und werden anhand derselben
Ausgangsaufgabe bewertet.

### 12.4 Falsifikationskriterien

Die zentrale Hypothese gilt für die untersuchte Anwendung als nicht bestätigt,
wenn mindestens eine der folgenden Bedingungen dauerhaft eintritt:

- unterschiedliche Eingänge erzeugen keine statistisch trennbaren Feldformen,
- gleiche Eingänge sind außerhalb definierter Toleranzen nicht reproduzierbar,
- das Array wird unter zulässigen Eingängen instabil,
- die Rückführung erreicht den Referenzzustand nicht zuverlässig,
- Grenzverletzungen sind im normalen Betrieb nicht beherrschbar,
- eine einfachere Baseline erreicht gleiche oder bessere Ergebnisse bei
  geringerem Gesamtaufwand,
- Auslese und Kalibrierung verbrauchen den möglichen Energie- oder Latenzvorteil.

## 13. Übergang zu einem Mixed-Signal-Testchip

Ein integrierter Testchip ist erst nach erfolgreichem Leiterplattennachweis
sinnvoll. Eine erste ASIC-Version sollte gezielt klein bleiben, beispielsweise
`8×8` oder `16×16` Zellen.

### 13.1 Mögliche CMOS-Bausteine

- MOS-Kapazitäten oder Metallkondensatoren als Zustandskapazität,
- Transkonduktanzzellen für Nachbarschaftskopplung,
- programmierbare Biasströme für Rückführung und Eingang,
- Source-Follower oder gepufferte differentielle Auslese,
- spaltenparallele oder multiplexierte ADCs,
- digitale Register und Kalibrier-DACs.

### 13.2 Prozesswahl

Ein ausgereifter Mixed-Signal-CMOS-Prozess ist für den ersten Testchip
zweckmäßiger als ein hochmoderner Logikprozess. Größere Versorgungsspannungen,
gut charakterisierte Analogbauelemente und geringere Maskenkosten können für den
Funktionsnachweis wichtiger sein als maximale Transistordichte.

Die konkrete Prozesswahl erfordert PDK-Zugang, Foundry-Regeln, Kostenprüfung und
eine belastbare Zielgeschwindigkeit. Dieses Papier legt deshalb keinen Prozess
verbindlich fest.

### 13.3 Kalibrierung

Bauteilstreuung erzeugt Zelloffsets und unterschiedliche Zeitkonstanten. Ein
Testchip benötigt daher:

- Offsetmessung ohne Eingang,
- programmierbare Referenzkorrektur,
- Kopplungs- und Rückführungstrimmwerte,
- gespeicherte Kalibrierdaten außerhalb des eigentlichen Feldarrays,
- Diagnosemodi zum isolierten Anregen einzelner Zellen.

## 14. Energie, Fläche und Skalierung

Ein möglicher Effizienzvorteil entsteht nur, wenn die Feldbildung nützliche
Merkmale mit weniger Datenbewegung oder weniger sequentiellen Operationen
bereitstellt. Er ist nicht allein aus der analogen Arbeitsweise ableitbar.

Die Gesamtenergie umfasst:

```text
E_gesamt = E_eingang
           + E_feld
           + E_stabilisierung
           + E_auslese
           + E_ADC
           + E_kalibrierung
           + E_digital
```

Mit wachsender Arraygröße steigen parasitäre Kapazitäten, Auslesezeit,
Kalibrierungsdaten und Fehlerwahrscheinlichkeit. Eine hierarchische Architektur
mit lokalen Feldblöcken und reduzierten Merkmalsausgängen kann günstiger sein
als ein einziges sehr großes vollständig ausgelesenes Array.

## 15. Technische Hauptrisiken

### 15.1 Rauschen und effektive Auflösung

Kontinuierliche Zustände sind störanfälliger als binäre Pegel. Der beanspruchte
Darstellungsgewinn besteht nur, wenn benachbarte Zustände zuverlässig
unterschieden werden können.

### 15.2 Bauteilstreuung und Drift

Offsets können scheinbare Feldmuster erzeugen. Kalibrierung, differentielle
Kodierung und Temperaturmessung sind deshalb Bestandteile der Architektur und
keine nachträglichen Ergänzungen.

### 15.3 Instabilität

Zu starke oder gerichtete Kopplungen können Schwingungen oder lokale Sättigung
verursachen. Der erste Demonstrator verwendet ausschließlich positive,
symmetrische und begrenzte Kopplung.

### 15.4 Ausleseaufwand

Eine vollständige hochauflösende Digitalisierung jeder Zelle kann den möglichen
Vorteil aufheben. Deshalb müssen vollständige Forschungsdiagnose und spätere
kompakte Merkmalsausgabe getrennt betrachtet werden.

### 15.5 Modellgrenze `±3`

Die Drei-Regime-Struktur ist eine prüfbare Entwurfsannahme. Ein Vergleich mit
zwei, vier und glatten Kennlinien entscheidet, ob sie für eine Zielaufgabe
tatsächlich das beste Verhältnis aus Informationsgehalt, Robustheit,
Energiebedarf und Kalibrierbarkeit bietet.

## 16. Abnahmekriterien des ersten Demonstrators

Der erste technische Meilenstein gilt als erreicht, wenn:

1. alle Zellen über den vorgesehenen Bereich steuerbar sind,
2. drei Rückführungsregime messtechnisch unterscheidbar sind,
3. mindestens fünf Eingangsmuster statistisch trennbare Feldformen erzeugen,
4. Wiederholungen innerhalb einer vorab festgelegten Toleranz liegen,
5. das Feld nach Entfernen des Eingangs zuverlässig zurückkehrt,
6. zulässige Eingänge keine dauerhafte Grenzverletzung erzeugen,
7. Temperatur-, Rausch- und Streuungseinflüsse dokumentiert sind,
8. ein vollständiger Vergleich mit mindestens zwei Baselines vorliegt.

Diese Kriterien belegen noch keinen industriellen Vorteil. Sie zeigen lediglich,
dass die konstruktive Grundidee technisch funktionsfähig und weiter
untersuchbar ist.

## 17. Entwicklungsfahrplan

### Phase 1: Mathematisches Referenzmodell

Implementierung des Feldmodells, Stabilitätsanalyse und Vergleich der
Rückführungskennlinien.

### Phase 2: SPICE-Einzelzelle

Schaltungsentwurf, Parameter-Sweeps, Rausch- und Monte-Carlo-Analyse.

### Phase 3: Diskrete Einzelzelle und Zelllinie

Messung der Rückführung, Begrenzung, Kopplung und Temperaturabhängigkeit.

### Phase 4: `4×4`-Demonstrator

Vollständige Feldkarten, definierte Eingangsmuster und Baselinevergleich.

### Phase 5: `8×8`-Demonstrator mit Sensor

Integration genau einer Zielanwendung, beispielsweise optische Kontrastfelder
oder eine taktile Fläche.

### Phase 6: Mixed-Signal-Testchip

Erst nach erfolgreichem End-to-End-Nachweis: Prozesswahl, Transistorentwurf,
Layout, Extraktion und Fertigung.

## 18. Schlussfolgerung

Ein feldbasierter Wahrnehmungschip ist mit bekannten Schaltungsprinzipien als
Forschungsdemonstrator konstruierbar. Die technisch konservativste Umsetzung
ist ein gekoppeltes resistiv-kapazitives Mixed-Signal-Array mit differentieller
Zustandskodierung, programmierbarer Rückführung, weicher Begrenzung und
vollständiger Diagnoseauslese.

Die Feldform entsteht durch gleichzeitige physikalische Wechselwirkung der
Zellen. Sie wird nicht als fertige Lösung digital vorausberechnet. Der
Arbeitsbereich `−3…+3` beschreibt einen normierten Funktionsraum mit drei
Regimen pro Polarität; seine Eignung muss gegenüber einfacheren und komplexeren
Kennlinien gemessen werden.

Der nächste belastbare Schritt ist keine vollständige Chipfertigung, sondern
eine Kombination aus mathematischem Modell, SPICE-validierter Einzelzelle und
einem kleinen Leiterplattenarray. Erst reproduzierbare Messdaten können zeigen,
ob die Architektur für eine konkrete Sensoraufgabe einen Vorteil gegenüber
klassischer Analog- oder Digitalverarbeitung besitzt.

## Literatur und technische Berührungspunkte

1. L. O. Chua und L. Yang, „Cellular Neural Networks: Theory“, *IEEE
   Transactions on Circuits and Systems*, 35(10), 1257–1272, 1988.
   DOI: https://doi.org/10.1109/31.7600
2. T. Asai, „Analog reaction-diffusion chip and its application“, *Oyo Buturi*,
   72(10), 1286–1290, 2003. DOI: https://doi.org/10.11470/oubutsu.72.10_1286
3. P. Lichtsteiner, C. Posch und T. Delbrück, „A 128×128 120 dB 15 µs Latency
   Asynchronous Temporal Contrast Vision Sensor“, *IEEE Journal of Solid-State
   Circuits*, 43(2), 566–576, 2008.
   DOI: https://doi.org/10.1109/JSSC.2007.914337
4. H. Jang et al., „In-sensor optoelectronic computing using electrostatically
   doped silicon“, *Nature Electronics*, 5, 519–525, 2022.
   DOI: https://doi.org/10.1038/s41928-022-00819-6
5. W. Moy et al., „A 1,968-node coupled ring oscillator circuit for
   combinatorial optimization problem solving“, *Nature Electronics*, 5,
   310–317, 2022. DOI: https://doi.org/10.1038/s41928-022-00749-3

---

## Aussagegrenze

Dieses Dokument beschreibt eine hypothetische, technisch prüfbare
Spezialarchitektur. Es dokumentiert keine fertige Hardware, keine nachgewiesene
Energieeinsparung, keine allgemeine Überlegenheit gegenüber Digitaltechnik und
keine über die technischen Messgrößen hinausgehenden Eigenschaften. Sämtliche
Vorteile sind als Messhypothesen zu behandeln.
