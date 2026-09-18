# Assignment 2 research: closed-loop household course

The evidence base behind SLOP4761. Everything here is background working material: the
student-facing course is the site under `src/`. Paths below are relative to this directory.

**Status (2026-09-18, second draft):** the course is now an engineering optimisation course
told through a consultancy case on five fixed homes. `course-design.md` §0 lists what the
second draft changes. The first draft's screening model is kept for the diagnostic bands;
the client cases, the scenario engine, the synthetic Release B year and the practice house
are new. Every figure the site publishes is exported to `../src/data/*.json`, so no page
retypes a number the model produced. Verification against primary sources is in
`verification-log.md`.

## Files

| File | What it is |
|---|---|
| `course-design.md` | **Start here.** The revised course design: sites, metrics, weeks, assessment, open decisions |
| `critique-log.md` | Every issue found in the planning draft, the evidence, the change, and before/after numbers; fairness acceptance criteria |
| `findings.md` | Condensed evidence by domain: household demand, climate, food, water, waste, energy, fairness precedents |
| `sources.md` | Bibliography with keys `[Sxx]`, access type (primary or summary) and confidence |
| `model/site_model.py` | Screening model: FAO-56 ETo, enHealth tank balance, reference designs, fairness screen |
| `model/presets.py` | Preset sets v1 (draft) → v4 (final) |
| `model/search_presets.py` | Constrained search for the most balanced realistic presets |
| `model/sensitivity.py` | Stress test of the reference bands under 11 perturbations |
| `model/band_thresholds.py` | Writes publishable thresholds and the reference-design recipe to `output/band-thresholds.md` |
| `model/reference_costs.py` | Prices the reference designs against the full course price schedule, and checks both hard constraints |
| `model/export_site_data.py` | Writes `../src/data/course-model.json`: diagnostic bands, reference costs and the price schedule |
| `model/case.py` | The five fixed client homes: personas, Release A dossiers, scaled plan geometry and its self-check |
| `model/scenario.py` | The scenario engine: seven decision variables, monthly balances within each client's permitted uses, peak-month energy, costs, care limits, client targets and the staff feasibility check |
| `model/release_b.py` | Release B: the synthetic measured year, specialist findings, CSVs and the data dictionary |
| `model/practice.py` | The Wattle Street practice house: every worked optimisation example, on invented round numbers |
| `model/measurement.py` | The $1,500 measurement schedule, the demonstrated practice plan and the per-home staff check |
| `model/export_cases.py` | Writes `../src/data/homes.json` and `design.json` |
| `model/data/climate_stations.json` | BoM monthly statistics for 10 stations |
| `model/output/` | Generated tables; `iteration-*` files are snapshots of earlier model versions |

## Reproduce

```sh
cd model
python site_model.py        # -> output/calibration.md / .json
python band_thresholds.py   # -> output/band-thresholds.md
python reference_costs.py   # -> output/reference-costs.md / .json
python sensitivity.py       # -> output/sensitivity.md
python export_site_data.py  # -> ../../src/data/course-model.json
python case.py              # geometry self-check for the five plans
python release_b.py         # -> ../../src/data/release-b.json and public/data/release-b/
python practice.py          # -> ../../src/data/practice.json and public/data/practice/
python measurement.py       # -> ../../src/data/measurement.json
python export_cases.py      # -> ../../src/data/homes.json, design.json (runs the staff check, ~2 min)
python search_presets.py    # -> output/search_results.json (~15 s)
```

Run them in that order after changing any course constant, preset, price, target or case
geometry.

## Headline conclusions

1. The draft's sites were unrealistic: roofs too small to supply even household water, and food potential that ignored water. It also had two near-identical cool climates and no tropical one.
2. The five climates **cannot** be made equally easy with realistic site parameters. Fairness comes from **climate-normalised reference bands inspired by NatHERS**, built from three constructed reference designs per site. Under 11 tested perturbations those reference designs kept broadly similar relative positions; that does not by itself prove equal grading outcomes.
3. Metrics must be capped, counted as used, and **net of imports**. They must include **protein**, not just calories, or the mushroom, insect and aquaponics weeks are invisible.
4. The classic "food scraps → larvae → fish" loop covers only ~10–17 % of fish feed. Australian feed rules also restrict what those larvae may eat. That is an honest teaching point, not a flaw.
5. 5 kWh/d and $30k are feasible guardrails at every site — but only once the reference
   designs stop buying storage the tank balance cannot use. Costed against the **full** price
   schedule, the earlier reference designs were $3.7k–$9.5k over the allowance at every site.
   Storage (Darwin), heating (Canberra) and irrigation water (Alice Springs) are where each
   site actually bites.
