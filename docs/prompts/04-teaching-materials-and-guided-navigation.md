Complete this local content and usability pass. Use straightforward implementation and reasonable small design decisions; do not stop at a plan. No subagents, dependency additions, new scientific research, model recalibration or generated images. Reuse existing text, data, CSS tokens and the deck pipeline. Read README.md, CLAUDE.md, the relevant content and current git status first. Preserve unrelated unfinished work, particularly research/export_sources.py and src/data/sources.json; do not stage them incidentally.

The fixed Slop branding, platform, collections, API and starter invariant tests stay intact. This prompt overrides older project instructions about weights, assignment tasks, keeping only two decks and an image-free visual direction. Update conflicting project-specific tests and design notes to the decisions below. Existing assertions are not authority to reject an explicit change; preserve true platform invariants.

## What to finish first

The weekly navigation commits through e204060 are useful. Keep src/lib/weeks.ts as the single topic map and retain its existing twelve-topic order. Week 3 is mushrooms. Do not restart the curriculum design.

The previous pass did NOT finish the assessment changes. A1 still requests a Food Loop Design, A2 builds on that, and quizzes are still 8% each. Finish these changes before embellishing the site:

- Five quizzes, weeks 3/5/8/10/12: 4% each, 20% total.
- Ten tutorial completion checkpoints, weeks 2–11: 2% each, 20% total. Weeks 1 and 12 are ungraded practice.
- A1 Year-long Measurement Programme: 20%, existing week-7 deadline.
- A2 Household Resilience Investment Proposal: 40%, existing assessment-period deadline.
- Total 100%. Represent tutorials as one weighted 20% assessment record containing ten checkpoints, not eleven weighted records. Each checkpoint is due Friday of its teaching week using the actual calendar. State good-faith completion requirements: legible attempt at every listed output, assumptions and units shown; correctness receives feedback, rather than changing the completion mark. Attendance alone is not completion; independent completion is allowed. Existing extension rules apply. Do not build an LMS or pretend the static site collects grades.

Preserve assignment URLs, replacing titles, briefs, rubrics and obsolete cross-references. A1 is a plan for twelve fictional months of measurement: what decision each measurement supports; sensor/manual method, location, units, frequency, accuracy; seasonal coverage, calibration and missing data; safety and costs within the separate $1,500 investigation allowance. No finished food-system design required. Provide a compact measurement primer before A1, linked from week 1 and the brief, covering water/rain/tank, soil/shade, food/waste logs and uncertainty. Adapt week 6 to assemble and review the measurement plan while retaining its preservation exercise in shorter form.

A2 uses supplied specialist findings to compare the existing baseline with three feasible retrofit options and justify one recommendation: flow diagram and conceptual site layout, important capacities/flows, cost, energy, reliability, maintenance, uncertainty and rejected options. Keep the $30,000 implementation allowance and 5 kWh/day energy limit with their existing definitions. Students may reject unsuitable subsystems with reasons. Do not require detailed pipe engineering or installation of every technology. Expose existing Release B data through a shared readable client-findings template and real download links; do not invent a new dataset. The supplied findings do not depend on A1 quality.

State the story clearly: a fictional policy and consultancy used to learn engineering. Nobody applies for a real loan or waits a real year. Weeks 1–6 scope possible systems and evidence; A1 is submitted in week 7; then the story jumps a year. Week 7 can preview water methods and the specialist handover, but do not imply the handover happened before A1's actual Friday deadline. Pre-handover calculations use labelled practice/scoping data, not actual observed findings. Keep the self-aware humour on welcome/help pages, away from safety guidance.

## 1. Three visible navigation groups

Use these exact groups consistently in navigation and in an explanatory homepage section:

1. **Weekly study** — Weeks, Lectures, Tutorials, Assessments. Start with Weeks; lecture/tutorial indexes remain useful alternative entry points.
2. **Course reference** — Clients, Programme & method. These are reusable resources, not another weekly task list.
3. **People & policies** — People, Policies.

Use visible group headings, spacing, restrained tinted surfaces or borders and existing Slop accents. Grouping must remain obvious in the mobile menu. Do not leave the same nine ungrouped links across the top and call the homepage cards sufficient. Use supported theme configuration or small local components/layout overrides; do not patch node_modules or replace the platform. Avoid duplicate competing navigation bars.

Merge the programme introduction into the START of /method/: fictional scenario, the two project phases, what the homeowner supplies and what the student produces. Follow it with a short linked contents list, then the existing methods, bands, costing, datasets and worked comparison. Keep the content, improve its order. /programme/ must still resolve through a supported redirect or short onward page; remove it as a competing main destination and update internal links.

Every week overview, lecture and tutorial should have a short contextual reference block with 1–3 useful deep links, e.g. the lead client's plan, the definition used in the calculation or the price schedule. Say why the student needs each. Link a relevant reference from each quiz as well, without changing the conceptual questions unnecessarily. Avoid dumping the entire reference index on every page.

## 2. Four small, reusable walkthroughs

Add an obvious labelled **How to use this page** button near the heading on Home, /weeks/, /clients/ and /method/. Home also offers **Take the site tour** in its start-here area. The walkthroughs are page-specific, 4–6 short steps each:

- Home: fictional setting; the three groups; assessment outputs; timeline modes; open Week 1.
- Weeks: choose a week; overview/lecture/tutorial/quiz links; deadlines versus workload; carry forward your output.
- Clients: choose one existing home; read the scaled plan and constraints; distinguish supplied facts from assumptions; find intake and specialist findings; keep the same client.
- Programme & method: read the scenario; understand measurement versus design; find definitions, bands, costs and datasets; follow a worked example.

Build one reusable lightweight walkthrough component with per-page step data. An inline step panel is fine: previous/next, step count, close and restart, and a link that scrolls to/highlights the corresponding real section. Avoid fragile screen-coordinate overlays or a new tour library. Announce step changes accessibly, support keyboard operation, restore focus on close and respect reduced motion. Never launch a blocking tour automatically. Provide readable help with JavaScript disabled. These tours explain navigation and workflow, not new assessment obligations.

## 3. One semester planner with two views

Put the SAME shared planner on Home and /weeks/, above the detailed weekly entries. The COMP4020 homepage is the visual reference: https://comp.anu.edu.au/courses/comp4020-agentic-coding-studio/ . Use its time-axis, separate marker rows and legend idea, adapted to this course. Do not copy its dates, break placement or assessment weights. Our calendar has a two-week break after week 5.

Two clearly labelled controls switch views:

**Deadlines & materials**: teaching weeks 1–12, actual break, assessment period; separate marker rows for overview, lecture/slides, tutorial, quizzes and assignment deadlines. Each marker is a real labelled link, with details on focus as well as hover and usable on touch. Show percentages and exact due dates where relevant. A2 belongs at its actual exam-period date, not at week 12 just because its metadata says week 12. Tutorial checkpoints are visible without pretending each is an extra assessment record. Include a legend and labels so colour is not the only distinction. Keep today's line only if the current date lies inside this course's actual calendar; no fictional current week.

**Suggested weekly effort**: stacked bars with hours on the vertical axis, one per teaching week, showing lecture/notes, tutorial, preparation/quiz, A1 and A2. Tooltips/focus details and an accessible table give category hours and the week's concrete assignment milestone. Explain that this is an illustrative planning guide, not observed student data, required attendance or a guarantee. It must encourage early incremental work, not a deadline spike. Use this course planning assumption unless an existing published contact-hour requirement genuinely conflicts:

- Every teaching week: 2 hours lecture/notes, 2 hours tutorial, 1 hour preparation/quiz.
- Weeks 1–6: 3 further hours A1 each week (8 hours total).
- Week 7: 2 hours A1 final checks/submission and 1 hour A2 orientation after the handover (8 total).
- Weeks 8–12: 3 further hours A2 each week (8 total).
- Exam period: a separate clearly labelled 4-hour A2 final review/submission allowance, NOT a four-hour-per-week bar. No compulsory break work; mark break catch-up as optional, outside the totals.

Thus the suggested budget is 96 hours over the twelve teaching weeks plus 4 hours in the assessment period. It is a modest fictional-course planning allowance, not a claim about official university credit-hour requirements. Tutorial submission time is inside its 2 hours; quiz time is inside preparation. Do not double count either. A1 milestones progress through client/decision inventory, sampling plan, biological measurements, QA/safety, costs, assembly and final check; A2 progresses through findings, options, sizing/reliability, costing, comparison and recommendation. Match those milestones to the final teaching pages.

Use simple native SVG/HTML/CSS, no chart dependency. Share planner data with weekly expected-effort summaries instead of duplicating hours in prose. Preserve real dates and labels. On mobile, use a readable scrollable chart container with a cue and a compact table/list alternative; never shrink text to fit sixteen columns. Page itself must not overflow. Both modes remain discoverable and non-JavaScript visitors can access both datasets.

## 4. Actual lightweight slides for all twelve weeks

There are currently deck files for weeks 1 and 9. Retain and link both; add the missing TEN through the existing src/decks/*.deck.mdx pipeline. Every lecture page must expose a prominent **Open slides** link that builds and opens its own week's actual presentation.

For each new deck, aim for eight short slides: this week's question and story position; 2–3 learning outcomes; key concepts; quantitative method with units; a small worked example; client/site implications; tutorial task and output; recap/self-check and existing references. Reuse accurate material and source links already in that week's notes. No online research is needed. You have discretion over phrasing and modest illustrative examples: clearly label invented example inputs as practice assumptions and check their arithmetic. Do not invent scientific, legal or safety facts. Retain caveats on uncertain existing figures. If no supported factual value exists, use symbols or a labelled hypothetical value.

These are simple teaching drafts, not blank placeholder slides. Optional illustration placeholders may reserve space with a useful caption; no 'TODO lecture', lorem ipsum or fake links. Keep text brief, use the existing deck theme, and use a simple flow diagram or table where useful. Do not spend time polishing elaborate slide art. Week 1/9 need only corrections to match the new tasks and navigation.

## 5. Make every tutorial independently understandable

Read and improve all twelve tutorials, not just week 1. Keep useful exercises and existing calculations but supply missing instructional detail. Each must contain: purpose and story stage; time allowance; exactly what to open/download; numbered actions; a table/template or small example; the named output; a completion/self-check list; where it goes next. Link back to the lecture method needed. Define every unexplained 'sheet', 'curve', 'log' or 'plan'. Previous tutorial outputs should be linked and briefly described, with a small labelled fallback practice example so a missed week does not make the exercise impossible.

Specifically week 1: define the **client evidence workbook** as the student's own spreadsheet or document, not a missing website feature. Provide a copyable template or working CSV download and explicit instructions to create it. Include tabs/sections for client facts, twelve-month climate, measurement planning and an assumptions/source log. Give column names and units, one filled illustrative row, and the exact existing client/data/source links used to fill the rest. Separate climate normals from the simulated monitoring-year data. Show a beginner how to choose one home, record its fixed constraints, fill one row, annotate its source and check units. Do not simply tell them to find a Bureau station page or memorise annual household demand. Week 1 is ungraded; state what they retain for week 2.

For weeks 2–11, identify the small 2% completion output and the checklist that earns completion. Week 6 must help assemble A1; weeks 7–12 progressively help A2. Make sure a conceptual/practice exercise is not inadvertently stated as a compulsory technology in the student's final design. Do not change formulas, research data or course constants simply to make writing easier.

## 6. Style now, imagery next

Use coherent spacing, grouped cards, typography, restrained Slop colour, phase labels and readable diagrams to give the site character now. Home should explain the site before showing technical detail. Use light self-awareness, for example 'The government is imaginary. Your water balance still has to add up.' Keep humour sparse.

Do not generate or fetch stock images this session. Remove obsolete project instructions that ban future conceptual imagery. In your final report suggest at most six useful illustration slots, each with page, purpose, aspect ratio and proposed caption. We will commission the images separately after this pass; do not create fake asset links or empty decorative boxes across the site in anticipation.

## 7. Verify and commit the actual outcome

Work in coherent batches: assessment/narrative repair; explicit tutorials and slides; grouped navigation and walkthroughs; shared planner and final integration. Make small descriptive local commits, staging explicit relevant files. Run the repo gate before committing as required. Do not produce endless planning documents or broaden into model work. Keep the repo's design contract concise and aligned with the final decisions.

Preserve starter invariant tests. Add focused assertions for 12 valid lecture-deck links, correct assessment totals/checkpoints, matching weekly topics/resources, and planner data sums/dates. Test observable behaviour for both planner controls and all four tours: open, next/back, close/restart, keyboard focus and actual target sections. Do not count the existence of a button as proof its interaction works. Manually read all tutorial instructions; run one week-1 workbook row yourself and report any missing inputs you fixed. Read week 3 as a complete overview/lecture/slides/tutorial/quiz bundle and week 6–7 as an A1/handover bundle.

Run mise exec -- pnpm check and then pnpm check:evidence. Do not bypass student-authored evidence blockers. Check the built Home, Weeks, Clients, Method, tutorial 1, week 3 and representative decks at desktop and mobile widths. Inspect every deck for obvious clipping through its built output; simple content must still fit. State the actual browser/viewport method and any limitations. Green content tests alone do not establish usability. No theme patching or dependency reinstall unless a missing dependency genuinely blocks the existing pipeline.

Finish with commit hashes and a concise completion matrix: assessment repair; navigation groups; four working tours; both planner views; twelve linked decks; twelve explicit tutorials; checks; remaining issues. Report counts actually verified, not intended counts. Include the correct local preview command/URL. List any omission explicitly rather than claiming the full request is complete. Leave PROCESS.md and reflections for the student, and do not publish.
