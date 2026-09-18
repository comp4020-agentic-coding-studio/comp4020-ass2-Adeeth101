"""The Wattle Street practice house: every worked optimisation example, on separate numbers.

The five client homes are assessed, so the teaching material must not solve them. This
module defines a sixth, clearly fictional practice case with ROUND-NUMBER practice
climate data (invented, not any real station), runs it through the same scenario
engine the staff check uses, and exports everything a tutorial needs: the monthly
balance, a storage-yield curve, a sixteen-option scenario grid with dominance marked,
the critical-flow and pump-head example, the peak-month energy example, and the
sensitivity cases. Students may copy these methods; the numbers transfer to nothing.

Run:  python practice.py   -> ../../src/data/practice.json and ../../public/data/practice/*.csv
"""

import csv
import json
import os
import sys

import site_model as sm
import scenario as sc
from case import Home, Rect, Circle, Zone, Point, Fact, BY_SID, E, totals

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_JSON = os.path.join(REPO, "src", "data", "practice.json")
OUT_DIR = os.path.join(REPO, "public", "data", "practice")

# Invented practice climate for "Wattle Flat". Round numbers so every step can be done
# by hand. NOT a Bureau of Meteorology station and not any of the five client climates.
RAIN = [40, 40, 50, 50, 60, 60, 60, 60, 50, 50, 40, 40]
ETO = [180, 150, 120, 80, 50, 40, 40, 60, 80, 120, 150, 170]
TMEAN = [22, 22, 19, 15, 12, 9, 8, 9, 12, 15, 18, 21]
DRY_FACTOR = 0.6

PRACTICE = Home(
    sid="P0", slug="wattle-street", short="Wattle Street", family="Practice",
    household="a practice household of two adults and two children, on the course's demand convention",
    place="Wattle Flat (invented practice town)",
    dwelling="Single-storey house with a garden shed",
    tenure="Practice case. No body corporate.",
    parcel_m2=648, plan_extent=(18.0, 36.0),
    cover=[
        Rect("B1", 2.0, 6.0, 12.0, 14.0, "House", "building", "", E(0.5)),
        Rect("B2", 12.5, 28.0, 4.0, 5.0, "Shed", "building", "", E(0.25)),
        Rect("H1", 14.5, 0.0, 3.5, 20.0, "Driveway", "hardstand", ""),
        Rect("H2", 2.0, 20.0, 12.0, 2.5, "Terrace", "hardstand", ""),
        Rect("G1", 1.0, 24.0, 10.0, 10.0, "Back beds", "growing", "the existing 30 m² of beds are here"),
        Rect("G2", 0.0, 0.0, 14.5, 5.5, "Front garden", "growing", ""),
        Rect("G3", 14.5, 20.0, 3.5, 8.0, "East strip", "growing", ""),
    ],
    roofover=[],
    circles=[Circle("T1", 12.0, 26.5, 0.9, "Existing 5 kL tank", "tank", "shed roof, gravity tap", kl=5)],
    zones=[
        Zone("R1", "House, north plane", (1.5, 13.0, 13.0, 7.5), [(1.5, 20.5), (14.5, 20.5)], False),
        Zone("R2", "House, south plane", (1.5, 5.5, 13.0, 7.5), [(1.5, 5.5), (14.5, 5.5)], False),
        Zone("R3", "Shed", (12.25, 27.75, 4.5, 5.5), [(12.25, 27.75)], True),
    ],
    points=[Point("P1", 14.2, 0.4, "Water meter", "service"),
            Point("L1", 9.0, 0.5, "RL 100.0", "level", "estimate"),
            Point("L2", 9.0, 35.5, "RL 100.8", "level", "estimate")],
    easements=[],
    floor_extent=(12.0, 14.0),
    rooms=[Rect("F1", 0, 0, 12.0, 14.0, "House", "room")],
    floor_points=[],
    slope=Fact("Falls about 0.8 m to the street.", "estimate"),
    services=[], inventory=[], observations=[], priorities=[], constraints=[], unknowns=[],
    permitted_tank_uses=("toilet", "laundry", "garden"),
    max_new_storage_kl=15.0,
    maintenance_h_week=3.0, min_attendance_days=2, unattended_days=14,
    existing_irrigated_m2=30.0, existing_irrigation="tank_gravity",
    priority_zones=(("G1", 30.0),),
    zone_quality={"G1": 1.0, "G2": 0.75, "G3": 0.8},
    priority_perennial_share=0.3,
    mains=True,
)
PRACTICE.presets = {"plot_m2": 648, "growable_m2": 208, "roof_m2": 220, "shared_growing_m2": 0,
                    "existing_storage_kl": 5, "other_water_kl_year": 0, "station": "practice",
                    "label": "Practice case"}
BY_SID["P0"] = PRACTICE
sc.WATER_PRICE["P0"] = 3.30

TARGETS = [
    dict(id="PT1", text="The existing 30 m² of beds fully watered from on-site water in every month of the average year",
         test=lambda r: r["priority_months_full"] == 12 and r["garden_mains_kl"] == 0),
    dict(id="PT2", text="Toilet and laundry supplied at least 70 % from rainwater over the year",
         test=lambda r: sc._share(r, sc.MONTHS, "toilet_laundry_tank", "toilet_laundry") >= 0.70),
]


def climate(dry: bool = False) -> sc.Climate:
    f = DRY_FACTOR if dry else 1.0
    cl = sc.Climate("practice dry year" if dry else "practice average year", sc.MONTHS[:], sm.DAYS[:],
                    [r * f for r in RAIN], [e * (1.05 if dry else 1.0) for e in ETO], TMEAN[:],
                    [t - 7 for t in TMEAN])
    cl.gfac = [sm.growing_factor(t, 0) for t in TMEAN]
    return cl


def ev(ch, dry=False, **kw):
    return sc.evaluate("P0", ch, climate(dry), spin_climate=climate(False), **kw)


def monthly_table(r):
    return [{k: (round(v, 2) if isinstance(v, float) else v) for k, v in m.items()
             if k in ("month", "rain", "eto", "inflow", "overflow", "indoor", "tank_indoor", "imported",
                      "garden_gross", "garden_tank", "garden_mains", "garden_unmet", "tank_end",
                      "toilet_laundry", "toilet_laundry_tank", "energy_declared")} for m in r["monthly"]]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    t = totals(PRACTICE)
    cl = climate()
    out = {"label": "PRACTICE CASE. Invented round-number data for teaching; not a client home and not a real climate.",
           "home": {"slug": PRACTICE.slug, "areas": t, "zones": [z.as_dict() for z in PRACTICE.zones],
                    "cover": [r.as_dict() for r in PRACTICE.cover], "circles": [c.as_dict() for c in PRACTICE.circles],
                    "points": [p.as_dict() for p in PRACTICE.points], "extent": PRACTICE.plan_extent},
           "climate": {"months": sc.MONTHS, "rain": RAIN, "eto": ETO, "tmean": TMEAN,
                       "pe": [round(x, 1) for x in cl.pe], "gfac": [round(g, 2) for g in cl.gfac],
                       "dry_factor": DRY_FACTOR},
           "targets": [{"id": x["id"], "text": x["text"]} for x in TARGETS]}

    # 1. Roof runoff by zone and month (enHealth App. B, after Martin 1980) [S08]
    runoff = {z.id: [round(sm.RUNOFF_A * max(0.0, p - sm.RUNOFF_B_MM_MONTH) * z.plan_m2 / 1000, 2) for p in RAIN]
              for z in PRACTICE.zones}
    out["runoff"] = {"by_zone": runoff, "annual": {k: round(sum(v), 1) for k, v in runoff.items()}}

    # 2. Existing condition
    base = ev(sc.existing_choice(PRACTICE))
    out["existing"] = {k: base[k] for k in ("imported_kl", "garden_mains_kl", "priority_months_full", "running_year",
                                            "capital", "energy_peak_declared", "fresh_kg")}
    out["existing"]["monthly"] = monthly_table(base)

    # 3. The sixteen-option grid. Every option drips the existing beds from the tank.
    grid = []
    for kl in (5, 10, 15, 20):
        for zones in (("R3", "R1"), ("R3", "R1", "R2")):
            for strat, sched in (("garden", "year_round"), ("indoor", "garden_first")):
                ch = sc.Choice(new_storage_kl=kl, zones=zones, strategy=strat, schedule=sched)
                r = ev(ch)
                d = ev(ch, dry=True)
                meets = {x["id"]: bool(x["test"](r)) for x in TARGETS}
                grid.append({
                    "id": f"O{len(grid) + 1}", "new_storage_kl": kl, "zones": "+".join(sorted(zones)),
                    "roof_m2": r["roof_connected_m2"], "strategy": strat, "schedule": sched,
                    "capital": r["capital"], "running_year": r["running_year"],
                    "imported_kl": r["imported_kl"], "priority_months_full": r["priority_months_full"],
                    "toilet_laundry_share": round(sc._share(r, sc.MONTHS, "toilet_laundry_tank", "toilet_laundry"), 2),
                    "energy_peak": r["energy_peak_declared"], "peak_month": r["peak_month"],
                    "dry_priority_months_full": d["priority_months_full"], "dry_imported_kl": d["imported_kl"],
                    "meets": meets, "feasible": all(meets.values()) and r["fits_budget"] and r["fits_energy"],
                    "bill": r["bill"], "capital_subtotal": r["capital_subtotal"],
                    "capital_contingency": r["capital_contingency"],
                })
    objectives = [("capital", -1), ("running_year", -1), ("imported_kl", -1), ("priority_months_full", 1),
                  ("dry_priority_months_full", 1)]
    for g in grid:
        g["dominated_by"] = [o["id"] for o in grid if o is not g
                             and all((o[k] - g[k]) * s >= -1e-9 for k, s in objectives)
                             and any((o[k] - g[k]) * s > 1e-9 for k, s in objectives)]
    feas = sorted([g for g in grid if g["feasible"]], key=lambda g: (g["capital"], g["running_year"]))
    out["grid"] = grid
    out["grid_objectives"] = [k for k, _ in objectives]
    out["cheapest_feasible"] = feas[0]["id"] if feas else None
    # Three named alternatives for the worked comparison.
    non_dom = sorted([g for g in feas if not g["dominated_by"]], key=lambda g: g["capital"])
    alt = {"minimum": feas[0]["id"] if feas else None, "balanced": None, "resilience": None}
    if len(non_dom) >= 3:
        alt["resilience"] = max(non_dom, key=lambda g: (g["dry_priority_months_full"], -g["capital"]))["id"]
        mid = [g for g in non_dom if g["id"] not in (alt["minimum"], alt["resilience"])]
        alt["balanced"] = mid[len(mid) // 2]["id"] if mid else None
    out["alternatives"] = alt

    # 4. Storage-yield curve for the balanced connection (all zones, indoor strategy).
    curve = []
    for kl in (0, 2, 5, 8, 10, 12, 15, 20, 25, 30):
        r = ev(sc.Choice(new_storage_kl=kl, zones=("R1", "R2", "R3"), strategy="indoor"))
        curve.append({"new_storage_kl": kl, "total_kl": kl + 5, "imported_kl": r["imported_kl"],
                      "overflow_kl": r["overflow_kl"], "priority_months_full": r["priority_months_full"],
                      "toilet_laundry_share": round(sc._share(r, sc.MONTHS, "toilet_laundry_tank", "toilet_laundry"), 3),
                      "capital": r["capital"]})
    out["storage_curve"] = curve

    # 5. Critical service flow and pump head
    fixtures = {"toilet cistern refill": 7.0, "washing machine fill": 11.0, "garden drip zone": 6.0}
    design_flow = fixtures["toilet cistern refill"] + fixtures["washing machine fill"]
    hp = sc.head_and_power(static_lift_m=1.8, outlet="indoor", flow_lpm=design_flow)
    out["hydraulics"] = {"fixtures": fixtures, "design_flow_lpm": design_flow, "static_lift_m": 1.8, **hp,
                         "empirical_kwh_per_kl": sc.KWH_PER_KL["pressure"]}

    # 6. Peak-month energy for the balanced alternative, with modules added for the example
    ch = sc.Choice(new_storage_kl=10, zones=("R1", "R2", "R3"), strategy="indoor", modules=("compost", "insects"))
    r = ev(ch)
    out["energy_example"] = {"choice": ch.describe(), "peak_month": r["peak_month"],
                             "modelled": r["energy_peak_modelled"], "declared": r["energy_peak_declared"],
                             "monthly": [{"month": m["month"], "pump": round(m["e_pump"], 2), "modules": round(m["e_mod"], 2),
                                          "total": round(m["energy_declared"], 2)} for m in r["monthly"]]}

    # 7. Sensitivity of the cheapest feasible option
    if feas:
        g = feas[0]
        chosen = sc.Choice(new_storage_kl=g["new_storage_kl"], zones=tuple(g["zones"].split("+")),
                           strategy=g["strategy"], schedule=g["schedule"])
        cases = {}
        cases["central"] = ev(chosen)
        cases["demand +20 %"] = ev(chosen, demand_factor=[1.2] * 12)
        cases["demand −20 %"] = ev(chosen, demand_factor=[0.8] * 12)
        cases["dry year"] = ev(chosen, dry=True)
        sens = []
        for name, rr in cases.items():
            sens.append({"case": name, "imported_kl": rr["imported_kl"],
                         "priority_months_full": rr["priority_months_full"],
                         "toilet_laundry_share": round(sc._share(rr, sc.MONTHS, "toilet_laundry_tank", "toilet_laundry"), 2),
                         "running_year": rr["running_year"]})
        # price and yield sensitivities are arithmetic on the central case
        cen = cases["central"]
        sens.append({"case": "capital prices +20 %", "capital": round(cen["capital"] * 1.2)})
        sens.append({"case": "yield −30 %", "fresh_kg": round(cen["fresh_kg"] * 0.7)})
        out["sensitivity"] = {"option": g["id"], "rows": sens, "capital": cen["capital"], "fresh_kg": cen["fresh_kg"]}
        out["chosen_monthly"] = monthly_table(cen)
        out["chosen_dry_monthly"] = monthly_table(cases["dry year"])

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    os.makedirs(OUT_DIR, exist_ok=True)
    tag = "# PRACTICE CASE - invented round-number data for SLOP4761 tutorials; not a client home and not a real climate."
    with open(os.path.join(OUT_DIR, "PRACTICE-wattle-street-climate.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow([tag]); w.writerow(["month", "rain_mm", "eto_mm", "tmean_c", "effective_rain_mm"])
        for m in range(12):
            w.writerow([sc.MONTHS[m], RAIN[m], ETO[m], TMEAN[m], round(cl.pe[m], 1)])
    with open(os.path.join(OUT_DIR, "PRACTICE-wattle-street-grid.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow([tag])
        cols = ["id", "new_storage_kl", "zones", "roof_m2", "strategy", "schedule", "capital", "running_year", "imported_kl",
                "priority_months_full", "toilet_laundry_share", "energy_peak", "dry_priority_months_full", "dry_imported_kl"]
        w.writerow(cols + ["meets_PT1", "meets_PT2", "dominated_by"])
        for g in grid:
            w.writerow([g[c] for c in cols] + [g["meets"]["PT1"], g["meets"]["PT2"], " ".join(g["dominated_by"])])
    with open(os.path.join(OUT_DIR, "PRACTICE-wattle-street-balance.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow([tag])
        cols = ["month", "rain", "eto", "inflow", "overflow", "indoor", "tank_indoor", "imported", "garden_gross",
                "garden_tank", "garden_mains", "garden_unmet", "tank_end"]
        w.writerow(cols)
        for m in out.get("chosen_monthly", []):
            w.writerow([m.get(c) for c in cols])
    print(f"wrote {OUT_JSON}")
    for g in grid:
        print(f"  {g['id']:>3} +{g['new_storage_kl']:>2} kL {g['zones']:9} {g['strategy']:6} {g['schedule'][:6]:6} ${g['capital']:>6,} "
              f"run ${g['running_year']:>4} imp {g['imported_kl']:>6} prio {g['priority_months_full']:>2} "
              f"TL {g['toilet_laundry_share']:.2f} dry {g['dry_priority_months_full']:>2} "
              f"{'FEAS' if g['feasible'] else '    '} dom by {g['dominated_by']}")
    print("  alternatives", alt)


if __name__ == "__main__":
    main()
