# Critique log

Each iteration records: the issue found, the evidence, the change, and the before/after numbers. Model snapshots are in `model/output/iteration-*.md`. Preset sets v1–v4 all live in `model/presets.py`, so every row can be re-run.

## Baseline: v1, the planning-chat draft

- **Sites:**

  | ID | Site | Plot | Roof | Rainfall |
  |---|---|---|---|---|
  | S1 | Cool-temperate suburban | 650 m² | 180 m² | 620 mm |
  | S2 | Hot-arid rural | 2 ha | 220 m² | 250 mm |
  | S3 | Humid subtropical peri-urban | 800 m² | 160 m² | 1,500 mm |
  | S4 | Mediterranean townhouse | 250 m² | 110 m² | 500 mm |
  | S5 | Cold upland rural | 1 ha | 200 m² | 1,100 mm |

  Fixed across all sites: 4 people, $30k, 5 kWh/d.
- **Metrics:**
  - potentials: water = roof × rain × 0.8; food = area × growing days × yield; N from per-person figures
  - closure ÷ potential as the score
  - linkage count
  - pass/fail budget and energy
- **Weeks:** perennials → mycology → insects → aquaponics → fermentation → water ×3 → waste → sanitation → integration. Sites lead in a simple rotation.
- **Assessment:** quizzes 5 × 8 %; A1 food loop 20 % (week 7); capstone 40 % (exam period); draft rubric 30/25/20/15/10.

## Iteration 1: does the draft survive real data? (model v1)

| # | Issue | Evidence | Change |
|---|---|---|---|
| C1 | Roofs far too small. No site could supply even household water: roof supply was 20–66 % of domestic demand | enHealth runoff formula [S08] + 150 L/p/d [S06]: S1 85 kL, S4 44 kL vs 219 kL demand | Roof areas from real dwellings (new-house floor ~232 m² [S43]; roof incl. garage/eaves 230–350 m²) |
| C2 | Food potential ignored water | Draft S2: 2,000 m² at 1,650 mm net irrigation = 3,300 kL/yr, 15× its roof yield (plus 19 kWh/d pumping) | Food potential is water-coupled: FAO-56 ETo [S11], effective rain [S12], irrigation limited by on-site water |
| C3 | "Growing days" was subjective | — | Replaced by a monthly season factor from BoM temperatures and heat days [S39] |
| C4 | S1 and S5 near-duplicates; no tropical coverage | Canberra vs Armidale: Tmean 13.1/13.4 °C, frost days 92/98, P/ETo 0.50/0.57 | **Darwin (tropical wet-dry) replaces the cold upland site** |
| C5 | Chill hours unusable from monthly means | Model 1,979 h vs published ~720 (Canberra); 0 vs ~150 (Brisbane) [S24] | Chill is reported as a regional category, not computed |

## Iteration 2: realistic sizes, two pairings (model v2; sets v2a, v2b)

| # | Issue | Evidence | Change |
|---|---|---|---|
| C6 | **Water metric punished ambition**: its denominator included the student's chosen garden, so a bigger garden lowered the score | "Competent" scored below "baseline" (S1 0.33 → 0.29) | Water closure = on-site water ÷ all water *actually used* (imports in the denominator). A larger garden can no longer lower it |
| C7 | No rain-fed growing, so any site with roof < domestic grew zero food | S4 townhouse: 0.0 food at every level | Monthly water-satisfaction model: rain first, then tank and greywater top-ups |
| C8 | Townhouse in the dry Mediterranean climate was worst on almost everything | v2a mean rank S4 4.0 | Dense-urban preset moved to the wet climate (Brisbane) with a strata garden; Adelaide becomes suburban (v2b) |

## Iteration 3: storage, imports, alignment (model v3; set v3)

| # | Issue | Evidence | Change |
|---|---|---|---|
| C9 | Water closure saturated at 100 % for Alice Springs (bore) and Darwin at *every* design level, and annual balances hid the dry season | Darwin needs 306–439 kL storage for an annual balance, >$39k at $130/kL [S31] | **Storage-limited monthly tank simulation.** Storage is funded from the same budget ($3k/$6k/$9k in the reference designs); domestic shortfalls are carted imports; bore capped at 100 kL/yr |
| C10 | kcal-only food metric made weeks 3–5 invisible in the score (constructive-alignment failure [S44]) | Mushrooms, fish and larvae add ~0 kcal | **Protein closure** added alongside energy closure |
| C11 | "Scraps → larvae → fish" can't close; feed law restricts substrates | Plant-based household waste gives 9–17 % of feed for 4 m² [S16][S22b][S28]; Australian feed rules [S29] | Closure is **net of imports**: fish protein counts only in proportion to on-site feed. Insect substrate must be plant-based; larvae heat-treated |
| C12 | Week 3 → 4 link (spent substrate → insects) is biologically weak | 1.46 % bioconversion on pure spent substrate [S23c] | Spent substrate → compost/soil (weeks 2, 10); ≤25 % of larval mix |
| C13 | Linkage count is gameable (many trivial links) | — | Replaced by **waste-stream recovery ratios** (food-waste dry matter, greywater volume, excreta N), each with a mass balance |
| C14 | Common permaculture fish (tilapia) is illegal in Australia | [S18] | Species list limited to legal fish with sourced temperature bands |

## Iteration 4: can presets be balanced, and is band scoring robust? (search, sensitivity; set v4)

| # | Issue | Evidence | Change |
|---|---|---|---|
| C15 | **Physical levers cannot equalise the climates** | Constrained search over ~250k realistic lever combinations: best ease-index spread still 1.35 SD (Canberra −0.55 … Darwin +0.80) | Fairness moves to scoring: **climate-normalised reference bands inspired by NatHERS** [S30] and BASIX [S48], built from three constructed reference designs rather than a population of simulated dwellings. v4 = best balanced realistic inventory, with no dominated site |
| C16 | Is band scoring stable under uncertainty? | 11 perturbations (yield ±33 %, demand 120/180, runoff, Kc, FCR, tank cost). Spread of the competent design's band position across sites: food ≤0.09, protein ≤0.08, nutrients ≤0.19, water ≤0.21, except demand at 120 L/p/d (0.39) | Bands must be **recomputed and republished if any course constant changes**. Narrow bands (Alice Springs food 3 percentage points) are noisy, so bands are **ordinal (4 levels)**, not a continuous score |
| C17 | Is 5 kWh/d meaningful? | Excellent designs peak at 2.8–3.9 kWh/d (56–77 %); peak drivers are Darwin dry-season pumping and Canberra tank heating | Keep 5 kWh/d as a guardrail; define exactly which loads count |
| C18 | Is $30k fair when storage costs differ? | Excellent reference designs $22–25k; storage is the site-sensitive line | Keep $30k new spend; presets list existing inventory (tanks, bore) |
| C19 | Quiz 3 (week 7) collides with the A1 due date (week 7) | Draft schedule | Two options for the student's decision (see course design §6) |
| C20 | Aquaponics (week 5) runs before the water weeks | FAO: 1–3 % of volume per day [S16], so 10–30 L/d | Explicit placeholder top-up of 20 L/d from roof water, "sized properly in weeks 7–9" |
| C21 | Sanitation sizing burden differs by climate | WHO storage 1.5–2 yr ≤20 °C vs >1 yr >20 °C [S09] | Built into the reference designs, so the bands absorb it; named in site sheets |
| C22 | Site-led worked examples could favour sites | Model conditions per site | Each site leads two weeks, one where its climate helps and one where it hurts |
| C23 | Custom sites could game the envelope | — | Same parameter sheet, same model, envelope from v4, bands computed by staff, approval by week 3 |

## Iteration 5: does the reference design actually fit the allowance? (recipe v5, 2026-09-18)

Triggered by the known gap recorded at the end of course design section 4.3: the reference
designs had been costed with the model's five simplified component prices, not the expanded
price schedule in section 2.2, and with no contingency. `model/reference_costs.py` now prices
the full bill of materials the recipe and the section 2.1 energy boundary imply.

| # | Issue | Evidence | Change |
|---|---|---|---|
| C24 | **The old totals never established budget compliance.** They omitted tank establishment, first flush, both pumps, UV, pre-filtration, urine diversion, compost bays, the insect unit, drip irrigation and the required 10 % contingency | Re-costed v4 recipe: excellent design $33,704 (S3) to $39,545 (S2) against a $30,000 allowance — over at **all five sites** | Reference costs are now computed from the published schedule with a published bill-of-materials rule, and `indicative_cost` in `site_model.py` is marked superseded |
| C25 | The aquaponics line bundles tank, pump and aeration, so charging it twice for an 8 m² bed pays for a pump and tank that are not bought | Schedule line S34: "tank, 4 m² grow bed, pump, aeration" | Additional 4 m² beds cost the bundle price less one pump line: $1,800, not $2,500 |
| C26 | **The excellent design was buying storage it could not use.** | Raising excellent new-storage spend from $4,000 to $9,000 moves water closure by at most 0.06 and garden water satisfaction by at most 0.04, while costing $5,600 with establishment | New storage spend drops to $3,000 / $3,500 / $4,000 |
| C27 | Added roof catchment was the most expensive water lever per point of closure | At 25 % of roof it costs $2,550–$5,250; at 5 % it costs $510–$1,050 and keeps the lever distinct from the competent design | Excellent added catchment drops from 25 % to 5 % |
| C28 | Feasibility had never been checked against the **full** counted-load boundary, only against the six load groups the screening model computes | Section 2.1 counts insect-unit climate control and greywater pumping, which the model does not compute | A declared uncertain-load allowance of 0.65 kWh/day is carried at its upper estimate, as section 2.1 requires of students |
| C29 | The sensitivity test's stability claim did not cover garden water satisfaction, which is published beside water closure | The test's stream list omitted it | `sensitivity.py` now tests it. It is the least stable indicator: spread ≤0.17 in 10 of 11 perturbations, 0.38 under the 120 L/p/d demand perturbation |
| C30 | The published ceiling note assumed Brisbane water closure and garden water satisfaction reach 100 % | Under recipe v5 the highest excellent value is 97 % | The note is generated from the data rather than written by hand, and now says band 4 is open at every site |

**Result after the change.** Every reference design fits both hard constraints, with headroom:

| | Budget headroom (worst site) | Declared peak energy (worst site) |
|---|---|---|
| Baseline | $17,900 | 2.61 kWh/d |
| Competent | $5,690 | 4.01 kWh/d |
| Excellent | $1,125 | 3.99 kWh/d |

Fairness screen re-run on recipe v5: still **no dominated pairs**, so F1 holds. Band widths
narrow slightly at the excellent end, which is the honest consequence of making the excellent
design affordable.

**What this does not establish.** $1,125 of headroom at Darwin is inside the noise of a
screening model built from commercial listings and course assumptions. The published claim is
that the reference designs fit the allowance *as the schedule prices them*, not that a real
build would cost this. The schedule omits garden establishment, tank heating hardware, labour,
earthworks, approvals and consumables; those omissions are published beside the schedule.

## Iteration 6: the consultancy redesign (second draft, 2026-09-18)

| # | Issue | Evidence | Change |
|---|---|---|---|
| C30 | The excellent reference design built new roof catchment on homes that are fixed existing properties | recipe v5 excellent: +5 % catchment | Recipe v6: no new catchment; excellent water closure falls 1–2 points at four sites; worst headroom rises to $2,280 |
| C31 | Closure scores cannot stand for what a client values | a design can raise closure while failing the household's actual priority | Client priority service targets per home, set from the scenario model with a feasibility margin; bands kept as diagnostics |
| C32 | The first scenario draft averaged pumping energy over the year, served every indoor use from the tank, and charged the existing condition for new equipment | `scenario.py` checkpoint review | Monthly energy with the peak month named; tank serves only each client's permitted uses; existing condition costs nothing in capital |
| C33 | Plans and dossiers were inconsistent: Canberra's "back garden" lay between the house and the street; Brisbane's path was both 600 and 700 mm | the checkpoint `case.py` geometry | All five plans relaid; areas derived and self-checked against presets within 15 m² or 4 % |
| C34 | The model irrigated dormant gardens in a Canberra winter, which kept the existing tank empty all year and contradicted the client | Release B first run | No irrigation is scheduled below 10 °C monthly mean; dormant months count as satisfied |
| C35 | The 372 m² claim misread its source | V11 | Removed; taught in week 9 with the source's two estimates and assumptions |

## Fairness acceptance criteria: final status

| Criterion | Status |
|---|---|
| F1: no preset dominated by another on every indicator | **Met** (v4: 0 dominated pairs) |
| F2: each preset easiest on ≥1 and hardest on ≥1 modelled indicator | **Partly met.** Canberra is easiest on nothing modelled; the Brisbane townhouse is hardest on nothing modelled. No realistic lever fixes this. Their real strengths and hardships sit outside the model: Canberra has the most even rainfall (28 % in driest 4 months vs Darwin 1.4 %), fewest heat days and high chill; the townhouse has 130 m² total growing space and strata/density constraints. These must be named on the site sheets. Band scoring means they don't affect marks |
| F3: the constructed reference designs keep similar relative band positions at every site | **Met** in the central case and 10 of 11 perturbations (spread ≤0.21). This does not independently prove equal grading outcomes for real student designs |
| F4: hard constraints feasible for an excellent design everywhere | **Met under recipe v5** (declared peak energy ≤4.01/5 kWh/d including the uncertain-load allowance; cost ≤$28,875/$30,000 including contingency). Under v4, costed against the full schedule, it was **not** met — see C24 |
| F5: every week has a sourced quantitative method | **Met** (see course design §5) |
| F6: every safety or legal rule is sourced | **Met** (feed, species, greywater, excreta, compost, fermentation, drinking water) |
| F7: preset parameters are ordinary for their site type | **Met with flagged assumptions** (growable areas, strata garden, bore cap) |

## Known limits of this research

- The screening model uses monthly means of an average year. It has no drought years, pests, soils or labour.
- Food yield is one reference number (1,500 kcal/m²/yr) with a published range of 500–3,000.
- Several figures rest on search summaries rather than full documents (marked in `sources.md`). Costs come from commercial listings.
- Water temperature is approximated by air temperature.
- Chill hours rely on nursery estimates.
