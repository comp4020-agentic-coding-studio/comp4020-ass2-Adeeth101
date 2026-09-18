"""
Site calibration model for the closed-loop household course (Assignment 2 research).

Purpose: test whether a set of preset sites gives every student a comparably
hard, comparably rich design problem, and test the proposed scoring method.
It is a *screening* model: monthly, transparent, built only from published
formulas and figures so a student could reproduce every number by hand.
It is not a design tool and its outputs are not predictions of real yields.

Every constant carries a source key that resolves in ../sources.md.
Run:  python site_model.py   -> writes output/calibration.md and .json
"""

import json
import math
import os
from dataclasses import dataclass, field, asdict

HERE = os.path.dirname(os.path.abspath(__file__))
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MID_DOY = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]

# --------------------------------------------------------------------------
# Fixed household (identical for every site)
# --------------------------------------------------------------------------
# [S03] NHMRC EER: man 1.8 m PAL 1.8 = 13.3 MJ/d; woman 1.7 m PAL 1.8 = 10.8;
# boy 10 y PAL 1.6 = 8.3; girl 10 y PAL 1.6 = 7.6
HOUSEHOLD_MJ_PER_DAY = 13.3 + 10.8 + 8.3 + 7.6
KCAL_PER_MJ = 239.0
HOUSEHOLD_KCAL_YEAR = HOUSEHOLD_MJ_PER_DAY * KCAL_PER_MJ * 365
# [S04] NHMRC protein RDI: men 64, women 46, boys 9-13 40, girls 9-13 35 g/d
HOUSEHOLD_PROTEIN_KG_YEAR = (64 + 46 + 40 + 35) * 365 / 1000
OCCUPANTS = 4
# [S06] Your Home: rainwater-only households ~150 L/person/day
DOMESTIC_L_PP_D = 150
# [S05] Jönsson et al. 2004 Swedish default: urine 4.0 + faeces 0.55 kg N per person-year.
# Children counted as half an adult (assumption).
HOUSEHOLD_N_KG_YEAR = 4.55 * (2 + 0.5 * 2)
# [S05] one person's urine fertilises 300-400 m2/yr -> ~12 g N/m2/yr uptake capacity
GARDEN_N_CAPACITY_KG_M2 = 0.012

# --------------------------------------------------------------------------
# Published formulas and coefficients
# --------------------------------------------------------------------------
RUNOFF_A, RUNOFF_B_MM_MONTH = 0.80, 2.0   # [S08] enHealth 2010 App. B (Martin 1980)
KC_MIXED_GARDEN = 0.95                     # [S11] FAO-56 Table 12 blend (assumption within table range)
YREF_KCAL_M2_YEAR = 1500                   # [S13][S14][S15] assumption inside published 500-3,000 range
GARDEN_PROTEIN_G_PER_100KCAL = 3.0         # assumption: mixed potato/legume/vegetable output
PUMP_KWH_PER_KL = 1.5                      # [S21] typical household rainwater pumping (low-flow events)
IRRIGATION_KWH_PER_KL = 0.7                # [S21] same pumps at >15 L/min
GREYWATER_FRACTION = 0.55                  # [S09][S26] shower+laundry+basins; kitchen excluded
TOILET_L_PP_D = 21.8                       # [S26] Beal & Stewart SEQ end-use study
# Aquaponics [S16] FAO 589 and [S20]
FEED_G_M2_D = 50                           # leafy greens 40-50, fruiting 50-80
FCR = 2.0                                  # silver perch 1.8-2.5 in trials
FILLET_YIELD = 0.40                        # assumption, flagged
FILLET_PROTEIN = 0.20                      # assumption, flagged
AQUAPONIC_CIRC_W, AERATION_W = 40, 15      # FAO 589 25-50 W pump; aeration assumption
UV_W, TOILET_FAN_W = 25, 5                 # assumptions
TANK_UA_W_PER_K = 5.0                      # assumption: ~1 m3 insulated tank
# Insects and food waste
HOUSEHOLD_FOOD_WASTE_KG_PP_YR = 95         # [S28] 2.46 Mt household food waste / ~26 M people
FOOD_WASTE_DM = 0.25                       # assumption
BSF_BIOCONVERSION_DM = 0.20                # [S22b] 20-28 % DM on food waste
PLANT_BASED_WASTE_SHARE = 0.6              # assumption: only plant-based scraps may feed insects destined for animal feed [S29]
INDOOR_REARING_FACTOR = round((20 - 12) / (27 - 12), 2)  # insects reared indoors at ~20 C, same thermal ramp as BSF_*

# --------------------------------------------------------------------------
# Biological thermal bands (water temperature approximated by monthly mean air T)
# --------------------------------------------------------------------------
FISH = {                                   # legal in Australia; tilapia is noxious [S18]
    "barramundi": (25, 30),               # [S19]
    "jade perch": (20, 30),               # [S19]
    "silver perch": (23, 28),             # [S20]
    "Murray cod": (18, 27),               # [S19] band is an assumption around "best ~25"
    "rainbow trout": (10, 18),            # [S16]
}
BSF_LOWER_C, BSF_OPT_C = 12.0, 27.0        # [S22]
MUSHROOM_BANDS = [(8, 20), (18, 30)]       # [S23] cool and warm oyster species
BIOGAS_LOW_C, BIOGAS_HIGH_C = 15.0, 35.0   # screening assumption


def load_climate():
    with open(os.path.join(HERE, "data", "climate_stations.json"), encoding="utf-8") as f:
        return json.load(f)["stations"]


def ra_mm_day(lat_deg, doy):
    """FAO-56 Eq. 21-25 extraterrestrial radiation as equivalent evaporation."""
    phi = math.radians(lat_deg)
    dr = 1 + 0.033 * math.cos(2 * math.pi * doy / 365)
    delta = 0.409 * math.sin(2 * math.pi * doy / 365 - 1.39)
    ws = math.acos(max(-1.0, min(1.0, -math.tan(phi) * math.tan(delta))))
    ra = (24 * 60 / math.pi) * 0.0820 * dr * (
        ws * math.sin(phi) * math.sin(delta) + math.cos(phi) * math.cos(delta) * math.sin(ws))
    return 0.408 * ra


def eto_month(lat, tmax, tmin, m):
    """FAO-56 Eq. 52 (Hargreaves), mm/month."""
    return 0.0023 * ((tmax + tmin) / 2 + 17.8) * math.sqrt(max(tmax - tmin, 0)) * ra_mm_day(lat, MID_DOY[m]) * DAYS[m]


def effective_rain(p):
    """FAO Training Manual 3, Annex 1."""
    return max(0.0, 0.8 * p - 25) if p > 75 else max(0.0, 0.6 * p - 10)


def chill_hours_month(tmax, tmin, m, base=7.2):
    if tmin >= base:
        return 0.0
    if tmax <= base:
        return 24.0 * DAYS[m]
    amp, mid = (tmax - tmin) / 2, (tmax + tmin) / 2
    return (1 - math.acos((base - mid) / amp) / math.pi) * 24 * DAYS[m]


def growing_factor(tmean, d35):
    """Screening weight 0..1: ramps 5->15 C, halved as >=35 C days approach 20/month."""
    return max(0.0, min(1.0, (tmean - 5) / 10)) * (1 - 0.5 * min(1.0, (d35 or 0) / 20))


@dataclass
class Site:
    sid: str
    label: str
    station: str
    dwelling: str
    plot_m2: float
    growable_m2: float
    roof_m2: float
    other_water_kl_year: float = 0.0   # licensed bore / dam / shared tank counted as on-site
    shared_growing_m2: float = 0.0     # e.g. strata or community allotment inside the site boundary
    existing_storage_kl: float = 0.0   # tanks already on site at handover
    notes: str = ""
    derived: dict = field(default_factory=dict)
    levels: dict = field(default_factory=dict)


# Reference designs used to set per-site bands (the NatHERS star-band idea [S30]).
#
# Recipe v5 (2026-09-18). v4 used storage_budget 3000/6000/9000 and extra_catchment
# 0/0/0.25. Re-costing the v4 designs against the full course price schedule
# (reference_costs.py) put the excellent design $3,704-$9,545 over the $30,000
# allowance at every site, because v4's costs omitted tank establishment, first
# flush, pumps, treatment, drip irrigation and the required 10 % contingency.
# Two facts drove the fix: the monthly tank balance saturates well below v4's
# storage (raising excellent storage from $4,000 to $9,000 moved water closure by
# at most 0.06), and added roof catchment is the most expensive water lever per
# point of closure. So storage spend drops to 3000/3500/4000 and the excellent
# design's added catchment drops from 25 % to 5 %. Nothing else changed. See
# ../critique-log.md iteration 5.
LEVELS = {
    # storage_budget: dollars of the allowance spent on new tank shells (at TANK_COST_PER_KL).
    # Establishment, first flush, pumps, treatment and contingency are costed separately
    # in reference_costs.py, which is the authority on what a reference design costs.
    "baseline": dict(demand=150, composting_toilet=False, greywater=0.0, production=0.5, yield_mult=0.8,
                     n_recovery=0.3, aquaponic_m2=0, extra_catchment=0.0, storage_budget=3000),
    "competent": dict(demand=150, composting_toilet=True, greywater=0.5, production=0.8, yield_mult=1.0,
                      n_recovery=0.6, aquaponic_m2=4, extra_catchment=0.0, storage_budget=3500),
    "excellent": dict(demand=130, composting_toilet=True, greywater=0.9, production=1.0, yield_mult=1.2,
                      n_recovery=0.8, aquaponic_m2=8, extra_catchment=0.05, storage_budget=4000),
}
# Simplified component costs (AUD) kept so the iteration-1..3 snapshots stay reproducible.
# `indicative_cost` below is SUPERSEDED for every published figure: it omits establishment,
# first flush, pumps, treatment, irrigation and the required contingency. reference_costs.py
# prices the full course schedule and is the authority on the budget hard constraint.
TANK_COST_PER_KL = 130            # [S31] 22.5 kL poly tank ~$2,900; 10-46 kL tanks $2,100-7,700
COMPOSTING_TOILET_COST = 3500     # [S32] $1,850-6,050 units
GREYWATER_COST = 2100             # [S33] diversion systems installed $1,600-2,600
AQUAPONIC_COST_PER_4M2 = 2500     # [S34] kits $1,995-3,495
EXTRA_CATCHMENT_COST_PER_M2 = 60  # assumption: simple skillion shed roof
BUDGET = 30000


def evaluate(site: Site, clim):
    c = clim[site.station]
    lat = c["lat"]
    tmax, tmin, rain = c["tmax"][:12], c["tmin"][:12], c["rain"][:12]
    d35 = (c.get("d35") or [0] * 13)[:12]
    d2 = (c.get("d2") or [0] * 13)[:12]
    evap = c.get("evap")
    tmean = [(a + b) / 2 for a, b in zip(tmax, tmin)]
    eto = [eto_month(lat, tmax[m], tmin[m], m) for m in range(12)]
    pe = [effective_rain(p) for p in rain]
    gfac = [growing_factor(tmean[m], d35[m]) for m in range(12)]
    season = sum(gfac) / 12
    net_irr_mm = [max(0.0, eto[m] * KC_MIXED_GARDEN - pe[m]) if gfac[m] > 0 else 0.0 for m in range(12)]
    irr_mm_year = sum(net_irr_mm)
    grow_area = site.growable_m2 + site.shared_growing_m2

    fish_months = {f: sum(1 for t in tmean if lo <= t <= hi) for f, (lo, hi) in FISH.items()}
    rot_best, rot_pair = 0, ("", "")
    names = list(FISH)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            (a0, a1), (b0, b1) = FISH[names[i]], FISH[names[j]]
            n = sum(1 for t in tmean if a0 <= t <= a1 or b0 <= t <= b1)
            if n > rot_best:
                rot_best, rot_pair = n, (names[i], names[j])
    annual_tmean = sum(tmean) / 12
    heat_kwh_day = max(
        0.0 if any(lo <= t <= hi for lo, hi in FISH.values()) else max(0.0, 10 - t) * TANK_UA_W_PER_K * 24 / 1000
        for t in tmean)

    site.derived = {
        "station_name": c["name"], "lat": lat,
        "annual_rain_mm": round(sum(rain)), "annual_eto_mm": round(sum(eto)),
        "pan_evap_x0.7_mm": None if not evap or evap[12] is None else round(evap[12] * 365 * 0.7),
        "aridity_P_over_ETo": round(sum(rain) / sum(eto), 2),
        "driest_4_months_share_of_rain": round(sum(sorted(rain)[:4]) / sum(rain), 3),
        "annual_tmean_c": round(annual_tmean, 1),
        "frost_days_le2c": round(sum(d2)), "hot_days_ge35c": round(sum(d35)),
        "growing_season_factor": round(season, 2),
        "roof_runoff_kl": round(sum(RUNOFF_A * max(0.0, r - RUNOFF_B_MM_MONTH) * site.roof_m2 / 1000 for r in rain)),
        "net_irrigation_mm_year": round(irr_mm_year),
        "fish_best_rotation": f"{' + '.join(rot_pair)} ({rot_best} mo)", "fish_rotation_months": rot_best,
        "bsf_productive_factor": round(sum(max(0.0, min(1.0, (t - BSF_LOWER_C) / (BSF_OPT_C - BSF_LOWER_C))) for t in tmean) / 12, 2),
        "mushroom_months": sum(1 for t in tmean if any(lo <= t <= hi for lo, hi in MUSHROOM_BANDS)),
        "chill_hours_model": round(sum(chill_hours_month(tmax[m], tmin[m], m) for m in range(12))),
        "biogas_temperature_factor": round(sum(max(0.0, min(1.0, (t - BIOGAS_LOW_C) / (BIOGAS_HIGH_C - BIOGAS_LOW_C))) for t in tmean) / 12, 2),
        "excreta_storage_years_WHO": 1.0 if annual_tmean > 20 else 1.75,  # [S25] Table 4.5
        "tank_heating_peak_kwh_day": round(heat_kwh_day, 2),
        "n_absorption_ratio_full_area": round(grow_area * GARDEN_N_CAPACITY_KG_M2 / HOUSEHOLD_N_KG_YEAR, 2),
        "monthly": {"tmean": [round(t, 1) for t in tmean], "rain": rain, "eto_mm": [round(e) for e in eto],
                    "net_irrigation_mm": [round(x) for x in net_irr_mm], "growing_factor": [round(g, 2) for g in gfac]},
    }

    etc = [eto[m] * KC_MIXED_GARDEN for m in range(12)]
    deficit = [max(0.0, etc[m] - pe[m]) if gfac[m] > 0 else 0.0 for m in range(12)]
    rainfed_satisfaction = [min(1.0, pe[m] / etc[m]) if etc[m] else 1.0 for m in range(12)]
    site.derived["rainfed_yield_factor"] = round(sum(gfac[m] * rainfed_satisfaction[m] for m in range(12)) / 12, 2)
    site.derived["bio_window"] = round((site.derived["fish_rotation_months"] / 12 + site.derived["bsf_productive_factor"]
                                        + site.derived["mushroom_months"] / 12) / 3, 2)

    for name, L in LEVELS.items():
        extra_roof = site.roof_m2 * L["extra_catchment"]
        roof = site.roof_m2 + extra_roof
        runoff = [RUNOFF_A * max(0.0, rain[m] - RUNOFF_B_MM_MONTH) * roof / 1000 for m in range(12)]
        inflow = [runoff[m] + site.other_water_kl_year / 12 for m in range(12)]
        per_person = L["demand"] - (TOILET_L_PP_D if L["composting_toilet"] else 0)
        domestic = [per_person * OCCUPANTS * DAYS[m] / 1000 for m in range(12)]
        grey = [d * GREYWATER_FRACTION * L["greywater"] for d in domestic]
        prod_area = grow_area * L["production"]
        capacity = site.existing_storage_kl + L["storage_budget"] / TANK_COST_PER_KL
        # Monthly tank simulation on a repeating average year (enHealth App. B method [S08]);
        # three-year spin-up, year three reported. Domestic has priority; a domestic shortfall
        # is carted in; gardens get greywater first, then whatever the tank still holds.
        tank = capacity / 2
        for year in range(3):
            dom_tank = imported = grey_used = garden_tank = overflow = 0.0
            sat, tank_irr = [], []
            for m in range(12):
                tank += inflow[m]
                if tank > capacity:
                    overflow += tank - capacity
                    tank = capacity
                take = min(tank, domestic[m]); tank -= take
                dom_tank += take; imported += domestic[m] - take
                need = prod_area * deficit[m] / 1000
                g = min(grey[m], need); t = min(tank, need - g); tank -= t
                grey_used += g; garden_tank += t; tank_irr.append(t)
                applied_mm = (g + t) * 1000 / prod_area if prod_area else 0.0
                sat.append(min(1.0, (pe[m] + applied_mm) / etc[m]) if etc[m] else 1.0)
        onsite_used = dom_tank + grey_used + garden_tank
        water_closure = onsite_used / (onsite_used + imported) if onsite_used + imported else 1.0
        garden_need = sum(prod_area * deficit[m] / 1000 for m in range(12))
        garden_satisfaction = (grey_used + garden_tank) / garden_need if garden_need else 1.0
        yield_factor = sum(gfac[m] * sat[m] for m in range(12)) / 12

        garden_kcal = prod_area * YREF_KCAL_M2_YEAR * L["yield_mult"] * yield_factor
        fish_feed_kg = L["aquaponic_m2"] * FEED_G_M2_D * 365 * rot_best / 12 / 1000
        larvae_dm_kg = (HOUSEHOLD_FOOD_WASTE_KG_PP_YR * OCCUPANTS * PLANT_BASED_WASTE_SHARE * FOOD_WASTE_DM
                        * BSF_BIOCONVERSION_DM * max(site.derived["bsf_productive_factor"], INDOOR_REARING_FACTOR))
        onsite_feed_share = min(1.0, larvae_dm_kg / (fish_feed_kg * 0.9)) if fish_feed_kg else 0.0
        # closure is net of imports: only fish grown on on-site feed counts toward protein closure
        fish_protein_kg = fish_feed_kg / FCR * FILLET_YIELD * FILLET_PROTEIN * onsite_feed_share
        protein = garden_kcal / 100 * GARDEN_PROTEIN_G_PER_100KCAL / 1000 + fish_protein_kg
        n_capacity = prod_area * GARDEN_N_CAPACITY_KG_M2 * (yield_factor / season if season else 0)
        energy = ((AQUAPONIC_CIRC_W + AERATION_W) * (1 if L["aquaponic_m2"] else 0) + UV_W + TOILET_FAN_W * L["composting_toilet"]) * 24 / 1000             + max(domestic) / 30 * PUMP_KWH_PER_KL             + max(tank_irr[m] / DAYS[m] for m in range(12)) * IRRIGATION_KWH_PER_KL             + (heat_kwh_day if L["aquaponic_m2"] else 0)
        cost = (L["storage_budget"] + COMPOSTING_TOILET_COST * L["composting_toilet"] + GREYWATER_COST * (L["greywater"] > 0)
                + AQUAPONIC_COST_PER_4M2 * L["aquaponic_m2"] / 4 + EXTRA_CATCHMENT_COST_PER_M2 * extra_roof)
        site.levels[name] = {
            "water_closure": round(water_closure, 2), "imported_kl": round(imported), "overflow_kl": round(overflow),
            "storage_kl": round(capacity), "garden_water_satisfaction": round(garden_satisfaction, 2),
            "food_kcal_closure": round(min(1.0, garden_kcal / HOUSEHOLD_KCAL_YEAR), 3),
            "protein_closure": round(min(1.0, protein / HOUSEHOLD_PROTEIN_KG_YEAR), 3),
            "nutrient_closure": round(min(L["n_recovery"] * HOUSEHOLD_N_KG_YEAR, n_capacity) / HOUSEHOLD_N_KG_YEAR, 2),
            "production_area_m2": round(prod_area),
            "peak_energy_kwh_day": round(energy, 2), "indicative_cost": round(cost),
            "insect_share_of_fish_feed": None if not fish_feed_kg else round(onsite_feed_share, 2),
            "fish_protein_kg_counted": round(fish_protein_kg, 2),
            "bio_window": site.derived["bio_window"],
        }
    return site


def storage_needed(inflow, draw):
    """Smallest tank that never runs dry over repeating average years; None if annual inflow < draw."""
    if sum(inflow) < sum(draw) - 1e-9:
        return None
    lo, hi = 0.0, 5000.0
    for _ in range(60):
        cap = (lo + hi) / 2
        v, ok = cap, True
        for _y in range(3):
            for m in range(12):
                v = min(cap, v + inflow[m] - draw[m])
                if v < -1e-9:
                    ok = False
                    break
            if not ok:
                break
        lo, hi = (lo, cap) if ok else (cap, hi)
    return hi


DIMENSIONS = [  # key, label, higher_is_easier; all read from the "competent" reference design
    ("water_closure", "water closure", True),
    ("food_kcal_closure", "food energy closure", True),
    ("protein_closure", "protein closure", True),
    ("nutrient_closure", "nutrient closure", True),
    ("garden_water_satisfaction", "garden water satisfaction", True),
    ("bio_window", "biological operating window", True),
    ("peak_energy_kwh_day", "peak process energy (kWh/d)", False),
]


def fairness(sites):
    ranks = {s.sid: {} for s in sites}
    for key, _l, higher in DIMENSIONS:
        big = 1e9
        order = sorted(sites, key=lambda s: (s.levels["competent"][key] if s.levels["competent"][key] is not None else (-big if higher else big)),
                       reverse=higher)
        for r, s in enumerate(order, 1):
            ranks[s.sid][key] = r
    dominated = [(a.sid, b.sid) for a in sites for b in sites if a is not b
                 and all(ranks[a.sid][k] <= ranks[b.sid][k] for k, _, _ in DIMENSIONS)]
    mean = {s.sid: round(sum(ranks[s.sid].values()) / len(DIMENSIONS), 2) for s in sites}
    ease = ease_index(sites)
    headroom = {s.sid: {k: round(s.levels["excellent"][k] - s.levels["baseline"][k], 2)
                        for k in ("water_closure", "food_kcal_closure", "protein_closure", "nutrient_closure")} for s in sites}
    return ranks, mean, dominated, headroom, ease


def ease_index(sites, level="competent"):
    """Mean standardised ease across DIMENSIONS (0 = set average). Continuous companion to ranks."""
    idx = {s.sid: 0.0 for s in sites}
    for key, _l, higher in DIMENSIONS:
        vals = [s.levels[level][key] for s in sites]
        mu = sum(vals) / len(vals)
        sd = (sum((v - mu) ** 2 for v in vals) / len(vals)) ** 0.5 or 1.0
        for s in sites:
            z = (s.levels[level][key] - mu) / sd
            idx[s.sid] += (z if higher else -z) / len(DIMENSIONS)
    return {k: round(v, 2) for k, v in idx.items()}


def table(rows, headers):
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
                     + ["| " + " | ".join(str(x) for x in r) + " |" for r in rows])


def run(preset_sets, out_name="calibration"):
    clim = load_climate()
    md = ["# Site calibration model output", "",
          "Generated by `site_model.py`. Screening model only — see `../findings.md` for method and limits.",
          f"Fixed household: 4 people, {HOUSEHOLD_MJ_PER_DAY:.1f} MJ/d, {HOUSEHOLD_PROTEIN_KG_YEAR:.1f} kg protein/yr, "
          f"{DOMESTIC_L_PP_D} L/person/d, {HOUSEHOLD_N_KG_YEAR:.1f} kg N/yr.", ""]
    dump = {}
    for set_name, sites in preset_sets.items():
        for s in sites:
            evaluate(s, clim)
        ranks, mean, dominated, headroom, ease = fairness(sites)
        md += [f"## {set_name}", "", table(
            [[s.sid, s.label, s.derived["station_name"], s.dwelling, s.plot_m2, s.growable_m2, s.shared_growing_m2, s.roof_m2, s.other_water_kl_year, s.existing_storage_kl]
             for s in sites],
            ["ID", "Site", "Station", "Dwelling", "Plot m²", "Growable m²", "Shared growing m²", "Roof m²", "Other water kL/yr", "Existing storage kL"]), ""]
        climate_keys = ["annual_rain_mm", "annual_eto_mm", "pan_evap_x0.7_mm", "aridity_P_over_ETo", "driest_4_months_share_of_rain",
                        "annual_tmean_c", "frost_days_le2c", "hot_days_ge35c", "growing_season_factor", "roof_runoff_kl",
                        "net_irrigation_mm_year", "fish_best_rotation", "bsf_productive_factor", "mushroom_months",
                        "chill_hours_model", "biogas_temperature_factor", "excreta_storage_years_WHO",
                        "tank_heating_peak_kwh_day", "n_absorption_ratio_full_area", "rainfed_yield_factor"]
        md += ["### Site conditions", "", table([[k] + [s.derived[k] for s in sites] for k in climate_keys], ["Metric"] + [s.sid for s in sites]), ""]
        md += ["### Reference designs (baseline / competent / excellent)", ""]
        lvl_keys = ["storage_kl", "water_closure", "imported_kl", "overflow_kl", "garden_water_satisfaction", "food_kcal_closure", "protein_closure", "nutrient_closure", "production_area_m2",
                    "peak_energy_kwh_day", "indicative_cost", "insect_share_of_fish_feed", "fish_protein_kg_counted"]
        md += [table([[k] + [" / ".join(str(s.levels[l][k]) for l in LEVELS) for s in sites] for k in lvl_keys],
                     ["Metric (b / c / e)"] + [s.sid for s in sites]), ""]
        md += ["### Fairness screen (competent design; rank 1 = easiest)", "",
               table([[label] + [ranks[s.sid][k] for s in sites] for k, label, _ in DIMENSIONS]
                     + [["**mean rank**"] + [mean[s.sid] for s in sites]] + [["**ease index** (0 = set mean)"] + [ease[s.sid] for s in sites]],
                     ["Dimension"] + [s.sid for s in sites]), "",
               "Dominated pairs (A at least as easy as B everywhere): " + (", ".join(f"{a}≥{b}" for a, b in dominated) or "none"), "",
               "Headroom between baseline and excellent reference designs (the width of each site's scoring band):", "",
               table([[k] + [headroom[s.sid][k] for s in sites] for k in headroom[sites[0].sid]], ["Stream"] + [s.sid for s in sites]), ""]
        dump[set_name] = {s.sid: {**{k: v for k, v in asdict(s).items() if k not in ("derived", "levels")},
                                  "derived": s.derived, "levels": s.levels} for s in sites}
        dump[set_name]["_fairness"] = {"ranks": ranks, "mean_rank": mean, "dominated": dominated, "headroom": headroom, "ease_index": ease}
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    with open(os.path.join(HERE, "output", out_name + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(os.path.join(HERE, "output", out_name + ".json"), "w", encoding="utf-8") as f:
        json.dump(dump, f, indent=1)
    return dump


if __name__ == "__main__":
    import sys
    from presets import PRESET_SETS
    run(PRESET_SETS)
    sys.stdout.reconfigure(encoding="utf-8")
    print(open(os.path.join(HERE, "output", "calibration.md"), encoding="utf-8").read())
