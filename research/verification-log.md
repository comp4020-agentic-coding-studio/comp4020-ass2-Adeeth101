# Verification log (2026-09-18)

Course design §7 required every medium- or low-confidence figure with safety, legal or
budget consequences to be checked against a primary source before publication. This file
records what was actually fetched and read, what changed, and what could not be
established. Keys resolve in `sources.md`.

Where a claim did not survive, the site either drops it or republishes it as a **course
design rule** rather than as a statement of law. A safety or legal claim does not become
true by being labelled a course assumption.

---

## V1 — Domestic water demand: 150 L/person/day [S06] — **claim not found, relabelled**

Fetched: `https://www.yourhome.gov.au/water/rainwater`, plus `/water` and
`/water/reducing-water-use`.

No per-person-per-day consumption figure appears anywhere on the Your Home rainwater
pages. The attribution was wrong. What the page does carry:

- "1 mm of rainfall on 1 m² of roof area = 1 L of rainwater" — **confirmed**.
- First-flush sizing: diverters "are typically sized to divert about 10L per 50m² of roof
  area" — **confirmed verbatim**.
- A tank-size table for a **4-person, mains-connected** household: whole of house
  5,000–20,000 L, with larger tanks "where average rainfall is highly seasonal or no mains
  water is available". That is the opposite scope from the one the figure was used for.

Nearest primary support, enHealth 2010 p.28 [S08]: "In areas supplied with mains water, the
average indoor use per household is estimated to be in the range of 300-740 L per day or
alternatively about 100-200 L per person per day." That is mains-supplied **indoor** use,
and it supports a range, not a point value.

**Action:** 150 L/person/day is published as a **course assumption** at the midpoint of
enHealth's 100–200 L/person/day indoor range, and is no longer attributed to Your Home. The
site says so wherever the figure appears.

## V2 — Roof runoff formula [S08] — **supported, attribution corrected**

Fetched: `https://www.cdc.gov.au/system/files/2025-10/enhealth-guidance-the-use-of-rainwater-tanks.pdf`
(HTTP 200, 64 pp). *Guidance on use of rainwater tanks*, enHealth, 3rd ed., ISBN
978-1-74241-325-9.

Appendix B p.46, verbatim: "run-off (litres) = A x (rainfall - B) x roof area"; A is "the
efficiency of collection and values of 0.80-0.85 … have been used (Martin 1980)"; B is "a
value of 2 mm per month (24 mm per year) … (Martin 1980)". The document's worked example,
"Run-off = 0.8 x (750-24) x 200 = 116,160 Litres", is reproduced by the model.

**Correction:** the formula is enHealth citing **Martin (1980)**, not WHO. WHO appears in
the document only for boiling and mosquito screening.

Also confirmed and now used: UV lamps "need to be replaced after between nine and 12
months", with an operational sensor; boiling need not be sustained; chlorination dosing of
40 mL liquid or 7 g granular calcium hypochlorite per 1,000 L.

## V3 — Greywater rules — **an NSW rule was being applied to five non-NSW sites**

The largest correction in the set. The draft's rule — subsurface only at ≥100 mm, no
storage, no kitchen water — is **NSW law**, and **none of the five course sites is in NSW**.

Fetched: NSW *Guidelines for greywater reuse in sewered, single household residential
premises* (DWE, May 2008) §3.6 and the NSW Health greywater diversion device page;
Queensland Plumbing and Wastewater Code 2024.1 and Business Queensland greywater pages; the
NT Government page "Reuse greywater at home" (HTTP 200) and the NT *Code of Practice for
Wastewater Management* (Chief Health Officer approval 4 Nov 2020, v1.0, 82 pp); SA *On-site
Wastewater Systems Code* 2013 with the Wastewater Regulations 2013; ACT greywater guideline,
2nd ed., October 2007 (Pub. No 07/1380).

| Requirement for **untreated** greywater | ACT (S1) | NT (S2, S5) | QLD (S3) | SA (S4) | NSW |
|---|---|---|---|---|---|
| Subsurface irrigation mandatory | no — surface and bucket diversion contemplated | **yes**, "below the surface of the ground" | **no** — the Code's land application area covers "subsurface or surface irrigation" | **yes**, "diverted to a subsurface land disposal system" | **yes** |
| A depth figure in the instrument | only for *treated* greywater (100–300 mm) | definitional only ("Subsurface … 100 mm to 150 mm"), not stated as the device criterion | none | none in the Code; defers to AS/NZS 1547 | **yes, ≥100 mm** |
| Kitchen water excluded | "not recommended" | **prohibited** | **included in the legal definition**; "not suitable for use in sewered areas" | "generally excluded … unless subject to sufficient treatment" | **prohibited** |
| Storage of untreated greywater | ≤24 h (recommendation) | ≤24 h | — | ≤24 h | **none at all** |
| WaterMark-certified device | — | not required | **required** | **required** | **required** |
| Instrument type | guidance only | prescribed code | code plus local approval | regulation plus code | guideline attached to a council-approval exemption |

So: subsurface mandatory **with** a number is NSW only; an absolute kitchen prohibition is
NSW and NT only; "no storage at all" is NSW only, the others allowing 24 hours; WaterMark
on the device is NSW, QLD and SA, not NT.

**Provenance caveats.** The NT Code was read from an Internet Archive snapshot because the
live NT host returned HTTP 403 on the PDF path; the NT Government's live greywater page,
which did fetch at HTTP 200, independently corroborates all three substantive NT rules. The
NT Code names the "Public and Environmental Health Regulations 2020" while NT.GOV.AU names
the 2014 Regulations as amended; the regulation text itself was not reached, so the
enabling-instrument citation is unverified. AS/NZS 1547 and AS/NZS 3500 are paywalled and
were **not read**, so no depth figure anywhere on the site is sourced to them.

**Action:** the course adopts the strictest column as a **course design rule** — subsurface
at ≥100 mm, no storage, no kitchen water — and says plainly that this is the course's rule,
not the law at four of the five sites. The comparison table is published in week 11, because
reading your own jurisdiction's instrument is part of the work. Nothing on the site tells a
student that a practice is lawful where the source says otherwise.

## V4 — WHO domestic water service levels [S07] — **supported, scope narrowed**

Fetched: WHO/SDE/WSH/03.02, Howard & Bartram, *Domestic water quantity, service level and
health*, from the WHO IRIS repository. Table S1 confirms the 20 / 50 / ≥100 L/capita/day
service levels verbatim.

But the report cautions that 20 L "should not necessarily be taken as evidence that 20
litres per capita per day is a health-based minimum" — its health-derived minimum is 7.5
L/c/d — and Table 6 extends "optimal" to "up to 300 l/c/d".

**Action:** cited as a global public-health adequacy framework, never as an Australian
design target. Used only to show that the course's 130–150 L/person/day sits above WHO's
"optimal" floor.

## V5 — Insects as feed [S29] — **not a regulator's rule; republished as a course rule**

Fetched: Lähteenmäki-Uutela et al. (2021) `https://edepot.wur.nl/553342` in full;
DiGiacomo (2023) *Animal Frontiers* 13(4):8; the **authoritative XML of the NSW Biosecurity
Regulation 2017** (`legislation.nsw.gov.au`, instrument sl-2017-0232, Part 2 Div 9);
Business Queensland swill and prohibited-poultry-feed pages.

All three draft claims — insects permitted as aquaculture feed in all states; substrates
must exclude meat, manure and catering waste; raw insects not permitted as feed — trace to
that single review, which cites one paywalled paper (DiGiacomo et al. 2019) for the second
and third. **No Australian regulator publishes any of them.**

What the binding law actually says. Restricted animal material means "any material derived
from a vertebrate" (cl 36). The prohibitions are "A person must not feed restricted animal
material to a **ruminant**" (cl 38(1)) and "A person must not feed material to a **pig** if
the material contains a mammal product" (cl 37(1)). The Division contains no provision about
fish, aquaculture or insects. Swill feeding is separately prohibited in every state and
territory and expressly covers hobby and pet animals — Business Queensland states the ban
applies to all pigs "including pet pigs", and to "all poultry, including pet poultry and
poultry owned by hobby farmers". FSANZ regulates insects as human food only and has no feed
position.

**Conclusion:** a household feeding its own fish is **not** captured by restricted-animal-
material or swill law, which bind pigs and ruminants. The draft's rule was stricter than the
law, and was attributed to the wrong kind of source.

**Action:** published as a **course design rule** with its biosecurity reasoning — insect
substrates are plant-based, larvae are heat-treated before feeding, and meat, dairy and fish
sludge go to compost or a digester — beside an accurate statement of what Australian law
actually prohibits and which animals it binds. Week 4 teaches the difference, because
telling the two apart is the transferable skill.

## V6 — Compost pasteurisation [S35] — **supported with a material correction**

AS 4454-2012 is paywalled and was **not read**. Authoritative secondary description fetched:
SA EPA *Compost guideline* `https://www.epa.sa.gov.au/files/7687_guide_compost.pdf` §5,
whose footnote 9 states the requirement "is consistent with the requirement specified in
section 3.2.1(a) of the Australian Standard 4454-2012 (4th edition)".

Verbatim: "a minimum of three turns and the core temperature is maintained in excess of
55oC for three consecutive days **following each turn**"; and for windrows containing
"manure, animal waste, food or grease trap waste and biosolids and/or their sludges", "a
minimum of five turns and the core temperature maintained in excess of 55[°]C for fifteen
consecutive days **following each turn**".

**Correction:** the draft read this as 15 days total across five turns. It is 15 days after
*each* of five turns, which is far more demanding. AS 4454 also defines composting as
running "not less than six weeks, including the pasteurisation phase".

**Scope:** this is a commercial windrow standard, described by a state regulator. It is not
a household requirement anywhere. The course uses it as the **performance target a household
hot-compost bay is designed against**, and says so.

WHO (2006) Vol. 4 composting figure **supported**: "Temperatures >50°C should be obtained
during at least one week in all material", immediately preceded by the caution that
composting "is mainly recommended as an off-site secondary treatment at large scale".

## V7 — Excreta and urine storage [S09] — **supported exactly, household scope added**

Read directly from the WHO 2006 Vol. 4 PDF (203 pp).

Table 4.5, dry excreta: 2–20 °C → "1.5 - 2 years"; >20–35 °C → "> 1 year"; alkaline
treatment → "pH >9 during > 6 months". All three match the draft.

Table 4.6, urine — four rows, not the two the draft carried: 4 °C / 1 month and 4 °C / 6
months, then **20 °C / 1 month → "Food crops that are to be processed, fodder crops"** and
**20 °C / 6 months → "All crops"**. The draft's two figures are correct.

**Scope the draft omitted:** Table 4.6 applies to "larger systems", meaning urine used on
crops eaten outside the source household. The text immediately above it reads: "For
individual one family system and when the urine is used solely for fertilization on
individual plots, no storage is needed." A one-month withholding period before harvest
applies to vegetables, fruit and root crops eaten raw.

**Action:** the course keeps storage as a **design rule**, and publishes WHO's household
position beside it, so a student can see the course being deliberately conservative rather
than reporting a requirement.

## V8 — Fermentation [S36] — **two methods had been fused; the pH claim is rescoped**

Fetched: NCHFP sauerkraut recipe `https://nchfp.uga.edu/how/ferment/recipes/sauerkraut/`
(adapted from USDA AIB No. 539, rev. 2015) and its general fermenting guidance; Colorado
State University Extension's sauerkraut resource; 21 CFR 114.3 via Cornell LII.

- NCHFP: 25 lb cabbage to ¾ cup canning salt (≈2.25 % by weight), 70–75 °F "fully fermented
  in about 3 to 4 weeks"; 60–65 °F takes 5–6 weeks; below 60 °F may not ferment; above
  75 °F may become soft. **The page gives no pH figure at all.**
- Colorado State Extension: "2—2.5% salt by weight" — matching the draft's percentage — but
  a different schedule, "68—72°F, for about 7—14 days".
- The draft's "2–2.5 % salt, 21–24 °C, 3–4 weeks, pH ≤4.6" therefore **fused two separately
  tested methods and added a pH threshold neither of them states.**

**What pH 4.6 actually is.** 21 CFR 114.3: acid foods have "a natural pH of 4.6 or below";
acidified foods are low-acid foods brought to "a finished equilibrium pH of 4.6 or below"
and are thereby shelf stable. It is the boundary below which *Clostridium botulinum* spores
will not germinate **in a sealed, shelf-stable product**. It is not a general pathogen
boundary: *E. coli* O157:H7, *Salmonella* and *Listeria* are unaffected by it.

**Is "2–2.5 % salt and pH ≤4.6" a general guarantee for any vegetable ferment? No.**
NCHFP's general guidance: "Use only recipes with tested proportions of ingredients"; "Do not
attempt to make sauerkraut or fermented pickles by cutting back on the salt required";
"There must be a minimum, uniform level of acid throughout the mixed product to prevent the
growth of botulinum bacteria." The numbers are properties of one validated cabbage recipe,
in which salt, the cabbage's own sugars and its buffering capacity were tested together.
Transplanting them to a vegetable with different buffering capacity, sugar content and
surface microbiota is not supported by anything read here. There is no equivalent Australian
home-fermentation standard.

**Action:** week 6 teaches **one named, cited recipe with its own stated conditions** and
says explicitly that the numbers do not transfer to other vegetables, that pH 4.6 is a
botulism boundary for sealed shelf-stable product rather than a general safety guarantee,
and that the source is US extension guidance. The course issues no recipes of its own, and
students design preservation capacity rather than making or eating anything.

## V9 — Prices [S31]–[S34] and the §2.2 schedule — **checked against Australian retail**

All pages fetched 2026-09-18. Prices AUD, mostly unit-only with freight extra.

| Schedule line | Course price | Market evidence found | Verdict |
|---|---|---|---|
| Poly storage, per kL | $130 | Duraplas 22.7 kL $2,995 (≈$132/kL); Bushmans 22.5 kL $3,090 (≈$137/kL); 30 kL $4,090 (≈$136/kL) | **supported at 22–30 kL**, which is where the bill-of-materials rule buys. $/kL is U-shaped — roughly $200–260/kL at 5–10 kL and ≈$157/kL at 46 kL — so the figure would understate both very small and very large tanks |
| Largest single poly tank | — | Bushmans 46,400 L is the practical ceiling of the mainstream range; a 50 kL moulding exists as a single-supplier outlier | The 25 kL bill-of-materials cap is **more conservative than the market allows**, and sits at the cheapest point of the $/kL curve |
| Composting toilet | $3,500 | Clivus CMHP (batch, three full-time) $3,900; CM8 Next Gen (5–10 people) from $4,750; Nature Loo NL3 $1,630 but rated for two full-time only | **supported** for a household of four, mid-range, ex-works, freight and installation extra |
| Greywater diversion, installed | $2,100 | Hardware $1,099–$2,639; installed bathroom and laundry $1,600–$3,200 | **plausible**; the installed figure rests on a search summary, so this is the weakest line in the schedule |
| Greywater treatment | $6,000 | Hardware $2,375–$2,650; Class A installed $4,000–$20,000+ | **within range**, very wide |
| Aquaponics, per 4 m² bed | $2,500 | 1,100 L with two beds (≈2.7 m²) $3,395–$3,495; compact ≈1.4 m² $599–$999 | **optimistic**: the market wants roughly $3,400 for 2.7 m². Kept as decided, and labelled as sitting at the low end |
| Point-of-entry UV | $1,200 | WaterMark-only units $283–$841; Viqua VH-410 $1,295; Armour 4 $1,550–$1,650 | **plausible for a sensor-equipped unit**, low for the top of that band. **No Australian retailer page claimed NSF/ANSI 55 Class A** — they cite WaterMark — so the site does not present Class A as an Australian requirement |
| Pump, each | $700 | Davey pressure pumps $399–$1,650 | **supported**. Onga, Grundfos and Bianco prices sit behind quote requests and could not be obtained |
| Cartridge pre-filtration | $400 | 20-inch twin housing $347–$407; cartridges $55–$182 each | **supported** for the housing, low once cartridges are counted |
| First flush and leaf screen, per downpipe | $150 | Diverters $50–$315, rain heads $26–$67; combined ≈$76–$200 | **supported** |
| Insect rearing unit | $300 | Mealworm three-tier pods $159.99. **No Australian black soldier fly unit publishes a price** | **weak**. Kept as a course assumption and flagged as such |
| Mushroom fruiting chamber | $800 | Automated tent with humidifier, inline fan, ducting and carbon filter $632 | **supported**, slightly conservative |
| Anaerobic digester | $1,500 | HomeBiogas 2 $1,433, listed out of stock | **supported** |
| Drip irrigation, per m² | $8 | Dripline alone ≈$3.55/m² at 300 mm emitter spacing; with filter, regulator, valve and timer ≈$8–15/m² for a small bed, falling toward ≈$5/m² over larger areas | **supported at the small end**, conservative over large areas |

**Not resolved:** installed greywater costs and the Class A treatment range rest on search
summaries rather than fetched pages. One tank supplier's price page returned HTTP 403 and
one retailer had a self-signed certificate. The schedule stays as decided; every line is
labelled indicative or course assumption, and the site states that it is a costing allowance
rather than a quotation.

## V10 — Fish: legality and temperature bands [S18][S19][S20] — **one wrong penalty, one missed licence**

Fetched: Business Queensland tilapia, barramundi, silver perch and jade perch pages;
NSW DPIRD tilapia, silver perch and trout pages; the current *Biosecurity Act 2014* (Qld)
PDF; the Qld penalty-unit value page; *Nature Conservation Act 2014* (ACT) and *Fisheries
Act 2000* (ACT) PDFs from legislation.act.gov.au, plus the *Nature Conservation (Exempt
Animals) Declaration 2026*; NT aquaculture, backyard-aquaponics and noxious-fish pages;
PIRSA noxious fish list and the *Aquaculture Act 2001* (SA); FAO Technical Paper 589.

### Tilapia — status supported, **penalty figure withdrawn**

Tilapia is "a category 3, 5, 6 and 7 restricted noxious fish under the *Biosecurity Act
2014*" in Queensland, and the page's "you must not" list includes "keep it". In NSW it is
"illegal … to move, release, possess, buy or sell". Both confirmed.

The draft's "penalties up to $220,000" is **wrong**. The keeping offence is s 45(1)(b),
maximum **500 penalty units**; at the Queensland penalty-unit value of $172.70 from 1 July
2026 that is **$86,350**. Neither government page states a dollar figure at all. $220,000 is
2,000 penalty units at a historical $110 unit value, and is also the NSW *Biosecurity Act
2015* category-2 individual maximum — a figure from a different Act in a different state.

**Action:** the site names the offence and the penalty-unit maximum, not a stale dollar
figure, and says the unit value changes.

### Keeping the five legal species — **the ACT was missed**

| | ACT (S1 Canberra) | NT (S2, S5) | QLD (S3) | SA (S4) |
|---|---|---|---|---|
| Barramundi | no conservation licence | no licence to keep, not for sale | no aquaculture authority | no aquaculture licence |
| Jade perch | no conservation licence | same | same | same |
| **Silver perch** | **licence required** | no licence | no authority | not noxious |
| **Murray cod** | **licence required** | no licence | no authority | not noxious |
| Rainbow trout | no conservation licence | no licence | no authority | not noxious |
| Redclaw crayfish | not established | not noxious | native | **noxious: not to be held without specific authorisation** |

*Nature Conservation Act 2014* (ACT) s 11 excludes fish from "animal" **unless** the fish
"has special protection status", which s 109 defines as an ACT-listed threatened native
species or an EPBC-listed threatened or migratory species. Silver perch is ACT-vulnerable
and EPBC critically endangered; Murray cod is EPBC-listed. Keeping a non-exempt animal is an
offence under s 133 — 100 penalty units, or **200 penalty units and two years** where the
animal has special protection status — and the Exempt Animals Declaration 2026 lists **no
fish**.

Separately, *Fisheries Act 2000* (ACT) s 76 makes importing a live fish into the ACT without
a licence or the conservator's written approval an offence, **for every species**. The same
Act's s 46 excludes non-commercial collections from "aquaculture", and Queensland and South
Australia both define aquaculture around sale, trade, business or research, so a household
system for its own table needs no aquaculture licence in QLD, SA or NT.

**Consequence for the course.** The screening model picks each site's fish rotation on
**temperature alone**. At Canberra it returns *Murray cod + rainbow trout*, seven months —
and Murray cod is exactly the species an ACT household may not keep without a licence. Re-run
with the two special-protection species removed, Canberra's best rotation is *jade perch +
rainbow trout*, six months.

**The Canberra bands do not move.** Protein closure stays at 1.6 / 5.5 / 8.9 % and counted
fish protein stays at 0.27 kg/year, because counted fish protein is limited by the on-site
larvae supply, not by how many months the fish grow. Losing a month of thermal window
changes nothing a student is scored on. That is the course's own headline finding arriving
from an unexpected direction, and week 5 teaches it that way.

**Action:** the model is left alone, since its output is unchanged and its species list is
documented as a thermal screen. Week 5 publishes the jurisdiction table, states plainly that
the model is blind to legality, and requires every design to name its species **and** the
approval pathway in its own jurisdiction. The Canberra site card carries the ACT licence
requirement.

### Temperature bands — better sources, one genuine conflict

| Species | Model band | What the primary sources say |
|---|---|---|
| Barramundi | 25–30 °C | Business Queensland: "requires water temperatures from 20–30°C", ideal 25–30, deaths below 13 °C. FAO Table 7.1 p.109: vital 18–34, optimal 26–29 |
| Silver perch | 23–28 °C | NSW DPIRD: tolerance 2–38 °C, "optimum growth occurring between 23 and 28°C". **Business Queensland says optimum 20–30 °C** — a real conflict between two government sources, so each is cited to its jurisdiction |
| Murray cod | 18–27 °C (**course assumption**) | NSW DPIRD gives only a culture target: "Temperatures should be maintained at 24-25°C". No Australian government tolerance range was found. The model's band stays, labelled an assumption |
| Jade perch | 20–30 °C (**course assumption**) | Business Queensland — **a government source, correcting the draft's note that only industry pages existed** — gives thresholds, not a band: spawns above 23 °C, aerate above 30 °C, growth "to decline rapidly" at 20 °C, feeding stops at 16 °C, mass deaths at 13 °C |
| Rainbow trout | 10–18 °C | FAO Table 7.1: vital 10–18, optimal 14–16. NSW DPIRD: 10–22 °C suitable, growth "best at about 15°C", stress above 19 °C |

**Action:** the species table on the site publishes the primary figure and its source for each
species, marks Murray cod's and jade perch's bands as course assumptions, and shows the
silver perch conflict rather than picking a winner.

### FAO Technical Paper 589 — **all four figures supported, with page numbers**

Verified against the PDF: feed rate ratio 40–50 g/m²/day leafy and 50–80 fruiting (p.17,
§2.4.2); "refrain from adding more than 20 kg of fish per 1 000 litres" (p.109, §7.3.3,
restated p.125, with tanks under 500 L halved to 1 kg per 100 L); "an aquaponic system uses
1-3 percent of its total water volume per day" (p.29, §3.4); Table 7.1 temperatures (p.109).
Table 7.1 contains no jade perch, silver perch or Murray cod — they appear only in the §7.4
prose list of suitable species, which is why their bands are assumptions.

**Access note:** several state sites sit behind bot protection and refused plain fetches;
those pages were read through a browser session. Queensland, ACT and SA legislation and the
FAO paper were read from downloaded PDFs. State fish movement, translocation and stocking
rules were not exhaustively checked, and the site says so.

---

## What this log changed

| Area | Before | After |
|---|---|---|
| Domestic water demand | sourced figure | course assumption, with the real enHealth range beside it |
| Runoff formula | attributed to WHO | enHealth citing Martin (1980) |
| Greywater | one rule, presented as law | a course design rule, with a five-jurisdiction comparison showing it is stricter than the law at four of five sites |
| Insect feed | presented as Australian law | a course design rule, with an accurate statement of what the law binds |
| Compost pasteurisation | 15 days across five turns | 15 days following **each** of five turns, and scoped to commercial windrows |
| Urine storage | storage times only | storage times plus WHO's "no storage needed" position for a one-family system |
| Fermentation | one fused rule with a pH guarantee | one named recipe with its own conditions, and pH 4.6 correctly scoped to sealed shelf-stable product |
| Prices | four retailer keys | thirteen schedule lines checked against fetched Australian listings |
| Tilapia penalty | "up to $220,000" | 500 penalty units under s 45 Biosecurity Act 2014 (Qld), $86,350 at the current unit value |
| Keeping fish | "legal species only" | a per-jurisdiction table; silver perch and Murray cod need an ACT licence, and every live fish entering the ACT needs one |

---

## V11 — Land per person for a complete diet [S14] — **not a universal threshold; the claim is withdrawn**

Checked 2026-09-18 for the second draft. Fetched and read in full: Ecology Action,
*"GROW BIOINTENSIVE Closed-Loop" Sustainability Protocol*, dated 22 October 2018, six pages.

The first draft's home page said a near-complete diet takes "something like 372 m² of good
ground per adult" and set that against "the largest site in this course has 500 m²". The
source does not support a threshold of that kind:

- p.3, footnote 1: the **minimum** farm size "for growing all of one person's soil fertility,
  human nutrition with a well-designed vegan diet **and income** on a sustainable basis will be
  approximately 4,000 square feet of planted surface, assuming **intermediate** GROW
  BIOINTENSIVE yields", which "may be significantly reduced" as skill and soil improve.
- p.6: vegan diets "can be grown on as little as 4,000-sq-ft with **beginning** GB yields, and
  … on as little 2,000-sq-ft with **intermediate** GB yields".

The same document therefore gives 4,000 ft² at intermediate yields (with income and soil
fertility included) and 2,000 ft² at intermediate yields (diet only). Both rest on a
60/30/10 crop split with compost crops, a 24-inch double-dug bed, closed-loop compost and
the method's own yield levels. None of the five households eats that diet or farms that way.

**Action:** the claim is removed from the home page, decks and harness. Week 9 teaches the
figures as method-specific estimates with their assumptions and explains why they cannot set
a fixed threshold for these clients. The largest **designated growing area** is 500 m²
(Darwin); the largest **whole plot** is the 2 ha Alice Springs parcel.

## V12 — Irrigation application efficiency [S12a] — **supported**

Checked 2026-09-18. Fetched: FAO *Irrigation Water Management Training Manual 4: Irrigation
scheduling*, Annex I, Table 8, "Indicative values of the field application efficiency (ea)":
surface irrigation (border, furrow, basin) 60 %, sprinkler 75 %, drip 90 %.

**Action:** used as indicative values in the gross irrigation calculation (drip 0.90,
sprinkler and hose 0.75), published as indicative with the source.

