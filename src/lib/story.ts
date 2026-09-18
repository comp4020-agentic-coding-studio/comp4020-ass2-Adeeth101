/** The narrative threads of the consultancy case. Brief, functional, and
 *  fictional: they give each home a client to answer to. Numbers never live
 *  here; they come from the generated data files. */

export const INTAKE: Record<string, { date: string; note: string[] }> = {
  S1: {
    date: "22 February 2027",
    note: [
      "Alex Taylor rang the programme's referral line after a summer in which the garden was watered from the mains every evening. Both parents work weekdays; the children are 9 and 12 and use the back lawn every afternoon.",
      "They want the fruit trees and raised beds kept going through summer without mains water, and anything installed to keep working through a Canberra July. Morgan's condition for signing: nothing that needs checking on a weeknight.",
    ],
  },
  S2: {
    date: "23 February 2027",
    note: [
      "Linh Nguyen has kept the block's pumps and lines running for fifteen years and works from home three days a week. The family carts water most summers and would like that to stop.",
      "David's condition is practical: if a part fails, it has to be on the shelf in town. The bore licence is metered and checked, and the family will not go over it.",
    ],
  },
  S3: {
    date: "24 February 2027",
    note: [
      "Priya and Rohan Patel bought the townhouse in 2019. The scheme's building committee has to see anything visible from common property, and a neighbour's pump was the subject of a noise complaint last year.",
      "They want food from a small space, a courtyard they can still sit in, and silence at night. They use a 40 m² plot in the shared garden and know it is not theirs.",
    ],
  },
  S4: {
    date: "25 February 2027",
    note: [
      "Elena Rossi keeps the vegetable beds and Marco keeps the household accounts. Every January the beds slump while the water bill climbs, and both of them are tired of it.",
      "Their questions at intake were about money: what it would cost to run, every year, before anything is agreed. The back lawn stays; that was the first thing they said.",
    ],
  },
  S5: {
    date: "26 February 2027",
    note: [
      "Kate and Josh Williams run a small business from home and drive south for four weeks every July. They buy water every late dry season and watch their tanks overflow every wet.",
      "They want the wet season carried into the dry, systems that look after themselves while they are away, and the overflow that scours the ground under the house sent somewhere on purpose.",
    ],
  },
};

/** What the senior reviewer asks when a proposal comes back for review. */
export const REVIEW_QUESTIONS: Record<string, string[]> = {
  S1: [
    "Which July night did you design the pump enclosure for, and where did that temperature come from?",
    "Your recommended option meets the summer target in an average year. What happens to the fruit trees in the dry year, and is the answer worth more storage?",
  ],
  S2: [
    "How much of the carting reduction comes from the roof, how much from the composting toilet, and how much from how the bore is drawn?",
    "Which component would you expect to fail first in January heat, and can it be bought in town?",
  ],
  S3: [
    "Where exactly is the pump, how loud is it at the boundary at 2 am, and what did you assume?",
    "Which of your produce figures depends on the shared-garden allocation, and what happens if the body corporate revokes it?",
  ],
  S4: [
    "State the new running cost in dollars a year, line by line. Which line would the family notice first?",
    "Is the January decline a water problem, a salinity problem or both, and does your design answer both?",
  ],
  S5: [
    "Walk me through the July absence: what runs, what is paused, and what would fail first if a pump stopped on day three?",
    "The last increment of storage takes carting from one load to zero. Is it worth what it costs?",
  ],
};
