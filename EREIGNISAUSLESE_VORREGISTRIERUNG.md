# Vorregistrierung: ereignisbasierte zeitliche Auslese

## Ausgangspunkt und Ziel

Räumliche Kopplung lieferte keinen Vorteil. Mehrere lokale Zeitskalen und
lokale begrenzte Adaptation ergaben höchstens kleine, nicht bestätigte
Hinweise. Dieser Versuch verändert deshalb nicht erneut die lokale Dynamik. Er
prüft, ob die bisherige Mittelwert-/Steigungs-Auslese zeitliche Information aus
dem unveränderten Feldverlauf verliert.

Der Lauf ist explorativ und kann höchstens eine Auslesevariante für einen
späteren unabhängigen Bestätigungslauf bestimmen.

## Eingefrorene Felddynamik

Für alle Vergleiche wird ausschließlich das ungekoppelte Ein-Zustands-Modell
mit konstanter Rückführung `1,6` verwendet:

`dx/dt = g·Eingang − 1,6(x−r) − Softbegrenzung + Rauschen`.

Arbeitsbereich `−3…+3`, Eingangsverstärkung, Streuung, Rauschen und
Softbegrenzung bleiben unverändert. Dieselben erzeugten Feldverläufe werden
allen Ausleseverfahren übergeben. Ein möglicher Unterschied kann damit nicht
aus einer anderen Zustandsdynamik stammen.

## Gemeinsame acht Momentankanäle

Jeder Zeitschritt wird zunächst mit der bestehenden kompakten Auslese auf acht
Kanäle abgebildet: Mittelwert, Betragsmittel, zwei Schwerpunktkoordinaten, zwei
räumliche Ausdehnungen sowie positiver und negativer Spitzenwert.

Für Ausleseverfahren mit fester relativer Skalierung werden diese Kanäle durch
die vorab festgelegten Beträge `3, 3, 1, 1, 1, 1, 3, 3` geteilt und auf
`−1…+1` begrenzt. Diese Normierung verwendet keine Trainings- oder Testdaten.

## Zwei Pflichtkontrollen

Beide Kontrollen liefern genau `16` Werte:

1. **Bisherige Auslese:** Mittelwert und lineare Steigung jedes der acht
   unnormierten Momentankanäle.
2. **Normierungskontrolle:** Mittelwert und lineare Steigung jedes der acht
   fest normierten Momentankanäle.

Ein Ereigniskandidat muss beide Kontrollen schlagen. Dadurch kann eine bloße
Wirkung der festen Kanalnormierung nicht als Ereignisvorteil gelten.

## Ereignisbildung

Für jeden normierten Momentankanal wird eine symmetrische Delta-Modulation mit
internem Referenzwert `q` verwendet. Startwert ist `q=0`. Pro Zeitschritt gilt:

- steigt der Kanal um mindestens die Schwelle `θ` über `q`, werden entsprechend
  viele positive Ereignisse erzeugt,
- fällt er um mindestens `θ` unter `q`, werden entsprechend viele negative
  Ereignisse erzeugt,
- `q` wird um die Anzahl der Ereignisse mal `θ` nachgeführt.

Positive und negative Ereignisse werden getrennt mit
`z(t+dt)=exp(−λ_e·dt)z(t)+n(t)` akkumuliert. Die acht positiven und acht
negativen Endwerte ergeben wiederum genau `16` externe Werte. Die mittlere
Ereignisanzahl wird nur als Aktivitätsproxy berichtet, nicht als Energieangabe.

## Kandidatenraum

Es werden genau `12` Ereignisvarianten geprüft:

- relative Ereignisschwelle `θ`: `0,05`, `0,10`, `0,20`,
- Leckrate `λ_e`: `0`, `0,8`, `1,6`, `3,2`.

`λ_e=0` ist eine Ereigniszählkontrolle ohne zeitliche Abwertung. Nach dem Lauf
werden keine Schwellen oder Leckraten ergänzt.

## Aufgaben und Zufallsbedingungen

Unverändert wiederverwendet werden:

1. die zehn Kontinuitätsklassen,
2. die zehn Zeitskalenklassen,
3. die zehn Adaptationsklassen.

Weitere Bedingungen:

- neue Seeds `503`, `541`, `577`,
- Rauschstufen `0,15`, `0,35`, `0,55`,
- `12` Trainings- und `24` Testsequenzen je Klasse,
- identische Eingänge, Feldverläufe und Zufallsbedingungen für alle Auslesen,
- Nächste-Zentroid-Auswertung ohne zusätzliches trainiertes Modell.

## Technische Gültigkeit

Vor der Aufgabenbewertung wird durch Tests festgehalten:

- jede Auslese liefert deterministisch genau `16` endliche Werte,
- ein Nullverlauf erzeugt keine Ereignisse,
- ein konstanter Verlauf erzeugt nach der anfänglichen Quantisierung keine
  fortlaufenden zusätzlichen Ereignisse,
- alle `12` Parameterkombinationen sind eindeutig.

## Explorative Auswahlregel

Für jeden Ereigniskandidaten werden gepaarte Genauigkeitsdifferenzen zu beiden
Pflichtkontrollen über drei Aufgaben, drei Seeds und drei Rauschstufen
berechnet.

Höchstens ein Kandidat wird ausgewählt. Er muss gegenüber **jeder** Kontrolle:

1. im Gesamtmittel mehr als `2,0` Prozentpunkte erreichen,
2. auf keiner Aufgabe im Mittel unter der Kontrolle liegen,
3. bei keiner Rauschstufe im Mittel unter der Kontrolle liegen.

Rangmaß ist der kleinere der beiden Gesamtvorteile. Differenzen gelten nach
Rundung auf `12` Dezimalstellen als gleich. Danach folgen geringere mittlere
Ereignisaktivität, höhere Schwelle, niedrigere Leckrate und schließlich der
Modellname.

Approximative 95-%-Intervalle werden für beide Kontrollvergleiche berichtet,
sind in dieser Exploration aber kein Bestätigungsnachweis. Erfüllt kein Modell
alle Bedingungen, endet der Mechanismus ohne Kandidaten.

## Aussagegrenze

Der Versuch bewertet eine mathematische Auslese unter festgelegter
Ausgabebandbreite. Er bewertet keine konkrete Ereignisschaltung, elektrische
Energie, Datenübertragung, Chipfläche oder Fertigbarkeit.
