# Vorregistrierung: zeitlich-räumlicher Hauptversuch

## Forschungsfrage

Kann ein gekoppeltes `4×4`-Feld zeitlich-räumliche Eingangsdynamik unter einer
festen kompakten Auslese nützlicher verdichten als identisch ausgelesene
Baselines? Geprüft werden wandernde, überlagerte, zeitlich integrierte und kurze
Eingänge mit Nachlauf.

Der frühere statische Versuch ist abgeschlossen. Seine Ergebnisse und Parameter
werden durch diesen Versuch nicht nachträglich verändert.

## Vorab festgelegte Sequenzklassen

1. Einzelpunkt von links nach rechts,
2. Einzelpunkt von rechts nach links,
3. Einzelpunkt von oben nach unten,
4. Einzelpunkt von unten nach oben,
5. zwei sich kreuzende Pulse,
6. zwei sich zeitweise überlagernde Pulse,
7. zeitlich aufgebauter horizontaler Gradient,
8. zeitlich abgebauter horizontaler Gradient,
9. kurze Störung in der Feldmitte mit anschließender Nullphase,
10. kurze Störung am Feldrand mit anschließender Nullphase.

Jede Sequenz umfasst `80` Schritte mit `dt = 0,02`. Verstärkungsstreuung,
Offset, Ausfälle und dynamisches Rauschen werden mit festen Seeds erzeugt.

## Modelle und Baselines

Verglichen werden unverändert vier Feldkennlinien (`2`, `3`, `4` und glatt),
ein ungekoppeltes dynamisches Array, ein lineares RC-Diffusionsnetz, eine
digitale zeitlich-räumliche Diffusion mit 12-Bit-Quantisierung und das
unverarbeitete zeitliche Eingangssignal.

Die Modellparameter aus dem statischen Referenzversuch werden nicht anhand des
zeitlichen Ergebnisses optimiert.

## Gemeinsame Auslese

In jedem Zeitschritt werden für jedes Modell dieselben acht Merkmale gebildet:
vorzeichenbehafteter Mittelwert, mittlerer Betrag, zwei Betragsschwerpunkte,
zwei räumliche Ausdehnungen sowie positiver und negativer Spitzenbetrag.

Für jeden der acht Kanäle werden anschließend genau zwei zeitliche Größen
verwendet: Mittelwert und lineare Steigung. Damit besitzt jedes Modell dieselben
`16` Ausgabewerte pro Sequenz. Die Klassifikation erfolgt ausschließlich mit
einem Nächste-Zentroid-Auswerter.

## Stichprobe

- Rauschstufen: `0,15`, `0,35`, `0,55`
- Seeds: `11`, `23`, `37`, `53`, `71`
- Training: `12` Sequenzen je Klasse
- Test: `24` Sequenzen je Klasse

## Primäre Messgröße und Entscheidung

Primär ist die mittlere Klassifikationsrate über die `15` gepaarten
Seed-Rausch-Kombinationen. Für die jeweils beste Feldvariante und beste Baseline
wird die Differenz je Kombination gebildet.

Ein Vorteil gilt in dieser Simulation nur dann als vorläufig sichtbar, wenn

1. die mittlere Differenz größer als `2,0` Prozentpunkte ist und
2. die untere Grenze des approximativen gepaarten 95-%-Intervalls größer als
   null ist.

Werden nicht beide Bedingungen erfüllt, bleibt ein Vorteil nicht nachgewiesen.
Die Auswahl der jeweils besten Variante ist Teil dieses vorregistrierten
Kriteriums und wird als explorativer Auswahlanteil im Bericht kenntlich gemacht.

## Aussagegrenze

Der Versuch ist ein dimensionsloses mathematisches Referenzmodell. Er belegt
weder elektrische Energieeinsparung noch Fertigbarkeit. Ein positives Ergebnis
wäre nur die Begründung für weitere Schaltungs- und Hardwareuntersuchungen.

