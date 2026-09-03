# Forschungsplan

## Zweck

Der nächste Forschungsabschnitt prüft, ob die gekoppelte Feldbildung erst dann
einen messbaren Nutzen zeigt, wenn nicht sämtliche 16 Zellwerte ausgelesen
werden. Der bestehende Vollfeldbefund bleibt unverändert dokumentiert.

Alle Aussagen bleiben auf die jeweils simulierte Aufgabe begrenzt.

## Ausgangsbefund

- Die vier Rückführungskennlinien erzeugen nahezu gleiche Trennraten.
- Die beste Feldvariante liegt 5,4 Prozentpunkte hinter der Rohsignal-Baseline.
- Die aktuelle innere Rückführung erreicht den Referenzbereich zu langsam.
- Im regulären Lauf treten keine Grenzüberschreitungen auf.

Die Regimezahl wird deshalb im nächsten Versuch nicht optimiert. Die langsame
Rückkehr wird als separater Parameterbefund geführt und nicht mit der
Mustertrennung vermischt.

## Abgeschlossener Versuch: kompakte Auslese

### Hypothese

Geprüft wurde, ob eine gekoppelte Feldvorverarbeitung bei begrenzter
Auslesebandbreite nützlicher ist als bei vollständiger Digitalisierung aller 16
Zellwerte.

### Vorab festgelegte Merkmale

Jedes `4×4`-Feld wird auf genau acht Skalare reduziert:

1. vorzeichenbehafteter Mittelwert,
2. mittlerer Betrag als Aktivitätsmaß,
3. horizontaler Betragsschwerpunkt,
4. vertikaler Betragsschwerpunkt,
5. horizontale räumliche Ausdehnung,
6. vertikale räumliche Ausdehnung,
7. positiver Spitzenwert,
8. Betrag des negativen Spitzenwerts.

Die Definitionen werden identisch auf alle Feldmodelle und Baselines angewendet.
Sie werden nach dem Lauf nicht verändert.

### Konstant gehalten

- Arbeitsbereich `−3…+3`,
- sämtliche Modellparameter und Kennlinien,
- sechs Eingangsmuster,
- drei Rauschstufen,
- fünf Seeds,
- Trainings- und Teststichproben,
- Nächste-Zentroid-Auswertung.

### Primäre Messgröße

Mittlere Mustertrennung über alle Seeds und Rauschstufen. Zusätzlich werden
Trennverhältnis und Wiederhol-RMSE berichtet.

### Entscheidungskriterium

Ein Nutzen der Feldbildung ist in dieser Aufgabe nur dann vorläufig sichtbar,
wenn die beste Feldvariante die beste identisch ausgelesene Baseline um mehr als
zwei Prozentpunkte übertrifft. Andernfalls bleibt der Nutzen nicht nachgewiesen.

Der beobachtete Vorsprung von `0,8` Prozentpunkten und das gepaarte Intervall von
`−0,8` bis `+2,3` Prozentpunkten erfüllen das Entscheidungskriterium nicht.

## Abgeschlossener Hauptversuch: zeitlich-räumliche Dynamik

Die Forschungsfrage wird auf wandernde, überlagerte, zeitlich integrierte und
kurze Eingangsmuster mit Nachlauf verschoben. Sequenzen, gemeinsame Auslese und
Erfolgskriterium stehen vor Ausführung in `TEMPORALER_VERSUCHSPLAN.md`.

Der unveränderte Lauf ergab `85,3 %` für die beste Feldvariante und `89,7 %`
für die beste Baseline. Die gepaarte Differenz von `−4,5` Prozentpunkten mit
einem approximativen 95-%-Intervall von `−5,5` bis `−3,5` Prozentpunkten
verfehlt beide Erfolgskriterien. In dieser Aufgabe ist ein Nutzen des
zeitlichen Zustands sichtbar, aber kein zusätzlicher Nutzen der räumlichen
Kopplung.

## Separater Rückführungsversuch

Die Rückführung wird unabhängig von der Sequenztrennung isoliert untersucht.
Dabei werden keine Musterkennzahlen zur Auswahl der Parameter verwendet.
Primäre Größe ist der Anteil der Zustände, die innerhalb der festgelegten Zeit
zum Referenzbereich zurückkehren.

## Übergang zu SPICE

Eine SPICE-Einzelzelle ist erst begründet, wenn mindestens eine mathematische
Aufgabe einen klaren, reproduzierbaren Kandidaten liefert. Bis dahin bleiben
elektrische Energie, reale Bauteilstreuung, Temperaturverhalten und
Fertigbarkeit ungeprüft.
