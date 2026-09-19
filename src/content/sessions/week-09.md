---
title: Running the tank balance, then breaking it
description:
  Week 9 tutorial — size storage on a monthly balance, find where the curve saturates, then re-run the whole thing against the synthetic dry year
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
---

## Before

Bring weeks 2 and 7 — demand and supply. Download the dry-year dataset for your
site before the session; it is on the [costing and method pages](/method/) and it
is clearly labelled synthetic.

## In the room

**Build the balance.** Domestic first, garden second, overflow when full. Spin up
three years. Students who skip the spin-up get an answer that depends entirely on
the starting volume they guessed.

**Then find your saturation point.** Step the tank up in 10 kL increments and plot
water closure against capacity. Everybody's curve flattens; the question is where.
Spending past your own flattening point is how the earlier version of this
course's reference designs went $9,545 over budget.

**Then break it.** Swap the average year for the dry year and run again. Name what
fails first, in which month, and what you would change.

## Afterwards

You now hold the water half of the capstone. Darwin students: explain, in one
sentence, how a site can overflow 245 kL and import 48 kL in the same year.
