---
title: The irrigation demand curve
description:
  Week 2 tutorial — turn twelve rows of climate normals into a monthly irrigation
  demand curve, and decide on the numbers how much ground you will actually plant
week: 2
date: 2027-03-04
teachers:
  - noor-bakhshi
related:
  - lectures/week-02
spec:
  - you can compute ETo for one month by hand from Tmax, Tmin and latitude, and check it against your spreadsheet
  - your twelve-row deficit table uses effective rain, not total rain
  - you have chosen a planted area and can justify it against water rather than against ambition
  - your monthly irrigation demand is stated in kilolitres, not millimetres
  - the planted area you chose respects the retained-area constraint on your home's dossier
---

## What this tutorial is for

The naive way to size a garden — area times days times yield — never asks where
the water comes from. Today you replace it with a monthly balance, and the curve
that falls out decides how much of your growable ground is worth planting.

**Story stage.** Scoping. The deficit you compute comes from long-term records,
not from your client's garden. What that garden actually draws is one of the
things Assignment 1 will propose to measure.

## Open these first

- **Your client evidence workbook**, sheet 2 (climate normals) — twelve rows of
  `rain_mm`, `tmax_c`, `tmin_c`, `eto_mm` and `effective_rain_mm`.
- **[Week 2's lecture](/lectures/week-02/)**, for the three FAO-56 equations. You
  need its method section open beside you.
- **Your home's dossier** at [clients](/clients/), for the growing envelope and
  any retained area the client will not let you plant.

### If you missed week 1

Build the workbook now from the [week 1 tutorial](/tutorials/week-01/) — it takes
about twenty minutes. If you would rather catch up afterwards, use the labelled
practice climate instead and redo it on your own home later:

**PRACTICE — Wattle Street, invented round numbers, not a real climate.** Rain
40, 40, 50, 50, 60, 60, 60, 60, 50, 50, 40, 40 mm. ETo 180, 150, 120, 80, 50, 40,
40, 60, 80, 120, 150, 170 mm. Growing envelope 207.8 m². These are round on
purpose, and no conclusion drawn from them is about anybody's home.

## The words this week uses

- **ETo** — *reference evapotranspiration*, in mm. The depth of water a reference
  grass surface would lose in a month. A property of the weather, not of your crop.
- **ETc** — *crop evapotranspiration*. ETo multiplied by a crop coefficient Kc.
  The course uses Kc 0.95 for a mixed vegetable garden.
- **Effective rain** — the part of the rain that reaches the roots. Always less
  than total rain.
- **Deficit** — ETc minus effective rain, in mm, floored at zero. A wet month does
  not bank water for a dry one.
- **The demand curve** — those twelve deficits converted to kilolitres for your
  chosen planted area. "Curve" because you will plot it; a twelve-row table is the
  same object.

## Do this

**1. One month by hand, first (20 minutes).** Pick January. Compute Ra from your
site's latitude and the day of year, then ETo from Equation 52, then ETc at Kc
0.95, then effective rain, then the deficit. It takes about fifteen minutes and it
is the only way to find out whether your spreadsheet is computing what you think
it is. Write the hand answer down before you build the sheet.

**2. Build the twelve rows (30 minutes).** Add these columns to sheet 2:

| month | eto_mm | kc | etc_mm | effective_rain_mm | deficit_mm |
|---|---|---|---|---|---|
| Jan | 186 | 0.95 | 176.7 | 25.1 | 151.6 |

That row is Canberra, from its sourced climate file. Check it: 186 × 0.95 = 176.7,
and 176.7 − 25.1 = 151.6 mm. The commonest error in the room is using **total**
rainfall instead of effective — it overstates what the sky delivers by 20 to 40 %
and makes every later tank look bigger than it is.

**3. Then the decision (25 minutes).** Multiply your deficit by candidate planted
areas until the annual irrigation figure stops being absurd:

    irrigation (kL) = deficit (mm) × planted area (m²) ÷ 1000

Alice Springs students will land somewhere well under their 400 m². **That is the
correct answer, not a compromise.** Check your chosen area against your home's
retained-area constraint before you commit to it: Canberra must leave at least
100 m² of the back lawn as lawn, and Brisbane's 40 m² allocation is common
property outside the lot.

**4. Write it in kilolitres (15 minutes).** Millimetres are a depth and kilolitres
are a volume; weeks 7 and 9 need the volume. Convert all twelve and put them on
sheet 2 beside the deficits.

## The output

**A twelve-row irrigation demand curve in kilolitres**, and a planted area you can
defend on water rather than on ambition, both on sheet 2 of your workbook.

## Check your own before you submit

1. Does your hand-computed January match your spreadsheet to within a few per cent?
2. Is every deficit computed from **effective** rain?
3. Is any deficit negative? It should be floored at zero.
4. Is the final column in kL, and does it have "kL" written on it?
5. Does your planted area fit inside the growing envelope **and** respect the
   retained area?
6. Is your chosen Kc written down, with a note that it is a course assumption?

## Where it goes next

The demand curve is fixed from here. Weeks 7 to 9 size supply against it. If you
later want to plant more, change the curve deliberately and say why — do not let
it drift to match a tank.
