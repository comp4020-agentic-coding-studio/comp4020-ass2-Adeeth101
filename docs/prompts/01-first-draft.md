Build the complete first local draft of my Assignment 2 course website in this repository. Continue through implementation, verification and local commits; do not stop after a plan or harness. Do not push, deploy or change repository visibility.

## Read and establish the contract

Read README.md, the supplied CLAUDE.md, src/course-config.ts, src/content.config.ts, src/site-config.ts, spec/ and scripts/check-evidence.ts. Preserve the fixed SlopU branding, palette, content collections, generated API and starter invariant tests.

Read the live brief and assessment rules:
https://comp.anu.edu.au/courses/comp4020-agentic-coding-studio/assessments/assignment-2/
https://comp.anu.edu.au/courses/comp4020-agentic-coding-studio/topics/assessment/

Read the repository's research/course-design.md first, followed by research/sources.md, research/findings.md, research/critique-log.md and research/model/output/band-thresholds.md. The complete original research and reproducible model are in research/. Its README contains older path/status notes: use these local paths. Treat earlier iteration outputs as historical comparisons; the decided design takes precedence.

Stay within this repository for local file access. All project inputs are here. Public primary-source browsing is allowed. Do not write or edit PROCESS.md or reflections: I write those myself. Report useful decision/commit references in your final response.

## My course decisions

- SLOP4761, level 4: Designing the Closed-Loop Household I: Food, Water and Waste.
- Sequel: SLOP4762 — Designing the Closed-Loop Household II: Energy and Shelter. Mention it on the home page, prerequisites, week 1 and week 12; label it a proposed follow-on course rather than inventing a live catalogue destination.
- Use the exact prerequisites in the design consistently.
- This is a sincere engineering design course about how much of a household food, water and waste loop can honestly be closed within a plot, budget and process-energy allowance. Make partial closure and unavoidable imports clear. Students design systems; they are not being asked to construct or operate them.
- Household: two adults and two children. Sites: Canberra suburban, Alice Springs rural-residential, Brisbane townhouse, Adelaide suburban and Darwin rural-residential. Preserve the decided parameters and existing inventory.
- Twelve topics in order: loop thinking; perennials and soil; mycology; insect farming; aquaponics; fermentation; water sourcing; treatment; water security/storage; waste management; sanitation; integration.
- Quizzes: five conceptual, non-numeric quizzes worth 8% each in weeks 3, 5, 8, 10 and 12. Food Loop Design: 20%, due week 7. Capstone Site-Specific Off-Grid Master Plan: 40%, exam period. No oral assessment.
- Keep 5 kWh/day peak-month process energy and a $30,000 course costing allowance, including the specified contingency. Follow the full counted-load list and uncertain-load rules in the design.
- Publish site cards, reference-band tables, assumptions, price schedule and one worked cross-site comparison. No interactive calculator.

## Evidence and modelling before publication

The research is a screening model, not a validated engineering design. Verify high-impact claims using primary sources, especially water demand, fish temperature/legality, feed rules, greywater, sanitation, fermentation and costs. Sources read only through search summaries need checking even if their confidence label is high. Record source URLs and verification notes in research/sources.md as you resolve them.

Use explicit labels for course assumptions, indicative costs, model estimates and synthetic datasets. A safety or legal claim cannot become true merely by labelling it a course assumption: verify its jurisdiction and scope or omit the unsupported operational claim. Distinguish conservative course design rules from actual legal requirements. For fermentation, the draft says 2–2.5% salt and pH at or below 4.6, never 22.5%; restrict specific advice to a verified recipe and its conditions rather than treating this as a universal guarantee.

Resolve the known reference-cost gap: the expanded price schedule and contingency are not included in the old model totals. Re-cost the reference designs using the decided schedule, avoid double-counting bundled pumps, and include applicable establishment components. Check feasibility against the full energy boundary too. Do not claim the old $22–25k totals establish compliance. If a reference recipe needs adjusting, use the smallest transparent adjustment that retains the five sites, budget, cap and scoring approach; document and recompute affected outputs. If feasibility remains unresolved, make that limitation visible and complete other work rather than inventing compliance.

Use climate-normalised reference bands inspired by NatHERS. They are performance evidence within the rubric, not automatic grades or proof of equal grading outcomes. Always pair water closure with garden water satisfaction. Waste-stream recovery is assessed by mass balances, not bands. Publish reference recipes, assumptions, thresholds and clear boundary inclusivity. Resolve rounding consistently with the model; do not silently turn rounded display values into different grading thresholds. Recompute all affected tables if constants or recipes change. The existing sensitivity test covers only its listed indicators; do not extend its claims to garden water satisfaction without testing it.

## Teaching and visual direction

Write concise, specific Australian English. Avoid generic hype and repetitive weekly templates filled with interchangeable prose. Each week should contain a concrete engineering question, a named quantitative method, a sourced worked example, an activity or dataset, and a tangible output that advances the student's design.

Every topic week 2–11 includes a Five sites section covering all five presets. Lead assignments: Canberra weeks 2/11; Alice Springs 7/10; Brisbane 3/8; Adelaide 5/6; Darwin 4/9. Weeks 1 and 12 integrate all sites. Preserve Canberra's rainfall/chill advantages and the townhouse's space/strata constraints.

Make the site feel like a carefully designed engineering field manual: readable typography, restrained visual hierarchy, useful flow diagrams, site comparison cards and clear units/source labels. Keep SlopU's required identity and palette. Avoid decorative dashboards, stock promotional copy and implementation details in student-facing pages. Use original, course-specific diagrams or artwork; a deliberate image-free design is acceptable if all starter imagery and metadata are properly replaced. Do not fabricate real staff identities or institutional endorsements.

Create a real, linked lecture deck with substantive teaching content. Supply clearly labelled synthetic troubleshooting data where required. Quiz pages should include meaningful conceptual questions with explanations or practice feedback, while making clear that the static site does not securely collect grades. Assessment briefs must explain deliverables, rubric, dates and how performance bands are used.

Choose a coherent dated semester using the starter's 2027 semester as the default and verify the calendar. The exam-period capstone date must remain within the course record's overall date range required by the starter invariant test; do not weaken that test. Explain teaching dates versus the assessment period where necessary. Use a single source of truth for repeated facts.

## Implementation and commits

First run the existing gate and inspect git status. Research is supplied as new files: include relevant research in the first appropriate commit, but exclude __pycache__, generated bytecode and irrelevant temporary files. Preserve unrelated changes.

Replace the supplied CLAUDE.md template with short course-specific rules and reasons: identity, evidence, voice, site coverage, scoring, safety, budget/energy, scope and verification. Keep it about this project. Add meaningful contract tests alongside the unchanged starter tests. Check built output/generated data where possible: identity, twelve semantic topics/dates, weights/quiz weeks, lead-site coverage, prerequisites/sequel, band integrity, paired water indicators and price bases. Avoid brittle exact prose matching and superficial keyword checks masquerading as safety verification.

Make small commits that reflect actual completed work. Suggested sequence: evidence/reference reconciliation; harness and contracts; identity/home/sites; weeks 1–6; weeks 7–12; assessments/prices/bands; deck/policies/visuals; final verification. You may regroup to keep coherent working stages. Run pnpm check before commits. If using an intentional red-test stage, report its expected failures honestly and immediately continue implementing until they pass. Do not stop at that stage.

Use mise exec -- pnpm if pnpm is not directly available. Avoid reinstalling dependencies unless necessary. This Windows installation has local theme fixes in node_modules; if `spawn npx ENOENT` or missing `<html lang>` recurs, report the exact blocker rather than silently patching dependencies. Continue independent work that is still possible.

## Verify the full draft

Run pnpm check, then pnpm check:evidence. The student-authored PROCESS.md may still block evidence readiness: report that precisely, do not fill it in or bypass the check. Remove all other starter-content blockers you can legitimately resolve.

Build and inspect the real local UI at 1920×1080 and 390×844. Check the home page, separated weeks, site tables, both assignment briefs, navigation and deck. Fix overflow, illegibility, broken links and inconsistent facts. If browser verification is unavailable, state what remains unverified. Do not claim a deployed-site test when only local output was inspected.

Finish with the local preview command/URL, commit hashes, tests and viewport checks performed, substantive design/evidence decisions, unresolved limitations and what I must supply before submission. The outcome should be a complete reviewable first draft, not scaffolding or a plan. No push, deployment or visibility change.
