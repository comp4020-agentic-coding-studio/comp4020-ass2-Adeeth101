---
title: The month the tank runs dry
description:
  Week 9 — the monthly storage balance, why annual averages hide drought, and a
  synthetic dry-year dataset to test your design against
week: 9
date: 2027-05-03
teachers:
  - teodor-vasilache
slides: /decks/week-09/
related:
  - sessions/week-09
  - assessments/capstone-master-plan
---

## The question

You have a supply curve from week 7 and a demand curve from week 2. **What size
tank turns one into the other, what does it cost, and what still fails?**

The last clause is the week. Every storage design fails somewhere; the question is
whether you know where before your marker does.

## The method: the monthly balance

    V(t) = min( capacity, V(t−1) + inflow(t) − demand(t) )

Run it over a repeating average year with a **three-year spin-up** and report year
three, so the starting volume you guessed stops mattering. Three rules:

1. **Domestic demand has first call.** A domestic shortfall is carted in, and
   carted water counts as an import in the closure denominator.
2. **The garden gets greywater first, then whatever the tank still holds.** A
   garden shortfall lowers garden water satisfaction, not water closure — which is
   exactly why the two are always published together.
3. **When the tank is full, inflow overflows.** Overflow is reported. It is not a
   loss you can spend.

Storage comes out of the same $30,000 as everything else, at $130 per kL for the
shell plus $1,000 per tank for pad, plumbing and overflow.

## Worked example: Darwin, where the annual balance lies

Darwin's numbers, all from the excellent reference design:

| Quantity | Figure |
|---|---|
| Roof yield | 411 kL/year |
| Domestic demand | 219 kL/year |
| Annual surplus | **+192 kL** |
| Storage | 76 kL (45 kL existing, 31 kL new) |
| **Water still imported** | **48 kL/year** |
| **Water overflowing** | **245 kL/year** |

Read those last two rows together. The site throws away 245 kL and buys 48 kL, in
the same year, with a surplus on paper of 192 kL. **1.4 % of Darwin's rain falls
in its driest four months.** The annual balance is not merely imprecise here; it
is the wrong question.

The obvious response is a bigger tank. Test it: raising new-storage spend from
$4,000 to $9,000 buys 38 more kilolitres and moves Darwin's water closure by
**0.06**, while consuming $5,600 of a $30,000 allowance once establishment is
counted. That result is why this course's own reference designs were re-costed and
their storage reduced — the earlier recipe was buying capacity the wet-dry cycle
could not use.

Storage saturates. Find where yours does before you spend the budget.

## The drought-year dataset

Average-year monthly means contain no droughts, so a design tuned to them is
tuned to a year that never happens. The course supplies a **clearly labelled
synthetic dry-year dataset** for each site — monthly rainfall scaled from that
site's Bureau of Meteorology statistics toward a low decile, then perturbed.

It is synthetic. It is not a historical drought and must not be described as one.
Its job is to make your design fail somewhere visible, so you can say what fails
first and what you would do about it.

## Five sites: storage, imports and overflow at the excellent design

| Site | Storage | Imported | Overflow | Where it bites |
|---|---|---|---|---|
| Darwin | 76 kL | 48 kL | **245 kL** | Six dry months. Storage is not the answer; demand management is |
| Adelaide | 36 kL | **61 kL** | 0 kL | Rain and demand are out of phase. The worst water closure in the set, 72 % |
| Canberra | 36 kL | 16 kL | 0 kL | Even rain means small storage works. The easiest site for this week |
| Alice Springs | 53 kL | 8 kL | 0 kL | The capped bore carries the site; without it, nothing closes |
| Brisbane | 34 kL | 10 kL | 8 kL | Good rain, but 170 m² of roof and nowhere to put a big tank |

## What this week hands you

A **sized storage system** with the month it empties named, the volume imported,
the volume overflowing, and the same figures re-run against the dry-year dataset.
A design that never fails on the dry year has not been tested hard enough.
