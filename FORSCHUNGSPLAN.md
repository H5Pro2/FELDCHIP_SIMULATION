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

## Nächster Versuch: kompakte Auslese

### Hypothese

Eine gekoppelte Feldvorverarbeitung könnte bei begrenzter Auslesebandbreite
nützlicher sein als bei vollständiger Digitalisierung aller 16 Zellwerte.

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

## Separater Rückführungsversuch

Die Rückführung wird erst nach dem kompakten Auslesetest isoliert untersucht.
Dabei werden keine Musterkennzahlen zur Auswahl der Parameter verwendet.
Primäre Größe ist der Anteil der Zustände, die innerhalb der festgelegten Zeit
zum Referenzbereich zurückkehren.

## Späterer zeitlicher Versuch

Falls die kompakte statische Auslese keinen Nutzen zeigt, folgt eine getrennte
Aufgabe mit wandernden, überlagerten und zeitlich integrierten Eingangsmustern.
Versuchsablauf und Auswertung werden vor diesem Lauf neu festgelegt.

## Übergang zu SPICE

Eine SPICE-Einzelzelle ist erst begründet, wenn mindestens eine mathematische
Aufgabe einen klaren, reproduzierbaren Kandidaten liefert. Bis dahin bleiben
elektrische Energie, reale Bauteilstreuung, Temperaturverhalten und
Fertigbarkeit ungeprüft.
