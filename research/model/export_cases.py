"""Export the five client cases and the design reference data the site renders.

Writes:
  src/data/homes.json    Release A: every home's dossier, plan geometry, areas,
                         client targets, decision ranges and the staff feasibility margin
  src/data/design.json   The course's design reference: end-use split, crop mixes,
                         module data, the retrofit price lines, rules and constants

Nothing here is typed into a page by hand: the site imports these files. Re-run after
any change to case.py or scenario.py.

Run:  python export_cases.py            (staff check included; takes a few minutes)
      python export_cases.py --fast     (reuses output/staff-check.json)
"""

import json
import math
import os
import sys

import site_model as sm
import reference_costs as rc
import scenario as sc
from case import HOMES, BY_SID, totals, TOL_ABS_M2, TOL_REL

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
STAFF_JSON = os.path.join(HERE, "output", "staff-check.json")

QUARTERS = [("January to March", ["Jan", "Feb", "Mar"]), ("April to June", ["Apr", "May", "Jun"]),
            ("July to September", ["Jul", "Aug", "Sep"]), ("October to December", ["Oct", "Nov", "Dec"])]
LOAD_KL = {"S2": 12, "S5": 15}
USE_LABEL = {"toilet": "toilet flushing", "laundry": "laundry", "shower": "showers and basins",
             "kitchen": "kitchen and drinking", "other": "other indoor uses", "garden": "garden irrigation"}


def bills(home, base) -> list:
    """Release A bills, from the existing condition in an average year."""
    m = {r["month"]: r for r in base["monthly"]}
    if home.mains:
        q = [(name, round(sum(m[x]["imported"] for x in months))) for name, months in QUARTERS]
        total = sum(v for _, v in q)
        return [
            {"text": f"Water: four quarterly bills totalling {total} kL, at ${sc.WATER_PRICE[home.sid]:.2f}/kL usage charge plus a fixed supply charge.",
             "status": "known", "quarters": [{"quarter": n, "kl": v} for n, v in q]},
            {"text": "Electricity: twelve monthly totals for the whole house. No circuit is metered separately.", "status": "known"},
        ]
    loads = []
    for x in sc.MONTHS:
        n = m[x]["imported"] / LOAD_KL[home.sid]
        loads.append({"month": x, "loads": round(n)})
    total_loads = max(1, round(base["imported_kl"] / LOAD_KL[home.sid]))
    price = sc.WATER_PRICE[home.sid] * LOAD_KL[home.sid]
    return [
        {"text": f"Carted water: {total_loads} invoices last year, each for {LOAD_KL[home.sid]} kL at ${price:,.0f} a load.",
         "status": "known", "loads": loads},
        {"text": "Electricity: twelve monthly totals for the whole house; the pumps are not metered separately.", "status": "known"},
    ]


def staff(fast: bool) -> dict:
    if fast and os.path.exists(STAFF_JSON):
        return json.load(open(STAFF_JSON, encoding="utf-8"))
    out = {}
    for h in HOMES:
        chk = sc.staff_check(h.sid)
        out[h.sid] = {
            "n_feasible": chk["n_feasible"], "n_pareto": chk["n_pareto"],
            "existing_targets": chk["existing_targets"],
            "cheapest": {k: chk["cheapest"][k] for k in ("choice", "capital", "energy_peak_declared", "peak_month",
                                                        "imported_kl", "running_year", "maintenance_h_year", "fresh_kg")},
            "cheapest_dry_targets": sc.meets_targets(h.sid, chk["cheapest_dry"]),
            "margin": chk["margin"],
        }
    with open(STAFF_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fast = "--fast" in sys.argv
    st = staff(fast)
    homes = []
    for h in HOMES:
        t = totals(h)
        base = sc.evaluate(h.sid, sc.existing_choice(h))
        p = h.presets
        zones = [z.as_dict() for z in h.zones]
        guttered_unconnected = [z for z in h.zones if z.gutter and not z.connected_now]
        margin = st[h.sid]["margin"]
        homes.append({
            "id": h.sid, "slug": h.slug, "short": h.short, "family": h.family, "household": h.household,
            "place": h.place, "dwelling": h.dwelling, "tenure": h.tenure,
            "station": p["station"], "climate_label": p["label"],
            "parcel_m2": h.parcel_m2, "mains": h.mains,
            "plan": {
                "extent": list(h.plan_extent),
                "cover": [r.as_dict() for r in h.cover],
                "roofover": [r.as_dict() for r in h.roofover],
                "circles": [c.as_dict() for c in h.circles],
                "zones": zones,
                "points": [x.as_dict() for x in h.points],
                "easements": h.easements,
            },
            "floor": {"extent": list(h.floor_extent), "rooms": [r.as_dict() for r in h.rooms],
                      "points": [x.as_dict() for x in h.floor_points]},
            "parcel": ({"extent": list(h.parcel["extent"]), "working_area": list(h.parcel["working_area"]),
                        "features": h.parcel["features"], "road": h.parcel["road"], "note": h.parcel["note"]}
                       if h.parcel else None),
            "scheme": h.scheme or None,
            "areas": {**t, "preset_roof_m2": p["roof_m2"], "preset_growable_m2": p["growable_m2"],
                      "preset_plot_m2": p["plot_m2"], "shared_allocation_m2": h.shared_allocation_m2,
                      "tolerance_abs_m2": TOL_ABS_M2, "tolerance_rel": TOL_REL},
            "dossier": {
                "slope": {"text": h.slope.text, "status": h.slope.status},
                "services": [{"service": s, "text": f.text, "status": f.status} for s, f in h.services],
                "inventory": [{"text": f.text, "status": f.status} for f in h.inventory],
                "bills": bills(h, base),
                "observations": h.observations,
                "priorities": h.priorities,
                "constraints": [{"text": f.text, "status": f.status} for f in h.constraints],
                "unknowns": h.unknowns,
                "permitted_uses": [USE_LABEL[u] for u in h.permitted_tank_uses],
                "existing_uses": [USE_LABEL[u] for u in h.existing_tank_uses],
                "bore_allocation_kl": p["other_water_kl_year"],
                "maintenance_h_week": h.maintenance_h_week,
                "min_attendance_days": h.min_attendance_days,
                "unattended_days": h.unattended_days,
                "existing_irrigated_m2": h.existing_irrigated_m2,
            },
            "targets": [{"id": x["id"], "text": x["text"]} for x in sc.TARGETS[h.sid]],
            "existing_meets": st[h.sid]["existing_targets"],
            "decision_ranges": {
                "new_storage_kl": sc.STORAGE_STEPS[h.sid],
                "storage_kind": h.storage_kind,
                "max_new_storage_kl": h.max_new_storage_kl,
                "connectable_zones": [z.id for z in guttered_unconnected],
                "added_area_max_m2": round(sc.added_capacity(h)),
                "retained_within_envelope_m2": h.retained_within_envelope_m2,
            },
            "feasibility": {
                # Rounded DOWN so the published margin is never more generous than the check.
                "budget_margin_at_least": int(math.floor(margin["budget"] / 500.0) * 500),
                "energy_margin_at_least": math.floor(margin["energy"] * 2) / 2,
                "dry_year_all_targets": all(st[h.sid]["cheapest_dry_targets"].values()),
            },
        })

    design = {
        "end_uses": [{"use": u, "label": USE_LABEL[u], "l_person_day": v} for u, v in sc.END_USES.items()],
        "greywater_uses": list(sc.GREYWATER_USES),
        "efficiency": sc.EFFICIENCY,
        "dormant_below_c": sc.DORMANT_BELOW_C,
        "crop_mixes": [{"key": k, **v} for k, v in sc.CROP_MIXES.items()],
        "existing_planting": sc.EXISTING_PLANTING,
        "kwh_per_kl": sc.KWH_PER_KL,
        "tariff_kwh": sc.TARIFF_KWH,
        "water_price": {h.sid: sc.WATER_PRICE[h.sid] for h in HOMES},
        "modules": [{"key": k, "label": v["label"], "capital": sum(sc.PRICE[c] * n for c, n in v["capital"]),
                     "kwh_steady": v["kwh"][0], "kwh_upper": v["kwh"][1],
                     "heat_below_c": v.get("heat_below_c"), "heat_kwh_per_k": v.get("heat_kwh_per_k"),
                     "hours_year": v["hours"], "attendance_days": v["attendance"], "pausable": v["pausable"],
                     "tolerance_days": v.get("tolerance"), "consumables_year": v["consumables"]}
                    for k, v in sc.MODULES.items()],
        "extra_schedule": [{"key": k, "price": v[0], "basis": v[1], "description": v[2]} for k, v in sc.EXTRA_SCHEDULE.items()],
        "strategies": sc.STRATEGIES,
        "schedules": sc.SCHEDULES,
        "hydraulics": {"outlet_head_m": sc.OUTLET_HEAD_M, "friction_allowance": sc.FRICTION_ALLOWANCE,
                       "pump_efficiency": sc.PUMP_EFFICIENCY},
        "food_n_kg_year": 2.3,
        "household_n_kg_year": round(sm.HOUSEHOLD_N_KG_YEAR, 1),
        "n_uptake_g_m2_year": round(sm.GARDEN_N_CAPACITY_KG_M2 * 1000),
    }
    for name, obj in (("homes.json", {"generated_by": "research/model/export_cases.py", "homes": homes}),
                      ("design.json", {"generated_by": "research/model/export_cases.py", **design})):
        with open(os.path.join(REPO, "src", "data", name), "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=1)
            f.write("\n")
    for x in homes:
        print(f"{x['id']} {x['short']:13} margin >= ${x['feasibility']['budget_margin_at_least']:,} and "
              f">= {x['feasibility']['energy_margin_at_least']} kWh/d; existing meets {x['existing_meets']}")


if __name__ == "__main__":
    main()
