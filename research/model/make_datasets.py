"""Generate the course's synthetic teaching datasets.

Everything written here is SYNTHETIC. The drought years are derived from each
site's Bureau of Meteorology monthly statistics by scaling toward a low decile
and perturbing with a fixed seed; they are not historical droughts and must never
be described as one. The aquaponic log is constructed from the textbook shape of
a nitrogen cycle with one fault deliberately introduced, so that the dataset has a
diagnosable answer.

Deterministic: the same seed produces the same files every run.

Run:  python make_datasets.py
  -> ../../src/data/datasets.json
  -> ../../public/data/*.csv
"""

import csv
import json
import os
import random

import site_model as sm
from presets import V4

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "src", "data")
PUBLIC = os.path.join(REPO, "public", "data")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

SHORT = {"S1": "canberra", "S2": "alice-springs", "S3": "brisbane", "S4": "adelaide", "S5": "darwin"}
LABEL = {"S1": "Canberra", "S2": "Alice Springs", "S3": "Brisbane", "S4": "Adelaide", "S5": "Darwin"}


def drought_years():
    """A dry year per site: annual total pulled to ~55-65 % of the mean, with the
    driest quarter cut hardest, because that is where a design actually fails."""
    rng = random.Random(4761)
    clim = sm.load_climate()
    out = {}
    for site in V4:
        rain = clim[site.station]["rain"][:12]
        order = sorted(range(12), key=lambda m: rain[m])
        driest = set(order[:4])
        dry = []
        for m in range(12):
            # Dry months lose more of their (already small) total than wet months.
            factor = rng.uniform(0.20, 0.45) if m in driest else rng.uniform(0.50, 0.80)
            dry.append(round(rain[m] * factor, 1))
        total, mean_total = sum(dry), sum(rain)
        out[site.sid] = {
            "site": LABEL[site.sid],
            "station": site.station,
            "mean_year_mm": [round(r, 1) for r in rain],
            "dry_year_mm": dry,
            "mean_annual_mm": round(mean_total),
            "dry_annual_mm": round(total),
            "share_of_mean": round(total / mean_total, 2),
        }
    return out


def aquaponic_log():
    """Sixty days of a cycling 1,000 L system with one fault.

    Days 1-24 are an ordinary cycle: ammonia rises then falls as Nitrosomonas
    establish, nitrite rises then falls as Nitrobacter follow, nitrate accumulates.
    From day 25 the fault: carbonate hardness is never replenished, nitrification
    acidifies the water, pH falls through 6.4 and nitrite oxidation stalls. Nitrite
    climbs back while ammonia stays low, which is the signature. A KH correction on
    day 46 recovers it.
    """
    rng = random.Random(589)
    rows = []
    for d in range(1, 61):
        if d <= 8:
            nh3 = 0.4 + 0.42 * d
            no2 = 0.05 * d
            no3 = 0.5 + 0.3 * d
            kh = 82 - 1.1 * d
        elif d <= 16:
            nh3 = max(0.15, 3.8 - 0.42 * (d - 8))
            no2 = 0.4 + 0.55 * (d - 8)
            no3 = 2.9 + 1.4 * (d - 8)
            kh = 73 - 1.6 * (d - 8)
        elif d <= 24:
            nh3 = max(0.05, 0.45 - 0.05 * (d - 16))
            no2 = max(0.05, 4.8 - 0.62 * (d - 16))
            no3 = 14 + 2.1 * (d - 16)
            kh = 60 - 2.2 * (d - 16)
        elif d <= 45:
            # The fault window: KH exhausted, pH falling, nitrite oxidation stalling.
            nh3 = 0.06 + 0.012 * (d - 24)
            no2 = 0.08 + 0.29 * (d - 24)
            no3 = 31 + 0.5 * (d - 24)
            kh = max(8, 42 - 1.7 * (d - 24))
        else:
            # Day 46: carbonate buffer restored. Recovery over about a fortnight.
            nh3 = max(0.04, 0.32 - 0.02 * (d - 45))
            no2 = max(0.05, 6.2 - 0.42 * (d - 45))
            no3 = 41 + 1.6 * (d - 45)
            kh = min(78, 12 + 4.6 * (d - 45))

        ph = 6.0 + 0.0135 * kh + rng.uniform(-0.04, 0.04)
        temp = 22.4 + 1.5 * (0.5 - abs((d % 14) - 7) / 14) + rng.uniform(-0.35, 0.35)
        note = ""
        if d == 1:
            note = "system started; 12 fish stocked, feeding 40 g/day"
        elif d == 25:
            note = "feed increased to 60 g/day"
        elif d == 46:
            note = "operator added carbonate buffer"
        rows.append({
            "day": d,
            "temp_c": round(temp, 1),
            "ph": round(ph, 2),
            "kh_mg_l_caco3": round(max(4, kh + rng.uniform(-1.5, 1.5))),
            "ammonia_mg_l": round(max(0.02, nh3 + rng.uniform(-0.03, 0.03)), 2),
            "nitrite_mg_l": round(max(0.02, no2 + rng.uniform(-0.06, 0.06)), 2),
            "nitrate_mg_l": round(max(0.3, no3 + rng.uniform(-0.7, 0.7)), 1),
            "note": note,
        })
    return rows


def main():
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(PUBLIC, exist_ok=True)
    dry = drought_years()
    log = aquaponic_log()

    payload = {
        "label": "SYNTHETIC DATA. Generated by research/model/make_datasets.py. Not measurements.",
        "drought_years": {
            "what_it_is": (
                "A dry year for each site, derived from that site's Bureau of Meteorology "
                "monthly rainfall statistics by scaling each month toward a low decile and "
                "perturbing with a fixed seed. The driest four months are cut hardest."
            ),
            "what_it_is_not": (
                "A historical drought. No year in these sites' records is reproduced here, "
                "and nothing in this dataset should be described as observed rainfall."
            ),
            "months": MONTHS,
            "sites": dry,
        },
        "aquaponic_log": {
            "what_it_is": (
                "Sixty days of water chemistry from a 1,000 L system with a 4 m2 grow bed, "
                "constructed from the textbook shape of a nitrogen cycle with one fault "
                "deliberately introduced so that the dataset has a diagnosable answer."
            ),
            "what_it_is_not": (
                "A measured log from a real system. The noise is generated, not observed."
            ),
            "columns": ["day", "temp_c", "ph", "kh_mg_l_caco3", "ammonia_mg_l", "nitrite_mg_l", "nitrate_mg_l", "note"],
            "rows": log,
        },
    }
    with open(os.path.join(DATA, "datasets.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1)
        f.write("\n")

    with open(os.path.join(PUBLIC, "SYNTHETIC-aquaponic-cycling-log.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["# SYNTHETIC DATA - generated, not measured. SLOP4761."])
        w.writerow(payload["aquaponic_log"]["columns"])
        for r in log:
            w.writerow([r[c] for c in payload["aquaponic_log"]["columns"]])

    for sid, d in dry.items():
        path = os.path.join(PUBLIC, f"SYNTHETIC-dry-year-{SHORT[sid]}.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow([f"# SYNTHETIC DATA - derived from BoM station {d['station']} statistics, not an observed year. SLOP4761."])
            w.writerow(["month", "mean_year_rain_mm", "dry_year_rain_mm"])
            for i, m in enumerate(MONTHS):
                w.writerow([m, d["mean_year_mm"][i], d["dry_year_mm"][i]])

    print(f"wrote src/data/datasets.json and {1 + len(dry)} CSV files in public/data/")
    for sid, d in dry.items():
        print(f"  {LABEL[sid]:14} mean {d['mean_annual_mm']:>5} mm -> dry {d['dry_annual_mm']:>5} mm ({d['share_of_mean']:.0%})")


if __name__ == "__main__":
    main()
