"""Stress-test the per-site band scoring method under parameter uncertainty.

For each perturbation, recompute the v4 presets and report, per stream, where the
'competent' reference design lands inside each site's baseline->excellent band.
If band scoring is fair, a competent design should land in a similar place at every site
and the ordering of sites should not flip wildly between perturbations."""

import copy
import json
import os
import sys

import site_model as sm
from presets import V4

HERE = os.path.dirname(os.path.abspath(__file__))
# garden_water_satisfaction was added 2026-09-18: it is published beside water closure,
# so the stability claim has to cover it rather than being extended to it by assumption.
STREAMS = ["water_closure", "garden_water_satisfaction", "food_kcal_closure",
           "protein_closure", "nutrient_closure"]
PERTURB = {
    "central": {},
    "yield -33%": {"YREF_KCAL_M2_YEAR": 1000},
    "yield +33%": {"YREF_KCAL_M2_YEAR": 2000},
    "demand 120 L/p/d": {"_demand": 120},
    "demand 180 L/p/d": {"_demand": 180},
    "runoff A 0.85": {"RUNOFF_A": 0.85},
    "Kc 0.85": {"KC_MIXED_GARDEN": 0.85},
    "Kc 1.05": {"KC_MIXED_GARDEN": 1.05},
    "FCR 1.5": {"FCR": 1.5},
    "FCR 2.5": {"FCR": 2.5},
    "tank $200/kL": {"TANK_COST_PER_KL": 200},
}


def run_once(changes):
    saved = {k: getattr(sm, k) for k in changes if not k.startswith("_")}
    levels_saved = copy.deepcopy(sm.LEVELS)
    for k, v in changes.items():
        if k == "_demand":
            for name in sm.LEVELS:
                sm.LEVELS[name]["demand"] = v if name != "excellent" else v - 20
        else:
            setattr(sm, k, v)
    clim = sm.load_climate()
    sites = [copy.deepcopy(s) for s in V4]
    for s in sites:
        sm.evaluate(s, clim)
    out = {}
    for s in sites:
        rel = {}
        for k in STREAMS:
            b, c, e = (s.levels[l][k] for l in ("baseline", "competent", "excellent"))
            rel[k] = None if e - b < 1e-6 else round((c - b) / (e - b), 2)
        out[s.sid] = {"band_width": {k: round(s.levels["excellent"][k] - s.levels["baseline"][k], 3) for k in STREAMS},
                      "competent_position": rel,
                      "competent_raw": {k: s.levels["competent"][k] for k in STREAMS},
                      "peak_kwh_excellent": s.levels["excellent"]["peak_energy_kwh_day"]}
    for k, v in saved.items():
        setattr(sm, k, v)
    sm.LEVELS.clear(); sm.LEVELS.update(levels_saved)
    return out


def main():
    results = {name: run_once(ch) for name, ch in PERTURB.items()}
    with open(os.path.join(HERE, "output", "sensitivity.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
    lines = ["# Sensitivity of per-site band scoring (v4 presets)", "",
             "Cell = where the *competent* reference design sits inside that site's baseline→excellent band "
             "(0 = baseline, 1 = excellent). Fair band scoring should give similar positions across sites.", ""]
    sids = list(results["central"])
    for stream in STREAMS:
        lines += [f"## {stream}", "", "| Perturbation | " + " | ".join(sids) + " | spread |", "|---|" + "---|" * (len(sids) + 1)]
        for name, res in results.items():
            vals = [res[s]["competent_position"][stream] for s in sids]
            nums = [v for v in vals if v is not None]
            spread = round(max(nums) - min(nums), 2) if nums else None
            lines.append(f"| {name} | " + " | ".join(str(v) for v in vals) + f" | {spread} |")
        lines.append("")
    lines += ["## Band widths (excellent − baseline), central case", "", "| Stream | " + " | ".join(sids) + " |", "|---|" + "---|" * len(sids)]
    for stream in STREAMS:
        lines.append(f"| {stream} | " + " | ".join(str(results['central'][s]['band_width'][stream]) for s in sids) + " |")
    lines += ["", "## Peak process energy of the excellent design (kWh/d)", "", "| Perturbation | " + " | ".join(sids) + " |", "|---|" + "---|" * len(sids)]
    for name, res in results.items():
        lines.append(f"| {name} | " + " | ".join(str(res[s]['peak_kwh_excellent']) for s in sids) + " |")
    with open(os.path.join(HERE, "output", "sensitivity.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
