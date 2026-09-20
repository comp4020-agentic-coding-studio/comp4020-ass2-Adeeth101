# Process overview

## What I built

SLOP4761 Designing the Closed Loop Household I: Food, Water & Waste. Twelve-week Slop University course, presented as a consultancy case. Students play the role of graduate engineers at a fictional company, providing consulting advice for five fixed households that are seeking a fictitious loan program. First, they develop a one-year measurement program (A1), followed by receiving data findings to defend a retrofit costing less than $30,000 and utilising 5 kWh/day peak month energy (A2). The idea behind this is that a learning site should have the ability to validate its own figures; all figures contained on the site are either generated from models stored within the repository or include sources that can be accessed without accessing the repository.

## How I got here

I developed the engineering idea before developing the course. A Python model located in research/model/, generates the geometry, water balance and cost of each of the five houses, along with a record of iterations and critiques against actual data. This loop destroyed my original version's assumptions -- roofs sized by eye provided only 20-66% of the household demand, and my water closure metric quickly teaches students (and me) that a fully autonomous closed-loop house is unrealistic. So instead, this course becomes an optimisation problem, so engineering was an easy sell.

Next, I validated the facts I would soon teach. research/verification-log.md documents what I retrieved. Some figures and numbers I stated, like the 150 L/person/day metric was missing citations. I made it a priority to justify the course as one rooted in real science and therefore citing everything was a must. Therefore, the site will publish this as a stated course assumption rather than as a reference - [`890a544`](https://github.com/comp4020-agentic-coding-studio/comp4020-ass2-Adeeth101/commit/890a544).

Claims regarding safety or legality do not become factual simply due to having been relabeled; therefore, any information that did not pass this validation process was removed.

The failures I am concerned with most were harness level, not code level. In my first version of the draft, students were allowed to create their own sites; however, this created dissimilar dossiers; thus, CLAUDE.md now clearly states: "There is no custom site available anywhere." The changes required to enforce this ran [`e06a79a...151c761`](https://github.com/comp4020-agentic-coding-studio/comp4020-ass2-Adeeth101/compare/e06a79a...151c761).

Finally, upon reviewing my own work, I felt that the site was overwhelming. Week 3 was labelled water monitoring while I was teaching mycology, and there was no cohesion. I intentionally limited the fix:

> Prioritise a correct, simple result with minimum rewriting… Fix this through a single weekly map based on the teaching content that already exists. Do not disguise unrelated content with a new heading.

Now, there is one source of weekly metadata driving the generation of twelve overviews pages and the navigation - [`2835d38...e204060`](https://github.com/comp4020-agentic-coding-studio/comp4020-ass2-Adeeth101/compare/2835d38...e204060), with assessments, tutorials and decks following in [`f5f9445...2d00320`](https://github.com/comp4020-agentic-coding-studio/comp4020-ass2-Adeeth101/compare/f5f9445...2d00320).

Lastly, I viewed the site in a browser instead of relying on the build. I documented what I observed - "the top bar cuts off ... it looks chaotic and unkempt," and there were some obvious typos, and these issues were addressed at [`d1f861c`](https://github.com/comp4020-agentic-coding-studio/comp4020-ass2-Adeeth101/commit/d1f861c).

Currently, the spec in spec/, is 98 validations confirming the contract weekly map to advertised pages, dossier facts to model. pnpm check passed 91 tests, and layout verification occurred at two marked viewport sizes.

