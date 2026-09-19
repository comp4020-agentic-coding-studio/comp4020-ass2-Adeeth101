---
title: Water is the yield limit, not sunlight
description:
  Week 2 — evapotranspiration, effective rain and the monthly deficit that
  decides how much of your growing area is actually productive
week: 2
date: 2027-03-01
teachers:
  - noor-bakhshi
related:
  - sessions/week-02
  - lectures/week-09
---

## The question

You have between 130 and 500 m² of growable ground depending on your site. The
naive sizing — area × days × yield — says Alice Springs, with 400 m² and a long
warm season, should out-produce Canberra. **It does not, and the reason is that
the naive sizing never asked where the water comes from.**

So: month by month, how much of the garden's water demand does rain meet, and
what does the shortfall do to yield?

## The method: FAO-56, three equations

**Reference evapotranspiration**, Hargreaves, FAO-56 Equation 52:

    ETo = 0.0023 × (Tmean + 17.8) × √(Tmax − Tmin) × Ra

`Ra` is extraterrestrial radiation from latitude and day of year (Equations
21–25). FAO warns this over-predicts in humid conditions, which is why Brisbane's
figure carries a caveat and the others do not.

**Crop demand:** ETc = ETo × Kc. This course uses Kc = 0.95 for a mixed garden, a
blend inside FAO-56 Table 12's range and a **course assumption**.

**Effective rain**, FAO Irrigation Training Manual 3, Annex 1:

    Pe = 0.8P − 25   for P > 75 mm/month
    Pe = 0.6P − 10   for P ≤ 75 mm/month

The deficit is ETc − Pe, floored at zero, and only in months warm enough to grow.

## Worked example: Canberra

Canberra's annual ETo is 1,244 mm against 616 mm of rain: P/ETo = 0.50. Run the
monthly deficit across the growing season and it sums to **932 mm of net
irrigation per square metre per year**.

Over the full 450 m² growable area:

    932 mm × 450 m² = 419,400 L = 419 kL/year

The roof delivers 142 kL, and the household has first call on it. **Canberra's
garden is water-limited long before it is land-limited**, and the excellent
reference design still only meets 20 % of the garden's deficit. That is not a
failure of the design. It is the site.

### Where Canberra wins, and the model cannot see it

Two advantages sit outside every number this course scores.

**Rainfall evenness.** 28 % of Canberra's rain falls in its driest four months —
the highest share of the five sites, against Darwin's 1.4 %. Even rain means
storage does less work, which is why Canberra's excellent design needs 36 kL of
tank where Darwin's needs 76 kL.

**Chill.** Chill hours cannot be computed from monthly means: the sine-curve
method gives Canberra 1,979 hours against the ~720 that regional guides report,
and gives Brisbane zero against ~150. So this course uses **regional chill
categories, not a formula**. Canberra sits in the high-chill band, which opens
apples, pears, cherries and walnuts. Brisbane is low-chill and Darwin is
effectively nil, so their orchards are a different list of species entirely.

## Five sites: net irrigation demand per m² of garden

| Site | Net irrigation | P/ETo | Chill category | What it means for the planting plan |
|---|---|---|---|---|
| Canberra | 932 mm/yr | 0.50 | high (~720 h) | Temperate fruit and nuts available; frost defines the annual season, not water |
| Alice Springs | **1,650 mm/yr** | 0.16 | low | Nearly twice Brisbane's demand per m². Irrigated area, not total area, is the real design variable |
| Brisbane | **651 mm/yr** | 0.85 | low (~150 h) | Lowest demand per m², but only 130 m² exists to plant, including the shared strata garden |
| Adelaide | 952 mm/yr | 0.43 | medium (~500 h) | Rain falls in winter and demand peaks in summer; the two barely overlap |
| Darwin | 832 mm/yr | 1.07 | nil | Wet season needs no irrigation at all; the dry season needs almost all of it |

## What this week hands you

A **planting plan with a monthly irrigation demand curve** underneath it: area
committed by month, deficit by month, and an honest statement of how much of your
growable area you are choosing to leave unplanted because you cannot water it.

Weeks 7 to 9 size the supply that curve is asking for. Do not adjust the curve to
suit a tank you have not yet sized.

Everything here is a **scoping estimate** from long-term climate records, not a
measurement of this garden. What the garden actually draws is one of the things
Assignment 1 has to buy.
