# Reference-band thresholds (v4 presets)

Climate-normalised reference bands inspired by NatHERS. Each cell lists the baseline / competent / excellent reference-design values for that site.
Bands: 1 = below baseline; 2 = baseline to competent; 3 = competent to excellent; 4 = at or beyond excellent.
Recompute with `python site_model.py && python band_thresholds.py` whenever any course constant changes.

| Indicator | S1 Cool-temperate inland suburban | S2 Hot-arid rural-residential | S3 Humid subtropical townhouse | S4 Mediterranean suburban | S5 Tropical wet-dry rural-residential |
|---|---|---|---|---|---|
| Water closure | 65 % / 81 % / 94 % | 78 % / 89 % / 97 % | 68 % / 84 % / 96 % | 42 % / 59 % / 72 % | 73 % / 79 % / 83 % |
| Garden water satisfaction (shown beside water closure) | 0.0 % / 15 % / 20 % | 1.0 % / 12 % / 16 % | 15 % / 72 % / 81 % | 0.0 % / 23 % / 27 % | 23 % / 29 % / 31 % |
| Food energy closure | 1.0 % / 3.3 % / 5.5 % | 0.2 % / 1.6 % / 2.9 % | 1.2 % / 3.9 % / 6.1 % | 1.1 % / 3.7 % / 5.9 % | 4.8 % / 10 % / 15 % |
| Protein closure | 1.6 % / 5.5 % / 8.9 % | 0.2 % / 2.8 % / 4.9 % | 1.8 % / 6.4 % / 9.9 % | 1.6 % / 6.1 % / 9.6 % | 7.4 % / 16 % / 25 % |
| Nutrient closure | 4.0 % / 10 % / 14 % | 1.0 % / 4.0 % / 6.0 % | 3.0 % / 8.0 % / 10 % | 3.0 % / 9.0 % / 12 % | 13 % / 21 % / 27 % |

Ceiling note: no indicator's excellent reference value reaches 100 % under this recipe, so band 4 is open at every site.

Rounding: bands are evaluated against the model's unrounded reference values. The percentages above are a rounded display of those values, not the thresholds themselves.

Not banded: waste-stream recovery (assessed from submitted mass balances against the rubric), hard constraints (pass/fail).

## Reference designs (identical recipe at every site)

| Parameter | Baseline | Competent | Excellent |
|---|---|---|---|
| Domestic demand (L/person/day) | 150 | 150 | 130 |
| Composting toilet | False | True | True |
| Share of greywater reused | 0.0 | 0.5 | 0.9 |
| Share of growable area in production | 0.5 | 0.8 | 1.0 |
| Yield vs reference (1,500 kcal/m²/yr) | 0.8 | 1.0 | 1.2 |
| Share of excreted N recovered | 0.3 | 0.6 | 0.8 |
| Aquaponic grow bed (m²) | 0 | 4 | 8 |
| Added roof catchment (share of roof) | 0.0 | 0.0 | 0.05 |
| New storage spend ($) | 3000 | 3500 | 4000 |
