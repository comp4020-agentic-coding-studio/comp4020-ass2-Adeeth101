"""Re-cost the three reference designs against the course price schedule (course-design.md
section 2.2), and check the two hard constraints for them.

Why this exists: the original model costed the reference designs from five simplified
component prices, with no establishment, delivery, treatment or contingency lines. Its
totals ($3k / $14.1k / $22-25k) therefore never established compliance with the $30,000
allowance. This module prices the full bill of materials that the reference recipe and
the counted-energy boundary imply, adds the required 10 % contingency, and reports
whether each reference design fits.

Run:  python reference_costs.py   -> writes output/reference-costs.md / .json
Every price key resolves in ../sources.md or is marked a course assumption in
course-design.md section 2.2.
"""

import json
import math
import os
import sys
from copy import deepcopy

import site_model as sm
from presets import V4

HERE = os.path.dirname(os.path.abspath(__file__))
BUDGET = 30000
CONTINGENCY = 0.10

# --- The course price schedule (course-design.md section 2.2) ------------------------
# basis: "indicative" = from a retail listing; "assumption" = set by the course.
SCHEDULE = {
    "tank_shell_per_kl": (130, "indicative", "Polyethylene rainwater storage, supply only [S31]"),
    "tank_establishment": (1000, "assumption", "Pad, inlet/outlet plumbing, overflow, per tank"),
    "first_flush_per_downpipe": (150, "assumption", "First-flush diverter and leaf screen, per downpipe"),
    "pump": (700, "assumption", "Pressure or transfer pump, each"),
    "uv_unit": (1200, "assumption", "Point-of-entry UV unit with sensor"),
    "prefiltration": (400, "assumption", "Cartridge pre-filtration train"),
    "catchment_per_m2": (60, "assumption", "Additional roof catchment (skillion shed roof)"),
    "composting_toilet": (3500, "indicative", "Composting toilet unit [S32]"),
    "urine_system": (900, "assumption", "Urine diversion and storage tank"),
    "greywater_diversion": (2100, "indicative", "Greywater diversion, bathroom and laundry, installed [S33]"),
    "greywater_treatment": (6000, "indicative", "Greywater treatment system [S33]"),
    "aquaponics_4m2": (2500, "indicative", "Aquaponics: tank, 4 m2 grow bed, pump, aeration [S34]"),
    "insect_unit": (300, "assumption", "Insect rearing unit (black soldier fly or mealworm)"),
    "mushroom_chamber": (800, "assumption", "Humidified mushroom fruiting chamber"),
    "compost_bays": (500, "assumption", "Hot-compost bays, set of three"),
    "digester": (1500, "assumption", "Household anaerobic digester"),
    "tree": (50, "assumption", "Fruit or nut tree, potted, each"),
    "drip_per_m2": (8, "assumption", "Drip irrigation, per m2 irrigated"),
}

# --- Bill-of-materials rules (course assumptions, published with the schedule) -------
MAX_TANK_KL = 25.0
ROOF_PER_DOWNPIPE_M2 = 75.0
# The aquaponics line bundles tank, pump and aeration. A second 4 m2 bed on the same
# system needs neither a second tank nor a second pump, so additional beds are charged
# at the bundle price less one pump line. This is the no-double-counted-pump rule.
EXTRA_BED = SCHEDULE["aquaponics_4m2"][0] - SCHEDULE["pump"][0]

# Priced in the schedule but not drawn in the reference bill, because no recipe
# parameter and no counted load implies them. A student who chooses them pays from the
# same allowance.
NOT_IN_REFERENCE = ["greywater_treatment", "digester", "mushroom_chamber", "tree"]

# Not priced by the schedule at all. Published so the allowance is not read as a quote.
UNPRICED = [
    "Garden establishment: soil improvement, mulch, seed and seedling stock",
    "Aquaculture tank heating or cooling hardware",
    "Labour beyond the lines marked installed",
    "Earthworks, slabs and access beyond the per-tank establishment line",
    "Council approval, plumbing certification and fitting of WaterMark-licensed devices",
    "Consumables and replacement: UV lamps, filter cartridges, imported fish feed, desludging",
]


def bill(site, L):
    """The reference design's bill of materials at one level."""
    grow_area = site.growable_m2 + site.shared_growing_m2
    extra_roof = site.roof_m2 * L["extra_catchment"]
    total_roof = site.roof_m2 + extra_roof
    new_kl = L["storage_budget"] / SCHEDULE["tank_shell_per_kl"][0]
    tanks = math.ceil(new_kl / MAX_TANK_KL) if new_kl > 0 else 0
    downpipes = math.ceil(total_roof / ROOF_PER_DOWNPIPE_M2)
    prod_area = grow_area * L["production"]
    beds = math.ceil(L["aquaponic_m2"] / 4) if L["aquaponic_m2"] else 0

    rows = [
        ("Rainwater storage (shell)", round(new_kl, 1), "kL",
         new_kl * SCHEDULE["tank_shell_per_kl"][0]),
        ("Tank establishment", tanks, "tank", tanks * SCHEDULE["tank_establishment"][0]),
        ("First-flush diverter and leaf screen", downpipes, "downpipe",
         downpipes * SCHEDULE["first_flush_per_downpipe"][0]),
        ("Additional roof catchment", round(extra_roof), "m2",
         extra_roof * SCHEDULE["catchment_per_m2"][0]),
        ("Pressure pump (domestic supply)", 1, "ea", SCHEDULE["pump"][0]),
        ("Transfer pump (garden irrigation)", 1, "ea", SCHEDULE["pump"][0]),
        ("Point-of-entry UV unit", 1, "ea", SCHEDULE["uv_unit"][0]),
        ("Cartridge pre-filtration train", 1, "ea", SCHEDULE["prefiltration"][0]),
        ("Composting toilet", int(L["composting_toilet"]), "ea",
         SCHEDULE["composting_toilet"][0] * L["composting_toilet"]),
        ("Urine diversion and storage", 1, "ea", SCHEDULE["urine_system"][0]),
        ("Greywater diversion (installed)", int(L["greywater"] > 0), "ea",
         SCHEDULE["greywater_diversion"][0] * (L["greywater"] > 0)),
        ("Aquaponics system", L["aquaponic_m2"], "m2",
         0 if not beds else SCHEDULE["aquaponics_4m2"][0] + EXTRA_BED * (beds - 1)),
        ("Insect rearing unit", int(beds > 0), "ea", SCHEDULE["insect_unit"][0] * (beds > 0)),
        ("Hot-compost bays", 1, "set", SCHEDULE["compost_bays"][0]),
        ("Drip irrigation", round(prod_area), "m2", prod_area * SCHEDULE["drip_per_m2"][0]),
    ]
    rows = [(n, q, u, round(c)) for n, q, u, c in rows if c > 0]
    subtotal = sum(c for _, _, _, c in rows)
    contingency = round(subtotal * CONTINGENCY)
    return rows, subtotal, contingency, subtotal + contingency


def cost_all(sites, levels):
    """Evaluate and cost every site at every level of `levels`."""
    levels = deepcopy(levels)  # `levels` may be sm.LEVELS itself
    saved = deepcopy(sm.LEVELS)
    sm.LEVELS.clear()
    sm.LEVELS.update(levels)
    clim = sm.load_climate()
    out, evaluated = {}, []
    for site in sites:
        s = deepcopy(site)
        sm.evaluate(s, clim)
        evaluated.append(s)
        out[s.sid] = {}
        for name, L in levels.items():
            rows, sub, cont, total = bill(s, L)
            out[s.sid][name] = {
                "rows": rows, "subtotal": sub, "contingency": cont, "total": total,
                "fits": total <= BUDGET, "headroom": BUDGET - total,
                "indicators": s.levels[name],
            }
    sm.LEVELS.clear()
    sm.LEVELS.update(saved)
    return out, evaluated


def worst_headroom(levels):
    res, _ = cost_all(V4, levels)
    return min(res[s][l]["headroom"] for s in res for l in levels)


# --- Energy boundary reconciliation (course-design.md section 2.1) -------------------
# The screening model prices six of the counted load groups. The remaining groups are
# only counted if the design contains the system that carries them. For the reference
# designs' own bill of materials that leaves two, and section 2.1 requires uncertain
# loads to be carried at their UPPER estimate when checking the 5 kWh/d cap.
ENERGY_CAP_KWH_DAY = 5.0
MODELLED_LOADS = [
    ("Water movement", "Domestic pressure pump, garden transfer pump", "modelled"),
    ("Water treatment", "Point-of-entry UV lamp", "modelled"),
    ("Water treatment", "Cartridge pre-filtration (unpowered)", "zero by design"),
    ("Aquaponics", "Circulation pump and aeration", "modelled"),
    ("Climate control", "Aquaculture tank heating", "modelled"),
    ("Sanitation", "Composting-toilet fan", "modelled"),
]
# Upper estimates for the counted loads the screening model does not compute, for a
# design whose bill of materials is the reference bill. Course assumptions, published.
UNCERTAIN_LOADS = [
    ("Climate control", "Insect rearing unit heating (40 W mat, winter duty)", 0.0, 0.50),
    ("Water movement", "Greywater pump, if the diversion is not gravity-fed", 0.0, 0.15),
]
UNCERTAIN_UPPER = sum(hi for *_, hi in UNCERTAIN_LOADS)
# Systems a student may add that the reference bill does not contain. Each brings its
# own counted loads, so the headroom below is what those additions have to fit inside.
OPTIONAL_LOADS = [
    ("Mycology", "Humidified fruiting chamber: fan and humidifier", 0.20, 0.60),
    ("Fermentation", "Temperature-controlled fermentation space", 0.05, 0.25),
    ("Food preservation", "Dehydrator for loop produce, peak-month average", 0.10, 0.30),
    ("Waste processing", "Digester heating or mixing", 0.00, 0.40),
    ("Waste processing", "Powered compost aeration (zero if hand-turned)", 0.00, 0.10),
]


def energy_check(costed):
    """Peak-month modelled load plus the declared upper estimate for uncertain loads."""
    out = {}
    for sid, levels in costed.items():
        out[sid] = {}
        for name, r in levels.items():
            modelled = r["indicators"]["peak_energy_kwh_day"]
            declared = round(modelled + UNCERTAIN_UPPER, 2)
            out[sid][name] = {
                "modelled_kwh_day": modelled,
                "uncertain_upper_kwh_day": UNCERTAIN_UPPER,
                "declared_peak_kwh_day": declared,
                "fits": declared <= ENERGY_CAP_KWH_DAY,
                "headroom_kwh_day": round(ENERGY_CAP_KWH_DAY - declared, 2),
            }
    return out


SIDS = ["S1", "S2", "S3", "S4", "S5"]
LVLS = ["baseline", "competent", "excellent"]


def write_outputs():
    costed, sites = cost_all(V4, sm.LEVELS)
    energy = energy_check(costed)
    labels = {s.sid: s.label for s in sites}
    money = lambda v: f"${v:,.0f}"
    L = ["# Reference-design costs and hard-constraint check (v4 presets, recipe v5)", "",
         "Generated by `reference_costs.py`. Every line is priced from the course price "
         "schedule in `../course-design.md` section 2.2; nothing here is a market quotation.",
         "", f"Allowance: {money(BUDGET)} of new spend, including a required "
         f"{CONTINGENCY:.0%} contingency. Listed existing site inventory is free.", "",
         "## Totals", "",
         "| Site | Level | Subtotal | Contingency | Total | Against the allowance |",
         "|---|---|---|---|---|---|"]
    for sid in SIDS:
        for lvl in LVLS:
            r = costed[sid][lvl]
            verdict = f"{money(r['headroom'])} spare" if r["fits"] else f"**over by {money(-r['headroom'])}**"
            L.append(f"| {sid} {labels[sid]} | {lvl} | {money(r['subtotal'])} | "
                     f"{money(r['contingency'])} | {money(r['total'])} | {verdict} |")

    L += ["", "## Bill of materials, excellent reference design", "",
          "The baseline and competent bills are the same list with the lines their recipe "
          "parameters do not switch on removed.", "",
          "| Line | " + " | ".join(SIDS) + " |", "|---|" + "---|" * len(SIDS)]
    names = []
    for sid in SIDS:
        for n, *_ in costed[sid]["excellent"]["rows"]:
            if n not in names:
                names.append(n)
    for n in names:
        cells = []
        for sid in SIDS:
            row = next((r for r in costed[sid]["excellent"]["rows"] if r[0] == n), None)
            cells.append("—" if row is None else f"{money(row[3])} ({row[1]} {row[2]})")
        L.append(f"| {n} | " + " | ".join(cells) + " |")

    L += ["", "### Bill-of-materials rules (course assumptions)", "",
          f"- New storage is delivered in tanks of at most {MAX_TANK_KL:.0f} kL, so the "
          "per-tank establishment charge scales with tank count.",
          f"- One first-flush diverter and leaf screen per {ROOF_PER_DOWNPIPE_M2:.0f} m² of connected roof.",
          "- Two pumps: one for domestic supply, one to move tank water to the garden. "
          "Both are counted loads in section 2.1.",
          f"- The aquaponics line bundles tank, pump and aeration. A second 4 m² bed on the "
          f"same system needs neither, so extra beds cost {money(EXTRA_BED)}, the bundle "
          "price less one pump. This is the rule that stops the pump being paid for twice.",
          "- Drip irrigation covers the whole production area, because the model irrigates "
          "the whole production area.",
          "",
          "### Priced in the schedule, not drawn in the reference bill", "",
          "No recipe parameter and no counted load implies these, so charging them to a "
          "threshold-setting design would inflate the thresholds. A student who chooses "
          "them pays for them from the same allowance.", ""]
    for k in NOT_IN_REFERENCE:
        v, basis, desc = SCHEDULE[k]
        L.append(f"- {desc} — {money(v)} ({basis})")
    L += ["", "### Not priced by the schedule at all", "",
          "Published so the allowance is not mistaken for a quotation. A real build carries "
          "these; the course's costing exercise does not.", ""]
    L += [f"- {u}" for u in UNPRICED]

    L += ["", "## Energy: the full counted boundary", "",
          f"Section 2.1 counts every load that runs the food, water and waste loop, requires "
          f"the peak-month average daily figure, and requires uncertain loads to be carried "
          f"at their upper estimate. Cap: {ENERGY_CAP_KWH_DAY:.0f} kWh/day.", "",
          "| Group | Load | In the screening model |", "|---|---|---|"]
    for group, load, status in MODELLED_LOADS:
        L.append(f"| {group} | {load} | {status} |")
    L += ["", "Counted loads the screening model does not compute for the reference bill, "
          "carried at their upper estimate:", "",
          "| Group | Load | Lower | Upper (kWh/day) |", "|---|---|---|---|"]
    for group, load, lo, hi in UNCERTAIN_LOADS:
        L.append(f"| {group} | {load} | {lo:.2f} | {hi:.2f} |")
    L += ["", f"Declared uncertain-load allowance: **{UNCERTAIN_UPPER:.2f} kWh/day**.", "",
          "| Site | Level | Modelled peak | + uncertain | Declared peak | Headroom |",
          "|---|---|---|---|---|---|"]
    for sid in SIDS:
        for lvl in LVLS:
            e = energy[sid][lvl]
            L.append(f"| {sid} | {lvl} | {e['modelled_kwh_day']:.2f} | "
                     f"{e['uncertain_upper_kwh_day']:.2f} | {e['declared_peak_kwh_day']:.2f} | "
                     f"{e['headroom_kwh_day']:.2f} kWh/day |")
    L += ["", "Systems the reference bill does not contain. Each carries counted loads, so "
          "the headroom above is what a student's additions have to fit inside.", "",
          "| Group | Load | Lower | Upper (kWh/day) |", "|---|---|---|---|"]
    for group, load, lo, hi in OPTIONAL_LOADS:
        L.append(f"| {group} | {load} | {lo:.2f} | {hi:.2f} |")

    text = "\n".join(L) + "\n"
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    with open(os.path.join(HERE, "output", "reference-costs.md"), "w", encoding="utf-8") as f:
        f.write(text)
    with open(os.path.join(HERE, "output", "reference-costs.json"), "w", encoding="utf-8") as f:
        json.dump({"budget": BUDGET, "contingency": CONTINGENCY, "schedule": SCHEDULE,
                   "not_in_reference": NOT_IN_REFERENCE, "unpriced": UNPRICED,
                   "bom_rules": {"max_tank_kl": MAX_TANK_KL,
                                 "roof_per_downpipe_m2": ROOF_PER_DOWNPIPE_M2,
                                 "extra_bed_cost": EXTRA_BED},
                   "energy": {"cap_kwh_day": ENERGY_CAP_KWH_DAY,
                              "uncertain_upper_kwh_day": UNCERTAIN_UPPER,
                              "modelled_loads": MODELLED_LOADS,
                              "uncertain_loads": UNCERTAIN_LOADS,
                              "optional_loads": OPTIONAL_LOADS,
                              "by_site": energy},
                   "costs": costed}, f, indent=1)
    return text


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(write_outputs())
