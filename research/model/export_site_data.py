"""Export everything the course website publishes as numbers into one JSON file.

The site imports `src/data/course-model.json` and renders from it. Nothing numeric is
retyped into a page, so a page cannot quietly disagree with the model that produced it.
Re-run this after any change to a course constant, a preset or the reference recipe.

Run:  python export_site_data.py
"""

import json
import os
import sys
from copy import deepcopy

import site_model as sm
import reference_costs as rc
from presets import V4

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "src", "data", "course-model.json")

BANDED = [
    ("water_closure", "Water closure",
     "On-site water used, divided by all water used including carted imports."),
    ("garden_water_satisfaction", "Garden water satisfaction",
     "The share of the garden's irrigation deficit actually met. Always published beside "
     "water closure, because a design can reach high water closure by leaving its garden dry."),
    ("food_kcal_closure", "Food energy closure",
     "Food energy produced and eaten, divided by the household's 40.0 MJ/day requirement."),
    ("protein_closure", "Protein closure",
     "Protein produced, divided by 185 g/day. Animal products count only in proportion to "
     "feed grown on site."),
    ("nutrient_closure", "Nutrient closure",
     "Nitrogen safely recovered and applied within crop uptake, divided by 13.6 kg N/year."),
]

SITE_NOTES = {
    "S1": {
        "short": "Canberra",
        "name": "Cool-temperate inland suburban",
        "place": "Canberra, ACT",
        "strengths": [
            "The most even rainfall of the five sites: 28 % of the year's rain falls in the "
            "driest four months, against 1.4 % at Darwin. Storage has less work to do.",
            "High winter chill, so temperate fruit and nut trees set crop without a low-chill "
            "cultivar list.",
            "Fewest days at or above 35 °C, so summer heat stress on the garden is the mildest "
            "of the set.",
        ],
        "constraints": [
            "92 days at or below 2 °C and the shortest growing season of the five.",
            "Fish and insects are thermally productive for roughly seven months without "
            "heating, and tank heating is the site's peak energy load.",
            "Below 20 °C mean, WHO dry-excreta storage runs 1.5 to 2 years rather than one, so "
            "the toilet needs about 75 % more chamber capacity than the warm sites.",
        ],
    },
    "S2": {
        "short": "Alice Springs",
        "name": "Hot-arid rural-residential",
        "place": "Alice Springs, NT",
        "strengths": [
            "Heat that does the work of machinery: hot composting and solar drying both run "
            "fast and for most of the year.",
            "A capped bore allocation of 100 kL/year, the only site with a water source that "
            "does not depend on the roof.",
            "Mushrooms are possible year round inside a humidified chamber, because the "
            "limiting factor is humidity rather than temperature.",
        ],
        "constraints": [
            "P/ETo of 0.16, the driest of the set, and about 1,650 mm/year of net irrigation "
            "demand per square metre of garden.",
            "90 days at or above 35 °C.",
            "The hardest food and nutrient closure of the five sites; water, not space, is what "
            "limits the garden.",
        ],
    },
    "S3": {
        "short": "Brisbane",
        "name": "Humid subtropical townhouse",
        "place": "Brisbane, Queensland",
        "strengths": [
            "Year-round growing and the highest rain-fed yield of the set, so irrigation does "
            "the least work here.",
            "Mild water temperatures suit both fish and insects without heating.",
        ],
        "constraints": [
            "130 m² of growing area in total, including the 40 m² shared strata garden: less "
            "than a third of the largest site.",
            "Strata and density rules govern odour, noise, shared property and neighbour "
            "amenity, none of which the model scores. Composting and insect rearing have to be "
            "designed around them.",
            "The garden can absorb only about 11 % of the household's excreted nitrogen, the "
            "lowest of the set, so surplus nutrient has to leave the site safely.",
            "High-intensity rainfall drives turbidity and first-flush load.",
        ],
    },
    "S4": {
        "short": "Adelaide",
        "name": "Mediterranean suburban",
        "place": "Adelaide, South Australia",
        "strengths": [
            "The mildest thermal regime of the five and the lowest process energy.",
            "A long, dry, warm autumn that suits preserving and fermentation.",
            "A trout and Murray cod rotation covers all twelve months.",
        ],
        "constraints": [
            "Winter rain against summer demand: the lowest water closure of the set, because "
            "the rain arrives when the garden does not need it.",
            "17 % of annual rain falls in the driest four months.",
        ],
    },
    "S5": {
        "short": "Darwin",
        "name": "Tropical wet-dry rural-residential",
        "place": "Darwin, Northern Territory",
        "strengths": [
            "The highest food, protein and nutrient potential of the five sites.",
            "Barramundi and insects are thermally productive all year without heating.",
        ],
        "constraints": [
            "1.4 % of annual rain falls in the driest four months. The reference designs still "
            "import water in the dry season while overflowing in the wet.",
            "The highest pumping energy of the set, and the dry season is when it peaks.",
        ],
    },
}


def main():
    costed, sites = rc.cost_all(V4, sm.LEVELS)
    energy = rc.energy_check(costed)
    by_sid = {s.sid: s for s in sites}
    sens = json.load(open(os.path.join(HERE, "output", "sensitivity.json"), encoding="utf-8"))

    spreads = {}
    for key, _, _ in BANDED:
        rows = []
        for name, res in sens.items():
            vals = [res[s]["competent_position"][key] for s in by_sid]
            vals = [v for v in vals if v is not None]
            if vals:
                rows.append({"perturbation": name, "spread": round(max(vals) - min(vals), 2)})
        rows.sort(key=lambda r: -r["spread"])
        spreads[key] = {"worst": rows[0], "second_worst": rows[1], "all": rows}

    data = {
        "generated_by": "research/model/export_site_data.py",
        "recipe_version": "v6",
        "preset_version": "v4",
        "household": {
            "occupants": "two adults and two children aged 9 to 13",
            "food_energy_mj_day": round(sm.HOUSEHOLD_MJ_PER_DAY, 1),
            "protein_g_day": 185,
            "domestic_water_l_person_day": sm.DOMESTIC_L_PP_D,
            "excreted_n_kg_year": round(sm.HOUSEHOLD_N_KG_YEAR, 1),
            "food_waste_kg_person_year": sm.HOUSEHOLD_FOOD_WASTE_KG_PP_YR,
            "garden_n_uptake_g_m2_year": round(sm.GARDEN_N_CAPACITY_KG_M2 * 1000),
        },
        "constraints": {
            "budget_aud": rc.BUDGET,
            "contingency": rc.CONTINGENCY,
            "energy_cap_kwh_day": rc.ENERGY_CAP_KWH_DAY,
            "uncertain_load_allowance_kwh_day": rc.UNCERTAIN_UPPER,
        },
        "indicators": [{"key": k, "name": n, "definition": d} for k, n, d in BANDED],
        "recipe": {lvl: sm.LEVELS[lvl] for lvl in rc.LVLS},
        "schedule": [
            {"key": k, "price": v, "basis": basis, "description": desc}
            for k, (v, basis, desc) in rc.SCHEDULE.items()
        ],
        "schedule_rules": {
            "max_tank_kl": rc.MAX_TANK_KL,
            "roof_per_downpipe_m2": rc.ROOF_PER_DOWNPIPE_M2,
            "extra_bed_aud": rc.EXTRA_BED,
            "not_in_reference": [rc.SCHEDULE[k][2] for k in rc.NOT_IN_REFERENCE],
            "unpriced": rc.UNPRICED,
        },
        "energy_boundary": {
            "modelled": [{"group": g, "load": l, "status": s} for g, l, s in rc.MODELLED_LOADS],
            "uncertain": [{"group": g, "load": l, "low": lo, "high": hi}
                          for g, l, lo, hi in rc.UNCERTAIN_LOADS],
            "optional": [{"group": g, "load": l, "low": lo, "high": hi}
                         for g, l, lo, hi in rc.OPTIONAL_LOADS],
        },
        "sensitivity": {
            "perturbations": list(sens.keys()),
            "spreads": spreads,
            "covers": [k for k, _, _ in BANDED],
        },
        "sites": [],
    }

    for sid in rc.SIDS:
        s, notes = by_sid[sid], SITE_NOTES[sid]
        d = s.derived
        data["sites"].append({
            "id": sid,
            "short": notes["short"],
            "name": notes["name"],
            "place": notes["place"],
            "station": s.station,
            "station_name": d["station_name"],
            "dwelling": s.dwelling,
            "plot_m2": s.plot_m2,
            "growable_m2": s.growable_m2,
            "shared_growing_m2": s.shared_growing_m2,
            "roof_m2": s.roof_m2,
            "existing_storage_kl": s.existing_storage_kl,
            "other_water_kl_year": s.other_water_kl_year,
            "strengths": notes["strengths"],
            "constraints": notes["constraints"],
            "climate": {
                "annual_rain_mm": d["annual_rain_mm"],
                "annual_eto_mm": d["annual_eto_mm"],
                "aridity_p_over_eto": d["aridity_P_over_ETo"],
                "driest_4_months_share": d["driest_4_months_share_of_rain"],
                "annual_tmean_c": d["annual_tmean_c"],
                "frost_days_le2c": d["frost_days_le2c"],
                "hot_days_ge35c": d["hot_days_ge35c"],
                "roof_runoff_kl": d["roof_runoff_kl"],
                "net_irrigation_mm_year": d["net_irrigation_mm_year"],
                "fish_best_rotation": d["fish_best_rotation"],
                "fish_rotation_months": d["fish_rotation_months"],
                "bsf_productive_factor": d["bsf_productive_factor"],
                "mushroom_months": d["mushroom_months"],
                "excreta_storage_years": d["excreta_storage_years_WHO"],
                "n_absorption_ratio": d["n_absorption_ratio_full_area"],
                "monthly": d["monthly"],
            },
            "bands": {
                key: {lvl: s.levels[lvl][key] for lvl in rc.LVLS} for key, _, _ in BANDED
            },
            "reference": {
                lvl: {
                    "cost_subtotal": costed[sid][lvl]["subtotal"],
                    "cost_contingency": costed[sid][lvl]["contingency"],
                    "cost_total": costed[sid][lvl]["total"],
                    "cost_headroom": costed[sid][lvl]["headroom"],
                    "fits_budget": costed[sid][lvl]["fits"],
                    "bill": [{"line": n, "qty": q, "unit": u, "cost": c}
                             for n, q, u, c in costed[sid][lvl]["rows"]],
                    "energy_modelled_kwh_day": energy[sid][lvl]["modelled_kwh_day"],
                    "energy_declared_kwh_day": energy[sid][lvl]["declared_peak_kwh_day"],
                    "energy_headroom_kwh_day": energy[sid][lvl]["headroom_kwh_day"],
                    "fits_energy": energy[sid][lvl]["fits"],
                    "storage_kl": s.levels[lvl]["storage_kl"],
                    "imported_kl": s.levels[lvl]["imported_kl"],
                    "overflow_kl": s.levels[lvl]["overflow_kl"],
                    "production_area_m2": s.levels[lvl]["production_area_m2"],
                    "insect_share_of_fish_feed": s.levels[lvl]["insect_share_of_fish_feed"],
                    "fish_protein_kg_counted": s.levels[lvl]["fish_protein_kg_counted"],
                } for lvl in rc.LVLS
            },
        })

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    return data


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    d = main()
    print(f"wrote {OUT}")
    print(f"  {len(d['sites'])} sites, {len(d['schedule'])} price lines, "
          f"{len(d['indicators'])} banded indicators")
