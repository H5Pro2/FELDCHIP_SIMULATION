# Vorregistrierung: technische Rückführungsprüfung

## Prüfziel

Gesucht wird ein Parameterbereich, in dem ausgelenkte `4×4`-Zustände
zuverlässig, dauerhaft und numerisch stabil zum individuellen Referenzfeld
zurückkehren. Die Prüfung verwendet keine Klassifikationsaufgabe und keine
Kennzahl aus den bisherigen Muster- oder Sequenzversuchen.

Der Versuch wird erst nach einem Commit dieser Vorregistrierung und des
zugehörigen Ausführungscodes gestartet.

## Rückkehrdefinition

Für jede Anfangsauslenkung wird der RMS-Abstand zum individuellen Referenzfeld
gemessen. Eine Rückkehr gilt nur dann als erfolgreich, wenn

- der RMS-Abstand höchstens `0,05` beträgt und
- dieser Zustand während der letzten `0,50` Sekunden des Laufs nicht wieder
  verlassen wird.

Ein kurzzeitiger Eintritt in die Toleranz zählt nicht als dauerhafte Rückkehr.
Die Einschwingzeit ist der Beginn des letzten ununterbrochenen
Toleranzabschnitts.

## Anfangsauslenkungen

Es werden genau `18` deterministische Abweichungsfelder geprüft:

- homogene Auslenkung mit beiden Vorzeichen und den Beträgen `0,5`, `1,5`,
  `2,5` und `3,0`,
- Mittelpunktimpuls und Randimpuls mit beiden Vorzeichen und Betrag `3,0`,
- Schachbrettmuster mit beiden Polaritäten und Betrag `3,0`,
- horizontaler und vertikaler Gradient in beiden Richtungen bis `±3,0`.

Die Anfangszustände werden als Abweichung vom jeweiligen Referenzfeld gebildet
und anschließend ausschließlich auf den Arbeitsbereich `−3…+3` begrenzt.

## Streuungsecken und Seeds

| Ecke | Referenzoffset σ | Zellstreuung σ | dynamisches Rauschen σ |
|---|---:|---:|---:|
| nominal | `0,04` | `0,08` | `0,035` |
| erhöht | `0,08` | `0,16` | `0,070` |

Beide Ecken verwenden die Seeds `11`, `23`, `37`, `53`, `71`. Ein Lauf dauert
`6,0` normierte Sekunden bei `dt = 0,02`.

## Vorab festgelegter Parameterraum

Geprüft werden drei Rückführungskennlinien:

1. konstant mit Verstärkung `0,15`, `0,4`, `0,8`, `1,2` oder `1,6`,
2. dreistufig mit innerer Verstärkung `0,15`, `0,4` oder `0,8`, äußerer
   Verstärkung `1,0` oder `1,6` und Grenzskalierung `0,75` oder `1,0`,
3. geglättet mit denselben inneren und äußeren Werten, denselben Grenzlagen und
   einer festen Übergangsbreite von `0,12`.

Die mittlere Stufe liegt arithmetisch zwischen innerer und äußerer Verstärkung.
Bei Grenzskalierung `1,0` liegen die Übergänge bei Betrag `1` und `2`; bei
`0,75` bei `0,75` und `1,5`.

Jede Kennlinie wird ungekoppelt und mit Kopplungsstärke `0,34` geprüft. Für die
gekoppelte Form werden zwei Gleichungen getrennt verglichen:

- Laplace-Kopplung des Absolutzustands,
- Laplace-Kopplung der Abweichung vom Referenzfeld.

Bei Kopplungsstärke null sind beide Formulierungen identisch und werden nur
einmal gerechnet. Der Sweep enthält damit genau `87` Parameterkandidaten und
`870` Kandidat-Ecke-Seed-Kombinationen.

## Technische Messgrößen

- dauerhafte Rückkehrrate,
- 95-%-Quantil der Einschwingzeit,
- 95-%-Quantil des RMS-Restfehlers,
- Anteil der Verläufe mit erneutem Toleranzverlassen,
- versuchte Grenzüberschreitungen,
- maximaler beobachteter Zustandsbetrag.

## Zulassungskriterium

Ein Kandidat ist für die anschließende Zeitschrittprüfung nur zulässig, wenn in
jeder der zehn Ecke-Seed-Kombinationen alle Bedingungen erfüllt sind:

1. dauerhafte Rückkehrrate `100 %`,
2. 95-%-Quantil der Einschwingzeit höchstens `5,0` Sekunden,
3. 95-%-Quantil des Restfehlers höchstens `0,05`,
4. kein erneutes Verlassen der Toleranz nach dem ersten Toleranzeintritt,
5. keine versuchte Grenzüberschreitung.

## Auswahl und numerische Bestätigung

Zulässige Kandidaten werden lexikografisch geordnet nach

1. kleinster schlechtester 95-%-Einschwingzeit,
2. kleinstem schlechtesten 95-%-Restfehler,
3. geringster Rückführungsverstärkung,
4. geringerer Modellkomplexität.

Genau die ersten drei Kandidaten werden ohne dynamisches Rauschen nochmals mit
`dt = 0,02` und `dt = 0,01` geprüft. Die technische Zulassung wird nur
bestätigt, wenn die dauerhafte Rückkehrrate gleich bleibt, die 95-%-
Einschwingzeiten höchstens `0,10` Sekunden und die 95-%-Restfehler höchstens
`0,005` voneinander abweichen.

Falls kein Kandidat sämtliche Bedingungen erfüllt, wird die Rückführungsprüfung
als negativ abgeschlossen. Grenzwerte oder Rangfolge werden nach dem Lauf nicht
verändert.

## Aussagegrenze

Eine erfolgreiche Rückführung wäre nur ein technischer Eignungsnachweis im
dimensionslosen Modell. Sie belegt weder einen Verarbeitungsvorteil noch
elektrische Stabilität, Energiebedarf oder Fertigbarkeit einer Schaltung.
