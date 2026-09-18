# Course design: decided (v5, second draft)

The contract for SLOP4761 after the review of the first draft. It supersedes v4 wherever
the two conflict; §0 lists every first-draft requirement this revision changes. The
evidence base (`findings.md`, `sources.md`, `verification-log.md`, `critique-log.md`)
still stands except where noted, and the screening model behind the first draft is kept
for the diagnostic reference bands.

## 0. What the second draft changes

| First-draft requirement (v4) | Second draft (v5) | Why |
|---|---|---|
| Students design a closed-loop household on a preset site; the deliverable is a site master plan | Students are graduate engineering consultants. A1 designs a year-long **measurement programme**; A2 turns a supplied specialist dossier into a **high-level investment proposal** for a homeowner's loan application | An engineering optimisation course told through one consultancy case, with measurement before design |
| Five preset sites, **or a custom site** approved by week 3 | **Five fixed existing homes only.** Custom sites are removed everywhere | Equal dossier completeness and marking comparability; no land substitution |
| Excellent reference design added +5 % roof catchment | **No new catchment.** A design may connect more of the roof that already exists (recipe v6) | Fixed existing properties |
| Assessment leaned on closure indicators and reference bands | Lowest-cost option that meets the **client's priority service targets**, then a justified case for any extra spending. Bands kept as **diagnostics only** | A constrained, multi-objective decision; no single score captures client values |
| "Everyone needs 372 m² to grow a near-complete diet"; "the largest site has 500 m²" | Removed. Ecology Action's figures are taught in week 9 with their diet, yield, soil and skill assumptions, and the document's own two estimates (V11). 500 m² is the largest designated growing area; the largest whole plot is 2 ha | Method-specific estimates are not a universal minimum |
| Week order by subsystem (perennials, mycology, insects, …); lead sites Canberra 2/11, Brisbane 3/8, Darwin 4/9, Adelaide 5/6, Alice Springs 7/10 | Measurement weeks 1–6, specialist handover week 7, design weeks 8–12; lead sites Canberra 2/7, Alice Springs 3/8, Brisbane 4/9, Adelaide 5/10, Darwin 6/11 (§7) | A1 needs measurement method before week 7; biological detail is revisited in week 9 |
| A1 "Food Loop Design"; capstone "Site-Specific Off-Grid Master Plan"; one shared rubric | A1 "Year-long Measurement Programme"; A2 "Household Resilience Investment Proposal"; separate rubrics (§8) | The deliverables changed |
| Prerequisites led with microbiology, soil science and chemistry | Engineering design, mass and energy balances, introductory statistics and measurement, spreadsheet modelling, basic CAD; environmental or biological study helpful | The course teaches the biology it needs |
| Two decks | Twelve decks, one per lecture, 8–12 teaching slides each | Every lecture needs its slides |
| One worked cross-site comparison of storage spend on the reference design | A worked optimisation on the **Wattle Street practice house** with invented round-number data | Worked examples must not solve an assessed home |
| Site cards and a parameter table | Per-home **Release A** intake dossier with scaled plans and **Release B** specialist findings with CSVs and a data dictionary | Consultancy narrative; A2 independent of A1 quality |

Everything not listed keeps its v4 decision: the identity, the household convention, the
safety and compliance table (§6.3), the energy boundary, the price schedule's original lines,
the five climates and the preset plot, growing and roof parameters (within the §4 rounding
tolerance), quiz weeks, and no oral assessment.

## 1. Identity

| Item | Decision |
|---|---|
| Code and title | **SLOP4761 — Designing the Closed-Loop Household I: Food, Water and Waste**, level 4 |
| Follow-on | **SLOP4762 — Designing the Closed-Loop Household II: Energy and Shelter**, a proposed follow-on course, never linked |
| Prerequisites | Prior engineering design; mass and energy balances; introductory statistics and measurement; spreadsheet modelling; basic CAD. Prior environmental or biological study is helpful; the course teaches the biology it uses |
| Tone | A sincere engineering course. Fiction is labelled once, on its introductory pages, not on every paragraph |

## 2. The consultancy case (teaching fiction)

- **Household Resilience Loan Programme**: a fictional government programme that lends to
  homeowners for self-sufficiency retrofits. Applicants need a credible engineering
  proposal. No real policy, lender, endorsement or link is invented.
- **Common Ground Engineering**: the fictional consultancy. Students are graduate engineers
  working under a senior reviewer (the teaching staff in role).
- **Programme rules used as course rules**: implementation cost at most **$30,000**
  including a 10 % contingency; **5 kWh/day** peak-month process energy; a separate common
  **$1,500 measurement allowance** for equipment and services, with consultant labour
  scheduled in hours and not charged. Borrowing more raises the application's exposure
  within this fictional scheme and needs a stronger alternatives case; the course does not
  teach that principal alone determines real credit risk. No income underwriting, interest
  rate, credit score or financial advice.
- **The deliverable is not a loan approval or a construction-certified design.** A2 is the
  technical annex and executive recommendation for an application.
- **Narrative**: client intake (week 1) → measurement proposal (weeks 2–6, A1 due week 7)
  → a jump of twelve fictional months → specialist handover (week 7) → engineering proposal
  (weeks 8–12, A2 in the exam period). Students do not collect real data.

## 3. Fixed household and reference data

Unchanged from v4: two adults and two children aged 9 to 13; 40.0 MJ/day food energy
[S03]; 185 g/day protein [S04]; 150 L/person/day domestic water as a course assumption
at the midpoint of enHealth's 100–200 L range (V1); 13.6 kg N/year excreted [S05].

New in v5, all course assumptions published on the method page:

- **End-use split** of 150 L/person/day: toilet 22, showers and basins 55, laundry 28,
  kitchen and drinking 30, other 15. It reproduces Beal and Stewart's toilet figure and a
  bathroom-plus-laundry greywater share of 0.55 [S26][S09]. Kitchen water is never greywater
  (course design rule, V3).
- **Irrigation**: gross need = area × max(0, Kc·ETo − Pe) ÷ application efficiency; drip
  0.90, sprinkler 0.75 [S12a]. No irrigation is scheduled in a month with mean temperature
  below 10 °C.
- **Crop mixes** for added area: leafy (350 kcal/m²/yr at a full season), mixed vegetables
  (900), staples and perennials (1,500), inside the measured Australian home-garden range
  [S13][S52]; each carries a protein density, Kc, perennial share and labour rate.
- **Modules**: compost bays, composting toilet with urine diversion, insect unit, mushroom
  chamber, aquaponics, digester. Each has capital from the schedule, steady and upper
  energy, heating below a temperature, hours a year, attendance interval, whether it can be
  paused for an absence, and consumables.
- **Pumping** 1.5 kWh/kL for pressure supply and 0.7 kWh/kL at garden flows [S21]; bore
  0.8 and greywater 0.3 kWh/kL (course assumptions); electricity $0.33/kWh.

## 4. The five fixed homes

| Home | Client (fictional) | Climate station | Plot | Designated growing area | Roof plan area | Existing storage |
|---|---|---|---|---|---|---|
| Canberra | Taylor | 070014 | 800 m² | 443 m² (preset 450) | 296 m² (preset 300) | 5 kL |
| Alice Springs | Nguyen | 015590 | 2 ha parcel, 50 × 40 m working area | 408 m² (400) | 351 m² (350) | 22 kL + 100 kL/yr bore |
| Brisbane | Patel | 040214 | 300 m² lot + 40 m² common-property allocation | 88 m² (90) + 40 m² | 168 m² (170) | 3 kL |
| Adelaide | Rossi | 023000 | 700 m² | 261 m² (250) | 229 m² (230) | 5 kL |
| Darwin | Williams | 014015 | 1 ha parcel, 60 × 40 m working area | 506 m² (500) | 305 m² (300) | 45 kL |

**Geometry is computed, never typed.** `model/case.py` holds every plan as rectangles and
circles in metres. Footprint, roof plan area (footprint plus eaves, plus roofs over
hardstand), roof zones and growing areas are derived from it and must reproduce the preset
within the larger of 15 m² or 4 %. The model's self-check also fails on overlapping
cover, anything outside a boundary, a roof zone off a roof, a tank on a building, a rural
working area outside its parcel, or rooms that do not tile the floor plan. Footprint, roof
plan area and roof surface area are taught as three different quantities.

**Brisbane's shared garden** is 40 m² of common property outside the 300 m² lot, held as a
revocable exclusive-use allocation. It is shown on a separate scheme plan and never added to
the lot.

**Canberra's growing envelope** includes the back lawn; the client keeps at least 100 m² of
it as lawn, so at most 343 m² may be cultivated. At the other homes retained recreation lies
outside the envelope.

### 4.1 Release A: homeowner intake (week 1)

Whole-plot plan (and, for rural homes, the whole parcel plus the enlarged working area);
floor plan locating wet areas and services; boundary dimensions and area; north arrow,
scale bar and legend; footprints; roof zones and downpipes; hardstand; access; growing
zones; retained recreation; trees and shade; spot levels; existing tanks, bore and
services; easements and ownership boundaries; equipment inventory; bills; homeowner
observations; priorities; case constraints (maintenance availability, permitted uses,
installation zones, acceptable disruption); and unknowns to be measured. Every dossier fact
is tagged **known**, **estimate** or **unknown**; service routes and ground conditions that
nobody has verified are marked unknown rather than drawn with survey certainty.

### 4.2 Release B: specialist findings (week 7)

A memo dated 14 April 2028 covering April 2027 to March 2028: twelve-month tables, seasonal
profiles, critical flow events and fixture flows, level survey for pump head, water
quality, soil and sun by growing zone with a relative productivity, a food-waste audit,
existing pump energy, recurring costs and maintenance observed, missing-data notes,
implications and remaining questions. Specialists analyse; they do not choose the system.
Downloadable CSVs carry units and a shared data dictionary.

The measured year is **synthetic**, generated by running each home's existing condition
through the scenario model on a seeded perturbed year (`model/release_b.py`), so tables,
tank levels, bills and memo agree. It is distinguished everywhere from sourced BoM long-term
climate and from the separate synthetic dry year. One observed year says nothing about
drought reliability. Every student choosing a home receives the same Release B, whatever
their A1 said; A2 asks for a short reconciliation of what their own plan would have missed.

## 5. The design problem

### 5.1 Decision variables (seven, discrete, bounded by what exists)

| Variable | Range | Bound |
|---|---|---|
| New storage | per-home steps, e.g. Canberra 0–20 kL, Darwin 0–112.5 kL, Brisbane 0–4 kL slimline | the client's installation zones |
| Connected roof zones | subsets of the existing guttered zones | existing roof only |
| Cultivated area beyond the existing plantings | 0 to the cultivable maximum, in quarter steps | growing envelope minus retained areas; Brisbane adds the allocation |
| Crop mix | leafy, mixed, staples and perennials | — |
| Water strategy | garden only; garden and permitted indoor uses; either with greywater diversion | the client's permitted uses; subsurface, same-day greywater (course rule) |
| Biological and sanitation modules | any subset of six | attendance, absence and energy limits |
| Operating schedule | year-round; rest added crops in the three peak-deficit months; garden-first in peak months | garden-first only where mains water exists |

### 5.2 Client priority service targets

Each home carries four targets, set from the model rather than as aspirations
(`model/scenario.py`, `TARGETS`). For every home the existing condition fails at least
one, and a staff check over the whole decision space found feasible options:

| Home | Targets (short form) | Feasible options | Cheapest feasible capital | Budget margin | Energy margin |
|---|---|---|---|---|---|
| Canberra | beds and trees fully watered on-site every month; toilet and laundry ≥90 % rainwater in winter; frost-proof; ≤2 h a week, nothing more often than weekly | 360 | $7,216 | $22,784 | 4.59 kWh/d |
| Alice Springs | carting ≤40 kL/yr; bore within allocation and draw rule; priority plantings ≥45 % of need on-site; locally serviceable | 352 | $9,515 | $20,485 | 3.75 kWh/d |
| Brisbane | toilet ≥70 % rainwater; ≥120 kg produce with the allocation; existing beds fully watered ≥9 months; quiet, 600 mm path, courtyard kept | 1,909 | $4,389 | $25,611 | 4.81 kWh/d |
| Adelaide | beds and trees ≥90 % on-site across December–February; new running cost ≤$250/yr; producing ≥10 months | 342 | $4,290 | $25,710 | 4.86 kWh/d |
| Darwin | carting ≤20 kL/yr; unattended through the July absence; overflow to a nominated point; main garden ≥60 % of dry-season need | 232 | $17,133 | $12,867 | 3.97 kWh/d |

The site publishes the targets and a rounded-down margin, not the configuration. In the
synthetic dry year every cheapest option misses at least one target, which is exactly where a
student must argue whether extra resilience is worth its cost. Students may explain target
conflicts or propose a phased approach. Nothing rewards spending the allowance.

### 5.3 What students evaluate

The existing-condition baseline plus three feasible alternatives — minimum intervention,
balanced and higher resilience — in a small reproducible spreadsheet grid, with dominated
options identified. Required calculations: monthly supply, demand and storage balance;
critical service flow in L/min and a justified pump head; capacities and duty cycles; useful
food and protein with stated limits; nutrient recovery against uptake; peak-month process
energy with the month named; capital and operating cost; sensitivity to demand, yield, price
and the dry year. Pipe diameters, fitting losses, reinforcement, wiring, certification and
fabrication drawings are out of scope: students specify performance requirements and
commissioning checks.

Imported resources, recurring costs, maintenance hours, uncertainty and contingency are all
counted. Preserved food is not counted twice, and output grown on imported feed is not
closed-loop output.

### 5.4 Diagnostics kept from the first draft

The five closure indicators and the climate-normalised reference bands (recipe v6) remain
as diagnostics on the method page. They are not a target, not a grade, and not a recipe to
approach. Water closure is never shown without garden water satisfaction beside it.

## 6. Constraints, prices and safety

### 6.1 Budget

$30,000 of new spend including 10 % contingency, priced only from the course schedule.
The v4 schedule stands; retrofit lines added in v5 (course assumptions): slimline tank
$450/kL and $300 per module; roof-zone connection $600 per zone; rainwater-to-mains
changeover $450; overflow to a nominated discharge point $800; frost protection $250;
acoustic enclosure $350 per pump; drip disc filter $200. What the schedule does not price is
published beside it, as in v4.

### 6.2 Energy

5 kWh/day, peak-month average, counted loads only (v4 §2.1 boundary), summed month by month
with uncertain loads at their upper estimate. The first scenario draft averaged pumping over
the year; v5 names the peak month.

### 6.3 Measurement allowance

$1,500 per home for equipment and services from an 18-line measurement schedule (course
assumptions). Demonstrated feasible before publication: the Wattle Street practice plan costs
$1,345 with 77 hours of consultant time. A staff check found comparable plans at every client
home costing $1,135–$1,470 (`model/output/measurement-check.md`); those plans are not
published.

### 6.4 Safety and compliance

Unchanged from v4 §4.2 and `verification-log.md` V3–V10: greywater, excreta and urine
storage, compost pasteurisation, one named fermentation recipe, insect substrates, drinking-
water treatment performance and fish legality are course design rules, each with its
jurisdiction and instrument, distinguished from the law. Students design; they do not build,
operate, eat from or drink from anything.

## 7. Twelve weeks

| Wk | Topic | Lead home | Assignment component produced |
|---|---|---|---|
| 1 | Client commission, programme rules, engineering boundaries, five-home intake | all five | client question and decision map, first pass |
| 2 | Site survey, requirements, mass balances and measurement objectives | Canberra | annotated measurement locations, variables list |
| 3 | Water monitoring: rainfall, roof runoff, demand, tank levels, flow | Alice Springs | water instrument table (quiz 1) |
| 4 | Soil, microclimate, crop demand and yield, spatial sampling | Brisbane | soil and sun sampling design |
| 5 | Food, waste and nutrient audits; biological options; measurement uncertainty | Adelaide | audit design and uncertainty budget (quiz 2) |
| 6 | Twelve-month sampling, sensors, calibration, data quality, cost, handover | Darwin | schedule, QC, costed plan, data dictionary |
| 7 | A1 due; twelve-month jump; specialist findings and uncertainty | Canberra | Release B interpretation and A1 reconciliation |
| 8 | Water-system sizing: storage, reuse, treatment, flow and energy | Alice Springs | monthly balance and pump duty (quiz 3) |
| 9 | Food-system selection: perennials, mushrooms, insects, aquaponics | Brisbane | module screening with reasons to accept or reject |
| 10 | Waste, sanitation, preservation and integrated balances | Adelaide | nutrient and waste balances (quiz 4) |
| 11 | Alternatives, constrained optimisation, costs and resilience | Darwin | scenario grid, dominance, sensitivity |
| 12 | Investment proposal, design review, bridge to SLOP4762 | all five | review-ready proposal (quiz 5) |

Every week from 2 to 11 carries a substantive Five homes comparison; each home leads
exactly twice. Leads are not chosen to line up with the easiest or hardest climate.
Measurement method needed for A1 is taught in weeks 1–6.

## 8. Assessment (totals 100 %)

| Item | Weight | When |
|---|---|---|
| Five conceptual quizzes, 8 % each | 40 % | weeks 3, 5, 8, 10, 12 |
| A1 Year-long Measurement Programme | 20 % | due week 7 |
| A2 Household Resilience Investment Proposal | 40 % | exam period |

No oral assessment.

**A1** (suggested 1,800–2,200 words plus plans and tables): client question and decision
map; annotated measurement locations; variable, instrument, range, accuracy, frequency and
duration table; twelve-month sampling schedule covering seasonal and event variation;
calibration and quality control; missing-data procedure; safety, permissions and household
data privacy; equipment and services cost against the $1,500 allowance and a labour schedule;
data dictionary; how the readings support the later design. Rubric: decision relevance 25;
measurement and sampling design 30; uncertainty and quality control 20; feasibility, cost and
safety 15; communication 10.

**A2** (suggested 2,500–3,000 words plus workbook and plans): executive recommendation;
client targets and acceptance criteria; interpretation of Release B; baseline and three
alternatives; reproducible workbook; selected concept layout and system-flow schematic;
capital and operating cost and the borrowing justification; sensitivity and failure
response; maintenance plan; approval and commissioning pathway; A1 reconciliation. Rubric:
engineering balances and sizing 25; alternatives, optimisation and value 25; interpretation
and uncertainty 20; client and site fit and feasibility 20; communication 10. No marks for
visual extravagance or for presenting a concept as build-ready.

## 9. Site and visual treatment

- Pages: home; programme (teaching fiction); clients index and one page per home, each with
  Release A and a separate Release B page; twelve lectures with decks; twelve tutorials; two
  assignment briefs and five quizzes; method (decision reference, costing, datasets, the
  Wattle Street worked optimisation, diagnostics); resources (glossary, formula sheet,
  templates); people; policies.
- Tutorials: a 60–90 minute sequence, concrete inputs, an annotated worked example, two
  graduated exercises, and worked feedback on practice data. No solution to an assessed home.
- Plans, charts and schematics are drawn in the page from data as SVG. No unlabelled
  placeholder stands where a student needs a number.
- Illustrations are optional and follow later. Until then each has a reserved slot with a
  temporary drawn illustration, and `research/asset-manifest.md` lists filename, page,
  purpose, dimensions and alt text.

## 10. Checked mechanically, judged manually

Spec tests (`spec/course-contract.test.ts`) check: identity and dates; twelve lectures,
twelve tutorials and twelve linked decks; assessment weights, weeks and rubrics; the lead-home
allocation and Five homes coverage; five fixed homes and no custom-site route or text; plan
geometry against presets and boundaries; Release A and B pages and dataset files with their
schema, units and synthetic labels; the paired water indicators; hard constraints and
reference costs; targets carrying a published feasibility margin; the practice grid's
dominance marks; and citations that resolve to a reference entry. Teaching quality, story
balance and diagram readability are judged in the browser at both marking viewports.

## 11. Decision record

- **2026-09-17** (v4): identity; quiz weeks; bands as performance evidence; site set; hard
  constraints; no oral; score tables, not a calculator.
- **2026-09-18** (v5): the consultancy redesign in §0. The first draft's commits are kept as
  history; nothing was rewritten to look test-first.
