"""Publishable band thresholds for the v4 presets: the three reference designs per site.
Band 1 = below baseline, 2 = baseline to competent, 3 = competent to excellent, 4 = at or beyond excellent."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "output", "calibration.json"), encoding="utf-8"))
v4 = next(v for k, v in d.items() if k.startswith("v4"))
BANDED = [("water_closure", "Water closure"), ("garden_water_satisfaction", "Garden water satisfaction (shown beside water closure)"),
          ("food_kcal_closure", "Food energy closure"), ("protein_closure", "Protein closure"), ("nutrient_closure", "Nutrient closure")]
sids = ["S1", "S2", "S3", "S4", "S5"]
pct = lambda x: f"{x*100:.1f} %" if x < 0.1 else f"{x*100:.0f} %"
lines = ["# Reference-band thresholds (v4 presets)", "",
         "Climate-normalised reference bands inspired by NatHERS. Each cell lists the baseline / competent / excellent reference-design values for that site.",
         "Bands: 1 = below baseline; 2 = baseline to competent; 3 = competent to excellent; 4 = at or beyond excellent.",
         "Recompute with `python site_model.py && python band_thresholds.py` whenever any course constant changes.", ""]
lines += ["| Indicator | " + " | ".join(f"{s} {v4[s]['label']}" for s in sids) + " |", "|---|" + "---|" * len(sids)]
for key, label in BANDED:
    lines.append(f"| {label} | " + " | ".join(" / ".join(pct(v4[s]['levels'][l][key]) for l in ("baseline", "competent", "excellent")) for s in sids) + " |")
ceiling = [f"{s} {label}" for key, label in BANDED for s in sids if v4[s]['levels']['excellent'][key] >= 0.999]
lines += ["", ("Ceiling note: no indicator's excellent reference value reaches 100 % under this recipe, so band 4 is open at every site."
               if not ceiling else "Ceiling note: the excellent value already reaches 100 % for " + "; ".join(ceiling)
               + ", so band 4 there means reaching 100 % and band 3 cannot be exceeded."), "",
          "Rounding: bands are evaluated against the model's unrounded reference values. The percentages above are a rounded display of those values, not the thresholds themselves.", "",
          "Not banded: waste-stream recovery (assessed from submitted mass balances against the rubric), hard constraints (pass/fail).", "",
          "## Reference designs (identical recipe at every site)", "",
          "| Parameter | Baseline | Competent | Excellent |", "|---|---|---|---|"]
import site_model as sm
labels = {"demand": "Domestic demand (L/person/day)", "composting_toilet": "Composting toilet", "greywater": "Share of greywater reused",
          "production": "Share of growable area in production", "yield_mult": "Yield vs reference (1,500 kcal/m²/yr)",
          "n_recovery": "Share of excreted N recovered", "aquaponic_m2": "Aquaponic grow bed (m²)",
          "extra_catchment": "Added roof catchment (share of roof)", "storage_budget": "New storage spend ($)"}
for k, lab in labels.items():
    lines.append(f"| {lab} | " + " | ".join(str(sm.LEVELS[l][k]) for l in ("baseline", "competent", "excellent")) + " |")
open(os.path.join(HERE, "output", "band-thresholds.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
sys.stdout.reconfigure(encoding="utf-8"); print("\n".join(lines))
