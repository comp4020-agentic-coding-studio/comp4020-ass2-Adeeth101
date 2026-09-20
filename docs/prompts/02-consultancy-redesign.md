Implement a complete second draft of SLOP4761 using the direction below. This is my review of the first draft and supersedes conflicting course-design decisions, harness rules and course-specific tests. Continue through the build and verification; do not stop at a plan or ask me to settle minor design choices. Preserve useful first-draft work and its commit history.

## The change I want

Make this an engineering optimisation course told through an ongoing consultancy case. Students have engineering experience and act as graduate consultants advising homeowners. A fictional government is promoting household self-sustainability through a selective loan programme. Homeowners need a credible engineering proposal to apply. Their consultant first designs a year-long measurement programme, then receives a specialist team's analysed findings and uses them to design a high-level investment proposal.

Only the five existing model homes are available. Remove the custom-site option everywhere. Give every home a household persona, a complete property dossier and an approximately scaled site diagram. The whole course should feel substantial: useful slides, diagrams, worked calculations, tutorials, datasets and assignment guidance. Fix the text overlaps in existing diagrams.

Read README.md, CLAUDE.md, research/course-design.md, research/verification-log.md, research/sources.md, the current content/data schemas, and the existing tests. Check the live Assignment 2 brief and assessment page. All local inputs are inside this repo. Update the existing design document and course harness to reflect this instruction. Preserve the fixed platform, SlopU identity and palette, collections, generated API and starter invariant tests.

## Identity and fictional programme

Keep SLOP4761 and its exact title, Designing the Closed-Loop Household I: Food, Water and Waste; level 4; proposed SLOP4762 sequel. Reframe prerequisites as prior engineering design, mass/energy balances, introductory statistics and measurement, spreadsheet modelling and basic CAD. Prior environmental or biological study is helpful; teach the necessary biological context in the course.

Use the fictional Household Resilience Loan Programme and the fictional consultancy Common Ground Engineering. Clearly label both as teaching fiction on their introductory pages. Do not invent real government policy, lender endorsements or links. Students are graduate engineering consultants working under a senior reviewer. The final submission is the technical annex and executive recommendation for a homeowner's application, not a promise of loan approval or a construction-certified design.

The programme's course rules retain a maximum $30,000 implementation cost including contingency, and 5 kWh/day peak-month process energy. Higher borrowing creates greater exposure within this fictional scheme and requires a stronger alternatives case. Do not teach that principal alone determines real-world credit risk. No household income underwriting, invented interest rate, credit score or financial-advice exercise is needed.

The narrative progresses from client intake to measurement proposal, then jumps forward twelve fictional months to a specialist analysis handover and engineering proposal. Students do not wait or collect real data for a year. The programme funds preliminary investigation separately: specify a common fictional $1,500 measurement equipment/services allowance; student labour is scheduled in hours, not charged. This is distinct from the $30,000 implementation allowance. Demonstrate one feasible measurement plan under $1,500 before publishing that exercise.

## Optimisation and scope of engineering

The design task is to identify the lowest-cost feasible option satisfying the client's priority service targets, then justify any extra expenditure for additional resilience or useful output. Treat it as a constrained, multi-objective decision; do not pretend a single closure score represents all client values.

Use five to eight understandable decision variables: tank capacity, connected existing roof area, growing area/crop mix, irrigation/reuse strategy, selected biological modules, and operating schedule. Publish plausible discrete ranges and explain why choices are bounded. Students evaluate an existing-condition baseline plus three feasible alternatives: minimum intervention, balanced and higher resilience. Require a small reproducible spreadsheet scenario grid and identify dominated options; no advanced optimiser, calculus or programming is required. Provide a practice example on separate numbers so the teaching material does not give away the assessed recommendation.

Each dossier supplies attainable priority service targets, with a demonstrated feasible option and adequate cost/energy margin. Set these from the updated model, not invented aspirations. Allow students to explain target conflicts or recommend a phased approach. Assess evidence and trade-offs rather than spending all the budget. Retain existing closure indicators and reference bands as diagnostics only where still valid; grade neither loan size nor proximity to an old excellent recipe. Include imported resources, recurring costs, maintenance hours, uncertainty and contingency. Do not count preserved food twice or imported-feed production as closed-loop output.

Required calculations: monthly water supply/demand and storage balance; critical service flow in L/min and a justified pump head assumption; capacities and duty cycles; useful food/protein contribution with stated limits; nutrient recovery versus uptake; peak-month process energy; capital and operating cost; sensitivity to demand, yield, price and a dry year. Use simplified performance curves/lookup tables where appropriate. Detailed pipe diameters, fitting losses, reinforcement, wiring, construction certification and fabrication drawings are out of scope. Students specify performance requirements and commissioning checks, not how to construct hazardous systems.

The five homes are fixed existing properties. No custom sites, substitution of land or arbitrary enlargement of roofs/plots. Select retrofit modules within specified installation zones. Existing roof areas and footprints are different quantities: explain their relationship. If old reference recipes include extra roofs, remove that option, re-evaluate feasibility and regenerate affected bands/costs transparently. Keep the five climates and the chosen plot/growing/roof parameters unless correcting an explicit internal contradiction; disclose any necessary correction.

Biological subsystems are options, not compulsory ornaments. Students may reject aquaponics, insects, mushrooms or another module with an evidence-based justification. Their measurement plan should prioritise plausible options without requiring equipment for every imaginable system.

## Five client dossiers

All households retain the common two-adult/two-child demand convention for comparability. Use these fictional clients; do not claim they are real people:

- Canberra: the Taylor family; winter reliability and preserving usable family garden space; limited weekday maintenance.
- Alice Springs: the Nguyen family; reducing imported water and staying within the existing bore allocation; strong preference for maintainable equipment.
- Brisbane townhouse: the Patel family; limited private/shared space, neighbour amenity and approval constraints; compact, quiet options.
- Adelaide: the Rossi family; summer irrigation reliability and manageable seasonal food production; clear concern about recurring costs.
- Darwin: the Williams family; wet/dry-season mismatch and reliable operation during absences; serviceable systems and overflow management.

Translate these preferences into explicit fictional constraints and priorities without stereotypes. Publish maintenance availability, permitted uses, installation restrictions and acceptable disruption as case assumptions. Give every site equivalent dossier completeness and teaching support.

Prepare two clearly separated releases per site:

Release A, homeowner intake: whole-plot plan, basic house floor plan sufficient to locate wet areas and services, boundary dimensions/area, north arrow/scale bar/legend, footprints, connected roof zones/downpipes, hardstand, access, usable growing zones, retained recreation, trees/shade, approximate slope/elevation, existing tanks/bore/utilities, known easements and ownership boundaries. Show the rural whole parcel plus an enlarged working area. For Brisbane explain whether the 40 m² shared garden is outside the private 300 m² lot and the household's permitted allocation; never double-count common property. Include equipment inventory, accessible bills and homeowner observations. Distinguish known facts, estimates and unknowns to be measured. Mark actual service routes/ground conditions unknown where appropriate rather than supplying fabricated survey certainty.

Release B, specialist findings: a dated memo after the fictional measurement year, twelve-month tables, seasonal profiles, critical demand/flow observations, water quality/soil/shade findings relevant to selection, uncertainty and missing-data notes, recurring cost/maintenance assumptions, implications and remaining questions. Specialists analyse conditions but do not choose the final system. Include downloadable CSVs, units and a data dictionary, with enough information for every required calculation. Keep the client, geometry, monthly totals and narrative consistent. Identify synthetic measured-year data explicitly, and distinguish it from sourced long-term climate data and a separate synthetic drought stress test. One observed year does not establish drought reliability.

The specialist dossier is supplied independently of A1 quality; all students selecting a site receive the same complete Release B. Students include a short reconciliation identifying what their own measurement plan would have missed. Do not penalise them twice for an A1 omission or require real sensor deployment.

Plans need to be internally consistent educational models, not survey-certified. Use SVG or equivalent controllable geometry for scaled diagrams and labels. Areas must approximately reconcile, with stated rounding tolerances; no tank outside the boundary or label collisions. An illustrated site view may complement the plan but must not replace it.

## Assessment and teaching sequence

Keep five conceptual quizzes at 8% each, in weeks 3, 5, 8, 10 and 12. Keep A1 at 20% due week 7, capstone at 40% in the exam period, and no oral assessment. Change titles and rubrics as follows.

A1: Year-long Measurement Programme. Deliver a client question/decision map; annotated measurement locations; variable/instrument/range/accuracy/frequency/duration table; sampling schedule covering twelve months and seasonal/event variation; calibration and quality control; missing-data procedure; safety, permissions and household data privacy; equipment/services cost and labour schedule; data dictionary; and explanation of how readings support future design. Use a suggested 1,800–2,200 words plus plans/tables. Rubric: decision relevance 25%, measurement/sampling design 30%, uncertainty/quality control 20%, feasibility/cost/safety 15%, communication 10%.

A2: Household Resilience Investment Proposal. Deliver an executive recommendation, client targets and acceptance criteria, interpretation of supplied findings, baseline and three alternatives, reproducible calculation workbook, selected concept layout and system-flow schematic, capital/operating costs and borrowing justification, sensitivity/failure response, maintenance plan, approval/commissioning pathway and A1 reconciliation. Suggested 2,500–3,000 words plus workbook/plans. Rubric: engineering balances/sizing 25%, alternatives/optimisation/value 25%, interpretation/uncertainty 20%, client/site fit and feasibility 20%, communication 10%. Do not award marks for visual extravagance or pretending a conceptual design is build-ready.

Replace the previous week order and lead-site assignments with this sequence:

1. Client commission, programme rules, engineering boundaries and five-home intake.
2. Site survey, requirements, mass balances and measurement objectives — Canberra leads.
3. Water monitoring: rainfall, roof runoff, demand, tank levels and flow — Alice Springs leads; quiz.
4. Soil, microclimate, crop demand/yield and spatial sampling — Brisbane leads.
5. Food/waste/nutrient audits, biological options and measurement uncertainty — Adelaide leads; quiz.
6. Twelve-month sampling, sensors, calibration, data quality, cost and handover — Darwin leads.
7. A1 due; twelve-month narrative jump; specialist findings and uncertainty — Canberra leads.
8. Water-system sizing: storage, reuse, treatment, flow and energy — Alice Springs leads; quiz.
9. Food-system selection: perennials, mushrooms, insects and aquaponics — Brisbane leads.
10. Waste, sanitation, preservation and integrated balances — Adelaide leads; quiz.
11. Alternatives, constrained optimisation, costs and resilience — Darwin leads.
12. Investment proposal, design review and bridge to SLOP4762; quiz.

Every week 2–11 still contains a substantive Five sites comparison; each site leads exactly twice. Do not claim every lead occurrence must correspond to the mathematically easiest/hardest climate. Each week produces a usable assignment component. Put the measurement-method instruction needed for A1 in weeks 1–6; biological detail can use linked reference lessons revisited in week 9.

## Teaching depth and visual treatment

Build twelve useful lecture pages, twelve corresponding tutorials/studios and twelve real linked decks. Aim for 8–12 substantive slides per deck, each with a teaching purpose rather than filler. Each tutorial should provide a 60–90 minute sequence, concrete inputs, an annotated worked example, two graduated exercises, and worked feedback or solution guidance on practice data. Do not publish a complete solution to the assessed cases. Add a glossary, formula/reference sheets and downloadable assignment templates. Plain Markdown/CSV and print-friendly HTML are acceptable; no need for a complicated document-generation pipeline.

Use the narrative throughout: client notes, site visit extracts, measurement proposals, specialist memos, design-review questions. Keep story excerpts brief and functional. The distinction between fictional case facts and factual engineering teaching should be clear without repetitive disclaimers on every paragraph.

Use diagrams and images wherever they teach: plot/floor plans, sensor maps, monthly water balance charts, system flows, option comparisons and process schematics. Fix existing overlapping diagram text and verify long labels at both viewports. Generated illustrative images can be supplied in a later asset pass; do not wait for them. Use polished temporary illustrations with reserved aspect ratios and maintain an asset manifest listing filename, intended page, purpose, dimensions and alt text. Essential plots and teaching diagrams must already work in this draft. Do not place an unlabelled placeholder where a student needs quantitative information.

The fictional houses/personas/programme can be invented and labelled as case assumptions. They need internal consistency, not exhaustive real-world validation. Actual teaching claims, formulas, biological yields and legal/safety requirements need suitable sources and scope. Cite near the claim with a link to a readable reference entry and primary source where available. Do not require students to inspect repository files to find a citation.

Remove the homepage assertion that everyone needs 372 m² to grow a near-complete diet. Ecology Action's method-specific figures are not a universal minimum. If discussed in a lesson, attribute them, state diet/yield/soil/skill assumptions and explain why they cannot establish a fixed threshold for these households. Primary reading to inspect: https://www.growbiointensive.org/PDF/GBSustainability_Protocol%20_2018.pdf . Also correct 'largest site has 500 m²': 500 m² is the largest designated growing area, whereas the largest whole plot is 2 ha. Prefer a homepage question about what this client's land can reliably provide and which improvements justify their costs, linked to the relevant lesson. Fix superseded assertions in decks, harness and source notes too.

## Workflow, evidence and verification

Start with git status and current checks. Do not rewrite prior commits or manufacture a test-first history. Update research/course-design.md with the revised contract, recording which first-draft requirements this changes. Keep the record factual and scoped to course decisions. Do not write PROCESS.md or reflections; I will author those. Implement in reviewable, descriptive commits, staging explicit files and inspecting the staged diff. Suggested boundaries: design/harness/test revisions; fixed client intake dossiers/plans; measurement teaching and A1; specialist dossiers; design/optimisation teaching and A2; decks/tutorials/assets; browser corrections. Use subject lines such as 'design: ...', 'content: ...', 'spec: ...', 'fix: ...' followed by what changed and why. Do not add commits merely to inflate the history. Preserve starter invariants; replace obsolete course assertions because the course changed, not to conceal implementation defects. Run pnpm check before commits and report any intentional transitional failures until resolved.

Add meaningful checks for five fixed sites/no custom-site route; diagram/data geometry consistency; Release A/B availability and dataset schema; twelve weeks and decks; assignment weights/dates; revised lead-site allocation; coupled water metrics; feasible reference costs; and citations where mechanically testable. Keep subjective teaching quality and diagram readability in manual review. Explain in the final report what is checked mechanically and what was judged manually.

Build and inspect the actual UI at 1920×1080 and 390×844, preferably using browser viewport emulation. Verify diagrams, legends, tutorials, decks, scrolling tables and downloads. Report the method and limitations precisely. Run pnpm check and pnpm check:evidence. PROCESS.md placeholders may remain the sole evidence blocker; never fill them in or suppress the gate. Use mise exec -- pnpm as needed. Preserve existing node_modules fixes; report recurrence of the known search-index ENOENT or missing html language issue rather than quietly editing dependencies.

Complete the second draft and provide preview instructions, a commit-to-decision table, actual verification results, remaining evidence gaps and the illustration asset manifest for the subsequent image pass. Distinguish observations from checks not performed. Do not push, deploy or change visibility. Do not stop for approval of routine wording, persona details, hypothetical geometry or other minor decisions within this brief.
