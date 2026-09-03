# Forschungsplan

## Zweck

Der nächste Forschungsabschnitt soll erklären, warum das aktuelle gekoppelte
Feldmodell bei vollständiger Auslese hinter der Rohsignal-Baseline liegt und ob
es unter einer technisch begründeten Randbedingung dennoch einen messbaren
Nutzen besitzt.

Alle Aussagen bleiben auf die jeweils simulierte Aufgabe begrenzt.

## Ausgangsbefund

- Die vier Rückführungskennlinien erzeugen ähnliche Trennraten.
- Die beste Feldvariante liegt 5,4 Prozentpunkte hinter der Rohsignal-Baseline.
- Die aktuelle innere Rückführung erreicht den Referenzbereich zu langsam.
- Im regulären Lauf treten keine Grenzüberschreitungen auf.

## Nächster Versuch: Rückführung gegen Trennbarkeit

### Hypothese

Eine stärkere innere Rückführung verkürzt die Rückkehrzeit, kann aber zugleich
die räumliche Trennbarkeit der Feldformen reduzieren.

### Vorab festgelegter Sweep

- innere Rückführungsstärke `k1`: `0,15`, `0,30`, `0,45`, `0,60`,
- Kopplungsstärke `d`: `0,15`, `0,30`, `0,45`,
- unveränderte Grenze: `−3…+3`,
- unveränderte sechs Eingangsmuster,
- unveränderte Rauschstufen und Seeds,
- identische Rohsignal-, RC- und ungekoppelte Baselines.

### Primäre Messgrößen

1. Mustertrennung bei mittlerer Rauschstufe,
2. Rückkehrerfolg innerhalb von fünf normierten Sekunden,
3. Wiederhol-RMSE,
4. Grenzverletzungsrate.

### Entscheidungskriterium

Eine Parametrierung ist nur dann ein Kandidat für den nächsten Schritt, wenn
sie mindestens `95 %` Rückkehrerfolg erreicht, keine reguläre Grenzverletzung
zeigt und ihre Mustertrennung nicht mehr als zwei Prozentpunkte unter dem
linearen RC-Netz liegt.

## Danach: kompakte Auslese

Nur wenn der Rückführungs-Sweep einen Kandidaten liefert, wird eine zweite
Aufgabe geprüft: vier fest definierte analoge Summenmerkmale statt der
vollständigen 16-Zell-Auslese. Diese Untersuchung testet die Hypothese, dass
eine Feldvorverarbeitung bei begrenzter Auslesebandbreite nützlich sein könnte.

Die Gewichte der vier Summenmerkmale werden vor dem Lauf festgelegt und nicht
anhand des Ergebnisses angepasst.

## Übergang zu SPICE

Eine SPICE-Einzelzelle ist erst begründet, wenn mindestens eine mathematische
Parametrierung gleichzeitig Rückkehr, Stabilität und eine klar benannte
Ausgangsaufgabe erfüllt. Bis dahin bleiben elektrische Energie, reale
Bauteilstreuung, Temperaturverhalten und Fertigbarkeit ungeprüft.
