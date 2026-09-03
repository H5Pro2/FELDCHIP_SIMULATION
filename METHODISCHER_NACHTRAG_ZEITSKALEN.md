# Methodischer Nachtrag: Gleichstandsbehandlung der Zeitskalen-Exploration

## Anlass

Die Vorregistrierung `f9aee95` legte bei gleicher mittlerer Differenz zur
Baseline als erste Tie-Break-Regel das kleinere Verhältnis
`λ_schnell/λ_langsam` fest. Eine numerische Präzision für den Begriff
„Gleichstand“ war dort nicht angegeben.

Nach dem ersten Ergebnislauf besaßen zwei Kandidaten dieselbe beobachtete
Gesamttrennrate von `0,7087962962962963`, ihre aus binären Fließkommazahlen
berechneten mittleren Vorteile unterschieden sich jedoch in der letzten
dargestellten Stelle:

- `zwei_zustaende_l1_s2_a0.5`: `0,02384259259259259`,
- `zwei_zustaende_l1.2_s2_a0.5`: `0,02384259259259258`.

Die Differenz von ungefähr `1×10⁻¹⁷` entspricht keiner unterscheidbaren
Trefferzahl und entstand ausschließlich durch Fließkommaarithmetik. Die
ursprüngliche Sortierung verwendete den ungerundeten Wert und hätte dadurch
zunächst `zwei_zustaende_l1_s2_a0.5` ausgewählt.

## Korrektur

Vor dem Ergebnis-Commit wurde die Auswahlregel so umgesetzt, dass die mittlere
Differenz für die Rangfolge auf `12` Dezimalstellen gerundet wird. Werte, die
danach gleich sind, gelten als Gleichstand. Anschließend greifen unverändert die
vorregistrierten Tie-Break-Regeln.

Damit wird wegen des kleineren Verhältnisses `λ_schnell/λ_langsam` von
`1,6667` statt `2,0` der Kandidat
`zwei_zustaende_l1.2_s2_a0.5` ausgewählt. Ein Regressionstest sichert diese
Auslegung ab.

## Umfang der Änderung

Die Änderung betrifft ausschließlich die Auswahl zwischen den beiden
gleichplatzierten Kandidaten und dadurch das Feld
`selected_confirmation_candidate` im Manifest. Unverändert blieben:

- Kandidatenraum und technische Zulassungsregeln,
- Eingangsdaten, Seeds, Rauschstufen und Aufgaben,
- sämtliche simulierten Zustände und Klassifikationsergebnisse,
- `technical_screen.csv`, `task_trials.csv` und `comparisons.csv`,
- Effektschätzungen und Intervalle beider Kandidaten.

Die unveränderten Prüfsummen lauten:

- `technical_screen.csv`: SHA-256 `900CDB777B30AA6BF082016AF12780DD1981715B15977F185C4B64C9AB2BE869`,
- `task_trials.csv`: SHA-256 `33476060BB46CCA24796BAC6DC050635A3C285D0BFCC85D4304FB518243ACF56`,
- `comparisons.csv`: SHA-256 `236C828AF266F82C1328D5A117582B7B04AD6C5117EC4BFD9106895BD93869D1`.

Das zunächst erzeugte, nicht veröffentlichte Manifest hatte SHA-256
`FB4ED0C0B8B28BA531717178018FF9F21BA88125CDBBBD4BDACFBFB55815A477`.
Das korrigierte und mit dem Ergebnis-Commit `43c1efb` veröffentlichte Manifest
hat SHA-256
`B57FDB0AB334730E723679C63C863C4D6E610B6BABC3F527FE687E64933142E9`.

## Einordnung

Die nachträgliche Präzisierung ist eine Abweichung von einer vollständig
spezifizierten Vorregistrierung und wird deshalb offengelegt. Sie verändert
weder Richtung noch Größe des explorativen Befunds. Der ausgewählte Kandidat
wird erst in einem neuen, vorab vollständig festgelegten Lauf mit frischen
Seeds bestätigend geprüft.

