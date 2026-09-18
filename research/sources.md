# Sources

All retrieved 2026-09-17. **Access** says how the figure was obtained:
- **primary**: I read the source document itself (page or PDF text).
- **summary**: I read a search-engine summary of the source, not the full document. Check it before relying on it in a published page.

**Confidence** rates the claim as used here, not the source overall.

Keys are cited as `[Sxx]` throughout `findings.md`, `model/site_model.py`, the critique log and the course design.

**`verification-log.md` records what was fetched and read on 2026-09-18** for every figure with safety, legal or budget consequences, and what changed as a result. Rows below carry a `V-` reference where that applies, and the verification log is the authority, not this table.

## Course brief

| Key | Source | Used for | Access | Confidence |
|---|---|---|---|---|
| S01 | COMP4020 Assignment 2 brief and spec, `comp.anu.edu.au/courses/comp4020-agentic-coding-studio/api/assessments/assignment-2.json` | Deliverable constraints: 12 dated weeks, a real deck, assessment totalling 100%, SLOPx761 code | primary | high |

## Household demand

| Key | Source | Used for | Access | Confidence |
|---|---|---|---|---|
| S03 | NHMRC, *Nutrient Reference Values for Australia and New Zealand*: Dietary energy, Tables 1–3. https://www.eatforhealth.gov.au/nutrient-reference-values/nutrients/dietary-energy | Energy requirements (EER): man 1.8 m PAL 1.8 = 13.3 MJ/d; woman 1.7 m PAL 1.8 = 10.8 MJ/d; boy 10 y PAL 1.6 = 8.3 MJ/d; girl 10 y PAL 1.6 = 7.6 MJ/d | primary | high |
| S04 | NHMRC NRV: Protein. https://www.eatforhealth.gov.au/nutrient-reference-values/nutrients/protein | Protein RDI: men 64 g/d, women 46 g/d, boys 9–13 40 g/d, girls 9–13 35 g/d | primary | high |
| S05 | Jönsson, H., Richert Stintzing, A., Vinnerås, B. & Salomon, E. (2004) *Guidelines on the use of urine and faeces in crop production*, EcoSanRes 2004-2. https://sswm.info/sites/default/files/reference_attachments/JOENSSON%202004%20Guidelines%20on%20the%20use%20of%20urine%20and%20faeces%20in%20crop%20production.pdf | Per person per year: urine 4.0 kg N, faeces 0.55 kg N; P 365 + 183 g; urine 550 kg. N = 0.13 × food protein. Urine of 1 person fertilises 300–400 m²/yr. 88 % of excreta N is in urine (Sweden) | primary | high |
| S06 | Australian Government, *Your Home*, Rainwater. https://www.yourhome.gov.au/water/rainwater | 1 mm on 1 m² = 1 L (**confirmed**); first-flush sizing "about 10L per 50m² of roof area" (**confirmed verbatim**); tank-size table for a 4-person mains-connected household. **The 150 L/person/day figure is not on this page or any Your Home water page** — see V1 | primary | high for what the page says; the 150 L/p/d attribution is **withdrawn** |
| S06a | enHealth (2010) *Guidance on use of rainwater tanks*, 3rd ed., p.28 | "In areas supplied with mains water, the average indoor use per household is estimated to be … about 100-200 L per person per day" — mains-supplied **indoor** use. The course's 150 L/person/day is published as a **course assumption** at the midpoint of this range (V1) | primary | high for the range; the point value is a course assumption |
| S07 | Howard, G. & Bartram, J. (2003; 2nd ed. 2020) *Domestic water quantity, service level and health*, WHO | Service levels: basic ~20, intermediate ~50, optimal ≥100 L/person/day | summary | high |
| S26 | Beal, C. & Stewart, R. (2015), South-East Queensland Residential End Use Study | Shower 40.6 L/p/d; toilet 21.8 L/p/d | summary | medium |
| S28 | DCCEEW / National Food Waste Strategy Feasibility Study (2021) | 7.6 Mt food loss and waste (312 kg/capita); households 2.46 Mt. Used as ~95 kg/person/yr household food waste | summary | medium |
| S02 | Frontier Economics for AER (2020), *Residential energy consumption benchmarks* | Context: 4-person households ~21 kWh/d total electricity | summary | medium |

## Climate, water sourcing and storage

| Key | Source | Used for | Access | Confidence |
|---|---|---|---|---|
| S39 | Bureau of Meteorology, *Climate statistics for Australian locations* (all years of record) for stations 070014, 015590, 040214, 023000, 014015, 094029, 086071, 009021, 056037, 063005 (plus 070351, 040842, 040913, 023090, 056238 checked). http://www.bom.gov.au/climate/averages/tables/cw_<station>_All.shtml | Monthly mean max/min, rainfall, days ≤2 °C, days ≥35 °C, pan evaporation, RH. Saved to `model/data/climate_stations.json` | primary | high |
| S08 | enHealth (2010) *Guidance on use of rainwater tanks*, 3rd ed., App. B p.46, ISBN 978-1-74241-325-9. https://www.cdc.gov.au/system/files/2025-10/enhealth-guidance-the-use-of-rainwater-tanks.pdf | Runoff = A × (rainfall − B) × roof area, A = 0.80–0.85, B = 2 mm/month — **enHealth citing Martin (1980), not WHO** (V2). Monthly balance; the document's worked example 0.8 × (750−24) × 200 = 116,160 L is reproduced by the model; UV lamps replaced every 9–12 months with an operational sensor; boiling need not be sustained | primary | high |
| S11 | Allen, R.G. et al. (1998) *Crop evapotranspiration*, FAO Irrigation and Drainage Paper 56, ch. 3 and 6. https://www.fao.org/4/x0490e/x0490e07.htm | Ra (Eq. 21–25); Hargreaves ETo = 0.0023(Tmean+17.8)(Tmax−Tmin)^0.5 Ra (Eq. 52), with the warning that it over-predicts in humid conditions; Kc Table 12 | primary | high |
| S12 | Brouwer, C. & Heibloem, M. (1986) *Irrigation Water Management Training Manual 3: Irrigation water needs*, FAO, Annex 1. https://www.fao.org/4/s2022e/s2022e08.htm | Effective rain Pe = 0.8P − 25 (P > 75 mm/month), 0.6P − 10 (P < 75) | primary | high |
| S21 | Retamal, M. et al. (UTS Institute for Sustainable Futures), energy intensity of household rainwater systems; also Griffith review "Energy intensity of rainwater harvesting systems" | 0.9–4.9 kWh/kL, typical 1.5 kWh/kL; ~0.7 kWh/kL at flows above 15 L/min | summary | medium |
| S43 | ABS, *New houses being built on smaller blocks* (2022); Statista/ABS new-house floor area | Average new-house site area in capital cities 432 m² (2021), Brisbane 459 m²; new-house floor area ~232 m² (FY2022) | summary | medium-high |

## Water treatment and sanitation

| Key | Source | Used for | Access | Confidence |
|---|---|---|---|---|
| S09 | WHO (2006) *Guidelines for the safe use of wastewater, excreta and greywater*, Vol. 4. https://www.knowwaste.net/Documents/Guideline%20for%20the%20safe%20use%20of%20wastewater,%20excreta%20and%20greywater-volumn4.pdf | Table 4.5: dry excreta storage 1.5–2 yr at 2–20 °C, >1 yr at >20–35 °C, or pH >9 for >6 months. Composting >50 °C for >1 week. Urine storage table (Table 3): 1 month at 20 °C for processed crops, 6 months at 20 °C for all crops. Greywater 100–200 L/p/d in industrialised regions (Western Australia 112) | primary | high |
| S10 | *NSW Guidelines for greywater reuse in sewered, single household residential premises* (DWE, May 2008) §3.6; NSW Health greywater diversion device page | Untreated greywater: "sub-surface irrigation, at a depth of 100 mm or more below the surface"; no storage; kitchen water excluded; WaterMark-licensed device fitted by a licensed plumber | primary | high **for NSW only** |
| S10a | Queensland Plumbing and Wastewater Code 2024.1; Business Queensland greywater pages | QLD includes kitchen water in the legal definition of greywater and permits "subsurface or surface irrigation"; WaterMark and local-government approval required (V3) | primary | high |
| S10b | NT Government, "Reuse greywater at home" (live page, HTTP 200); NT *Code of Practice for Wastewater Management*, CHO approval 4 Nov 2020 (read via Internet Archive; the live host returned 403) | NT: must not use kitchen wastewater; must release below the ground's surface; must not keep untreated greywater more than 24 hours. The 100–150 mm depth is **definitional**, not the stated device criterion (V3) | primary (live page) / archive (Code) | high for the three rules; the enabling-regulation citation is unverified |
| S10c | SA *On-site Wastewater Systems Code* 2013; SA Wastewater Regulations 2013 | SA: untreated greywater "diverted to a subsurface land disposal system"; no depth figure in the Code, which defers to AS/NZS 1547 (paywalled, not read); kitchen generally excluded; WaterMark required (V3) | primary | high |
| S10d | ACT greywater guideline, 2nd ed., October 2007 (Pub. No 07/1380) | ACT has **no greywater-specific regulation**. Surface and bucket diversion of untreated greywater is contemplated; depth figures apply only to *treated* greywater; kitchen water is "not recommended" (V3) | primary | high |
| S40 | WHO International Scheme to Evaluate Household Water Treatment Technologies (harmonised protocol, 2018) | 3-star: ≥4 log bacteria and protozoa, ≥5 log viruses. 2-star: ≥2 log bacteria, ≥3 log viruses, ≥2 log protozoa. 1-star: meets 2-star for two pathogen classes | summary | high |
| S41 | BioSand filter studies (PubMed 28362307; PMC3752749; Water Research 2013, intermittent vs continuous) | Mature filter ~2.5 log E. coli; continuous 3.71 vs intermittent 1.67 log; field average 1.1 log | summary | medium |
| S42 | NSF/ANSI 55 Class A UV systems | ≥40 mJ/cm² over lamp life, with UV sensor and flow restrictor | summary | medium-high |
| S35 | SA EPA *Compost guideline* §5, https://www.epa.sa.gov.au/files/7687_guide_compost.pdf, whose footnote 9 attributes the requirement to AS 4454-2012 §3.2.1(a). **The Standard itself is paywalled and was not read** | ≥55 °C for three consecutive days **following each** of at least 3 turns; for manure, animal waste, food or grease-trap feedstocks, ≥55 °C for fifteen consecutive days **following each** of at least 5 turns — more demanding than the draft's reading (V6). A **commercial windrow** standard, not a household requirement | primary (the EPA guideline) | high for the EPA text; the Standard is second-hand |
| S27 | Household anaerobic digestion literature (food-waste methane ~0.44–0.48 m³ CH₄/kg VS mesophilic/thermophilic; home systems 50–70 % of optimum) | Temperature dependence of household digesters | summary | low-medium |

## Food systems

| Key | Source | Used for | Access | Confidence |
|---|---|---|---|---|
| S16 | Somerville, C. et al. (2014) *Small-scale aquaponic food production*, FAO Fisheries and Aquaculture Technical Paper 589. https://www.fao.org/4/i4021e/i4021e.pdf | Feed rate ratio 40–50 g/m²/d leafy, 50–80 fruiting. Max 20 kg fish per 1,000 L. Fish eat 1–2 % body weight/d. Water loss 1–3 % of volume/d. 2,000 L/h at 1.5 m head needs a 25–50 W pump. Tilapia FCR 1.4–1.8. Table 7.1 temperatures: trout 10–18 (opt 14–16), carp and tilapia opt 25–30. Tropical 22–32 °C, cold-water 10–18 °C | primary | high |
| S17 | Rakocy, J. et al., UVI aquaponic system (via *Aquaponics: The Basics*, Springer 2019) | UVI feeding-rate ratio 60–100 g/m²/d (tilapia, raft) | summary | medium |
| S18 | NSW DPI and Business Queensland pages on tilapia | Tilapia is a declared noxious fish; illegal to keep; Queensland penalties up to $220,000 | summary | high |
| S19 | Business Queensland, *Barramundi aquaculture*; jadeperch.com (industry) for jade perch and Murray cod; DPI Victoria figure for trout (via a fish-vet blog) | Barramundi needs 20–30 °C, ideal 25–30. Jade perch 20–30, stops feeding <15. Murray cod best ~25, tolerates 5–30 briefly. Trout optimum 10–22 | summary | medium (industry sources for two species) |
| S20 | NSW DPI, *Silver perch* aquaculture page | Optimum 23–28 °C for commercial production | summary | medium-high |
| S49 | Rowland (2005), Aquaculture Research; Kibria (1999), J. Applied Ichthyology | Silver perch FCR 2.3–2.5 in ponds at low density; 1.8 in a salinity trial | summary | medium |
| S22 | Chia, S.Y. et al. (2018) Threshold temperatures and thermal requirements of black soldier fly. *PLOS ONE* 13(11): e0206097 | Lower developmental threshold 10.4–12.3 °C. Egg-to-adult 91 d at 19 °C, 42 d at 28 °C, 32 d at 31 °C. Best population growth ~30 °C | summary | medium-high |
| S22b | Review: *Black soldier fly larvae and their affinity for organic waste processing*, Waste Management (2022) | On food waste: 52 % substrate reduction, 28 % bioconversion (dry matter) over 14 d | summary | medium |
| S37 | Barragán-Fonseca, K. et al. (2017) Nutritional value of BSF larvae, *J. Insects as Food and Feed* | Larvae dry matter 35–45 %; crude protein 37–63 % DM; fat 7–39 % DM | summary | medium |
| S29 | Lähteenmäki-Uutela, A. et al. (2021) Regulations on insects as food and feed: a global comparison. *J. Insects as Food and Feed* 7(5): 849–856. https://edepot.wur.nl/553342 | Australia: insects may be fed to aquaculture species in all states; insects for feed must not be reared on meat, manure or catering waste; raw (unheated) insects are not permitted as feed. **No Australian regulator publishes any of these**; the review cites one paywalled paper (DiGiacomo et al. 2019) that was not read (V5) | primary (the review) | **low as a statement of Australian law**. Used as a course design rule, not a legal claim |
| S29a | NSW Biosecurity Regulation 2017, Part 2 Div 9 (authoritative XML, legislation.nsw.gov.au, sl-2017-0232); Business Queensland swill and prohibited-poultry-feed pages | Restricted animal material is "any material derived from a vertebrate" (cl 36); the feeding prohibitions bind **ruminants** (cl 38) and **pigs** (cl 37). No provision covers fish, aquaculture or insects. Swill feeding is prohibited in every state and covers pet and hobby animals. A household feeding its own fish is not captured (V5) | primary | high |
| S23 | Ohio State Mycology; GroCycle; Fungi Perfecti species pages | Oyster fruiting ranges: P. ostreatus ~13–24 °C; blue oyster ~7–18 °C; pink P. djamor ~18–30 °C; golden ~18–30 °C | summary | low-medium |
| S23b | Oyster mushroom yield studies (PMC5050175; PubMed 12715251; Sci. Rep. 2025) | Biological efficiency: straw ~60–80 %; sawdust ~13–61 %; supplemented substrates up to ~100 % | summary | medium |
| S23c | *Effects of black soldier fly larvae on biotransformation and residues of spent mushroom substrate and wet distiller's grains*, Scientific Reports (2024) | Bioconversion on 100 % spent mushroom substrate only 1.46 %; adding 25 % spent substrate to distillers' grains did not reduce conversion | summary | medium-high |
| S23d | MDPI *Agronomy* 10(9):1239 (2020); Penn State analysis of fresh mushroom compost | ~5 kg fresh spent substrate per kg mushrooms for lower-efficiency species; spent compost N 2.65 % DM, C:N ~13 | summary | medium |
| S38 | USDA FoodData Central: mushrooms, oyster, raw | 33 kcal and 3.31 g protein per 100 g | summary | medium-high |
| S36 | NCHFP sauerkraut recipe, adapted from USDA AIB No. 539 rev. 2015, https://nchfp.uga.edu/how/ferment/recipes/sauerkraut/, plus NCHFP general fermenting guidance | 25 lb cabbage to ¾ cup canning salt (**≈2.25 % by weight**); 70–75 °F "fully fermented in about 3 to 4 weeks". **The page states no pH figure.** "Use only recipes with tested proportions of ingredients"; "Do not attempt to make sauerkraut or fermented pickles by cutting back on the salt required" (V8) | primary | high for this recipe; **does not generalise to other vegetables** |
| S36a | Colorado State University Extension, *Understanding and making sauerkraut* | "2—2.5% salt by weight … approximately 3 Tbsp. of salt per 5 pounds of shredded cabbage", but a different schedule: "68—72°F, for about 7—14 days". The draft had fused this with the NCHFP schedule (V8) | primary | high for this recipe |
| S36b | 21 CFR 114.3 (Cornell LII) | Acid foods have "a natural pH of 4.6 or below"; acidified foods are brought to "a finished equilibrium pH of 4.6 or below" and are thereby shelf stable. pH 4.6 is the ***Clostridium botulinum* boundary for sealed shelf-stable product**, not a general pathogen boundary: *E. coli* O157:H7, *Salmonella* and *Listeria* are unaffected (V8) | primary | high |
| S13 | Csortan, G., Ward, J. & Roetman, P. (2020) Productivity, resource efficiency and financial savings: South Australian home food gardens. *PLOS ONE* 15(4). https://pmc.ncbi.nlm.nih.gov/articles/PMC7156066/ | Median yield 0.21 kg/m²/30 d (range 0.02–1.42); 24 % of gardens >0.5. Median irrigation 20 L/m²/30 d, 52 L for vegetable-only areas | primary | high |
| S52 | McDougall, R., Kristiansen, P. & Rader, R. (2019) Small-scale urban agriculture results in high yields… *PNAS* 116(1) | 13 Sydney urban farms and gardens: mean 5.94 kg/m², about twice commercial vegetable farms | summary | medium-high |
| S14 | Ecology Action, GROW BIOINTENSIVE FAQ | ~4,000 ft² (~372 m²) per adult for a near-complete vegan diet, including compost crops, under good conditions | summary | medium |
| S15 | Peri-urban food forest nutritional yield case study, *Urban Forestry & Urban Greening* (2019) | 0.08 ha young food forest: 713 kg/yr, 415,075 kcal (~519 kcal/m²/yr) | summary | medium |
| S24 | Nursery and home-garden guides (Fruit Tree Lane; PlantNet; Daleys) | Chill hours = hours below 7.2 °C. Low chill 150–450 h, medium 450–650, high 650+. Canberra ~720, Adelaide ~500, Brisbane ~150, Darwin ~0 | summary | low (commercial, unsourced estimates) |

## Costs

All costs are commercial listings: low confidence, and only good enough to check budget feasibility.

| Key | Source | Used for |
|---|---|---|
| S31 | Tanks Online and similar retailers | 22,500 L poly tank ~$2,876 (~$128/kL); 10–46 kL tanks $2,100–7,700 |
| S32 | Eco Off Grid / Ecoflo listings | Composting toilets: Nature Loo ~$1,850–2,775; Clivus Multrum CM14 from $6,050 |
| S33 | The Quote Yard (VIC/WA 2026 guides); Water Capture | Greywater diversion $800–2,500; gravity bathroom and laundry systems $1,200–2,800; treatment systems $3,000–12,000+ |
| S34 | Woodvale Fish & Lily Farm and other kit sellers | Backyard aquaponics kits $1,995–3,495; compact kits $599–999 |

## Course design and fairness precedents

| Key | Source | Used for | Access | Confidence |
|---|---|---|---|---|
| S30 | CSIRO Australian Housing Data, *How NatHERS star bands were created – and how they've evolved*. https://ahd.csiro.au/how-nathers-star-bands-were-created/ | Climate-specific star bands exist because "a single, national MJ/m² target would bias results". 2006 bands aimed for "the same proportion of designs" at each star level in every climate. The Area Correction Factor levels the field for small homes. Bands are re-derived when climate files change | primary | high |
| S48 | NSW BASIX water targets (planning portal help notes) | Water-reduction targets range 0–40 % by climate zone, set from utility data and long-term BoM climate | summary | medium-high |
| S44 | Biggs, J. (1996) Enhancing teaching through constructive alignment. *Higher Education* 32: 347–364 | Outcomes, activities and assessment must align, so metrics should reward what the weeks teach | summary | high |
| S45 | O'Neill, G. (2017) It's not fair! Students and staff views on the equity of … students' choice of assessment methods. *Irish Educational Studies* 36(2) | Choice is only fair if options are equivalent in workload, support, feedback and chance of success; recommends an equity template | summary | medium-high |
| S46 | Adesope, O., Trevisan, D. & Sundararajan, N. (2017) Rethinking the use of tests: a meta-analysis of practice testing. *Review of Educational Research* 87(3). ERIC EJ1141817 | Practice tests beat restudying and all other comparison conditions (effect size not quoted here: the ERIC abstract omits it) | primary (abstract) | high |
| S47 | FAO *Food self-sufficiency and international trade*; energy self-sufficiency definitions | Self-sufficiency ratio vs self-consumption. A ratio of production to demand can exceed 100 % and rewards surplus, so closure is capped and counted as used | summary | medium |
