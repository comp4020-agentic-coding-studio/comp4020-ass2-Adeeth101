---
title: Log reductions, not reassurance
description:
  Week 8 — the multi-barrier train, what each barrier is measured to achieve, and
  the difference between a filter's laboratory figure and its field figure
week: 8
date: 2027-04-26
teachers:
  - teodor-vasilache
related:
  - sessions/week-08
  - assessments/quiz-3
---

## The question

Roof water is not clean. **What does each barrier in your treatment train
actually remove, expressed as a number somebody else could check, and what does
running it cost in energy?**

"Filtered" is not an answer. Neither is "we boil it if we are worried".

## The method: barriers, each with a measured log reduction

A log reduction is an order of magnitude: 1 log removes 90 %, 2 logs 99 %, 3 logs
99.9 %. The WHO household water treatment scheme rates performance **separately
for bacteria, viruses and protozoa**, because a technology strong against one can
be useless against another:

| Rating | Bacteria | Viruses | Protozoa |
|---|---|---|---|
| Three star | ≥4 log | ≥5 log | ≥4 log |
| Two star | ≥2 log | ≥3 log | ≥2 log |
| One star | meets the two-star bar for two of the three classes | | |

Measured performance for the barriers this course costs:

- **First flush and leaf screen.** No log rating. It removes the load the rest of
  the train would otherwise have to handle.
- **Sedimentation and cartridge pre-filtration.** Turbidity control. Its job is to
  let the disinfection step work, and UV's job is impossible through turbid water.
- **BioSand filter.** About **2.5 log** for *E. coli* once mature. But run
  intermittently it drops to **1.67 log** against 3.71 log continuous, and the
  field average across studies is about **1.1 log**. The gap between the
  laboratory figure and the field figure is the teaching point of this week.
- **Ultraviolet disinfection.** Class A systems deliver **≥40 mJ/cm² over lamp
  life**, with a UV sensor and a flow restrictor. Lamps need replacing every
  **nine to twelve months** — an operating cost, not a capital one.

One scope correction worth carrying: **no Australian retailer page reviewed for
this course claimed NSF/ANSI 55 Class A.** Australian units cite **WaterMark**.
Do not write a Class A claim into a design you have not sourced.

## Worked example: Brisbane

Brisbane has the smallest roof (170 m²) and the most intense rain (1,146 mm a
year in a subtropical pattern). First flush, at 10 L per 50 m²:

    170 m² ÷ 50 × 10 L = 34 L diverted per event

Over the year that is real water lost, and Brisbane can least afford it — which is
the trade. Divert less and the pre-filter clogs faster and the UV sees higher
turbidity.

Energy for the treatment train:

    UV lamp 25 W × 24 h = 0.60 kWh/day

Against a 5 kWh/day allowance that is 12 %, running continuously, all year,
whether or not anyone draws water. It is the largest constant load in the
reference design, and the first thing to interrogate if your energy budget is
tight.

### Brisbane's other constraint

The townhouse is the hardest site for this week for a reason that is not
hydraulic. 130 m² of growing area, a shared strata garden, and neighbours close
enough that a tank overflow, a filter backwash or a treatment plant's noise is
somebody else's problem. Amenity and shared-property rules are design constraints
here in a way they are not on a two-hectare block, and no indicator in this course
scores them. Your site notes must.

## Five sites

| Site | Raw-water character | What the train has to handle |
|---|---|---|
| Brisbane | High-intensity subtropical rain | Highest first-flush and turbidity load per mm; least roof to lose it from |
| Darwin | Extreme wet-season intensity | Enormous flows for six months, then nothing. Size for the wet, operate for the dry |
| Canberra | Moderate, even | The easiest raw water in the set |
| Adelaide | Long dry spells between events | Roof accumulates dust and debris for months, so the first flush after a dry spell carries the year's worst load |
| Alice Springs | Very few events, plus bore water | Bore water is a different problem: dissolved solids and hardness, not pathogens. The train needs a different barrier |

## What this week hands you

A **treatment train drawn barrier by barrier**, each with its log reduction by
pathogen class and its source, plus the train's counted energy load. Where you
cannot source a figure, say the barrier is unquantified rather than assigning it a
number.

The water quality you are designing against now comes from your home's Release B
findings, not from a generic assumption — which is usually where a train drawn
before the handover stops being adequate.
