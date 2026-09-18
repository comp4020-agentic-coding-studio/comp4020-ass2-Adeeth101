"""The published worked cross-site comparison.

One design idea, taken through all five sites: **spend more of the allowance on
rainwater storage.** Starting from the excellent reference design, new-storage
spend is stepped from $2,000 to $10,000 and everything downstream is recomputed —
capacity, the monthly tank balance, water closure, garden water satisfaction,
imports, overflow, and the full schedule cost including contingency.

It is the right idea to publish because the answer genuinely differs by site, and
because getting it wrong is what put the previous reference designs over budget.

Run:  python comparison.py   -> ../../src/data/comparison.json
"""

import json
import os
import sys
from copy import deepcopy

import site_model as sm
import reference_costs as rc
from presets import V4

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "src", "data", "comparison.json"))
STEPS = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
BASE = 4000  # the excellent reference design's setting


def main():
    clim = sm.load_climate()
    rows = {}
    for spend in STEPS:
        levels = deepcopy(sm.LEVELS)
        levels["excellent"]["storage_budget"] = spend
        costed, sites = rc.cost_all(V4, levels)
        for s in sites:
            lv = s.levels["excellent"]
            c = costed[s.sid]["excellent"]
            rows.setdefault(s.sid, []).append({
                "spend": spend,
                "storage_kl": lv["storage_kl"],
                "water_closure": lv["water_closure"],
                "garden_water_satisfaction": lv["garden_water_satisfaction"],
                "imported_kl": lv["imported_kl"],
                "overflow_kl": lv["overflow_kl"],
                "cost_total": c["total"],
                "headroom": c["headroom"],
                "fits": c["fits"],
            })

    summary = {}
    for sid, rs in rows.items():
        base = next(r for r in rs if r["spend"] == BASE)
        top = rs[-1]
        # The point at which another $1,000 of shell buys less than one point of
        # water closure: where the design stops being worth more money.
        knee = None
        for a, b in zip(rs, rs[1:]):
            if b["water_closure"] - a["water_closure"] < 0.01:
                knee = a["spend"]
                break
        last_fitting = max((r["spend"] for r in rs if r["fits"]), default=None)
        summary[sid] = {
            "base": base,
            "top": top,
            "gain_water_closure": round(top["water_closure"] - base["water_closure"], 3),
            "gain_garden": round(top["garden_water_satisfaction"] - base["garden_water_satisfaction"], 3),
            "extra_cost": top["cost_total"] - base["cost_total"],
            "saturates_at": knee,
            "largest_affordable_spend": last_fitting,
        }

    labels = {s.sid: s.label for s in V4}
    payload = {
        "question": (
            "Starting from the excellent reference design, what does another dollar of "
            "rainwater storage actually buy at each site?"
        ),
        "method": (
            "New-storage spend is stepped from $2,000 to $10,000 at $130/kL for the shell. "
            "Each step re-runs the monthly tank balance with a three-year spin-up and "
            "re-prices the whole bill of materials from the course schedule, including the "
            "required 10 % contingency and the per-tank establishment charge, which steps "
            "up every 25 kL."
        ),
        "base_spend": BASE,
        "steps": STEPS,
        "labels": labels,
        "rows": rows,
        "summary": summary,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1)
        f.write("\n")
    return payload


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = main()
    print(f"wrote {OUT}")
    for sid, s in p["summary"].items():
        print(f"  {sid}: +{s['gain_water_closure']:.3f} water closure and "
              f"+{s['gain_garden']:.3f} garden for ${s['extra_cost']:,} more; "
              f"saturates at ${s['saturates_at']}; largest affordable ${s['largest_affordable_spend']}")
