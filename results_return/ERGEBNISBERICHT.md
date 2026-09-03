# Ergebnisbericht: technische Rückführungsprüfung

## Ergebnis

Von `87` Kandidaten erfüllen `10` die vorregistrierten Hauptkriterien.
Für die Zeitschrittprüfung wurden `3` Kandidaten ausgewählt; `3` erfüllen auch deren Kriterien.

Damit ist die technische Frage im Rahmen dieses Modells positiv beantwortet: Es existieren stabile und dauerhaft rückführbare Parameterkandidaten. Daraus folgt noch keine Auswahl für eine Verarbeitungsarchitektur.

## Bestätigte Kandidaten

| Kandidat | schlechteste t95 | schlechtester Restfehler | größte Δt95 | größte ΔRestfehler |
|---|---:|---:|---:|---:|
| `konstant_lo1.6_hi1.6_s1_k0.34_abweichung` | 2.726 s | 0.00618 | 0.030 s | 0.000028 |
| `konstant_lo1.6_hi1.6_s1_k0.34_absolut` | 2.866 s | 0.03455 | 0.037 s | 0.000003 |
| `konstant_lo1.6_hi1.6_s1_k0_abweichung` | 3.080 s | 0.00740 | 0.030 s | 0.000073 |

Der bestplatzierte Kandidat verwendet konstante Rückführung `1,6`, Kopplungsstärke `0,34` und koppelt die Abweichung vom Referenzfeld. Die ebenfalls bestätigte Absolutzustandskopplung besitzt mit `0,03455` einen deutlich größeren schlechtesten Restfehler als die Abweichungskopplung mit `0,00618`.

Vier nichtlineare Kandidaten erfüllen zwar die Hauptkriterien, erreichen wegen der vorregistrierten Rangfolge aber nicht die Zeitschrittprüfung. Dieser Sweep weist daher keinen technischen Vorteil der nichtlinearen Kennlinien nach.

## Reproduzierbarkeit

Zwei vollständige Ausführungen erzeugten die zentralen Dateien bitgenau identisch.

- `trials.csv`: SHA-256 `EDAB3553814FFC82982A0977953BC1CD6FEBD28ECE441CD30FFB7285C3D199A7`
- `dt_validation.csv`: SHA-256 `51FC6670CDF5D2CFBEE6AC8E8222B303197FCD7B8BDD993F2B3991A3814EE98D`
- `manifest.json`: SHA-256 `4497BA57825369B43679F7CB8552CBCAF6F8379008C1F0C8363F2AE025E2B90C`

## Aussagegrenze

Die Prüfung bewertet ausschließlich Rückkehr, Bereichseinhaltung und numerische Stabilität im dimensionslosen Modell. Sie belegt keinen Verarbeitungsvorteil und keine elektrische Realisierbarkeit.
