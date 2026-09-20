The current course is very close to what I want. Your priorities are a substantial visual improvement using my supplied images, finishing small outstanding integration work, and checking the whole result. Do not restart the design or rewrite the curriculum.

Import the images from my supplied artwork archive into the repository. Other project inputs are inside the repo. Do not push, deploy or change visibility. Do not write PROCESS.md or reflections. Preserve unrelated work. No subagents or new dependencies unless a genuine technical blocker requires one; use existing tools first.

## Current state and scope

Read README.md, CLAUDE.md and git status before edits. At handoff, HEAD is 2d00320, with only research/export_sources.py untracked. Preserve that file. Recent completed commits:
- f5f9445: revised assessments and weights.
- 46349eb: expanded tutorials and workbook instructions.
- b8f3abf: twelve decks.
- cfa491e: navigation and four walkthroughs.
- 2d00320: shared planner and contract tests.

The most recent independent local gate passed: 89 tests, twelve structurally valid decks, successful typecheck/build/link checks, and cached accessibility checks. That is a baseline, not proof of current visual quality. check:evidence failed because PROCESS.md contains the starter comment and fake hashes a1b2c3d/e4f5a6b. Leave student-authored prose alone and report these blockers.

Your scope is (1) final integration cleanup and (2) image integration/visual polish, followed by verification and a report. Do not write the student's process account or publish. Do not invent additional features, new research or new model assumptions.

## Latest course specification — preserve this

SLOP4761 Designing the Closed-Loop Household I: Food, Water and Waste, level 4, engineering audience. Retain exact metadata, prerequisites and sequel references. A lightly self-aware fictional consultancy and government loan scheme is a classroom exercise, not a real programme. Students advise one of five fixed model homes. No custom properties or enlarged plots/roofs. The narrative moves from a twelve-month measurement proposal to supplied specialist findings and a conceptual engineering investment recommendation; no real year elapses.

Keep src/lib/weeks.ts as the authoritative topic map. Twelve dated weeks retain their existing order: household evidence; soil/plants; mushrooms; insects; aquaponics; preservation and measurement-plan assembly; water sourcing/handover; treatment; storage; waste; sanitation/options; integration. Week 3 is mushrooms. Preserve calendar dates, including the two-week break after week 5. A1 is due Friday in week 7; the fictional handover follows submission, though teaching may preview it earlier.

Assessment: five quizzes at 4% each in weeks 3/5/8/10/12; ten tutorial completion checkpoints at 2% each in weeks 2–11, represented as one 20% assessment record; A1 Year-long Measurement Programme 20%, week 7; A2 Household Resilience Investment Proposal 40%, existing exam-period deadline. Total 100%. Weeks 1 and 12 tutorials are ungraded. Completion rewards a legible good-faith attempt covering the stated outputs, not attendance or numerical perfection. No LMS/grade collection is to be built.

A1 plans measurements, decisions, methods, locations, frequency, units, accuracy, calibration, seasonal coverage, missing data, safety and the separate $1,500 investigation allowance. A2 compares baseline plus three options using supplied findings, then recommends a concept with important flow/capacity calculations, layout, costs, energy, maintenance and uncertainty. Preserve $30,000 implementation and 5 kWh/day process-energy constraints and their published definitions. No compulsory installation of every technology or detailed pipe design.

Three visible navigation groups: Weekly study (Weeks, Lectures, Tutorials, Assessments); Course reference (Clients, Programme & method); People & policies (People, Policies). /method/ begins with the programme narrative and then methods; old /programme/ links still resolve. Weekly overviews lead into their own lecture, tutorial and quiz where scheduled. Relevant reference links connect study pages to reusable resources.

Four optional page-specific walkthroughs: Home, Weeks, Clients, Programme & method. Keep obvious help buttons, keyboard support, next/back/close/restart and real section targets. Avoid intrusive automatic tours.

One shared planner on Home and Weeks: switch between deadline/material markers and suggested effort. Preserve dates and meaningful accessible links. Effort is a labelled course planning assumption: each teaching week 2h lecture/notes, 2h tutorial, 1h preparation/quiz plus 3h assignments; weeks 1–6 A1, week 7 2h A1 plus 1h A2, weeks 8–12 A2. Total 96 teaching-week hours plus a separate 4h exam-period finalisation allowance. Break work is optional and not silently counted. No duplicate counting of tutorial/quiz time.

Twelve actual linked slide decks; simple accurate teaching content is sufficient. All tutorials must name inputs, actions, templates/examples, outputs, checks and next steps. Tutorial 1 explains the client evidence workbook and supplies CSV templates. Preserve usable instructional content and the existing scaled SVG plans, charts and quantitative methods.

## Finish the interrupted cleanup

Bring research/course-design.md and the project CLAUDE.md into agreement with the above. CLAUDE.md was still stating 8% quizzes; src/site-config.ts retained an image-free comment. The harness also referred to nonexistent Illustration.astro and research/asset-manifest.md: replace those claims with the actual implementation you deliver.

Tutorial 1 still claimed no site was easier than another and implied the model proved that. Correct this, and equivalent week-1 claims if present, to the qualified position: different constraints, contextual reference bands, and no proof of equal grading. Preserve existing source qualifications. No new scientific research needed.

## Images and visual treatment — main priority

The ZIP contains eight JPEG files, with descriptive filenames: brick-veneer house, engineer/suburban house, Brisbane townhouse, engineering illustration, blockwork rural house, suburban architectural illustration, ivory paper texture, and elevated tropical house. Inspect ALL eight visually before mapping them. Filenames alone are not sufficient. Check archive paths before extraction; write only intended asset files, never overwrite source files from archive paths.

Expected roles, subject to visual confirmation:
- home-hero: engineer examining a household; prominent homepage artwork.
- client-canberra: brick-veneer suburban house.
- client-alice-springs: blockwork rural house.
- client-brisbane: townhouse.
- client-adelaide: remaining suburban double-brick house.
- client-darwin: elevated tropical house.
- measurement-to-proposal: engineering workbench/process illustration.
- paper-background: subtle decorative texture.

Use stable descriptive filenames under src/assets/images/ and the existing Astro image pipeline. Preserve originals where useful but do not commit the ZIP, redundant full-resolution variants or temporary extraction files. Generate appropriately sized responsive output, declare dimensions, lazy-load below-the-fold images and keep the hero loading appropriately prioritised. Do not stretch or crop off the main subject. Inspect mobile crops explicitly.

Give the homepage an intentional editorial composition: clear course identity and fictional premise, generous hero artwork, an obvious start-here action, clearly grouped materials and a readable planner. Keep the course structure and deliverables easy to find. Use existing Slop gold #b97d1c, bronze #8a5c13, warm grey #6b6154 and theme surface/text tokens; preserve Slop branding and marks. Add richness through imagery, whitespace, hierarchy and consistent card treatment rather than animations, extra widgets or more prose.

Use the five home portraits consistently on client cards and corresponding dossier pages. Label them as conceptual illustrations; the supplied scaled plans determine geometry. Images must not imply mandatory upgrades or replace technical drawings. Put the process illustration on Programme & method where it explains measurement-to-proposal; reuse sparingly elsewhere if useful. Background paper should be barely perceptible. Keep text, tables, code and deck content on legible surfaces. Support existing light/dark behaviour; a light paper texture must not make dark-theme text unreadable. Decorative CSS backgrounds require no spoken description; meaningful images need concise accurate alt text. Captions must not pretend generated artwork is a photograph or survey.

Make navigation grouping convincing at desktop and mobile widths. Current group headings use CSS ::before text on the first links, not actual semantic groups. Inspect how wrapping affects their association; improve local markup if necessary using supported extension points. Do not patch node_modules. Preserve fixed collections/API/build pipeline. Do not merely add images above an otherwise broken or cramped layout.

Record a concise asset inventory in research/asset-manifest.md: actual file, purpose, placement, dimensions, alt/caption, and the fact it is supplied generated conceptual artwork. Do not invent copyright/licence claims. Do not generate additional images unless I ask. If one supplied image is unusable, explain exactly why and use the other suitable assets instead of forcing it.

## Acceptance and verification

Verify the current built site, not just source. Use existing browser automation or supported local browser tooling. Check 1920×1080 and 390×844; report exact emulation/iframe/window method and limitations. Do not claim genuine window-size tests if you used another method.

1. Home, Weeks, Clients, one full client dossier, Method, Assessments, tutorial 1: inspect layout, text contrast, image crops, grouping, missing assets, page overflow and readable tables. Check all five client portraits for correct mapping. Take representative before/after screenshots for your own comparison, keeping temporary files out of commits.
2. Both planner modes on Home and Weeks: keyboard/touch usability, correct dates, marker destinations, hours/totals, readable mobile alternative and no clipped tooltips. Check important controls with JavaScript disabled where practical.
3. All four tours: actual opening, next/back, close/restart, target scrolling, focus restoration and keyboard behaviour. String assertions are not behavioural proof.
4. All twelve overview/lecture/tutorial/deck routes and all five quiz links: confirm correct-week destinations and no missing assets. Inspect each built deck for obvious overflow/clipping; generated artwork is optional in decks.
5. Read week 3 as a complete bundle, weeks 6–7 for the assignment/handover transition, and week 11 for a non-adjacent coherence check. Walk through one tutorial-1 workbook row using its actual template and input data; fix contradictory instructions such as mismatched row labels.
6. Confirm assessment total/checkpoint counts, findings downloads, source qualifications and old programme route. Preserve scientifically meaningful caveats. Distinguish tests of existence from checks of correctness.
7. Run mise exec -- pnpm check, then mise exec -- pnpm check:evidence. Preserve starter invariants; amend relevant project assertions when fixing intended behaviour. Do not fake green evidence by altering PROCESS.md or disabling checks.

Make coherent local commits for contract cleanup, artwork/visual integration and final verified fixes as appropriate; gate before committing according to the repo convention. Stage explicit files and inspect diffs. Avoid speculative refactors and repeated full checks without new changes. Do not install dependencies or edit theme packages to chase unrelated problems.

## Report back, then stop

Give a concise but complete report with:
- Actual changes and commit hashes; whether the working tree has anything left.
- Asset mapping and every image's placement, including unused images and why.
- A verification matrix: area, check performed, result, limitation. Use PASS / FAIL / NOT CHECKED; never turn 'not checked' into 'pass'. Separate automated gates from human/browser/content inspection.
- Any unresolved functional, visual or course-coherence issues, prioritised by submission impact.
- Correct local preview instructions, noting that an existing server may need --force and preview serves the built output.
- Remaining student actions: personally review the result, author PROCESS.md with real commit citations, authorise publication, then verify the deployed site. Do not write that account or publish yourself.

The goal is a visually much stronger version of the current near-final course, with evidence that it works. Stop after this local handoff.
