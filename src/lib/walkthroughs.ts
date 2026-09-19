/** Step data for the four page walkthroughs.
 *
 *  Each step names a real section of the page it runs on, by the id that section
 *  already carries. The component scrolls to it and highlights it, so a step
 *  that names a missing id is a broken walkthrough rather than a silent one —
 *  the spec checks every target resolves in the built page. */

export interface WalkthroughStep {
  title: string;
  body: string;
  /** The id of the real section this step is about. */
  target: string;
  /** The link text shown on the "take me there" control. */
  targetLabel: string;
}

export interface Walkthrough {
  id: string;
  label: string;
  intro: string;
  steps: WalkthroughStep[];
}

export const WALKTHROUGHS: Record<string, Walkthrough> = {
  home: {
    id: "home",
    label: "Take the site tour",
    intro: "Five steps, about a minute. It explains how this site is arranged and where to start.",
    steps: [
      {
        title: "The setting is invented. The engineering is not.",
        body:
          "You advise a fictional household applying to a fictional government loan programme. " +
          "The government is imaginary; the climates, water balances, soils, pumps and prices are " +
          "real, and your water balance still has to add up.",
        target: "orientation",
        targetLabel: "the three questions",
      },
      {
        title: "The site has three groups",
        body:
          "Weekly study is what you do each week. Course reference is material you come back to " +
          "all semester. People and policies is the admin. The top navigation is grouped the same " +
          "way, and so is the menu on a phone.",
        target: "three-groups",
        targetLabel: "the groups",
      },
      {
        title: "Four things are assessed",
        body:
          "Ten small tutorial checkpoints, five short quizzes, a measurement programme in week 7 " +
          "and an investment proposal in the assessment period. Half the marks are for the weekly " +
          "work the assignments are assembled from.",
        target: "what-you-submit",
        targetLabel: "what you submit",
      },
      {
        title: "The planner has two views",
        body:
          "Deadlines and materials shows what exists and when it is due. Suggested weekly effort " +
          "shows roughly how the hours fall, so you can spread the work rather than meet it all at " +
          "a deadline. Both are on this page and on the weekly map.",
        target: "planner",
        targetLabel: "the planner",
      },
      {
        title: "Start at week 1",
        body:
          "Choose a client home, build the evidence workbook, and fill one row properly. Every " +
          "week after it writes into that file.",
        target: "start-here",
        targetLabel: "week 1",
      },
    ],
  },

  weeks: {
    id: "weeks",
    label: "How to use this page",
    intro: "Four steps. How a teaching week is put together, and what to carry between them.",
    steps: [
      {
        title: "Choose the week you are in",
        body:
          "Twelve weeks, each with its own overview page. The overview says what the week asks and " +
          "what you should be holding when it ends — read that before the lecture.",
        target: "week-by-week",
        targetLabel: "the week list",
      },
      {
        title: "Each week has the same four pieces",
        body:
          "An overview, a lecture with slides, a tutorial, and sometimes a quiz. Every page in a " +
          "week carries the same row of links at the top, so you can move between them without " +
          "coming back here.",
        target: "week-by-week",
        targetLabel: "any week",
      },
      {
        title: "Deadlines are not the same as workload",
        body:
          "The planner's first view shows when things are due. Its second view shows where the " +
          "hours actually fall, which is earlier than the deadlines suggest — the assignments are " +
          "built a few hours a week from week 1, not written at the end.",
        target: "planner",
        targetLabel: "the planner",
      },
      {
        title: "Carry your output forward",
        body:
          "Every tutorial names what it produces and where that output is used again. The chain " +
          "runs from week 1's workbook through to the proposal, so a week skipped is a gap rather " +
          "than a set of notes to catch up on.",
        target: "stages",
        targetLabel: "the three stages",
      },
    ],
  },

  clients: {
    id: "clients",
    label: "How to use this page",
    intro: "Five steps. How to read a client home and what to take from it.",
    steps: [
      {
        title: "Choose one home, once",
        body:
          "Five existing homes in five Australian climates. There is no sixth option and no custom " +
          "site. You keep the same client all semester, because the comparison between homes is " +
          "part of what the course teaches.",
        target: "the-homes",
        targetLabel: "the five homes",
      },
      {
        title: "Read the plan to scale",
        body:
          "Each home's page carries a scaled site plan and floor plan with a north arrow and a " +
          "scale bar. Roof plan area, connected roof area and footprint are three different " +
          "numbers — a design that confuses them is wrong by a large factor.",
        target: "the-homes",
        targetLabel: "a home",
      },
      {
        title: "Tell a fact from an assumption",
        body:
          "Every dossier fact is tagged known, estimate or still to be measured. Copy those tags " +
          "into your workbook and do not promote them. The unknowns are the seed of Assignment 1.",
        target: "comparison",
        targetLabel: "the comparison",
      },
      {
        title: "Two releases per home",
        body:
          "Release A is the week 1 intake dossier: the property, the inventory, the constraints " +
          "and the client's own targets. Release B is the specialist findings handed over in " +
          "week 7, with the measured year as CSV. Both are linked from each home's page.",
        target: "the-homes",
        targetLabel: "a home",
      },
      {
        title: "Their priorities, not yours",
        body:
          "Each household states what it actually wants. The retrofit you recommend has to meet " +
          "those targets, not the ones that would score well.",
        target: "comparison",
        targetLabel: "the comparison",
      },
    ],
  },

  method: {
    id: "method",
    label: "How to use this page",
    intro: "Four steps. What the scenario is, and where the reference material lives.",
    steps: [
      {
        title: "Read the scenario first",
        body:
          "A fictional loan programme, a fictional consultancy, a real client brief. It gives the " +
          "engineering a client, a deadline and a budget — and it is the reason your proposal has " +
          "to argue for its cost rather than just state it.",
        target: "the-scenario",
        targetLabel: "the scenario",
      },
      {
        title: "Measurement, then design",
        body:
          "Weeks 1 to 6 work out what you would need to know and produce a measurement programme. " +
          "Weeks 8 to 12 use the supplied findings to choose and justify a retrofit. Knowing which " +
          "phase you are in tells you whether a number is an estimate or a finding.",
        target: "two-phases",
        targetLabel: "the two phases",
      },
      {
        title: "Definitions, bands and their limits",
        body:
          "Five capped indicators with published definitions, and per-site bands built from three " +
          "constructed designs. A band is evidence inside a marking criterion. It is never a grade, " +
          "and the page publishes the sensitivity testing with its limits.",
        target: "reference-bands",
        targetLabel: "the bands",
      },
      {
        title: "Costs, datasets and a worked example",
        body:
          "The price schedule is the only place a design may be costed from. The datasets page " +
          "holds the synthetic data and says what it is not. The worked comparison takes one design " +
          "idea through all five sites — read it before you build your own options grid.",
        target: "contents",
        targetLabel: "the contents list",
      },
    ],
  },
};

export const walkthrough = (id: string): Walkthrough => {
  const w = WALKTHROUGHS[id];
  if (!w) throw new Error(`no walkthrough ${id}`);
  return w;
};
