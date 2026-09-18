---
title: Which fish you may keep, and for how many months
description:
  Week 5 — feed-rate ratios, stocking limits and seasonal species rotation, plus
  the jurisdiction question the thermal model cannot see
week: 5
date: 2027-03-22
teachers:
  - noor-bakhshi
related:
  - sessions/week-05
  - assessments/quiz-2
---

## The question

Aquaponics is sized from the feed, not from the fish and not from the plants.
**Given your climate and the law where your site is, what can you keep, for how
many months, and what does that let you grow above it?**

## The method: the feed-rate ratio

FAO Technical Paper 589, *Small-scale aquaponic food production*, gives the three
numbers a small system is sized from:

| Rule | Figure | Where |
|---|---|---|
| Feed rate ratio, leafy greens | 40–50 g of feed per m² of grow bed per day | p. 17, §2.4.2 |
| Feed rate ratio, fruiting vegetables | 50–80 g/m²/day | p. 17, §2.4.2 |
| Maximum stocking density | 20 kg of fish per 1,000 L, and "strongly recommended not to exceed" | p. 109, §7.3.3 |
| Daily water loss | 1–3 % of system volume | p. 29, §3.4 |

That last one matters more than it looks. A 1 m³ system loses 10–30 L a day —
about 5 % of the household's daily domestic water. This course uses a placeholder
top-up of **20 L/day** and sizes it properly in weeks 7 to 9. Aquaponics is not
where your water goes.

## Worked example: Adelaide

Adelaide's monthly mean runs 11.3 to 22.7 °C. No single legal species covers
that, so the site needs a **rotation** — and rotation means a harvest-and-restock
cycle, not one continuous stock.

A 4 m² bed at 50 g/m²/day for twelve months:

    50 × 4 × 365 = 73 kg feed/year
    73 kg ÷ FCR 2.0 = 36.5 kg live fish
    × 40 % fillet × 20 % protein = 2.9 kg of protein

Then apply the closure rule. Adelaide's larvae cover 9 % of the ration, so only
9 % of that fish is grown on site:

    2.9 kg × 0.09 = 0.26 kg of protein counted, against 67.5 kg required

The fish tank is a **nitrogen delivery system for the grow bed** that happens to
produce a meal. Size it for the greens.

## What the model cannot see: you may not be allowed to keep it

The screening model ranks species by temperature alone. For Canberra it returns
**Murray cod and rainbow trout, seven months** — and Murray cod is precisely the
species an ACT household may not keep without a licence.

The *Nature Conservation Act 2014* (ACT) excludes fish from the definition of
"animal" **unless** the fish has special protection status, which covers
ACT-listed threatened species and EPBC-listed ones. Silver perch is ACT-vulnerable
and EPBC critically endangered; Murray cod is EPBC-listed. Keeping a non-exempt
animal with special protection status carries up to 200 penalty units and two
years, and the current exempt-animals declaration lists no fish at all. Separately,
**importing any live fish into the ACT** needs a licence or the conservator's
written approval.

| Species | ACT | NT | Queensland | South Australia |
|---|---|---|---|---|
| Barramundi | No conservation licence; import licence still applies | No licence to keep | No aquaculture authority | No aquaculture licence |
| Jade perch | As above | No licence | No authority | No licence |
| **Silver perch** | **Licence required** | No licence | No authority | Not noxious |
| **Murray cod** | **Licence required** | No licence | No authority | Not noxious |
| Rainbow trout | No conservation licence | No licence | No authority | Not noxious |
| Redclaw crayfish | Not established | Not noxious | Native | **Noxious: not to be held without authorisation** |

Queensland, South Australia and the Northern Territory all define aquaculture
around **sale, trade, business or research**, so a household system for its own
table needs no aquaculture licence there. Tilapia is restricted noxious matter
everywhere it appears: the Queensland keeping offence is 500 penalty units, about
$86,350 at the current unit value — not the $220,000 that circulates online, which
is a different Act in a different state at a historical unit value.

**And here is the part worth remembering.** Re-run the model for Canberra with the
two special-protection species removed and the best rotation becomes jade perch
and rainbow trout, six months instead of seven. **Canberra's bands do not move at
all.** Counted fish protein stays at 0.27 kg/year, because it is limited by the
larvae supply from week 4, not by the thermal window. The legal constraint costs
you nothing you were being scored on — but you still have to design around it, and
say so.

## Temperature bands, and one conflict

| Species | Course band | Primary source |
|---|---|---|
| Barramundi | 25–30 °C | Business Queensland: needs 20–30 °C, ideal 25–30, deaths below 13 °C. FAO Table 7.1: vital 18–34, optimal 26–29 |
| Silver perch | 23–28 °C | NSW: tolerance 2–38 °C, optimum 23–28. **Queensland says optimum 20–30 °C.** Two government sources disagree; cite the one for your jurisdiction |
| Murray cod | 18–27 °C (**course assumption**) | The only government figure found is a culture target: maintain at 24–25 °C |
| Jade perch | 20–30 °C (**course assumption**) | Business Queensland gives thresholds, not a band: spawns above 23 °C, aerate above 30 °C, growth declines at 20 °C, mass deaths at 13 °C |
| Rainbow trout | 10–18 °C | FAO Table 7.1: vital 10–18, optimal 14–16. NSW: 10–22 °C suitable, best near 15 °C |

## Five sites

| Site | Best thermal rotation | Months | The catch |
|---|---|---|---|
| Darwin | Barramundi + jade perch | 12 | None thermally; this is the site aquaponics was invented for |
| Brisbane | Murray cod + rainbow trout | 12 | 12 months, but the bed competes with the garden for 130 m² |
| Adelaide | Murray cod + rainbow trout | 12 | Two full changeovers a year, each one a restocking event |
| Alice Springs | Jade perch + rainbow trout | 11 | Summer cooling, not winter heating, is the load |
| Canberra | Murray cod + rainbow trout (7) | 7 → **6 legally** | Licence, or drop to jade perch and trout. Either way about 0.5 kWh/day of winter tank heating |

## What this week hands you

A sized fish and bed pair, the species named **with its approval pathway in your
own jurisdiction**, and the imported-feed line carried forward from week 4.
