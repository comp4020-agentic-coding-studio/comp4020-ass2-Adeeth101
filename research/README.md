# Assignment 2 research: closed-loop household course

The evidence base behind SLOP4761. Everything here is background working material: the
student-facing course is the site under `src/`. Paths below are relative to this directory.

**Status (2026-09-18):** research, five critique iterations and the reference-cost
reconciliation done. All design decisions are recorded in `course-design.md` §9, and the
figures the site publishes are exported to `../src/data/course-model.json` so no page
retypes a number the model produced. Figure verification against primary sources
(`course-design.md` §7) is recorded in `sources.md`.

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
| `model/export_site_data.py` | Writes `../src/data/course-model.json`, the single source of truth the website renders from |
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
python search_presets.py    # -> output/search_results.json (~15 s)
```

Run the first five in that order after changing any course constant, preset or reference
recipe: the bands, the costs and the published site data all derive from `site_model.py`.

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
