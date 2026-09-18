# Course design: decided (v4)

Planning design for SLOP4761, with every decision the student made on 2026-09-17 applied. It rests on four critique iterations (`critique-log.md`), `findings.md` and `sources.md`. Nothing has been sent to the builder agent yet.

## 1. Identity

| Item | Decision |
|---|---|
| Code | **SLOP4761** (the repo fixed the last three digits; level 4) |
| Title | **Designing the Closed-Loop Household I: Food, Water and Waste** |
| Level | 4xxx undergraduate, engineering |
| Prerequisites | Introductory microbiology; soil science or plant biology; introductory chemistry; an introductory environmental course; engineering design principles; some CAD and modelling experience |
| Follow-on course | **SLOP4762 — Designing the Closed-Loop Household II: Energy and Shelter** (adds energy physics and introductory thermodynamics as prerequisites) |
| Sequel mentions | Home page, prerequisites, week 1 (out of scope), week 12 (bridge) |
| Tone | Sincere engineering course |

**Argument (working wording):** *A household isn't self-sufficient because it produces everything. It's self-sufficient when every output of one system is the input to another, within a fixed plot, budget and energy allowance.*

On a real plot, full food self-sufficiency is out of reach (~372 m² per adult [S14]). The course therefore measures **how much of the loop you close, honestly counted**.

## 2. Fixed for every student

| Item | Value | Status |
|---|---|---|
| Household | 2 adults + 2 children (9–13 y) | course rule |
| Food demand | 40.0 MJ/d; protein 185 g/d | sourced [S03][S04] |
| Reference domestic water | 150 L/person/day (219 kL/yr). Reductions count only if evidenced | **verify before publishing** [S06] |
| Excreted N | 13.6 kg N/yr | sourced [S05]; children as 0.5 adult is a course assumption |
| Energy allowance | **5 kWh/day, peak month, counted loads only (§2.1)** | course rule |
| Budget | **$30,000 course costing allowance** for new spend, priced only from the course price schedule (§2.2). Listed existing inventory is free | course rule |
| Biogas and other energy outputs | Recorded, not credited in part 1; only digestate nutrients count | course rule |

### 2.1 Energy: what counts

**Counted:** all electricity or fuel used to run the food, water and waste loop.

| Group | Loads |
|---|---|
| Water movement | Domestic pressure pumps, transfer pumps, irrigation pumps, greywater pumps |
| Water treatment | UV lamps, dosing pumps, any powered filtration |
| Aquaponics | Circulation pumps, aeration |
| Climate control of biological systems | Heating or cooling of fish tanks, insect units, mushroom chambers and fermentation spaces; humidifiers; fans |
| Sanitation | Composting-toilet fans and heaters, urine-system pumps |
| Waste processing | Digester heating or mixing, powered compost aeration |
| Food preservation beyond the household kitchen | Dehydrators, dedicated fermentation or cold storage for loop produce |

**Not counted** (they belong to SLOP4762): general household appliances, the household fridge and cooking, lighting, space heating or cooling of living areas, water heating for bathing and laundry.

**Required of students:**
- Report the peak-month average daily load, with the month named.
- List every counted load with its power, duty cycle and source.
- **List uncertain or omitted loads explicitly**, each with an estimated range.
- Take the upper end of any uncertain load when checking the 5 kWh/d limit.

### 2.2 Budget: the course price schedule

$30,000 is a **course costing allowance, not a market quotation**. Assessment uses the published schedule below, whatever real prices are, because the screening model simplifies or omits some establishment, installation and treatment costs.

The schedule is labelled honestly:
- **Indicative** = based on a retail listing [S31–S34]
- **Course assumption** = set by the course for assessment consistency

Figures must be checked before publishing; see §7.

| Component | Course price | Basis |
|---|---|---|
| Polyethylene rainwater storage (supply) | $130 per kL | indicative [S31] |
| Tank establishment: pad, inlet/outlet plumbing, overflow | $1,000 per tank | course assumption |
| First-flush diverter + leaf screen | $150 per downpipe | course assumption |
| Pressure or transfer pump | $700 each | course assumption |
| Point-of-entry UV unit with sensor | $1,200 | course assumption |
| Cartridge pre-filtration train | $400 | course assumption |
| Additional roof catchment (skillion shed roof) | $60 per m² | course assumption |
| Composting toilet (unit) | $3,500 each | indicative [S32] |
| Urine diversion and storage tank | $900 | course assumption |
| Greywater diversion, bathroom + laundry, installed | $2,100 | indicative [S33] |
| Greywater treatment system | $6,000 | indicative [S33] |
| Aquaponics: tank, 4 m² grow bed, pump, aeration | $2,500 per 4 m² bed | indicative [S34] |
| Insect rearing unit (black soldier fly or mealworm) | $300 | course assumption |
| Humidified mushroom fruiting chamber | $800 | course assumption |
| Hot-compost bays (set of 3) | $500 | course assumption |
| Household anaerobic digester | $1,500 | course assumption |
| Fruit or nut tree (potted) | $50 each | course assumption |
| Drip irrigation | $8 per m² irrigated | course assumption |
| Contingency | 10 % of subtotal, required | course rule |

**Bill-of-materials rules** (course assumptions, published with the schedule, applied in `model/reference_costs.py`):
- New storage arrives in tanks of at most 25 kL, so the per-tank establishment charge scales with tank count.
- One first-flush diverter and leaf screen per 75 m² of connected roof.
- Two pumps: one for domestic supply, one to move tank water to the garden. Both are counted loads under §2.1.
- The aquaponics line bundles tank, pump and aeration, so a second 4 m² bed on the same system costs $1,800 — the bundle price less one pump line. This is the rule that stops a pump being paid for twice.
- Drip irrigation covers the whole production area, because the model irrigates the whole production area.

**Priced but not drawn in the reference designs** (no recipe parameter or counted load implies them; a student who chooses them pays from the same allowance): greywater treatment, anaerobic digester, mushroom fruiting chamber, fruit and nut trees.

**Not priced by the schedule at all**, published so the allowance is not read as a quotation: garden establishment (soil, mulch, seed and stock); aquaculture tank heating hardware; labour beyond the lines marked installed; earthworks and access beyond the per-tank establishment line; council approval, plumbing certification and WaterMark device fitting; consumables and replacement (UV lamps, filter cartridges, imported fish feed, desludging).

## 3. The five preset sites

| ID | Site | Climate station | Dwelling | Plot | Growable | Roof | Existing inventory |
|---|---|---|---|---|---|---|---|
| S1 | Cool-temperate inland suburban | Canberra 070014 | house + garage + carport | 800 m² | 450 m² | 300 m² | 5 kL tank |
| S2 | Hot-arid rural-residential | Alice Springs 015590 | house + machinery shed | 2 ha | 400 m² | 350 m² | 22 kL tank; bore capped at 100 kL/yr |
| S3 | Humid subtropical townhouse | Brisbane 040214 | townhouse | 300 m² | 90 m² + 40 m² strata garden | 170 m² | 3 kL tank |
| S4 | Mediterranean suburban | Adelaide 023000 | detached house | 700 m² | 250 m² | 230 m² | 5 kL tank |
| S5 | Tropical wet-dry rural-residential | Darwin 014015 | elevated house + shed | 1 ha | 500 m² | 300 m² | 45 kL tank |

**Decided:**
- Darwin replaces the cold-upland site.
- The townhouse is in Brisbane.
- Adelaide is the Mediterranean suburban site.

**Site cards** must carry the written strengths and constraints, **including those the model cannot score**:

- **S1 Canberra.**
  - *Strengths:* **the most even rainfall of the five (28 % falls in the driest 4 months, vs 1.4 % in Darwin)**; **high chill for temperate fruit and nuts**; fewest heat days.
  - *Constraints:* 92 frost days; shortest season; fish and insects active ~7 months without heat (~0.5 kWh/d winter tank heating); excreta storage 1.5–2 years.
- **S2 Alice Springs.**
  - *Strengths:* heat for composting and drying; a capped bore; year-round mushroom options in a humid chamber.
  - *Constraints:* P/ETo 0.16; 1,650 mm/yr irrigation need; 90 days ≥35 °C; hardest food and nutrient closure of the set.
- **S3 Brisbane townhouse.**
  - *Strengths:* year-round growing; highest rain-fed yield; mild temperatures for fish and insects.
  - *Constraints:* **restricted space (130 m² total growing area incl. the shared strata garden)**; **density and strata constraints** (neighbour amenity, odour, shared-property rules); can absorb only ~11 % of household N on site; high-rainfall turbidity and first-flush load.
- **S4 Adelaide.**
  - *Strengths:* mild climate; lowest process energy; suits preserving; trout and Murray cod rotation covers 12 months.
  - *Constraints:* winter rain against summer demand (lowest water closure of the set); 17 % of rain in the driest 4 months.
- **S5 Darwin.**
  - *Strengths:* highest food, protein and nutrient potential; barramundi and insects all year.
  - *Constraints:* 1.4 % of rain in the driest 4 months, so dry-season imports even with 91 kL storage while 200+ kL overflows in the wet; highest pumping energy.

**Custom sites.** Approval by week 3. Requirements:
- the same parameter sheet, a named BoM station, and a source for every value;
- values inside the preset envelope (growable 90–500 m², roof 170–350 m², bore ≤100 kL/yr, existing storage ≤45 kL), or a justification for each exception;
- staff compute the site's bands with the published method.

## 4. Indicators and scoring

### 4.1 Indicators

All are capped at 100 %, counted as used rather than produced, and net of imports [S47].

| Indicator | Definition | How assessed |
|---|---|---|
| Water closure | On-site water used (roof, capped bore, reused greywater) ÷ all water used, including carted or imported water | Banded |
| **Garden water satisfaction** (always shown beside water closure) | Share of the garden's irrigation deficit actually met | Banded, and always reported with water closure: a design can reach high water closure by leaving its garden under-watered |
| Food energy closure | kcal produced *and eaten* ÷ 40 MJ/d requirement | Banded |
| Protein closure | Protein produced ÷ 185 g/d; animal products count only in proportion to feed grown on site | Banded |
| Nutrient closure | N safely recovered *and* applied within crop uptake (~12 g N/m²/yr) ÷ 13.6 kg N/yr | Banded |
| Waste-stream recovery | % of food-waste dry matter, greywater volume and excreta N routed to a productive use | **Not banded.** The model has no reference calculation for it. Assessed from the submitted mass balances against the rubric, unless a separate reference calculation is added later |

**Supporting evidence** (reported, not banded): storage size, overflow and import months, insect share of fish feed.

### 4.2 Hard constraints (pass/fail)

- **Energy:** peak-month counted process energy ≤5 kWh/d (§2.1), with uncertain loads at their upper estimate.
- **Budget:** new spend ≤$30,000 from the course price schedule (§2.2), including the 10 % contingency.
- **Safety and legal compliance:**
  - excreta storage per WHO temperature bands [S09]
  - greywater: subsurface only, no storage, no kitchen water [S10]
  - composting pasteurisation [S35]
  - fermentation: 2–2.5 % salt, pH ≤4.6 [S36]
  - drinking-water treatment claims stated as log reductions [S40]
  - insects fed to animals: plant-based substrates only, heat-treated [S29]
  - legal fish species only; tilapia is a declared noxious fish [S18]

### 4.3 Climate-normalised reference bands inspired by NatHERS

**What they are.** The idea comes from NatHERS's climate-specific star bands [S30], but this is **not the NatHERS method**. NatHERS derives its bands from a population of housing simulations. These bands come from **three constructed reference designs** (baseline, competent, excellent) run through the course's screening model for each site.

**Published on the course site:**
- the three reference designs (one recipe for all sites)
- their assumptions
- each site's thresholds

**Bands:**

| Band | Meaning |
|---|---|
| 1 | Below baseline |
| 2 | Baseline to competent |
| 3 | Competent to excellent |
| 4 | At or beyond excellent |

**Bands are performance evidence inside the rubric, not an automatic grade.** Reasoning, justification and honest uncertainty carry more weight than where a number lands.

**Why not equalise the sites instead?** Realistic site parameters cannot make these climates equally hard. In a constrained search, the best realistic spread was still 1.35 SD (C15).

**What the sensitivity test does and doesn't show (C16, C29):** across 11 tested perturbations, the constructed reference designs keep broadly similar relative positions inside their sites' bands. Worst-case spread by indicator: food energy 0.07, protein 0.06, nutrient 0.17, water closure 0.24, **garden water satisfaction 0.38**. The two largest arise under the same perturbation, domestic demand at 120 L/person/day; excluding it, no indicator spreads by more than 0.17. Garden water satisfaction is the least stable of the five and was only brought inside the test on 2026-09-18, so earlier stability claims did not cover it. The test does **not** independently prove equal grading outcomes for real student designs.

**Recompute rule:** the bands must be recomputed and republished whenever any course constant changes. That includes household demand, allowances, the price schedule, yield or other model coefficients, and the reference-design recipe.

**Thresholds** (v4 presets; baseline / competent / excellent; from `model/output/band-thresholds.md`):

| Indicator | S1 Canberra | S2 Alice Springs | S3 Brisbane townhouse | S4 Adelaide | S5 Darwin |
|---|---|---|---|---|---|
| Water closure | 65 / 81 / 94 % | 78 / 89 / 97 % | 68 / 84 / 96 % | 42 / 59 / 72 % | 73 / 79 / 83 % |
| Garden water satisfaction | 0 / 15 / 20 % | 1 / 12 / 16 % | 15 / 72 / 81 % | 0 / 23 / 27 % | 23 / 29 / 31 % |
| Food energy closure | 1.0 / 3.3 / 5.5 % | 0.2 / 1.6 / 2.9 % | 1.2 / 3.9 / 6.1 % | 1.1 / 3.7 / 5.9 % | 4.8 / 10 / 15 % |
| Protein closure | 1.6 / 5.5 / 8.9 % | 0.2 / 2.8 / 4.9 % | 1.8 / 6.4 / 9.9 % | 1.6 / 6.1 / 9.6 % | 7.4 / 16 / 25 % |
| Nutrient closure | 4 / 10 / 14 % | 1 / 4 / 6 % | 3 / 8 / 10 % | 3 / 9 / 12 % | 13 / 21 / 27 % |

**Ceiling:** no excellent value reaches 100 % under recipe v5, so band 4 is open at every site.

**Rounding:** bands are evaluated against the model's unrounded reference values. The percentages above are a rounded display of those values, not the thresholds themselves.

**Reference-design recipe** (same at every site):

| Parameter | Baseline | Competent | Excellent |
|---|---|---|---|
| Domestic demand (L/person/day) | 150 | 150 | 130 |
| Composting toilet | no | yes | yes |
| Greywater reused | 0 % | 50 % | 90 % |
| Growable area in production | 50 % | 80 % | 100 % |
| Yield vs 1,500 kcal/m²/yr reference | 0.8× | 1.0× | 1.2× |
| Excreted N recovered | 30 % | 60 % | 80 % |
| Aquaponic grow bed | none | 4 m² | 8 m² |
| Added roof catchment | none | none | +5 % of roof |
| New storage spend (tank shells) | $3,000 | $3,500 | $4,000 |

**Gap resolved (2026-09-18, recipe v5).** The v4 designs had been costed with the model's five simplified prices and no contingency, giving $3k / $14.1k / $22–25k. Re-costed against the §2.2 schedule by `model/reference_costs.py`, the v4 excellent design came to $33,704–$39,545 — over the allowance at **every** site. Two changes fixed it, and nothing else in the recipe moved: new-storage spend fell to $3,000 / $3,500 / $4,000, because the monthly tank balance saturates (the extra $5,000 moved water closure by at most 0.06), and the excellent design's added catchment fell from 25 % to 5 %, because it was the most expensive water lever per point of closure. Every reference design now fits both hard constraints. See `critique-log.md` iteration 5.

| Level | Cost range across the five sites | Worst budget headroom | Worst declared peak energy |
|---|---|---|---|
| Baseline | $10,307 – $12,100 | $17,900 | 2.61 kWh/d |
| Competent | $21,540 – $24,310 | $5,690 | 4.01 kWh/d |
| Excellent | $24,860 – $28,875 | $1,125 | 3.99 kWh/d |

Totals include the required 10 % contingency, and the energy figures include a declared 0.65 kWh/d upper-estimate allowance for the counted loads the screening model does not compute. $1,125 of headroom at Darwin is inside the noise of a screening model priced from commercial listings, so the published claim is that the reference designs fit the allowance **as the schedule prices them**, not that a real build would cost this.

## 5. Twelve weeks

Ordered by what feeds what. Each topic week has a "Five sites" worked section. Each site leads two weeks, one where its climate helps and one where it hurts.

| Wk | Topic | Core quantitative method | Loop links | Lead site |
|---|---|---|---|---|
| 1 | Loop thinking and the site sheet | Mass balances; household demand [S03–S05]; indicators; reference bands; energy-load and price-schedule rules | Whole framework; what's out of scope (energy and shelter → SLOP4762) | all |
| 2 | Perennial food systems and soil | ETo (FAO-56 Eq. 52), Kc, effective rain [S11][S12]; yield ranges [S13–S15]; chill categories [S24] | In: compost, spent substrate, greywater, urine N. Out: food, prunings | **S1** (helps: chill) |
| 3 | Mycology | Biological efficiency [S23b]; species temperature bands [S23]; spent-substrate mass [S23d] | In: prunings, straw. Out: mushrooms; spent substrate → soil/compost (not larvae [S23c]) | **S3** (helps: humidity) |
| 4 | Insect farming | Degree-days and threshold temperatures [S22]; bioconversion [S22b]; composition [S37]; feed rules [S29] | In: *plant-based* scraps, ≤25 % spent substrate. Out: heat-treated larvae → fish; frass → soil. Meat and dairy → week 10 | **S5** (helps: warm all year) |
| 5 | Aquaponics | Feed-rate ratio, stocking, FCR [S16][S49]; legal species bands [S18–S20]; larvae cover only ~10–17 % of feed | In: larvae, top-up water (placeholder 20 L/d, sized in weeks 7–9). Out: fish, greens, nutrient water | **S4** (hurts: seasonal species switching) |
| 6 | Fermentation and cultured microbes | Salt %, temperature, pH safety [S36]; surplus-to-winter storage balance | In: seasonal surplus. Out: preserved food; bokashi/silage pre-treatment → week 10 | **S4** (helps: mild) |
| 7 | Water sourcing | Roof runoff formula [S08]; bore allocation; effective rain [S12] | Roof, bore, surface → raw water | **S2** (hurts: arid) |
| 8 | Filtration and treatment | Multi-barrier; log reductions and WHO star ratings [S40]; BioSand [S41]; UV dose [S42]; pumping energy [S21] | Raw → potable; energy against the allowance | **S3** (hurts: turbidity, density) |
| 9 | Water security and storage | Monthly tank balance, reliability, overflow and import months [S08]; drought-year dataset | Storage sizing against climate; budget trade-off | **S5** (hurts: 6-month dry season) |
| 10 | Waste management | AS 4454 pasteurisation [S35]; C:N; digester temperature [S27]; WHO composting [S09] | Food waste, meat/dairy, spent substrate, fish sludge → compost/digestate → soil | **S2** (helps: heat) |
| 11 | Sanitation | WHO storage times by temperature; urine storage [S09]; greywater rules [S10]; N uptake limit [S05] | Excreta and urine → N; greywater → subsurface irrigation | **S1** (hurts: cold → longer storage) |
| 12 | Integration | Whole-household model; failure modes; bands; bridge to SLOP4762 | Closes the loop | all |

## 6. Assessment (totals 100 %)

| Item | Weight | When |
|---|---|---|
| Quizzes: 5 × 8 %, conceptual multiple choice, no maths | 40 % | **Weeks 3, 5, 8, 10, 12** (none in A1's due week) |
| Assignment 1: Food Loop Design | 20 % | Due week 7 |
| Capstone: The Site-Specific Off-Grid Master Plan | 40 % | Exam period |

**No oral defence.** The troubleshooting dataset, calculations and written justification already test understanding. An oral should only be reconsidered if it is short and either mandatory, ungraded, or assessed under identical conditions for every student.

### Assignment 1

Covers weeks 1–6, for the chosen site. Deliverables:
- parameter sheet
- sized designs for the five food subsystems, with stated assumptions
- mass balance
- energy and protein closure
- nutrient flows
- partial energy-load list (counted, uncertain and omitted)
- price-schedule costing
- ±20 % yield sensitivity
- one troubleshooting dataset (e.g. an aquaponics nitrite/pH log)

### Capstone

Deliverables:
- the A1 loop revised with feedback
- water and waste systems integrated
- all banded indicators with garden water satisfaction beside water closure
- waste-stream mass balances
- full energy-load list and price-schedule costing (hard constraints)
- safety and legal checklist
- scaled CAD site layout
- a drought-year dataset: what fails first, and the design response

### Rubric (draft, both assignments)

| Criterion | Weight |
|---|---|
| Calculations and justified assumptions | 30 % |
| Loop integration (mass balances, waste-stream recovery) | 25 % |
| Site fit (uses the site's strengths, designs around its constraints, including the unmodelled ones) | 20 % |
| Data-driven troubleshooting | 15 % |
| Drawings and communication | 10 % |

Band positions are **performance evidence** within "calculations" and "loop integration", never a separate automatic score.

### Datasets

- Climate: real BoM statistics per site.
- Sensor logs and drought years: **clearly labelled synthetic** data derived from those statistics.

## 7. Before anything is published: figure verification

Every figure marked medium or low confidence in `sources.md` must be verified against a primary source. If it cannot be upgraded, the site must label it **"course assumption"** or **"indicative value"** rather than presenting it as settled fact.

**Priority checks:**
1. Domestic water demand, 150 L/person/day [S06] (find it on a Your Home page, or relabel as a course assumption).
2. Prices [S31–S34] and every course-assumption price in §2.2.
3. Greywater requirements [S10] (primary NSW Health / Water NSW text).
4. Fish temperature bands [S19][S20] (primary DPI or Business Queensland pages; Murray cod and jade perch currently rest on industry sources).
5. Mushroom assumptions [S23][S23b][S23d] (species fruiting ranges, biological efficiency, spent-substrate mass).

**Also medium/low:** S14, S15, S17, S21, S22b, S24, S26, S27, S28, S41, S49.

## 8. Site scope for this submission

- **Build:** published score tables, clear site cards, band tables, and **one worked comparison** of the same design idea across sites. **No interactive calculator** (possible later extension).
- **Priorities:** a coherent twelve-week course, assessment pages, the deck, policies, mobile layout, and verification.

## 9. Decision record (2026-09-17)

1. Identity: SLOP4761 / SLOP4762 titles as in §1; 4xxx undergraduate.
2. Quizzes in weeks 3, 5, 8, 10, 12.
3. Scoring: climate-normalised reference bands inspired by NatHERS, as ordinal performance evidence. Publish recipe, assumptions and thresholds; recompute on any constant change. Garden water satisfaction beside water closure. Waste-stream recovery via mass balances and rubric. Careful sensitivity wording.
4. Sites: Darwin replaces cold upland; townhouse in Brisbane; Adelaide suburban; keep written unmodelled strengths and constraints.
5. Hard constraints: 5 kWh/d peak-month counted loads, with uncertain and omitted loads declared. $30,000 as a costing allowance governed by a published price schedule.
6. No oral defence.
7. Score tables and site cards, not a calculator. Verify medium/low figures or label them.
