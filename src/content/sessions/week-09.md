---
title: Running the tank balance, then breaking it
description:
  Week 9 tutorial — size storage on a monthly balance, find where the curve
  saturates, then re-run the whole thing against the synthetic dry year
week: 9
date: 2027-05-06
teachers:
  - teodor-vasilache
related:
  - lectures/week-09
  - assessments/capstone-master-plan
spec:
  - your balance runs a three-year spin-up and reports the third year
  - you report the month the tank is emptiest, the volume imported and the volume overflowed
  - you have identified the storage volume beyond which your water closure stops improving materially
  - the same model has been re-run against the dry-year dataset and the first failure is named
  - your supply side uses your home's measured year, labelled as synthetic case data
---

## What this tutorial is for

You have a supply curve and a demand curve. Storage is what turns one into the
other. Today you size it, find the point past which more storage buys nothing, and
then break it on purpose.

**Story stage.** Design. Your supply side is now your home's measured year rather
than a scoping estimate — but one year, even a real one, does not establish
reliability, which is why the dry year exists.

## Open these first

- **Your home's specialist findings** for the measured year's monthly roof inflow
  and imports, from [clients](/clients/).
- **Your workbook**, sheet 2, for the irrigation demand curve.
- **The dry-year dataset for your site** — download it before the session from the
  [datasets page](/method/datasets/). It is clearly labelled synthetic.
- **[Week 9's lecture](/lectures/week-09/)** for the monthly balance method. This week
  also has [slides](/decks/week-09/).

### If you missed week 7 or 8

You do not need them. The supply side comes from your findings page and the demand
side from week 2. If you are missing week 2 as well, use **PRACTICE — Wattle Street:
a flat irrigation demand of 3 kL a month from October to March and zero otherwise.**
Invented round numbers.

## The words this week uses

- **Monthly balance** — start volume, plus inflow, minus draw, capped at capacity,
  floored at zero. Twelve rows, then repeat.
- **Spin-up** — running the balance for three years and reporting only the third, so
  the answer stops depending on the starting volume you guessed.
- **Saturation** — the storage volume past which water closure stops improving
  materially. The knee in the curve.
- **Water closure** — the fraction of water demand met from on-site sources.
  **Never reported without garden water satisfaction beside it.**

## Do this

**1. Build the balance (30 minutes).** Domestic first, garden second, overflow when
full. Spin up three years. Students who skip the spin-up get an answer that depends
entirely on the starting volume they guessed.

| month | start_kl | inflow_kl | domestic_draw_kl | garden_draw_kl | overflow_kl | end_kl | imported_kl |
|---|---|---|---|---|---|---|---|

Report the month the tank is emptiest, the volume imported, and the volume
overflowed. All three, every time.

**2. Then find your saturation point (25 minutes).** Step the tank up in 10 kL
increments and plot water closure against capacity. Everybody's curve flattens; the
question is where. Spending past your own flattening point is how the earlier version
of this course's reference designs went $9,545 over budget.

**3. Then break it (25 minutes).** Swap the average year for the dry year and run
again. Name what fails first, in which month, and what you would change. Write the
answer as a sentence, not a number.

**4. Report the pair (5 minutes).** Water closure and garden water satisfaction go on
the sheet together. A high closure achieved by not watering the garden is not a
result, and reporting it alone is the one presentational rule this course enforces
everywhere.

## The output

**A sized store with its saturation point identified**, re-run against the dry year
with the first failure named, and the water pair reported together.

## Check your own before you submit

1. Did you spin up three years and report the third?
2. Are the emptiest month, the imported volume and the overflowed volume all on the
   sheet?
3. Does your closure-against-capacity curve actually flatten, and have you marked
   where?
4. Has the dry year been run through the **same** model, not a simplified one?
5. Is the first dry-year failure named as a sentence — what, when, and what you
   would change?
6. Is garden water satisfaction beside every water closure figure?
7. Is the dry-year data labelled synthetic wherever you have quoted it?

## Where it goes next

You now hold the water half of Assignment 2. Darwin students: explain, in one
sentence, how a site can overflow 245 kL and import 48 kL in the same year.
