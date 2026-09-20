Implement this focused usability and curriculum-coherence pass now. Prioritise a correct, simple result with minimum rewriting. This instruction supersedes conflicting requirements from the earlier consultancy redesign, particularly its new topic order, 40% quiz weighting, twelve-deck requirement and extensive new tutorial production. Do not resume the whole previous expansion project. No subagents, new dependencies, broad research, model redesign or image generation. Read the current files you need, make the changes and verify them. Do not stop at a plan.

## Outcome

A student must immediately understand what this course is, what they submit, and what to do this week. The consultancy is an explicitly hypothetical classroom simulation, with a lightly humorous, self-aware voice. The current site mixes a water-monitoring week outline with a mushroom lecture/tutorial/quiz. Fix this through a single weekly map based on the teaching content that already exists. Do not disguise unrelated content with a new heading.

Read the repo README and CLAUDE.md, src/lib/calendar.ts, src/site-config.ts, src/content.config.ts, the existing lecture/session/assessment frontmatter and relevant pages/tests. Check current git status and preserve unfinished work, including the untracked sources export. Preserve the fixed SlopU branding/palette, collection names, API and starter invariant tests. Do not read outside the working repo for project inputs. Public assignment brief: https://comp.anu.edu.au/courses/comp4020-agentic-coding-studio/assessments/assignment-2/ .

## 1. One sequence, reuse existing material

Use this sequence everywhere. It follows the existing lecture/tutorial subjects, so retain their main explanations and worked examples:

1. Meet your client: household systems and evidence.
2. Soil, plants and irrigation demand.
3. Mushrooms: substrate, yield and what to measure.
4. Insects: waste streams and conversion limits.
5. Aquaponics: feed, fish and operating conditions.
6. Preservation and assembling the measurement plan.
7. Water sourcing and the specialist handover.
8. Treatment, reuse and service requirements.
9. Storage and seasonal reliability.
10. Waste recovery and integrated balances.
11. Sanitation, nutrient limits and choosing between options.
12. Integration and the investment recommendation.

Keep existing week numbers, dates, break and quiz weeks 3/5/8/10/12. Retain the original lead sites already used in the existing lessons: Canberra 2/11, Brisbane 3/8, Darwin 4/9, Adelaide 5/6, Alice Springs 7/10. Supersede the alternative lead-site map in the unfinished redesign. Preserve useful Five sites material.

The narrative has three stages: weeks 1–6 learn how candidate systems work and determine what evidence to collect; week 7 submits A1 then jumps twelve fictional months; weeks 7–12 use supplied findings to select and justify a retrofit. Calculations before the handover are scoping/practice estimates, not claims about actual measured results. Add short introductions and handoff sentences to existing teaching pages; do not rewrite their bodies wholesale.

## 2. Homepage and weekly navigation

Create a lightweight single source of weekly metadata, for example src/lib/weeks.ts. Map week number, topic, date, short narrative brief, lecture URL, tutorial URL, optional quiz URL, assignment milestones and expected tutorial output. Reuse calendar helpers. Use actual collection entries and existing routes rather than duplicating their dates/weights.

Create /weeks/ and twelve /weeks/week-NN/ overview pages using one shared template. Each overview starts with the shared resource navigation, then 100–180 words explaining this week's question, narrative stage, learning task and concrete output. Follow with a short ordered 'Do this week' checklist. Include previous/next week links.

At the top of weekly overviews, lecture pages and tutorial pages, show consistently labelled navigation links styled as tabs: 'Week overview', 'Lecture', 'Tutorial', and 'Quiz' only when one is due that week. Mark the active page with aria-current. These are normal links, not JavaScript tab panels; do not use ARIA tab roles incorrectly. Quiz pages should link back to their owning week and show the same resource navigation if practical. Link slide decks from the Lecture page where they exist, explicitly labelled 'Slides'. Lecture pages without decks say 'Lecture notes'; do not pretend notes are slides or link to missing decks.

Make 'Weeks' the primary navigation item. Keep Assessment and Clients prominent; move Programme/Method/People/Policies into a compact Resources menu or footer using simple existing components. Existing lecture and tutorial collection routes remain functional for the fixed platform. Do not delete those collections.

Homepage order:
1. Exact course identity and a plain-language introduction: 'A fictional consultancy. Five model homes. Real engineering decisions.' Explain that students design a measurement programme and an investment proposal; nobody waits a real year or applies for a real loan. Add one light line such as 'The government is imaginary. Your water balance still has to add up.' Avoid jokes in safety guidance.
2. 'Start here': choose a client, open Week 1, see assessment. Three links, no dense dashboard.
3. A compact deliverables/weights summary with links and due weeks.
4. A twelve-week timeline with an entry for every week, dates, topic and a one-line task; mark the existing break and assignment deadlines, with an exam-period milestone after week 12.

Each timeline entry has separately colour-coded dots beside explicit link labels: Overview, Lecture, Tutorial, and Quiz or Assignment when relevant. Provide a legend; use existing permitted theme tokens and accessible contrast. Colour is supplementary, never the only meaning. Make the entire dot-plus-label link clickable and keyboard accessible. Use a vertical timeline on phones (and on desktop too if simplest); no custom interactive visualisation. Reuse the current Timeline component only if it reduces work.

## 3. Assessments: concrete, consistent and light

Use exactly:
- Five quizzes at 4% each = 20%, weeks 3/5/8/10/12.
- Ten tutorial completion checkpoints at 2% each = 20%, weeks 2–11.
- A1 Year-long Measurement Programme = 20%, due week 7.
- A2 Household Resilience Investment Proposal = 40%, existing exam-period due date.
Total 100%. Weeks 1 and 12 tutorials remain useful but ungraded.

Retain the existing quiz questions where aligned to the retained topic order. Confirm each question is supported by the linked lecture/tutorial material from that week or earlier. Change only unsupported or contradictory questions. Quizzes remain conceptual; existing feedback UI can remain. State that course marks/submission are handled through the course LMS; this static site offers questions and feedback, not secure grade collection. Do not invent an LMS URL.

Represent tutorial completion as one 20% assessment entry, due at the final week-11 checkpoint, containing all ten dated checkpoints. Avoid also counting ten additional weighted entries. Each tutorial names one small submission from its existing exercise (table, sketch, brief calculation or justified decision) and adds a short objective completeness checklist. Award the full 2% for an on-time, legible good-faith attempt covering the listed items, including stated uncertainty; numerical correctness receives feedback rather than changing this completion mark. Copying a blank template is not completion. Equivalent independent completion is allowed; attendance alone earns no mark. Each checkpoint is due Friday of its week; follow existing extension policy rather than inventing punitive rules.

The two old assignment briefs still contradict the consultancy narrative. Replace only those briefs and necessary cross-references; keep their URLs to minimise broken links. A1 specifies a twelve-month measurement plan, sensor/location/frequency/accuracy table, seasonal sampling, calibration/missing-data plan, decision links, safety and costs within the separate $1,500 investigation allowance. Do not require completed system designs or all five biological modules. Add a compact measurement primer to week 1 notes and link it from A1: water demand/flow/tank/rain monitoring, soil/shade, food/waste audits, uncertainty, sampling and an example measurement table. Week 6 tutorial assembles the plan. This provides the required water/waste measurement instruction BEFORE the week-7 deadline even though detailed water-system sizing is taught later.

A2 uses the supplied specialist findings to compare baseline plus three options, justify cost/service/reliability trade-offs and recommend one concept with system-flow diagram, layout, sizing, costs, maintenance and uncertainty. Reuse existing dossier JSON/CSV and model outputs. Expose Release B through one shared, concise findings template for five clients, linked at week 7 and from A2; the data already exists, so do not regenerate a new research project. Clearly state that findings are supplied independently of A1 quality and the year passes only in the story. Mark them as issued after A1; this is teaching sequence, not secure access control.

Keep the revised assignment rubrics already recorded in research/course-design.md if they match these tasks. Correct all student-facing references to 'Food Loop Design', the old capstone obligations, 8% quizzes, obsolete weights, mandatory subsystem installation and obsolete weekly titles. A2 may reject unsuitable modules with reasons. Use one source for repeated assessment facts where inexpensive.

## 4. Scope control

Keep the five client dossiers, existing plans, datasets, formulas, prices and model. Do not redo research or recalibrate bands. Do not add a calculator or generate ten new decks. Keep the two existing real decks, make their topic links honest, and repair obvious overlap if seen. Existing short lecture notes are acceptable. Optional decorative illustrations can use clearly labelled conceptual placeholders; core text, assessment requirements, links and numerical diagrams must be usable and accurate. No blank mandatory lecture/tutorial pages or fake download links.

Use self-aware humour sparingly in the home/week summaries: this is an educational role-play, not a real consultancy portal. Keep instructions direct and reduce intimidating institutional prose. Keep source qualifications intact. If the untracked sources export can support a simple readable reference page without further research, integrate it; otherwise leave it untouched and report it. Do not broaden this into the earlier full enrichment project.

## 5. Checks, commits and handoff

Update the design contract and project CLAUDE.md concisely so future changes follow this simplified scope. Record why the week order now follows existing teaching: preserving substantive work while removing confusing mismatches. Do not write PROCESS.md or reflections. Preserve history.

Add/update focused built-output tests: twelve week overviews; valid same-week lecture/tutorial links; quiz tabs exactly in 3/5/8/10/12; new weights total 100 without double counting; ten tutorial checkpoints in weeks 2–11; no assessed quiz references to later untaught topics where mechanically testable; no obsolete water-monitoring label for mushroom week 3. Preserve the starter invariant tests. Manually read week 3 overview/lecture/tutorial/quiz together and check weeks 6–7's A1/handover sequence. Spot-check the other quiz weeks. Tests cannot substitute for these content checks.

Use a few coherent commits: weekly navigation/homepage; content/assessment alignment; final fixes/tests. Stage explicit files, inspect diffs, and use descriptive messages. Run pnpm check before commits; rerun after fixes, not repeatedly without a reason. At the end run pnpm check:evidence and report student-authored PROCESS.md blockers without bypassing them. Use mise exec -- pnpm if needed. Avoid dependency reinstall or theme patches.

Check the built home timeline, week navigation, week 3 sequence and assessment summary at 1920×1080 and 390×844, plus obvious diagram text overlap. Fix only relevant issues. Report how viewport checking was done and any limitation. Do not push, deploy or change visibility.

Finish with preview instructions, commit hashes, tests/results, confirmation of the final weights and week-3 alignment, and a short list of genuine remaining tasks. Deliver a coherent navigable local course now; do not stop after proposing this plan.
