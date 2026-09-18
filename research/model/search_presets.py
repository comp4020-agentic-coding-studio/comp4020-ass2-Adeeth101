"""Constrained search for a balanced preset set.

Each lever is only allowed to move inside a range that is ordinary for that kind of site
(ranges and their justification are in ../findings.md). Sites are
evaluated once per variant; combinations are then scored on the spread of the ease index,
dominance, and a small penalty for drifting from the typical value of each lever.
"""

import itertools
import json
import os
import sys

from site_model import Site, evaluate, load_climate, DIMENSIONS

HERE = os.path.dirname(os.path.abspath(__file__))
LEVEL = "competent"

# (sid, label, station, dwelling, plot, lever grid, typical values)
SPACE = {
    "S1": ("Cool-temperate inland suburban", "070014", "detached house + garage", 800,
           dict(growable_m2=[300, 375, 450], roof_m2=[250, 300], existing_storage_kl=[5, 22]),
           dict(growable_m2=350, roof_m2=260, existing_storage_kl=5)),
    "S2": ("Hot-arid rural-residential", "015590", "house + machinery shed", 20000,
           dict(growable_m2=[400, 600, 800], roof_m2=[350, 450], other_water_kl_year=[60, 100], existing_storage_kl=[22, 45]),
           dict(growable_m2=600, roof_m2=450, other_water_kl_year=100, existing_storage_kl=22)),
    "S3": ("Humid subtropical townhouse", "040214", "townhouse", 300,
           dict(growable_m2=[90], shared_growing_m2=[40, 70, 100], roof_m2=[150, 170], existing_storage_kl=[3, 10]),
           dict(growable_m2=90, shared_growing_m2=60, roof_m2=150, existing_storage_kl=3)),
    "S4": ("Mediterranean suburban", "023000", "detached house", 700,
           dict(growable_m2=[250, 300, 350], roof_m2=[230, 270], existing_storage_kl=[5]),
           dict(growable_m2=300, roof_m2=250, existing_storage_kl=5)),
    "S5": ("Tropical wet-dry rural-residential", "014015", "elevated house + shed", 10000,
           dict(growable_m2=[400, 500, 600], roof_m2=[300, 350], existing_storage_kl=[22, 45]),
           dict(growable_m2=600, roof_m2=350, existing_storage_kl=45)),
}


def variants(sid, spec, clim):
    label, station, dwelling, plot, grid, typical = spec
    keys = list(grid)
    out = []
    for combo in itertools.product(*(grid[k] for k in keys)):
        kw = dict(zip(keys, combo))
        s = Site(sid, label, station, dwelling, plot, kw.pop("growable_m2"), kw.pop("roof_m2"), **kw)
        evaluate(s, clim)
        drift = sum(abs(dict(zip(keys, combo))[k] - typical[k]) / (typical[k] or 1) for k in keys) / len(keys)
        out.append((s, dict(zip(keys, combo)), drift))
    return out


def score(combo):
    sites = [c[0] for c in combo]
    ease = {s.sid: 0.0 for s in sites}
    ranks = {s.sid: {} for s in sites}
    for key, _l, higher in DIMENSIONS:
        vals = [s.levels[LEVEL][key] for s in sites]
        mu = sum(vals) / len(vals)
        sd = (sum((v - mu) ** 2 for v in vals) / len(vals)) ** 0.5 or 1.0
        for s in sites:
            z = (s.levels[LEVEL][key] - mu) / sd
            ease[s.sid] += (z if higher else -z) / len(DIMENSIONS)
        for r, s in enumerate(sorted(sites, key=lambda x: x.levels[LEVEL][key], reverse=higher), 1):
            ranks[s.sid][key] = r
    dominated = sum(1 for a in sites for b in sites if a is not b
                    and all(ranks[a.sid][k] <= ranks[b.sid][k] for k, _, _ in DIMENSIONS))
    spread = max(ease.values()) - min(ease.values())
    drift = sum(c[2] for c in combo) / len(combo)
    return spread + dominated * 0.5 + 0.3 * drift, spread, dominated, drift, ease


def main():
    clim = load_climate()
    pools = [variants(sid, spec, clim) for sid, spec in SPACE.items()]
    best = []
    for combo in itertools.product(*pools):
        obj, spread, dom, drift, ease = score(combo)
        if len(best) < 10 or obj < best[-1][0]:
            best.append((obj, spread, dom, drift, ease, [c[1] for c in combo]))
            best.sort(key=lambda x: x[0])
            best = best[:10]
    result = [dict(objective=round(b[0], 3), ease_spread=round(b[1], 3), dominated_pairs=b[2], mean_drift=round(b[3], 3),
                   ease_index={k: round(v, 2) for k, v in b[4].items()},
                   levers=dict(zip(SPACE, b[5]))) for b in best]
    with open(os.path.join(HERE, "output", "search_results.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1)
    sys.stdout.reconfigure(encoding="utf-8")
    for r in result[:5]:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
