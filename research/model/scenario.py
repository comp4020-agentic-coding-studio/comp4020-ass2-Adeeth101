"""Scenario evaluation for the five fixed client properties (second draft).

SLOP4761's design task is a constrained, multi-objective decision: find the lowest-cost
option that meets a client's priority service targets inside the programme's hard
constraints, then justify any extra spending. This module is the staff reference
implementation of that evaluation. It is deliberately monthly and spreadsheet-sized:
every line can be rebuilt in a student workbook, which is what Assignment 2 asks for.

It replaces the first draft's closure-score model as the basis of assessment. The
closure indicators (water, garden water satisfaction, food energy, protein, nutrient)
are still computed, but only as diagnostics.

What the first scenario draft got wrong, and what this version does instead:

  * energy was averaged over the year; it is now summed month by month and the peak
    month's daily average is reported, with the month named;
  * the tank supplied every indoor use; it now supplies only the uses each client
    permits, and the rest is imported (mains or carted);
  * the existing condition was charged for new pumps and drip; it now costs nothing in
    capital and its running cost comes from its own water, carting and electricity;
  * modules had no capacities, attendance intervals or absence limits; they now do,
    and those limits decide feasibility at Canberra (weekend-only care) and Darwin
    (four-week absence).

Sources: formulas and coefficients come from site_model.py and reference_costs.py and
carry their source keys there. New course assumptions are marked `# course assumption`.

Run:  python scenario.py     -> staff check: existing condition and the cheapest
                                 feasible option per home, average and dry year.
"""

import itertools
import json
import math
import os
import sys
from dataclasses import dataclass, field, replace

import site_model as sm
import reference_costs as rc
from case import HOMES, BY_SID, totals

HERE = os.path.dirname(os.path.abspath(__file__))
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
OCCUPANTS = 4

# ---------------------------------------------------------------------------
# Household water: the 150 L/person/day convention split by end use.
# course assumption: the split is chosen to reproduce Beal & Stewart's toilet figure
# (21.8 L/p/d) and a bathroom plus laundry share of 0.55 [S26][S09]; the total is the
# course's 150 L/p/d convention (V1).
# ---------------------------------------------------------------------------
END_USES = {"toilet": 22.0, "shower": 55.0, "laundry": 28.0, "kitchen": 30.0, "other": 15.0}
INDOOR = tuple(END_USES)
GREYWATER_USES = ("shower", "laundry")          # kitchen excluded: course design rule (V3)
assert abs(sum(END_USES.values()) - 150) < 1e-9

# ---------------------------------------------------------------------------
# Irrigation. Field application efficiency, FAO Training Manual 4, Annex I, Table 8 [S12a].
# ---------------------------------------------------------------------------
EFFICIENCY = {"drip": 0.90, "sprinkler": 0.75, "hose": 0.75}
# course assumption: no irrigation is scheduled in a month whose mean air temperature is
# below 10 degC. Growth is slow, deciduous trees are dormant, and soil moisture from rain
# carries the plantings; the FAO effective-rain expression would otherwise report a small
# winter deficit that nobody would irrigate.
DORMANT_BELOW_C = 10.0
KC_PERENNIAL = 0.80        # course assumption inside FAO-56 Table 12 ranges for fruit trees [S11]

# Crop mixes for cultivated area beyond the existing plantings. Reference yields are
# annual food energy at full water and a full twelve-month season; the site's monthly
# growing factor and water satisfaction scale them. course assumption, chosen inside the
# measured Australian home-garden range [S13][S52].
CROP_MIXES = {
    "leafy": dict(label="Leafy and salad crops", kcal_m2=350, kcal_per_kg=180, protein_g_100kcal=8.0,
                  kc=1.00, perennial=0.0, labour_h_m2=0.90),
    "mixed": dict(label="Mixed vegetables", kcal_m2=900, kcal_per_kg=330, protein_g_100kcal=4.0,
                  kc=0.95, perennial=0.15, labour_h_m2=0.60),
    "staple": dict(label="Staples and perennials", kcal_m2=1500, kcal_per_kg=650, protein_g_100kcal=2.5,
                   kc=0.90, perennial=0.50, labour_h_m2=0.35),
}
# The existing plantings each client wants kept (trees and beds): mixed output, a
# perennial share, and lower labour because they are already established.
EXISTING_PLANTING = dict(kcal_m2=800, kcal_per_kg=350, protein_g_100kcal=3.0, kc=0.85, labour_h_m2=0.40)

# ---------------------------------------------------------------------------
# Energy. Specific energy of pumping [S21]; module loads are course assumptions.
# ---------------------------------------------------------------------------
KWH_PER_KL = {"pressure": 1.5, "garden": 0.7, "bore": 0.8, "greywater": 0.3}
TARIFF_KWH = 0.33          # course assumption, $/kWh
# Mains usage charge ($/kL) and carting price ($/kL) are case facts from each client's bills.
WATER_PRICE = {"S1": 3.10, "S2": 28.0, "S3": 3.40, "S4": 3.60, "S5": 22.0}

# Biological and sanitation modules. Energy is (steady kWh/day, upper kWh/day) for months
# the module runs; heating adds a temperature-driven term. Hours are per year. Attendance
# is the longest interval the module can be left between visits in normal operation;
# `pausable` says whether it can be run down and left for an absence.
MODULES = {
    "compost": dict(label="Hot-compost bays", capital=[("compost_bays", 1)], kwh=(0.0, 0.0),
                    hours=30, attendance=7, pausable=True, consumables=0),
    "composting_toilet": dict(label="Composting toilet with urine diversion",
                              capital=[("composting_toilet", 1), ("urine_system", 1)],
                              kwh=(0.12, 0.12), heat_below_c=10.0, heat_kwh_per_k=0.03,
                              hours=25, attendance=14, pausable=True, consumables=80),
    "insects": dict(label="Insect rearing unit", capital=[("insect_unit", 1)], kwh=(0.0, 0.0),
                    heat_below_c=20.0, heat_kwh_per_k=0.06, hours=40, attendance=3, pausable=True,
                    consumables=30),
    "mushrooms": dict(label="Humidified mushroom chamber", capital=[("mushroom_chamber", 1)],
                      kwh=(0.30, 0.60), hours=40, attendance=2, pausable=True, consumables=180),
    "aquaponics": dict(label="Aquaponics, one 4 m² bed", capital=[("aquaponics_4m2", 1)],
                       kwh=(1.32, 1.32), hours=120, attendance=1, pausable=False, tolerance=3,
                       consumables=220),
    "digester": dict(label="Household anaerobic digester", capital=[("digester", 1)], kwh=(0.0, 0.10),
                     heat_below_c=20.0, heat_kwh_per_k=0.03, hours=60, attendance=1, pausable=True,
                     consumables=40),
}
MUSHROOM_BANDS = sm.MUSHROOM_BANDS
FISH = sm.FISH

# Extra schedule lines for retrofit work on fixed existing properties. Course
# assumptions, published with the schedule.
EXTRA_SCHEDULE = {
    "slimline_tank_per_kl": (450, "assumption", "Slimline modular tank, 600 mm wide or less, supply, per kL"),
    "slimline_establishment": (300, "assumption", "Slimline module installation: base, connection, overflow, per module"),
    "zone_reconnection": (600, "assumption", "Roof-zone connection: gutter check, downpipe and charged line to storage, per zone"),
    "mains_changeover": (450, "assumption", "Automatic rainwater-to-mains changeover for an indoor non-potable supply"),
    "overflow_discharge": (800, "assumption", "Tank overflow to a nominated discharge point with an energy dissipater"),
    "frost_protection": (250, "assumption", "Frost protection: pump enclosure and pipe lagging"),
    "acoustic_enclosure": (350, "assumption", "Acoustic enclosure for one pump"),
    "disc_filter": (200, "assumption", "Disc filter and flushing valve for a drip system"),
}
SCHEDULE = {**rc.SCHEDULE, **EXTRA_SCHEDULE}
PRICE = {k: v[0] for k, v in SCHEDULE.items()}
BUDGET = rc.BUDGET
ENERGY_CAP = rc.ENERGY_CAP_KWH_DAY
CONTINGENCY = rc.CONTINGENCY

# Hydraulics for the critical-service-flow check. course assumption.
OUTLET_HEAD_M = {"indoor": 15.0, "drip": 10.0}
FRICTION_ALLOWANCE = 0.25
PUMP_EFFICIENCY = 0.40


def head_and_power(static_lift_m, outlet="indoor", flow_lpm=20.0):
    """Total head, hydraulic and shaft power at the duty point, and duty-point kWh/kL."""
    total = (static_lift_m + OUTLET_HEAD_M[outlet]) * (1 + FRICTION_ALLOWANCE)
    q = flow_lpm / 60000.0                                  # m3/s
    hyd_w = 1000 * 9.81 * q * total
    return {"static_m": static_lift_m, "outlet_m": OUTLET_HEAD_M[outlet],
            "friction": FRICTION_ALLOWANCE, "total_head_m": round(total, 1),
            "hydraulic_w": round(hyd_w), "input_w": round(hyd_w / PUMP_EFFICIENCY),
            "duty_kwh_per_kl": round(9.81 * total / (3600 * PUMP_EFFICIENCY), 3)}


# ---------------------------------------------------------------------------
# Climate series
# ---------------------------------------------------------------------------
@dataclass
class Climate:
    name: str
    months: list
    days: list
    rain: list
    eto: list
    tmean: list
    tmin: list
    pe: list = field(default_factory=list)
    gfac: list = field(default_factory=list)

    def __post_init__(self):
        if not self.pe:
            self.pe = [sm.effective_rain(p) for p in self.rain]


def mean_climate(sid: str) -> Climate:
    home = BY_SID[sid]
    c = sm.load_climate()[home.presets["station"]]
    tmax, tmin, rain = c["tmax"][:12], c["tmin"][:12], c["rain"][:12]
    d35 = (c.get("d35") or [0] * 13)[:12]
    tmean = [(a + b) / 2 for a, b in zip(tmax, tmin)]
    eto = [sm.eto_month(c["lat"], tmax[m], tmin[m], m) for m in range(12)]
    cl = Climate("long-term mean", MONTHS[:], sm.DAYS[:], rain[:], eto, tmean, tmin[:])
    cl.gfac = [sm.growing_factor(tmean[m], d35[m]) for m in range(12)]
    return cl


def with_rain(base: Climate, rain: list, name: str, eto_scale: float = 1.0) -> Climate:
    cl = Climate(name, base.months[:], base.days[:], list(rain), [e * eto_scale for e in base.eto],
                 base.tmean[:], base.tmin[:])
    cl.gfac = base.gfac[:]
    return cl


def dry_climate(sid: str) -> Climate:
    """The synthetic dry year from make_datasets.py, preceded in the balance by mean years."""
    import make_datasets as md
    d = md.drought_years()[sid]
    return with_rain(mean_climate(sid), d["dry_year_mm"], "synthetic dry year", eto_scale=1.05)


# ---------------------------------------------------------------------------
# Decision variables
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Choice:
    """One point in the decision space: the seven decision variables."""
    new_storage_kl: float = 0.0
    zones: tuple = ()                 # roof zones connected to storage
    added_m2: float = 0.0             # cultivated area beyond the existing plantings
    crop_mix: str = "mixed"
    strategy: str = "garden"          # garden | indoor | garden_grey | indoor_grey
    modules: tuple = ()
    schedule: str = "year_round"      # year_round | fallow_peak | garden_first
    existing: bool = False            # the existing condition itself

    def describe(self) -> str:
        bits = [f"+{self.new_storage_kl:g} kL", "zones " + "+".join(sorted(self.zones)),
                f"+{self.added_m2:g} m2 {self.crop_mix}", self.strategy, self.schedule]
        if self.modules:
            bits.append("/".join(sorted(self.modules)))
        return ", ".join(bits)


STRATEGIES = {
    "garden": "Rainwater to the garden only",
    "indoor": "Rainwater to the garden and the client's permitted indoor uses",
    "garden_grey": "Rainwater to the garden, plus greywater diversion to subsurface irrigation",
    "indoor_grey": "Rainwater to the garden and permitted indoor uses, plus greywater diversion",
}
SCHEDULES = {
    "year_round": "Crop the added area all year",
    "fallow_peak": "Rest the added annual crops in the three highest-deficit months",
    "garden_first": "In the three highest-deficit months, reserve the tank for the garden and switch indoor uses to the mains",
}


def existing_choice(home) -> Choice:
    return Choice(zones=tuple(z.id for z in home.zones if z.connected_now), existing=True,
                  strategy="indoor" if not home.mains else "garden")


def priority_m2(home) -> float:
    return home.existing_irrigated_m2


def placement(home, added_m2: float) -> dict:
    """Where the added cultivated area goes: best zones first, after the existing
    plantings and the client's retained lawn. Returns {zone: m2} and the weighted quality."""
    cap = {}
    for r in home.cover:
        if r.kind == "growing":
            cap[r.id] = r.area
    for z, a in home.priority_zones:
        cap[z] -= a
    if home.retained_within_envelope_m2:
        cap["G3"] -= home.retained_within_envelope_m2          # Canberra's back lawn
    if home.shared_allocation_m2:
        cap["SG"] = home.shared_allocation_m2
    order = sorted(cap, key=lambda z: -home.zone_quality.get(z, 1.0))
    left, used = added_m2, {}
    for z in order:
        take = min(max(0.0, cap[z]), left)
        if take > 0:
            used[z] = take
            left -= take
    q = sum(home.zone_quality.get(z, 1.0) * a for z, a in used.items()) / added_m2 if added_m2 else 1.0
    return {"zones": used, "quality": q, "unplaced": left}


def added_capacity(home) -> float:
    t = totals(home)
    return max(0.0, t["cultivable_max_m2"] - priority_m2(home)) + home.shared_allocation_m2


def priority_quality(home) -> float:
    tot = sum(a for _, a in home.priority_zones)
    return sum(home.zone_quality.get(z, 1.0) * a for z, a in home.priority_zones) / tot if tot else 1.0


def _heat(mod: dict, t: float) -> float:
    below = mod.get("heat_below_c")
    return max(0.0, below - t) * mod.get("heat_kwh_per_k", 0.0) if below is not None else 0.0


def _fish_heat(t: float) -> float:
    """Tank heating when no legal species' band covers the month (site_model's rule)."""
    if any(lo <= t <= hi for lo, hi in FISH.values()):
        return 0.0
    return max(0.0, 10 - t) * sm.TANK_UA_W_PER_K * 24 / 1000


def evaluate(sid: str, ch: Choice, cl: Climate = None, spinup_years: int = 2,
             start_level_kl: float = None, spin_climate: Climate = None, demand_factor: list = None) -> dict:
    """Monthly water balance, service checks, food, nutrients, energy, cost and care."""
    home = BY_SID[sid]
    cl = cl or mean_climate(sid)
    spin = spin_climate or mean_climate(sid)
    zones = {z.id: z for z in home.zones}
    existing_kl = sum(c.kl for c in home.circles if c.kind == "tank")
    storage = existing_kl + ch.new_storage_kl
    roof = sum(zones[z].plan_m2 for z in ch.zones)
    mods = set(ch.modules)
    mix = CROP_MIXES[ch.crop_mix]
    P = priority_m2(home)
    q_p = priority_quality(home)
    place = placement(home, ch.added_m2)
    A_sg = place["zones"].get("SG", 0.0)              # Brisbane shared allocation: scheme tap water
    A = ch.added_m2 - A_sg                             # added area watered from the lot's own systems
    q_a = (sum(home.zone_quality.get(z, 1.0) * a for z, a in place["zones"].items() if z != "SG") / A) if A else 1.0
    q_sg = home.zone_quality.get("SG", 1.0)

    if ch.existing:
        tank_uses = set(home.existing_tank_uses)
    elif ch.strategy.startswith("indoor") or not home.mains:
        tank_uses = set(home.permitted_tank_uses)
    else:
        tank_uses = {"garden"} | set(home.existing_tank_uses)
    grey = ch.strategy.endswith("_grey") and not ch.existing
    bore_ok = set(home.bore_uses)
    bore_cap_year = home.presets["other_water_kl_year"]
    bore_cap_month = bore_cap_year / 12.0
    method = {"mains_sprinkler": "sprinkler", "tank_gravity": "hose"}.get(home.existing_irrigation, "drip") \
        if ch.existing else "drip"
    eff = EFFICIENCY[method]
    garden_mains_backup = ch.existing and home.mains and home.existing_irrigation in (
        "mains_sprinkler", "mains_drip", "tank_gravity")

    per_person = dict(END_USES)
    if "composting_toilet" in mods:
        per_person["toilet"] = 0.0

    def peak_months(c):
        return set(sorted(range(12), key=lambda m: -(c.eto[m] * mix["kc"] - c.pe[m]))[:3])

    def run_year(c: Climate, tank: float, factors=None):
        factors = factors or [1.0] * 12
        rows = []
        bore_left = bore_cap_year
        peak = peak_months(c)
        fallow = peak if ch.schedule == "fallow_peak" else set()
        garden_first = peak if (ch.schedule == "garden_first" and home.mains) else set()
        for m in range(12):
            d = c.days[m]
            inflow = sm.RUNOFF_A * max(0.0, c.rain[m] - sm.RUNOFF_B_MM_MONTH) * roof / 1000
            tank += inflow
            overflow = max(0.0, tank - storage)
            tank -= overflow
            # The bore pumps into the tank when there is room (the existing arrangement
            # at Alice Springs), at most one-twelfth of the allocation a month; any
            # monthly allowance left over can still serve a shortfall directly.
            bore_month = min(bore_cap_month, bore_left)
            bore_in = min(bore_month, max(0.0, storage - tank)) if bore_ok else 0.0
            tank += bore_in
            bore_month -= bore_in
            bore_left -= bore_in

            # Garden need first, so that a garden-first month can reserve the tank.
            etc_p = c.eto[m] * EXISTING_PLANTING["kc"]
            etc_a = c.eto[m] * mix["kc"]
            active_a = (1.0 - mix["perennial"]) * (0.0 if m in fallow else 1.0) + mix["perennial"]
            growing = 0.0 if c.tmean[m] < DORMANT_BELOW_C else 1.0
            gross_p = P * max(0.0, etc_p - c.pe[m]) / 1000 / eff * growing
            gross_a = A * max(0.0, etc_a - c.pe[m]) / 1000 / eff * active_a * growing
            gross_sg = A_sg * max(0.0, etc_a - c.pe[m]) / 1000 / eff * active_a * growing

            use = {u: per_person[u] * OCCUPANTS * d / 1000 * factors[m] for u in INDOOR}
            from_tank = {u: 0.0 for u in INDOOR}
            from_bore = {u: 0.0 for u in INDOOR}
            imported = 0.0
            state = {"tank": tank}

            def draw_garden(need_p, need_a):
                t_p = t_a = 0.0
                if "garden" in tank_uses:
                    t_p = min(state["tank"], need_p); state["tank"] -= t_p
                    t_a = min(state["tank"], need_a); state["tank"] -= t_a
                return t_p, t_a

            # greywater: same month only (no storage), subsurface, perennials and trees only
            grey_avail = sum(use[u] for u in GREYWATER_USES) if grey else 0.0
            g_p = min(grey_avail, gross_p * home.priority_perennial_share) if grey else 0.0
            grey_avail -= g_p
            g_a = min(grey_avail, gross_a * mix["perennial"]) if grey else 0.0
            need_p, need_a = gross_p - g_p, gross_a - g_a
            t_p = t_a = 0.0
            if m in garden_first:
                t_p, t_a = draw_garden(need_p, need_a)
                need_p -= t_p; need_a -= t_a
            elif ch.existing and home.existing_timer_share:
                # a mechanical tap timer runs the drip before the house draws water
                t_p, _ = draw_garden(need_p * home.existing_timer_share, 0.0)
                need_p -= t_p

            aqua_topup = 0.020 * d if "aquaponics" in mods else 0.0
            for u in INDOOR:
                need = use[u]
                if u in tank_uses and m not in garden_first:
                    t = min(state["tank"], need); state["tank"] -= t; from_tank[u] = t; need -= t
                if need > 0 and u in bore_ok and bore_month > 0:
                    b = min(bore_month, need); bore_month -= b; bore_left -= b; from_bore[u] = b; need -= b
                imported += need
            topup_tank = min(state["tank"], aqua_topup) if "garden" in tank_uses else 0.0
            state["tank"] -= topup_tank
            imported += aqua_topup - topup_tank

            if m not in garden_first:
                x_p, x_a = draw_garden(need_p, need_a)
                t_p += x_p; t_a += x_a
                need_p -= x_p; need_a -= x_a
            tank = state["tank"]
            b_p = b_a = 0.0
            if "garden" in bore_ok and bore_month > 0:
                b_p = min(bore_month, need_p); bore_month -= b_p; bore_left -= b_p; need_p -= b_p
                b_a = min(bore_month, need_a); bore_month -= b_a; bore_left -= b_a; need_a -= b_a
            mains_g = 0.0
            if garden_mains_backup:
                mains_g = need_p + need_a
                need_p = need_a = 0.0
            imported += mains_g + gross_sg                   # the allocation is watered from the scheme tap

            applied_p = gross_p - need_p
            applied_a = gross_a - need_a
            sat_p = min(1.0, (c.pe[m] + applied_p * eff * 1000 / P) / etc_p) if P and etc_p else 1.0
            sat_a = min(1.0, (c.pe[m] + applied_a * eff * 1000 / A) / etc_a) if A and etc_a else 1.0
            if not growing:
                sat_p = sat_a = 1.0          # dormant: nothing scheduled, nothing stressed

            # Energy, kWh for the month.
            tank_indoor = sum(from_tank.values())
            pressure_pumped = tank_indoor if (home.existing_pressure_pump or not ch.existing) else 0.0
            garden_tank = t_p + t_a
            if ch.existing:
                garden_pumped = garden_tank if (home.existing_garden_pump or home.existing_irrigation == "tank_drip") else 0.0
            else:
                garden_pumped = garden_tank
            bore_total = bore_in + sum(from_bore.values()) + b_p + b_a
            grey_used = g_p + g_a
            grey_gravity = sid == "S5"                       # elevated house: gravity diversion
            e_pump = (pressure_pumped + topup_tank) * KWH_PER_KL["pressure"] \
                + garden_pumped * KWH_PER_KL["garden"] + bore_total * KWH_PER_KL["bore"] \
                + (0.0 if grey_gravity else grey_used * KWH_PER_KL["greywater"])
            e_mod = e_mod_up = 0.0
            t_air = c.tmean[m]
            for k in mods:
                md = MODULES[k]
                if k == "mushrooms" and not any(lo <= t_air <= hi for lo, hi in MUSHROOM_BANDS):
                    continue
                steady, upper = md["kwh"]
                h = _fish_heat(t_air) if k == "aquaponics" else _heat(md, t_air)
                e_mod += (steady + h) * d
                e_mod_up += (upper + h) * d

            rows.append(dict(
                month=c.months[m], days=d, rain=c.rain[m], eto=c.eto[m], inflow=inflow, overflow=overflow,
                indoor=sum(use.values()), tank_indoor=tank_indoor, bore=bore_total,
                imported=imported, garden_gross=gross_p + gross_a, garden_grey=grey_used,
                garden_tank=garden_tank, garden_bore=b_p + b_a, garden_mains=mains_g,
                garden_unmet=need_p + need_a, garden_scheme=gross_sg,
                prio_gross=gross_p, prio_unmet=need_p, sat_p=sat_p, sat_a=sat_a, tank_end=tank,
                toilet_laundry=use["toilet"] + use["laundry"],
                toilet_laundry_tank=from_tank["toilet"] + from_tank["laundry"],
                toilet=use["toilet"], toilet_tank=from_tank["toilet"],
                energy_model=(e_pump + e_mod) / d, energy_declared=(e_pump + e_mod_up) / d,
                e_pump=e_pump / d, e_mod=e_mod_up / d))
        return rows, tank

    tank = storage / 2 if start_level_kl is None else start_level_kl
    for _ in range(spinup_years):
        _, tank = run_year(spin, tank)
    rows, _ = run_year(cl, tank, demand_factor)
    fallow = peak_months(cl) if ch.schedule == "fallow_peak" else set()

    # ---- food, protein and nutrients --------------------------------------------------
    season = sum(cl.gfac) / 12
    act = [(1.0 - mix["perennial"]) * (0.0 if m in fallow else 1.0) + mix["perennial"] for m in range(12)]
    yf_p = sum(cl.gfac[m] * rows[m]["sat_p"] for m in range(12)) / 12 * q_p
    yf_a = sum(cl.gfac[m] * rows[m]["sat_a"] * act[m] for m in range(12)) / 12 * q_a
    yf_sg = sum(cl.gfac[m] * act[m] for m in range(12)) / 12 * q_sg
    kcal_p = P * EXISTING_PLANTING["kcal_m2"] * yf_p
    kcal_a = A * mix["kcal_m2"] * yf_a + A_sg * mix["kcal_m2"] * yf_sg
    kg_fresh = kcal_p / EXISTING_PLANTING["kcal_per_kg"] + kcal_a / mix["kcal_per_kg"]
    protein_kg = (kcal_p * EXISTING_PLANTING["protein_g_100kcal"] + kcal_a * mix["protein_g_100kcal"]) / 1e5
    monthly_output = [cl.gfac[m] * (P * q_p * rows[m]["sat_p"] * EXISTING_PLANTING["kcal_m2"]
                                    + (A * q_a * rows[m]["sat_a"] + A_sg * q_sg) * mix["kcal_m2"] * act[m]) / 12
                      for m in range(12)]

    fish_protein, insect_share, mushrooms_kg, aqua_kcal = 0.0, None, 0.0, 0.0
    bsf = max(sum(max(0.0, min(1.0, (t - sm.BSF_LOWER_C) / (sm.BSF_OPT_C - sm.BSF_LOWER_C))) for t in cl.tmean) / 12,
              sm.INDOOR_REARING_FACTOR)
    larvae_dm = (sm.HOUSEHOLD_FOOD_WASTE_KG_PP_YR * OCCUPANTS * sm.PLANT_BASED_WASTE_SHARE * sm.FOOD_WASTE_DM
                 * sm.BSF_BIOCONVERSION_DM * bsf) if "insects" in mods else 0.0
    if "aquaponics" in mods:
        fish_months = sum(1 for t in cl.tmean if any(lo <= t <= hi for lo, hi in FISH.values()))
        feed = 4 * sm.FEED_G_M2_D * 365 * max(fish_months, 7) / 12 / 1000
        insect_share = min(1.0, larvae_dm / (feed * 0.9)) if feed else 0.0
        fish_protein = feed / sm.FCR * sm.FILLET_YIELD * sm.FILLET_PROTEIN * insect_share
        aqua_kcal = 4 * CROP_MIXES["leafy"]["kcal_m2"] * season
    if "mushrooms" in mods:
        fruiting = sum(1 for t in cl.tmean if any(lo <= t <= hi for lo, hi in MUSHROOM_BANDS))
        mushrooms_kg = 10.0 * 0.70 * fruiting        # 10 kg dry straw a month at 70 % BE [S23b]
    kcal_total = kcal_p + kcal_a + aqua_kcal + mushrooms_kg * 330
    protein_kg += fish_protein + mushrooms_kg * 0.0331 + aqua_kcal * CROP_MIXES["leafy"]["protein_g_100kcal"] / 1e5

    food_n = 2.3                                     # course assumption: 380 kg/yr food waste at 0.6 % N wet
    n_rec = 0.0
    if mods & {"compost", "insects", "digester"}:
        n_rec += food_n * 0.6
    else:
        n_rec += food_n * 0.3                        # the existing bins or tumbler
    if "composting_toilet" in mods:
        n_rec += sm.HOUSEHOLD_N_KG_YEAR * 0.6
    uptake = (P * yf_p + A * yf_a + A_sg * yf_sg) / season * sm.GARDEN_N_CAPACITY_KG_M2 if season else 0.0
    n_applied = min(n_rec, uptake)

    S = lambda k: sum(r[k] for r in rows)
    onsite = S("tank_indoor") + S("bore") + S("garden_grey") + S("garden_tank")
    garden_need = S("garden_gross")
    garden_onsite = S("garden_grey") + S("garden_tank") + S("garden_bore")
    peak_i = max(range(12), key=lambda m: rows[m]["energy_declared"])

    # ---- capital ------------------------------------------------------------------------
    bill = []

    def add(key, qty, label=None, unit="ea"):
        if qty > 0:
            bill.append({"key": key, "line": label or SCHEDULE[key][2], "qty": qty, "unit": unit,
                         "cost": round(PRICE[key] * qty)})

    pumps = 0
    if not ch.existing:
        if ch.new_storage_kl > 0:
            if home.storage_kind == "slimline":
                add("slimline_tank_per_kl", ch.new_storage_kl, unit="kL")
                add("slimline_establishment", math.ceil(ch.new_storage_kl / 2.0), unit="module")
            else:
                add("tank_shell_per_kl", ch.new_storage_kl, unit="kL")
                add("tank_establishment", math.ceil(ch.new_storage_kl / rc.MAX_TANK_KL), unit="tank")
        newly = [zones[z] for z in ch.zones if not zones[z].connected_now]
        add("zone_reconnection", len(newly), unit="zone")
        add("first_flush_per_downpipe", sum(max(1, len(z.downpipes)) for z in newly), unit="downpipe")
        if home.mains and ch.strategy.startswith("indoor") and not home.existing_pressure_pump:
            add("pump", 1, "Pressure pump for the indoor non-potable supply")
            add("mains_changeover", 1)
            pumps += 1
        if not (home.existing_garden_pump or home.existing_irrigation == "tank_drip"):
            add("pump", 1, "Garden transfer pump")
            pumps += 1
        existing_drip = home.existing_irrigated_m2 if home.existing_irrigation in ("tank_drip", "mains_drip") else 0.0
        add("drip_per_m2", round(max(0.0, P + A - existing_drip)), unit="m2")
        if grey:
            add("greywater_diversion", 1)
        for k in sorted(mods):
            for key, n in MODULES[k]["capital"]:
                add(key, n)
        if sid == "S1" and pumps:
            add("frost_protection", 1)
        if sid == "S3" and pumps + grey:
            add("acoustic_enclosure", pumps + (1 if grey else 0), unit="pump")
        if sid == "S5":
            add("overflow_discharge", 1)
        if sid == "S2" and A > 0:
            add("disc_filter", 1)
    subtotal = sum(b["cost"] for b in bill)
    contingency = round(subtotal * CONTINGENCY)
    capital = subtotal + contingency

    # ---- running cost, maintenance, attendance -----------------------------------------
    energy_kwh_year = sum(rows[m]["energy_model"] * cl.days[m] for m in range(12))
    water_cost = (S("imported") - S("garden_scheme")) * WATER_PRICE[sid]
    consumables = sum(MODULES[k]["consumables"] for k in mods)
    new_filter = (not ch.existing) and home.mains and ch.strategy.startswith("indoor")
    if home.existing_pressure_pump or new_filter:
        consumables += 60                             # cartridge filter train
    if grey:
        consumables += 30
    running = energy_kwh_year * TARIFF_KWH + water_cost + consumables
    hours = 4 + 1.5 * len(ch.zones) + P * EXISTING_PLANTING["labour_h_m2"] + ch.added_m2 * mix["labour_h_m2"] \
        + sum(MODULES[k]["hours"] for k in mods) + (8 if grey else 0)
    attendance = min([MODULES[k]["attendance"] for k in mods] + [7 if (P + ch.added_m2) else 30])
    absence_ok = all(MODULES[k]["pausable"] or MODULES[k].get("tolerance", 0) >= home.unattended_days
                     for k in mods)
    new_running = (energy_kwh_year * TARIFF_KWH + consumables) if not ch.existing else 0.0

    res = {
        "choice": ch.describe() if not ch.existing else "existing condition",
        "climate": cl.name,
        "storage_kl": round(storage, 1), "roof_connected_m2": round(roof, 1),
        "cultivated_m2": round(P + ch.added_m2, 1), "added_m2": ch.added_m2,
        "placement": {k: round(v, 1) for k, v in place["zones"].items()},
        "monthly": [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()} for r in rows],
        "inflow_kl": round(S("inflow"), 1), "overflow_kl": round(S("overflow"), 1),
        "indoor_kl": round(S("indoor"), 1), "tank_indoor_kl": round(S("tank_indoor"), 1),
        "bore_kl": round(S("bore"), 1), "imported_kl": round(S("imported") - S("garden_scheme"), 1),
        "scheme_water_kl": round(S("garden_scheme"), 1),
        "garden_need_kl": round(garden_need, 1), "garden_onsite_kl": round(garden_onsite, 1),
        "garden_mains_kl": round(S("garden_mains"), 1), "garden_grey_kl": round(S("garden_grey"), 1),
        "garden_unmet_kl": round(S("garden_unmet"), 1),
        "priority_months_full": sum(1 for r in rows if r["sat_p"] >= 0.995),
        "priority_share": round(1 - S("prio_unmet") / S("prio_gross"), 3) if S("prio_gross") else 1.0,
        "priority_sat_min": round(min(r["sat_p"] for r in rows), 3),
        "water_closure": round(onsite / (onsite + S("imported")), 3) if onsite + S("imported") else 1.0,
        "garden_water_satisfaction": round(garden_onsite / garden_need, 3) if garden_need else 1.0,
        "food_kcal": round(kcal_total), "fresh_kg": round(kg_fresh + mushrooms_kg),
        "food_energy_closure": round(kcal_total / sm.HOUSEHOLD_KCAL_YEAR, 4),
        "protein_kg": round(protein_kg, 1),
        "protein_closure": round(protein_kg / sm.HOUSEHOLD_PROTEIN_KG_YEAR, 4),
        "producing_months": sum(1 for v in monthly_output if max(monthly_output) and v >= 0.3 * max(monthly_output)),
        "n_recovered_kg": round(n_rec, 2), "n_uptake_kg": round(uptake, 2), "n_applied_kg": round(n_applied, 2),
        "nutrient_closure": round(n_applied / sm.HOUSEHOLD_N_KG_YEAR, 3),
        "insect_share_of_fish_feed": None if insect_share is None else round(insect_share, 2),
        "peak_month": rows[peak_i]["month"],
        "energy_peak_modelled": round(rows[peak_i]["energy_model"], 2),
        "energy_peak_declared": round(rows[peak_i]["energy_declared"], 2),
        "energy_kwh_year": round(energy_kwh_year),
        "bill": bill, "capital_subtotal": subtotal, "capital_contingency": contingency, "capital": capital,
        "running_year": round(running), "running_energy": round(energy_kwh_year * TARIFF_KWH),
        "running_water": round(water_cost), "running_consumables": consumables,
        "new_running_year": round(new_running),
        "maintenance_h_year": round(hours, 1), "attendance_days": attendance, "absence_ok": absence_ok,
    }
    res["fits_budget"] = capital <= BUDGET
    res["fits_energy"] = res["energy_peak_declared"] <= ENERGY_CAP
    res["fits_maintenance"] = hours <= home.maintenance_h_week * 52 + 1e-9
    res["fits_attendance"] = attendance >= home.min_attendance_days
    res["fits_absence"] = absence_ok
    return res


# ---------------------------------------------------------------------------
# Client priority service targets. Thresholds were set from this model so that a
# feasible option exists with a real margin (see `staff_check`), not as aspirations.
# ---------------------------------------------------------------------------
def _summer_share(res, months):
    """Share of the existing plantings' irrigation need met from on-site water."""
    rows = [r for r in res["monthly"] if r["month"] in months]
    need = sum(r["prio_gross"] for r in rows)
    mains = sum(r["garden_mains"] for r in rows)
    got = need - sum(r["prio_unmet"] for r in rows) - mains
    return max(0.0, got) / need if need else 1.0


def _share(res, months, num, den):
    rows = [r for r in res["monthly"] if r["month"] in months]
    d = sum(r[den] for r in rows)
    return sum(r[num] for r in rows) / d if d else 1.0


TARGETS = {
    "S1": [
        dict(id="T1", metric="priority_months_full", text="The raised beds and fruit trees (45 m²) fully watered from on-site water, with no mains irrigation, in every month of the average year",
             test=lambda r: r["priority_months_full"] == 12 and r["garden_mains_kl"] == 0),
        dict(id="T2", metric="winter_toilet_laundry", text="Toilet and laundry supplied at least 90 % from rainwater in June, July and August",
             test=lambda r: _share(r, ["Jun", "Jul", "Aug"], "toilet_laundry_tank", "toilet_laundry") >= 0.90),
        dict(id="T3", metric="structural", text="Everything installed keeps working through a Canberra July: pumps and exposed pipework frost-protected, and the energy check made in the peak month",
             test=lambda r: True),
        dict(id="T4", metric="care", text="At least 100 m² of the back lawn kept; at most 2 hours of care a week, none of it needed more often than weekly",
             test=lambda r: r["fits_maintenance"] and r["fits_attendance"]),
    ],
    "S2": [
        dict(id="T1", metric="imported_kl", text="Carted water cut to 40 kL a year or less in the average year",
             test=lambda r: r["imported_kl"] <= 40),
        dict(id="T2", metric="bore_kl", text="Bore draw within the 100 kL allocation, and never more than one-twelfth of it in a month",
             test=lambda r: r["bore_kl"] <= 100.0 + 1e-6),
        dict(id="T3", metric="priority_share", text="The shade-house vegetables and fruit block (90 m²) given at least 45 % of their yearly irrigation need from on-site water",
             test=lambda r: r["priority_share"] >= 0.45),
        dict(id="T4", metric="structural", text="Every pump, filter and fitting a type stocked in Alice Springs",
             test=lambda r: True),
    ],
    "S3": [
        dict(id="T1", metric="toilet_share", text="At least 70 % of toilet flushing supplied from rainwater in the average year",
             test=lambda r: _share(r, MONTHS, "toilet_tank", "toilet") >= 0.70 or r["monthly"][0]["toilet"] == 0),
        dict(id="T2", metric="fresh_kg", text="At least 120 kg of fresh produce a year from the lot and the shared-garden allocation together",
             test=lambda r: r["fresh_kg"] >= 120),
        dict(id="T3", metric="priority_months_full", text="The existing beds (12 m²) fully watered from rainwater in at least 9 months of the average year",
             test=lambda r: r["priority_months_full"] >= 9),
        dict(id="T4", metric="care", text="Nothing audible above 45 dB(A) at a boundary at night, everything delivered through the 600 mm path, the courtyard sitting area kept, and at most 3 hours of care a week",
             test=lambda r: r["fits_maintenance"]),
    ],
    "S4": [
        dict(id="T1", metric="summer_share", text="The vegetable beds and fruit trees (56 m²) at least 90 % watered from on-site water across December to February",
             test=lambda r: _summer_share(r, ["Dec", "Jan", "Feb"]) >= 0.90),
        dict(id="T2", metric="new_running_year", text="New running costs of $250 a year or less, stated in dollars",
             test=lambda r: r["new_running_year"] <= 250),
        dict(id="T3", metric="producing_months", text="The garden producing in at least 10 months of the average year",
             test=lambda r: r["producing_months"] >= 10),
        dict(id="T4", metric="care", text="The back lawn kept; at most 3 hours of routine care a week",
             test=lambda r: r["fits_maintenance"]),
    ],
    "S5": [
        dict(id="T1", metric="imported_kl", text="Carted water cut to 20 kL a year or less in the average year",
             test=lambda r: r["imported_kl"] <= 20.5),
        dict(id="T2", metric="absence", text="Everything runs unattended through a four-week absence in July, with no delivery needed that month",
             test=lambda r: r["fits_absence"] and next(m for m in r["monthly"] if m["month"] == "Jul")["imported"] <= 0.5),
        dict(id="T3", metric="structural", text="Overflow taken to a nominated discharge point away from the piers",
             test=lambda r: any(b["key"] == "overflow_discharge" for b in r["bill"])),
        dict(id="T4", metric="dry_share", text="The main garden (120 m²) at least 60 % watered from on-site water through the dry season, May to October",
             test=lambda r: _summer_share(r, ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]) >= 0.60),
    ],
}


def meets_targets(sid: str, res: dict) -> dict:
    return {t["id"]: bool(t["test"](res)) for t in TARGETS[sid]}


def feasible(sid: str, res: dict) -> bool:
    return (res["fits_budget"] and res["fits_energy"] and res["fits_maintenance"]
            and res["fits_attendance"] and res["fits_absence"] and all(meets_targets(sid, res).values()))


# ---------------------------------------------------------------------------
# The decision space. Discrete, small, and bounded by what exists on each property.
# ---------------------------------------------------------------------------
STORAGE_STEPS = {
    "S1": [0, 5, 10, 15, 20],
    "S2": [0, 10, 22.5, 45, 67.5, 90],
    "S3": [0, 2, 4],
    "S4": [0, 5, 10, 15],
    "S5": [0, 22.5, 45, 67.5, 90, 112.5],
}
AREA_FRACTIONS = [0.0, 0.25, 0.5, 0.75, 1.0]
MODULE_SETS = [(), ("compost",), ("compost", "composting_toilet"), ("compost", "insects"),
               ("compost", "mushrooms"), ("compost", "insects", "aquaponics"), ("digester",),
               ("compost", "composting_toilet", "insects")]


def zone_sets(home):
    now = tuple(z.id for z in home.zones if z.connected_now)
    extra = sorted((z for z in home.zones if not z.connected_now and z.gutter), key=lambda z: -z.plan_m2)
    return [now + tuple(z.id for z in extra[:k]) for k in range(len(extra) + 1)]


def decision_space(home):
    room = added_capacity(home)
    areas = sorted({round(room * f) for f in AREA_FRACTIONS})
    strategies = STRATEGIES if home.mains else ("indoor", "indoor_grey")
    schedules = SCHEDULES if home.mains else ("year_round", "fallow_peak")
    for kl, zs, a, mix, strat, mods, sch in itertools.product(
            STORAGE_STEPS[home.sid], zone_sets(home), areas, CROP_MIXES, strategies, MODULE_SETS, schedules):
        if a == 0 and (mix != "mixed" or sch == "fallow_peak"):
            continue
        if sch == "garden_first" and not strat.startswith("indoor"):
            continue
        yield Choice(kl, zs, a, mix, strat, mods, sch)


OBJECTIVES = [("capital", -1), ("running_year", -1), ("maintenance_h_year", -1), ("imported_kl", -1),
              ("food_kcal", +1), ("garden_water_satisfaction", +1)]


def dominated(a: dict, b: dict) -> bool:
    """True if b is at least as good as a on every objective and better on one."""
    ge = all((b[k] - a[k]) * s >= -1e-9 for k, s in OBJECTIVES)
    gt = any((b[k] - a[k]) * s > 1e-9 for k, s in OBJECTIVES)
    return ge and gt


def pareto(results):
    return [r for r in results if not any(dominated(r, o) for o in results if o is not r)]


def staff_check(sid: str) -> dict:
    """Existing condition, then every feasible option: the cheapest demonstrates that the
    client targets are attainable, and the margin says by how much."""
    home = BY_SID[sid]
    base = evaluate(sid, existing_choice(home))
    feas = []
    for ch in decision_space(home):
        r = evaluate(sid, ch)
        if feasible(sid, r):
            r["_choice"] = ch
            feas.append(r)
    feas.sort(key=lambda r: (r["capital"], r["running_year"]))
    front = pareto(feas)
    cheapest = feas[0] if feas else None
    out = {"existing": base, "existing_targets": meets_targets(sid, base), "n_feasible": len(feas),
           "n_pareto": len(front)}
    if cheapest:
        dry = evaluate(sid, cheapest["_choice"], dry_climate(sid))
        out["cheapest"] = {k: v for k, v in cheapest.items() if k != "_choice"}
        out["cheapest_dry"] = dry
        out["margin"] = {"budget": BUDGET - cheapest["capital"],
                         "energy": round(ENERGY_CAP - cheapest["energy_peak_declared"], 2)}
        out["cheapest_choice"] = cheapest["_choice"].__dict__
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    only = sys.argv[1:] or [h.sid for h in HOMES]
    for sid in only:
        h = BY_SID[sid]
        base = evaluate(sid, existing_choice(h))
        print(f"\n{sid} {h.family}: existing  import {base['imported_kl']} kL  bore {base['bore_kl']}  "
              f"garden mains {base['garden_mains_kl']}  prio months {base['priority_months_full']}  "
              f"E {base['energy_peak_declared']} ({base['peak_month']})  running ${base['running_year']}  "
              f"hours {base['maintenance_h_year']}  targets {meets_targets(sid, base)}")
        chk = staff_check(sid)
        print(f"   feasible options {chk['n_feasible']}, Pareto {chk['n_pareto']}")
        if "cheapest" in chk:
            c = chk["cheapest"]
            print(f"   cheapest: {c['choice']}")
            print(f"     capital ${c['capital']:,}  margin ${chk['margin']['budget']:,}  E {c['energy_peak_declared']} "
                  f"({c['peak_month']}) margin {chk['margin']['energy']}  running ${c['running_year']}  "
                  f"hours {c['maintenance_h_year']}  import {c['imported_kl']}  kcal {c['food_kcal']}  fresh {c['fresh_kg']} kg")
            d = chk["cheapest_dry"]
            print(f"     dry year: import {d['imported_kl']}  prio months {d['priority_months_full']}  targets {meets_targets(sid, d)}")
