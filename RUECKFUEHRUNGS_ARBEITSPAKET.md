# Technische Rückführungsuntersuchung

## Ziel

Dieses Arbeitspaket sucht unabhängig von jeder Klassifikationsaufgabe einen
Parameterbereich, in dem ein angeregtes `4×4`-Feld zuverlässig und schnell zum
individuellen Referenzzustand zurückkehrt.

Die Rückführung ist eine technische Pflichtprüfung. Solange kein belastbarer
Parameterbereich gefunden ist, wird keine untersuchte Dynamik als hinreichend
definierte Chipmethode behandelt.

## Trennung vom Hauptversuch

Parameter werden ausschließlich anhand technischer Rückführungsgrößen gewählt.
Klassifikationsraten, Trennverhältnisse oder Merkmale des zeitlichen
Hauptversuchs dürfen die Auswahl nicht beeinflussen.

## Geplanter Sweep

- innere und äußere Rückführungsverstärkung,
- Lage und Breite der Regimegrenzen,
- Kopplungsstärke,
- Zellstreuung und Referenzoffset,
- verschiedene Anfangsauslenkungen bis zum Grenzbereich `−3…+3`.

## Messgrößen

- Anteil der Läufe innerhalb der Rückkehrtoleranz,
- Zeit bis zum erstmaligen und dauerhaften Eintritt in die Toleranz,
- Restfehler nach fester Beobachtungszeit,
- Überschwingen und erneutes Verlassen der Toleranz,
- versuchte Grenzüberschreitungen,
- numerische Stabilität bei verkleinertem Zeitschritt.

Der konkrete Sweep und seine Grenzwerte sind vor seiner Ausführung in
`RUECKFUEHRUNG_VORREGISTRIERUNG.md` festgelegt. Ergebnisse dieses Arbeitspakets
dürfen nicht rückwirkend in den zeitlichen Hauptversuch eingesetzt werden.
