"""The measurement programme's price list, a demonstrated plan under the allowance, and a
staff check that a comparable plan fits at every client home.

The fictional Household Resilience Loan Programme funds preliminary investigation
separately from the $30,000 implementation allowance: a common $1,500 allowance for
measurement equipment and services. Consultant labour is scheduled in hours and not
charged. Every price here is a course assumption for that fictional programme.

The course promised to demonstrate one feasible plan under $1,500 before publishing the
exercise. That demonstration is on the Wattle Street practice house and is published in
week 6. The per-home plans below are a staff check only: they show the allowance is
workable at each home, and they are deliberately not published, because designing them
is Assignment 1.

Run:  python measurement.py  -> ../../src/data/measurement.json and output/measurement-check.md
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ALLOWANCE = 1500

SCHEDULE = [
    ("M01", "Tipping-bucket rain gauge with logger", 190, "each", "rain, event intensity"),
    ("M02", "Manual rain gauge, read by the household", 25, "each", "rain, daily; a cross-check on M01"),
    ("M03", "Tank level logger (pressure transducer)", 240, "each", "stored volume, inflow and draw by difference"),
    ("M04", "Inline pulse water meter, 20 mm, with logger", 180, "each", "flow on one line, such as a garden or laundry supply"),
    ("M05", "Optical pulse reader and logger for an existing meter", 150, "each", "whole-house or bore flow at 10 s resolution"),
    ("M06", "Clamp-on ultrasonic flow logger, hire", 70, "week", "short campaigns on pipes that cannot be cut"),
    ("M07", "Pressure logger", 160, "each", "pump cut-in and cut-out, fixture pressure"),
    ("M08", "Soil laboratory panel, one composite sample", 95, "sample", "texture, pH, EC, organic carbon, nitrate, phosphorus"),
    ("M09", "Soil moisture sensor with logger", 150, "each", "irrigation response, one depth"),
    ("M10", "Water chemistry panel", 85, "sample", "hardness, dissolved solids, pH, iron, turbidity"),
    ("M11", "E. coli and total coliforms", 70, "sample", "microbial quality"),
    ("M12", "Temperature logger (air or water)", 55, "each", "frost exposure, tank or chamber temperature"),
    ("M13", "Sun-path survey kit, hire", 60, "visit", "direct-sun hours by zone and season"),
    ("M14", "Scales and labelled bins for a food-waste audit", 40, "set", "food and garden waste by stream"),
    ("M15", "Plug-in energy meter", 35, "each", "one appliance or pump on a plug"),
    ("M16", "Circuit energy monitor, installed", 220, "each", "a hard-wired pump or circuit"),
    ("M17", "Logger data service", 120, "year", "remote download; optional if loggers are read by hand"),
    ("M18", "Calibration kit: graduated container, reference gauge, stopwatch", 40, "set", "field checks of meters and gauges"),
]
PRICE = {k: p for k, _, p, _, _ in SCHEDULE}

PRACTICE_PLAN = [
    ("M01", 1, "Rain at the back fence, clear of the shed and trees"),
    ("M02", 1, "Beside M01; the household reads it on weekdays"),
    ("M03", 1, "Existing 5 kL tank"),
    ("M05", 1, "Mains meter at the street"),
    ("M04", 1, "Garden tap line, so garden use separates from indoor use"),
    ("M08", 3, "Back beds, front garden, east strip"),
    ("M11", 2, "Tank, once after a dry spell and once two days after heavy rain"),
    ("M12", 1, "Air temperature at the back beds"),
    ("M14", 1, "Four one-week audits, one a season"),
    ("M18", 1, "Quarterly checks of M01 and both meters"),
]
PRACTICE_LEFT_OUT = [
    ("M17", "Loggers are downloaded by hand at the monthly visit, which the hours schedule already carries."),
    ("M09", "Gravimetric soil moisture samples at the monthly visit answer the same question for no equipment cost."),
    ("M15", "There is no pump at Wattle Street yet, so there is nothing to meter."),
]
PRACTICE_HOURS = [
    ("Installation and baseline survey", 1, 8.0),
    ("Monthly visit: download, gauge read, soil sample", 12, 1.5),
    ("Quarterly calibration check", 4, 2.0),
    ("Food-waste audit week: briefing and analysis", 4, 2.0),
    ("Soil sampling for the laboratory panel", 1, 3.0),
    ("Water sampling runs", 2, 1.0),
    ("Monthly data processing and quality control", 12, 2.0),
    ("Handover report", 1, 6.0),
]

# Staff check: a comparable plan at each client home. NOT published (it is A1's answer).
STAFF = {
    "S1": [("M01", 1), ("M03", 1), ("M05", 1), ("M04", 1), ("M08", 4), ("M12", 2), ("M11", 2), ("M14", 1), ("M18", 1)],
    "S2": [("M01", 1), ("M03", 1), ("M04", 1), ("M05", 1), ("M10", 2), ("M11", 1), ("M08", 3), ("M14", 1), ("M18", 1)],
    "S3": [("M01", 1), ("M03", 1), ("M05", 1), ("M08", 3), ("M13", 2), ("M11", 1), ("M14", 1), ("M18", 1)],
    "S4": [("M01", 1), ("M03", 1), ("M05", 1), ("M04", 1), ("M08", 3), ("M09", 1), ("M14", 1), ("M18", 1), ("M15", 1)],
    "S5": [("M01", 1), ("M03", 2), ("M04", 1), ("M08", 3), ("M11", 2), ("M14", 1), ("M18", 1)],
}


def cost(plan):
    return sum(PRICE[k] * n for k, n, *_ in plan)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    practice_cost = cost(PRACTICE_PLAN)
    assert practice_cost <= ALLOWANCE, practice_cost
    hours = sum(n * h for _, n, h in PRACTICE_HOURS)
    staff = {sid: cost(p) for sid, p in STAFF.items()}
    assert all(c <= ALLOWANCE for c in staff.values()), staff
    data = {
        "allowance": ALLOWANCE,
        "schedule": [{"key": k, "item": i, "price": p, "unit": u, "measures": m} for k, i, p, u, m in SCHEDULE],
        "practice_plan": {
            "lines": [{"key": k, "item": next(s[1] for s in SCHEDULE if s[0] == k), "qty": n,
                       "unit_price": PRICE[k], "cost": PRICE[k] * n, "where": w} for k, n, w in PRACTICE_PLAN],
            "total": practice_cost, "headroom": ALLOWANCE - practice_cost,
            "left_out": [{"key": k, "why": w} for k, w in PRACTICE_LEFT_OUT],
            "hours": [{"task": t, "times": n, "hours_each": h, "hours": n * h} for t, n, h in PRACTICE_HOURS],
            "hours_total": hours,
        },
        "staff_check_note": "A comparable plan was costed at each client home and fits the allowance; the plans are not published because designing them is Assignment 1.",
        "staff_check_max": max(staff.values()),
    }
    with open(os.path.join(REPO, "src", "data", "measurement.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    lines = ["# Measurement allowance: staff check (not published)", "",
             f"Allowance ${ALLOWANCE:,}. Practice plan ${practice_cost:,} ({hours:.0f} h of consultant time).", "",
             "| Home | Plan | Cost | Headroom |", "|---|---|---|---|"]
    for sid, p in STAFF.items():
        lines.append(f"| {sid} | " + ", ".join(f"{k}x{n}" for k, n in p) + f" | ${staff[sid]:,} | ${ALLOWANCE - staff[sid]:,} |")
    with open(os.path.join(HERE, "output", "measurement-check.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
