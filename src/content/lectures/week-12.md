---
title: What fails first
description:
  Week 12 — assembling the whole household model, testing it against the two hard
  constraints and a dry year, and naming the failure you cannot design away
week: 12
date: 2027-05-24
teachers:
  - harriet-oyelaran
  - teodor-vasilache
related:
  - sessions/week-12
  - assessments/capstone-master-plan
  - assessments/quiz-5
---

## The question

Eleven weeks have each produced a sized subsystem. **Put them in one model, run
the year, and find out which one gives way first.**

Almost every design fails somewhere the student did not expect, because the
subsystems compete for three shared resources — water, area and the daily energy
allowance — and each week sized its piece as though it had first call.

## The method: one balance, five checks

Assemble every week's output into a single annual model, then run five checks in
this order.

**1. Do the mass balances close?** Water in equals water used plus overflow plus
loss. Dry matter in equals dry matter out plus a stated respiration term. Nitrogen
in equals nitrogen applied plus nitrogen stored plus nitrogen exported. A stream
that appears in no balance has been forgotten.

**2. Does the energy fit?** Peak-month average daily load, with the month named,
every counted load listed with its power and duty cycle, and **uncertain loads at
their upper estimate**. The reference designs declare 0.65 kWh/day of uncertain
load on top of what the model computes, and land between 2.18 and 4.01 kWh/day
against the 5 kWh/day cap. If you added a mushroom chamber, a controlled
fermentation space, a dehydrator and a heated digester, their combined upper
estimate is about 1.65 kWh/day — more headroom than some sites have left.

**3. Does the budget fit?** Every line from the published schedule, plus the
required 10 % contingency. The excellent reference designs cost $24,860 to
$28,875. At Darwin that leaves **$1,125** of a $30,000 allowance, which is inside
the noise of a screening model priced from retail listings. Treat a design that
lands within a few thousand dollars of the cap as untested, not as compliant.

**4. Do the indicators pair?** Water closure is never reported without garden
water satisfaction. Alice Springs' excellent reference design reaches 97 % water
closure with 16 % garden water satisfaction, and a design that shows only the
first number is hiding the second.

**5. What happens in a dry year?** Re-run against the synthetic dry-year dataset
and name what fails first.

## What the five sites teach together

| Site | Binding constraint | The number that tells you |
|---|---|---|
| Canberra | **Season length and cold** | 92 frost days; 1.75-year excreta storage; larvae thermally productive 19 % of the year |
| Alice Springs | **Water, absolutely** | 1,650 mm/yr of irrigation demand per m²; 97 % water closure achieved by watering 16 % of the deficit |
| Brisbane | **Area and proximity** | 130 m² of growing space; 11 % nitrogen uptake; strata rules no indicator scores |
| Adelaide | **Phase, not volume** | Rain in winter, demand in summer; 61 kL imported and nothing overflowing |
| Darwin | **Timing, not volume** | 411 kL collected, 245 kL overflowed, 48 kL imported, in the same year |

Five different answers to the same brief. None of them closes the loop.

## The honest summary

At the excellent reference design, across all five sites:

- **Food energy closure: 2.9 % to 15 %.** The household still buys most of its
  food.
- **Protein closure: 4.9 % to 25 %.** Better, and almost entirely from the garden
  rather than from fish.
- **Water closure: 72 % to 97 %** — but paired garden water satisfaction of
  **16 % to 81 %**.
- **Nutrient closure: 6 % to 27 %.** Most of the household's nitrogen leaves.

A course that concluded otherwise would be selling something. What these designs
demonstrate is not self-sufficiency; it is **how far a well-reasoned design gets,
and exactly where it stops** — which is the more useful thing to be able to
calculate.

## The boundary, and what lies past it

Every figure above excludes energy and shelter. Your digester's biogas was
recorded and not credited. Your house's heating, cooling, lighting, cooking, hot
water and fridge were never in the counted-load list at all — and a four-person
household uses about 21 kWh a day in total, against the 5 kWh/day this course
governs.

So the loop you have modelled sits inside a much larger one you have not touched.
That larger loop is **SLOP4762 — Designing the Closed-Loop Household II: Energy
and Shelter**, a proposed follow-on course which would add energy physics and
introductory thermodynamics to the prerequisites, and which would let the biogas,
the thermal mass and the roof area you have already committed start earning their
keep.

Design part one so that part two is still possible. A roof entirely given to
catchment has nowhere left for collectors.

## What this week hands you

The **capstone skeleton**: assembled model, five checks run, failure modes named,
and an explicit list of what you did not model and what you were not sure about.
The uncertainty list is marked. Leaving it short does not make it shorter.
