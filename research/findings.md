# Findings

Condensed evidence behind the course design. `[Sxx]` keys resolve in `sources.md`. Model numbers come from `model/output/calibration.md` (preset set v4) unless stated.

## 1. The fixed household (identical at every site)

| Quantity | Value | Basis |
|---|---|---|
| Occupants | 2 adults + 2 children aged 9–13 | course decision |
| Food energy | 40.0 MJ/d (≈9,560 kcal/d; 3.49 M kcal/yr) | man 13.3 + woman 10.8 (PAL 1.8) + boy 8.3 + girl 7.6 (PAL 1.6) [S03] |
| Protein | 185 g/d (67.5 kg/yr) | RDI 64 + 46 + 40 + 35 [S04] |
| Domestic water (reference) | 150 L/person/day = 600 L/d = 219 kL/yr | rainwater-only guidance [S06]; WHO "optimal" ≥100 [S07] |
| Toilet share | 21.8 L/p/d removable with a composting toilet | [S26] |
| Reusable greywater | ~55 % of domestic (shower, laundry, basins; not kitchen) | [S26][S10] (fraction is an assumption) |
| Excreted nitrogen | 13.6 kg N/yr (4.55 kg per adult-equivalent; children = 0.5) | [S05] |
| Household food waste | ~95 kg/person/yr (380 kg/yr) | [S28] |

**Design consequence:** the numbers make the course sincere and humbling. Growing a near-complete diet needs ~372 m² per adult [S14]. Every preset can therefore close only a fraction of its food energy, so metrics must be framed as *closure*, not self-sufficiency.

## 2. Climate data and site choice

- BoM long-record stations give monthly mean temperature, rain, frost and heat days, and pan evaporation [S39].
- Evapotranspiration uses Hargreaves (FAO-56 Eq. 52 [S11]). It matches pan × 0.7 within ~5 % at Canberra, Alice Springs, Adelaide and Darwin. It over-predicts in humid Brisbane, which FAO-56 warns about.
- **Draft duplicate:** the planning draft's "cool temperate" (Canberra) and "cold upland" (Armidale) are near-duplicates:

  | Station | Tmean | Frost days | P/ETo |
  |---|---|---|---|
  | Canberra | 13.1 °C | 92 | 0.50 |
  | Armidale | 13.4 °C | 98 | 0.57 |

  Meanwhile nothing covered Australia's tropical wet-dry zone. Darwin brings the most distinct water problem of any site: 1.4 % of annual rain falls in the driest four months.
- **Chill hours cannot be derived from monthly means.** The sine-curve method gives Canberra 1,979 h versus ~720 h in regional guides, and Brisbane or Adelaide 0 versus ~150 or ~500 [S24]. Use regional chill categories, not a formula.

| Site (station) | Rain mm | ETo mm | P/ETo | Tmean °C | Days ≤2 °C | Days ≥35 °C | Rain in driest 4 months |
|---|---|---|---|---|---|---|---|
| Canberra (070014) | 616 | 1,244 | 0.50 | 13.1 | 92 | 5 | 28 % |
| Alice Springs (015590) | 284 | 1,803 | 0.16 | 21.0 | 30 | 90 | 16 % |
| Brisbane (040214) | 1,146 | 1,353 | 0.85 | 20.6 | 0 | 4 | 19 % |
| Adelaide (023000) | 525 | 1,207 | 0.43 | 17.0 | 0 | 17 | 17 % |
| Darwin (014015) | 1,733 | 1,620 | 1.07 | 27.7 | 0 | 14 | 1.4 % |

## 3. Food systems: what the numbers allow

### Perennials and annual garden

- **Yields:** SA home gardens have a median of 0.21 kg/m²/30 d; top quartile >0.5 [S13]. Sydney urban farms average 5.94 kg/m²/yr [S52]. A young food forest gave ~519 kcal/m²/yr [S15].
- **Model assumptions:**
  - Reference yield of 1,500 kcal/m²/yr under a full season with no water limit.
  - Scaled monthly by temperature (5→15 °C ramp; heat-day penalty) and by water satisfaction.
  - Effective rain [S12]; irrigation topping up the deficit.
- **Irrigation need per m² differs threefold between sites:** Brisbane 651 mm, Canberra 932, Adelaide 952, Darwin 832 (all in the dry season), Alice Springs 1,650. So food potential must be water-coupled. The draft's "area × days × yield" gave Alice Springs a 2,000 m² garden needing 3,300 kL/yr, 15× its roof yield.

### Mycology

- Oyster species yield 60–80 % biological efficiency on straw [S23b]. Cool and warm species cover mean temperatures of 8–30 °C, so fruiting is possible 9–12 months a year at every site [S23].
- Arid Alice Springs (3 pm RH 25 %) needs a humid chamber: a water and energy cost.
- **Link correction:** larvae convert only **1.46 %** of pure spent mushroom substrate [S23c], so "spent substrate → insects" is a weak link. Spent substrate (N 2.65 % DM, C:N ~13 [S23d]) belongs in compost or soil for perennials, or as ≤25 % of a larval feed mix.

### Insects

- Black soldier fly larvae stop developing below ~10–12 °C [S22]. Productive factor: Canberra 0.19, Adelaide 0.33, Brisbane 0.57, Alice Springs 0.58, Darwin 0.97.
- Indoor rearing at ~20 °C gives ~0.53 anywhere, and is the fairness lever.
- **Legal constraint [S29]:** in Australia, insects used as feed must not be reared on meat, manure or catering waste, and raw (live, unheated) insects are not permitted as feed. Meat and dairy scraps and fish sludge therefore go to compost or a digester, not to larvae destined for fish. Larvae are heat-treated before feeding. (Whether feed codes bind a private household is an interpretation; a sincere course should adopt the stricter rule.)

### Aquaponics

- **Balancing:** 40–50 g feed/m²/d for leafy greens and ≤20 kg fish per 1,000 L [S16]. Water loss is 1–3 % of volume per day, so a 1 m³ system needs only 10–30 L/d. That small figure makes the forward reference to the water weeks harmless.
- **Species:** tilapia is illegal in Australia [S18]. Legal options by temperature:

  | Species | Growth band | Source |
  |---|---|---|
  | Barramundi | 25–30 °C | [S19] |
  | Jade perch | 20–30 °C | [S19] |
  | Silver perch | 23–28 °C | [S20] |
  | Murray cod | ~18–27 °C | [S19] |
  | Rainbow trout | 10–18 °C | [S16] |

  A two-species seasonal rotation covers 11–12 months everywhere except Canberra (7 months; ~0.5 kWh/d winter tank heating).
- **Key mass balance:** household plant-based food waste (~228 kg/yr) at 20 % dry-matter conversion yields larvae covering only **9–17 % of the feed** for a 4 m² bed and 5–8 % for 8 m². Fish protein grown on on-site feed is ~0.3–0.5 kg/yr, under 1 % of household protein.
  - The iconic "scraps → larvae → fish" loop **cannot close without imported feed**.
  - Closure metrics must be net of imports, or the week is scored on fiction.
  - This is a strong, honest teaching point for weeks 4–5.

### Fermentation

- 2–2.5 % salt by weight, 21–24 °C for 3–4 weeks, safe at pH ≤4.6 [S36].
- Its loop role is preservation (moving summer surplus into winter), not new calories. Bokashi and silage also pre-treat waste for week 10.
- Hot sites (Darwin, Alice Springs) need temperature control; mild Adelaide suits it best.

## 4. Water

- **Sourcing:** runoff = 0.8 × (rain − 2 mm/month) × roof area; tank size by monthly balance [S08]. Both are reproducible by hand and ideal for week 7.
- **Storage is the real constraint.** Annual balances hide it:
  - Darwin's roof collects 411 kL/yr, but a competent design with 91 kL storage still imports 58 kL in the dry season while overflowing 201 kL in the wet.
  - At ~$130/kL [S31], storage cost is the most site-sensitive budget line. Annual-average security can't show drought risk; a drought-year dataset is needed (week 9).
- **Treatment:**
  - Multi-barrier approach: first flush, sedimentation, filtration, disinfection [S08].
  - Performance language: WHO household water treatment star ratings, i.e. log reductions by pathogen class [S40].
  - Measured technology data: BioSand ~2.5 log E. coli when mature, far less when run intermittently [S41]; UV Class A ≥40 mJ/cm² with a sensor [S42]. Gives real numbers for data-driven troubleshooting.
- **Energy:** household pumping ~1.5 kWh/kL at low flow, ~0.7 at higher flow [S21].

## 5. Waste and sanitation

- **Composting:** AS 4454 pasteurisation is ≥55 °C for 3 days per turn over ≥3 turns, and 15 days for higher-risk material [S35]. WHO requires >50 °C for >1 week [S09].
- **Dry excreta storage [S09]:** 1.5–2 years at 2–20 °C, >1 year at 20–35 °C. Canberra and Adelaide therefore need ~75 % more chamber capacity than Brisbane, Alice Springs or Darwin, a climate-dependent sizing burden. Urine: 1 month at 20 °C for processed crops, 6 months for all crops.
- **Greywater rules [S10]:** untreated greywater only to subsurface irrigation ≥10 cm deep; no storage; no kitchen water.
- **Biogas:** strongly temperature-dependent. Screening factor: Darwin 0.63 vs Canberra 0.07 [S27]. Biogas is *energy*, which belongs to part 2, so part 1 should credit only the digestate's nutrients.
- **Nutrient uptake:** ~12 g N/m²/yr [S05]. Nutrients are over-supplied on every preset:

  | Site | Excreted N the garden can absorb |
  |---|---|
  | Brisbane townhouse | 11 % |
  | Adelaide | 22 % |
  | Alice Springs | 35 % |
  | Canberra | 40 % |
  | Darwin | 44 % |

  Safe export or treatment of surplus N is a real design problem, not a failure.

## 6. Energy and budget

- **Process loads** of the excellent reference designs (pumps, aeration, UV, toilet fan, irrigation, tank heating):

  | Site | Modelled peak kWh/d | Declared peak, incl. uncertain loads |
  |---|---|---|
  | Canberra | 3.30 (tank heating) | 3.95 |
  | Alice Springs | 2.91 | 3.56 |
  | Brisbane | 2.78 | 3.43 |
  | Adelaide | 2.71 | 3.36 |
  | Darwin | 3.34 (dry-season pumping) | 3.99 |

  The screening model computes six of the counted load groups. §2.1 also counts insect-unit climate control and greywater pumping, which it does not compute, so the reference designs carry a declared **0.65 kWh/d** upper-estimate allowance for those — the same rule §2.1 imposes on students. A **5 kWh/d** allowance is then a feasible guardrail at every site (67–80 % used). It binds as soon as a student adds a humidified mushroom chamber, a temperature-controlled fermentation space, a dehydrator or a heated digester: those together have an upper estimate of ~1.65 kWh/d against 0.99–1.64 kWh/d of headroom. For context, a 4-person home uses ~21 kWh/d total [S02].
- **Budget:** the reference designs were previously costed from five simplified prices with no contingency, giving $22–25k for the excellent level. Re-costed against the full §2.2 schedule they came to **$33.7k–$39.5k** — over the $30k allowance at every site. Recipe v5 cuts new-storage spend (which the tank balance had saturated) and the excellent design's added catchment; the excellent designs now cost **$24,860–$28,875** including the 10 % contingency. **$30k new spend** is feasible but not loose, and only because presets list existing site inventory (tanks, bore). See `critique-log.md` iteration 5.

## 7. Fairness precedents and assessment evidence

- **NatHERS** could not use one national MJ/m² target because it "would bias results". It sets climate-specific star bands so that the same share of designs lands at each star level in every climate, with an Area Correction Factor for small homes [S30]. **BASIX** sets water targets from 0–40 % by climate zone [S48]. Both are direct precedents for per-site scoring bands.
- **Choice of assessment** is only equitable if options are equivalent in workload, support and chance of success; O'Neill recommends an equity template [S45]. That is the standard the five presets must meet.
- **Constructive alignment** [S44]: metrics must reward what the weeks teach. A kcal-only food metric makes weeks 3–5 invisible, because mushrooms, insects and fish add ~0 kcal.
- **Low-stakes practice testing** beats restudying [S46]. That supports conceptual, non-numeric multiple-choice quizzes as a keep-up mechanism.
- **Self-sufficiency ratios** that count production rather than use can exceed 100 % and reward waste [S47]. So closure is capped, counted as *used*, and net of imports.
