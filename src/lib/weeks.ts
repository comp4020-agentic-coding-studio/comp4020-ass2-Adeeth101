/** The one place the semester's shape is written down.
 *
 *  Every week-facing page — the home timeline, /weeks/, each week overview, and
 *  the week banner on lectures and tutorials — reads this file. Dates, weights
 *  and page titles are deliberately *not* here: they live in the content
 *  collections and in `calendar.ts`, and the pages join the two. What is here is
 *  the narrative no collection entry can carry on its own: which stage of the
 *  commission a week belongs to, which client home leads its worked example,
 *  what question the week answers, and what a student leaves the tutorial with.
 *
 *  *Why one file:* the course previously carried two different week orders in
 *  two different modules, and the home page advertised a topic the lecture did
 *  not teach. One exported map cannot disagree with itself. */

import { weeks as weekNumbers } from "./calendar";

export type Stage = "learn" | "handover" | "design";

export interface WeekStage {
  key: Stage;
  label: string;
  /** The span, worded for a reader rather than for a legend. */
  span: string;
  blurb: string;
}

export const STAGES: Record<Stage, WeekStage> = {
  learn: {
    key: "learn",
    label: "Understanding the systems",
    span: "Weeks 1–6",
    blurb:
      "You meet the client and work through each candidate system — garden, mushrooms, insects, " +
      "fish, preservation — far enough to know what it needs and what would have to be measured " +
      "before anyone spent money on it. Every calculation in these weeks is a scoping estimate on " +
      "published figures, not a claim about this house.",
  },
  handover: {
    key: "handover",
    label: "Submission and handover",
    span: "Week 7",
    blurb:
      "Assignment 1 goes in, and the story jumps twelve fictional months. The specialist team " +
      "hands back what a measurement year at your home found (Release B), and from here on your " +
      "numbers come from those findings rather than from a scoping estimate.",
  },
  design: {
    key: "design",
    label: "Choosing and justifying the retrofit",
    span: "Weeks 8–12",
    blurb:
      "With the measured year in hand you size, cost and compare the options, then argue for the " +
      "one you recommend — the cheapest arrangement that meets the household's own targets, plus " +
      "an honest case for any dollar spent beyond it.",
  },
};

export interface WeekEntry {
  week: number;
  /** The topic, worded the same way everywhere it appears. */
  topic: string;
  stage: Stage;
  /** The preset id of the home whose worked example leads the week, or null when
   *  the week works across all five. */
  lead: string | null;
  /** Whether that home's climate makes the week's subsystem easier or harder.
   *  Each of the five leads once each way, so no student's home is quietly the
   *  easy one. */
  leadRole?: "helps" | "hurts";
  /** One line for the page lede and the meta description, saying something the
   *  brief's opening sentence does not. */
  summary: string;
  /** The question the week answers and why it comes here. */
  brief: string;
  /** What a student leaves the tutorial holding. */
  output: string;
  /** An assignment milestone that falls in this week, if any. */
  milestone?: string;
}

const ENTRIES: WeekEntry[] = [
  {
    week: 1,
    topic: "Meet your client: household systems and evidence",
    summary:
      "What crosses this fence line in a year, and how much of it nobody has actually measured.",
    stage: "learn",
    lead: null,
    brief:
      "You are handed one of five households and asked the question the whole course turns on: " +
      "what crosses this fence line in a year, and which of those flows could feed something else " +
      "on the same block? Before that is a design question it is a bookkeeping one, so the week " +
      "sets up the closure ratio the course scores and the site sheet every later week writes " +
      "into. You also meet the client properly — their priorities are theirs, not the course's, " +
      "and the retrofit you eventually recommend has to meet the targets they set rather than the " +
      "ones that would score well. Nothing here is measured yet. The annual demand figures are " +
      "standard published values for a household of this size, and the site sheet marks every row " +
      "as known, estimated or still to be measured.",
    output:
      "A site sheet with twelve rows of station climate data, every value sourced or labelled a course assumption.",
  },
  {
    week: 2,
    topic: "Soil, plants and irrigation demand",
    summary:
      "Why water rather than sunlight decides how much of the garden is worth planting.",
    stage: "learn",
    lead: "S1",
    leadRole: "helps",
    brief:
      "The obvious way to size a garden — area times days times yield — gives the wrong answer, " +
      "and the reason is that it never asks where the water comes from. This week replaces it with " +
      "a monthly water balance: reference evapotranspiration from FAO-56, effective rain rather " +
      "than total rain, and a crop coefficient, month by month. What falls out is a deficit curve, " +
      "and that curve decides how much of your growable ground is worth planting at all. Canberra " +
      "leads the worked example, because it is the site where a generous growing season and a " +
      "modest deficit pull in opposite directions. The deficit you compute here comes from " +
      "long-term climate records, not from your client's garden: establishing what that garden " +
      "actually draws is one of the things Assignment 1 will have to pay for.",
    output:
      "A twelve-row irrigation demand curve in kilolitres, and a planted area you can defend on water rather than on ambition.",
    milestone: "Tutorial checkpoint 1 of 10 (2 %) due 5 pm Friday.",
  },
  {
    week: 3,
    topic: "Mushrooms: substrate, yield and what to measure",
    summary:
      "What a household fruiting operation really contributes, and where the substrate goes afterwards.",
    stage: "learn",
    lead: "S3",
    leadRole: "helps",
    brief:
      "Mushrooms are the first of the biological modules, and they are a useful disappointment. " +
      "Sized honestly from biological efficiency, a household fruiting operation contributes a " +
      "fraction of a per cent of the year's energy — so the interesting output is not the food, it " +
      "is the five kilograms of spent substrate that leave for every kilogram picked. That " +
      "substrate is a genuinely good soil input and a genuinely bad insect feed, and knowing which " +
      "is the week's real content. Brisbane leads, because it is the site where some oyster species " +
      "fruits in all twelve months and the binding constraint turns out to be strata rules rather " +
      "than biology. The yields here come from the literature with a stated confidence; what your " +
      "client's own prunings supply is a measurement question you carry into Assignment 1.",
    output:
      "A substrate mass balance with both arrows drawn: substrate in, mushrooms out, spent substrate to soil and compost.",
    milestone: "Quiz 1 (8 %), sat at the start of the tutorial, on weeks 1–3.",
  },
  {
    week: 4,
    topic: "Insects: waste streams and conversion limits",
    summary:
      "How much of the fish feed a household's own scraps can actually cover.",
    stage: "learn",
    lead: "S5",
    leadRole: "helps",
    brief:
      "Search for a closed-loop household diagram and you will find the same arrow every time: " +
      "kitchen scraps to black soldier fly larvae, larvae to fish, fish to you. This week sizes it. " +
      "On dry-matter bioconversion and a household's actual plant-based waste stream, the loop " +
      "supplies a minority of the fish feed and the rest is imported — which is a result worth " +
      "having rather than a reason to abandon the module. Larvae also have a developmental " +
      "temperature threshold, so the months the unit runs at all is a site question. Darwin leads, " +
      "because it is the best site there is for this subsystem, which makes the shortfall elsewhere " +
      "easier to read. The waste tonnage is a standard per-household figure; what this house throws " +
      "out, and when, goes on the measurement list.",
    output:
      "A larval yield derived from your household's waste stream, with the imported share of fish feed stated on the diagram.",
    milestone: "Tutorial checkpoint 3 of 10 (2 %) due 5 pm Friday.",
  },
  {
    week: 5,
    topic: "Aquaponics: feed, fish and operating conditions",
    summary:
      "Sizing a system from its feed, and finding out what you are allowed to keep in it.",
    stage: "learn",
    lead: "S4",
    leadRole: "hurts",
    brief:
      "Aquaponics is sized from the feed, not from the fish and not from the plants: the FAO " +
      "feed-rate ratio sets grow-bed area from daily feed input, and stocking density follows. That " +
      "makes it the tidiest arithmetic in the course and also the piece most exposed to things the " +
      "model cannot see. Which species you may keep at all is a question of jurisdiction rather " +
      "than temperature, and the answer differs across the five homes. Adelaide leads the worked " +
      "example. The week also names the operating conditions a running system has to hold — " +
      "temperature band, pH, alkalinity — because those are what a measurement programme would have " +
      "to watch, and what a troubleshooting log will later show going wrong. Protein counted from " +
      "fish is reported net of imported feed, every time.",
    output:
      "A grow bed sized from the feed-rate ratio, a species choice with its temperature band, and the approval pathway named.",
    milestone: "Quiz 2 (8 %), on weeks 4–5.",
  },
  {
    week: 6,
    topic: "Preservation and assembling the measurement plan",
    summary:
      "Moving the glut into the trough, then turning six weeks of unknowns into a measurement programme.",
    stage: "learn",
    lead: "S4",
    leadRole: "helps",
    brief:
      "A garden produces a glut and then produces very little; a household eats at a constant rate " +
      "all year. Preservation is the storage term between those two curves, and it creates no " +
      "calories — it moves them through time and loses some in transit. You size it in kilograms " +
      "and floor area, and you cost any temperature control it needs, because that load lands in " +
      "week 12's energy budget. The second half of the week is the one that matters for Assignment " +
      "1. Every module so far has left behind a list of things nobody actually knows about this " +
      "house; you turn that list into a measurement programme — instruments, positions, frequency, " +
      "accuracy, cost against the allowance — with each reading tied to the decision it will " +
      "inform. Adelaide leads again, on its summer.",
    output:
      "A sized preservation store, and a draft measurement plan in which every instrument answers a named decision.",
    milestone: "Tutorial checkpoint 5 of 10 (2 %) due 5 pm Friday. This is the week Assignment 1 is assembled.",
  },
  {
    week: 7,
    topic: "Water sourcing and the specialist handover",
    summary:
      "What a roof delivers month by month — and the week the measured year comes back.",
    stage: "handover",
    lead: "S2",
    leadRole: "hurts",
    brief:
      "Two things happen this week. Assignment 1 is submitted — the measurement programme you have " +
      "been assembling since week 1 — and then the story jumps twelve fictional months. The " +
      "specialist team hands back Release B: the analysed findings of a measurement year at your " +
      "home, identical for every student who took that home, whatever their programme said. From " +
      "here your figures are findings rather than estimates. The teaching content is water supply: " +
      "the enHealth runoff formula applied month by month, a capped bore where the home has one, " +
      "and the supply curve every later water decision is built on. Alice Springs leads, because it " +
      "is the hardest site there is for a roof. Annual totals are how people end up with a tank " +
      "that runs dry in September.",
    output:
      "A monthly supply curve laid over week 2's demand curve, on the same axis and in the same units.",
    milestone:
      "Assignment 1, the year-long measurement programme (20 %), is due 5 pm Friday. The specialist findings are handed over in the lecture on the Monday, as a preview of what the measured year produced; the deadline is not moved by it.",
  },
  {
    week: 8,
    topic: "Treatment, reuse and service requirements",
    summary:
      "What each barrier removes, expressed as a number somebody else could check.",
    stage: "design",
    lead: "S3",
    leadRole: "hurts",
    brief:
      "Roof water is not clean, and “filtered” is not an answer. This week builds a multi-barrier " +
      "treatment train in which every barrier carries a log reduction by pathogen class, sourced, " +
      "with laboratory and field performance kept apart. Running it costs energy, so the train's " +
      "continuous and intermittent loads are separated and totalled against the daily cap. This is " +
      "also where reuse acquires its service requirements: which end uses each water quality may " +
      "serve, and what a builder would have to demonstrate before the household drank any of it. " +
      "Brisbane leads. Now that Release B is in hand, the water quality you design against is the " +
      "one the measurement year found at your home rather than a generic assumption — which is " +
      "usually where a first treatment train stops being adequate.",
    output:
      "A barrier sequence with a sourced log reduction on each barrier and its running energy costed.",
    milestone: "Quiz 3 (8 %), on weeks 6–8.",
  },
  {
    week: 9,
    topic: "Storage and seasonal reliability",
    summary:
      "What size store, what it costs, and the month it still runs dry.",
    stage: "design",
    lead: "S5",
    leadRole: "hurts",
    brief:
      "You have a supply curve and a demand curve; storage is what turns one into the other. The " +
      "method is a monthly balance run with a spin-up, so the starting volume stops mattering, " +
      "reporting the month the tank is emptiest, the volume imported and the volume overflowed. The " +
      "point of the week is the saturation: past some volume more storage buys almost nothing, and " +
      "finding that knee is the difference between a design and a shopping list. Then you break it. " +
      "The same model is re-run against the synthetic dry year and you name what fails first. Darwin " +
      "leads, because it is where the annual balance lies most confidently. One measured year, even " +
      "a real one, does not establish drought reliability, and the dry-year dataset is labelled " +
      "synthetic wherever it appears.",
    output:
      "A sized store with its saturation point identified, re-run against the dry year with the first failure named.",
    milestone: "Tutorial checkpoint 8 of 10 (2 %) due 5 pm Friday.",
  },
  {
    week: 10,
    topic: "Waste recovery and integrated balances",
    summary:
      "Where every organic stream goes, and whether the balance closes when you add it up.",
    stage: "design",
    lead: "S2",
    leadRole: "helps",
    brief:
      "Every stream goes somewhere. Household food waste, spent mushroom substrate, fish sludge, " +
      "and the meat and dairy that weeks 4 and 5 sent away unprocessed each need a named " +
      "destination and a mass in dry matter — and the balance has to close, with any loss stated as " +
      "an assumption rather than left as a residual. A compost design states the pasteurisation " +
      "target it is designed against and whose standard that is. Biogas is recorded and not " +
      "credited; only the digestate's nutrients count toward anything. Alice Springs leads, because " +
      "it is the site where the heat does most of the work for you. This is the first week where " +
      "the subsystems stop being separate: an arrow drawn wrongly in week 3 shows up here as a " +
      "balance that will not close.",
    output:
      "A closed dry-matter balance in which every organic stream has a destination and every loss term is stated.",
    milestone: "Quiz 4 (8 %), on weeks 9–10.",
  },
  {
    week: 11,
    topic: "Sanitation, nutrient limits and choosing between options",
    summary:
      "The nitrogen the garden cannot absorb, and how to choose between the alternatives.",
    stage: "design",
    lead: "S1",
    leadRole: "hurts",
    brief:
      "The household excretes far more nitrogen each year than its garden can take up, and that gap " +
      "is the constraint that caps every site. You size excreta and greywater systems against your " +
      "home's storage band, build an uptake-limited nitrogen balance, and find a destination for " +
      "the surplus. Where the course's design rule is stricter than the law in your client's " +
      "jurisdiction the page says so and says why — and you cite your own jurisdiction's actual " +
      "greywater instrument rather than the course's rule. Canberra leads, and pays for being cold. " +
      "The second half of the week is the comparison itself: the existing condition against three " +
      "alternatives in one grid, dominated options marked, and the cheapest arrangement that meets " +
      "the client's targets identified before anything dearer is argued for.",
    output:
      "A nitrogen balance with a destination for the surplus, and an options grid with the dominated options marked.",
    milestone: "Week 11's material is examinable in quiz 5, which is sat in week 12.",
  },
  {
    week: 12,
    topic: "Integration and the investment recommendation",
    summary:
      "Putting eleven sized subsystems into one model and finding out which gives way first.",
    stage: "design",
    lead: null,
    brief:
      "Eleven weeks have each produced a sized subsystem, and each one assumed it had first call on " +
      "water, area and the daily energy allowance. This week puts them in one model, runs the year, " +
      "and finds out which gives way first — because almost every design fails somewhere the " +
      "student did not expect. You run the five whole-system checks, price the full bill of " +
      "materials from the published schedule with its contingency, and compare the answer across " +
      "the five homes. Then you write the recommendation: what you would build, what it costs to " +
      "run, what the extra money buys over the cheapest option that meets the targets, and the " +
      "failure you could not design away. Naming that last one is most of what separates an " +
      "engineering proposal from a brochure.",
    output:
      "A whole-system model that passes both hard constraints, plus the capstone skeleton and an uncertainty list.",
    milestone:
      "Quiz 5 (4 %), on weeks 11–12. Assignment 2, the household resilience investment proposal (40 %), falls in the assessment period. Week 12’s tutorial is ungraded assembly.",
  },
];

const BY_WEEK = new Map(ENTRIES.map((entry) => [entry.week, entry]));

if (BY_WEEK.size !== weekNumbers.length) {
  throw new Error(
    `weeks.ts describes ${BY_WEEK.size} weeks; the calendar has ${weekNumbers.length}`,
  );
}

export const courseWeeks: WeekEntry[] = ENTRIES;

export function weekEntry(week: number): WeekEntry {
  const entry = BY_WEEK.get(week);
  if (!entry) throw new Error(`no week ${week}`);
  return entry;
}

/** Weeks 2 to 11 carry a graded tutorial completion checkpoint. Weeks 1 and 12
 *  are ungraded practice: week 1 has nothing to build on yet, and week 12's
 *  session is assembly for A2 rather than a piece of its own. */
export const CHECKPOINT_WEEKS: number[] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
export const CHECKPOINT_WEIGHT = 2;

/** True when this week's tutorial output is a graded checkpoint. */
export const isCheckpointWeek = (week: number): boolean => CHECKPOINT_WEEKS.includes(week);

/** The two-digit slug the lectures, tutorials and week overviews all share. */
export const weekSlug = (week: number): string => String(week).padStart(2, "0");

export const lectureHref = (week: number): string => `/lectures/week-${weekSlug(week)}/`;
export const tutorialHref = (week: number): string => `/sessions/week-${weekSlug(week)}/`;
export const weekHref = (week: number): string => `/weeks/week-${weekSlug(week)}/`;
