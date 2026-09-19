/** The semester planner's data: the same numbers behind both views, and behind
 *  the expected-effort line on each week overview.
 *
 *  Dates come from `calendar.ts` and weights from the assessment collection, so
 *  nothing here is a second copy of either. What is here is the course's
 *  **planning assumption** about effort — an illustrative guide, not observed
 *  student data and not a contact-hour requirement. */

import { TEACHING_WEEKS, fridayOf, lectureDate, studioDateOrFallback } from "./calendar";
import { CHECKPOINT_WEEKS, courseWeeks } from "./weeks";

export type EffortKey = "lecture" | "tutorial" | "prep" | "a1" | "a2";

export interface EffortCategory {
  key: EffortKey;
  label: string;
  /** What the hours actually cover, for the accessible table and the tooltip. */
  note: string;
}

export const EFFORT_CATEGORIES: EffortCategory[] = [
  { key: "lecture", label: "Lecture and notes", note: "The lecture, its slides, and reading the week's notes afterwards" },
  { key: "tutorial", label: "Tutorial", note: "The session itself. Tidying and submitting the checkpoint is inside this, not extra" },
  { key: "prep", label: "Preparation and quiz", note: "Preparing for the tutorial. In a quiz week, sitting the quiz is inside this, not extra" },
  { key: "a1", label: "Assignment 1", note: "The measurement programme, built a few hours a week from week 1" },
  { key: "a2", label: "Assignment 2", note: "The investment proposal, built from week 7's handover onwards" },
];

export interface WeekEffort {
  week: number;
  hours: Record<EffortKey, number>;
  total: number;
  /** The concrete assignment milestone this week's assignment hours go into. */
  milestone: string;
}

/** The course planning assumption. Every teaching week carries 2 h lecture and
 *  notes, 2 h tutorial and 1 h preparation; the assignment hours bring each week
 *  to 8. Tutorial submission time sits inside the tutorial's 2 h and quiz time
 *  inside the 1 h of preparation — neither is counted twice. */
const BASE = { lecture: 2, tutorial: 2, prep: 1 } as const;

const A1_MILESTONES: Record<number, string> = {
  1: "Client chosen, evidence workbook built, decision inventory started",
  2: "Irrigation demand curve, and the first unknowns written as decisions",
  3: "Substrate balance, and what would have to be measured to trust it",
  4: "Waste-stream rows added to the register",
  5: "Biological operating conditions added as measurement rows",
  6: "QA, safety and access; the register costed against the allowance",
  7: "Both cross-checks, final costing, submission",
};

const A2_MILESTONES: Record<number, string> = {
  7: "Findings read; the baseline written down",
  8: "Treatment and reuse; service requirements for each end use",
  9: "Storage sized, saturation found, dry year run",
  10: "Waste balance closed; recovery options costed",
  11: "Three options built and compared; dominated ones struck out",
  12: "Recommendation drafted, uncertainty listed, skeleton assembled",
};

function hoursFor(week: number): Record<EffortKey, number> {
  const h: Record<EffortKey, number> = { ...BASE, a1: 0, a2: 0 };
  if (week <= 6) h.a1 = 3;
  else if (week === 7) {
    h.a1 = 2;
    h.a2 = 1;
  } else h.a2 = 3;
  return h;
}

export const weekEffort: WeekEffort[] = Array.from({ length: TEACHING_WEEKS }, (_, i) => {
  const week = i + 1;
  const hours = hoursFor(week);
  const total = Object.values(hours).reduce((a, b) => a + b, 0);
  const milestone = week <= 6 ? A1_MILESTONES[week] : A2_MILESTONES[week];
  return { week, hours, total, milestone: milestone ?? "" };
});

/** The assessment period allowance: a single block, not a weekly bar. */
export const ASSESSMENT_PERIOD_HOURS = 4;
export const ASSESSMENT_PERIOD_NOTE =
  "A separate allowance for final review, drawing and submission after teaching ends — one block of four hours, not four hours a week.";

export const TEACHING_TOTAL = weekEffort.reduce((sum, w) => sum + w.total, 0);
export const GRAND_TOTAL = TEACHING_TOTAL + ASSESSMENT_PERIOD_HOURS;

export const BREAK_NOTE =
  "No compulsory work in the mid-semester break. Catching up there is optional and sits outside these totals.";

export const EFFORT_CAVEAT =
  "An illustrative planning guide, not observed student data, not required attendance and not a guarantee. It is drawn to encourage steady weekly work rather than a fortnight of panic.";

/** Marker rows for the deadlines view. One row per kind of thing. */
export type MarkerKind = "overview" | "lecture" | "tutorial" | "quiz" | "assignment";

export interface Marker {
  kind: MarkerKind;
  week: number;
  label: string;
  detail: string;
  href: string;
  /** ISO date the marker sits on. */
  date: string;
}

export const MARKER_ROWS: { kind: MarkerKind; label: string }[] = [
  { kind: "overview", label: "Week overview" },
  { kind: "lecture", label: "Lecture and slides" },
  { kind: "tutorial", label: "Tutorial" },
  { kind: "quiz", label: "Quiz" },
  { kind: "assignment", label: "Assignment deadline" },
];

/** Built here rather than in the component so the spec can check the dates and
 *  the sums without rendering anything. */
export function buildMarkers(
  assessments: { id: string; week: number; weight: number; title: string; due: Date }[],
): Marker[] {
  const markers: Marker[] = [];
  const pad = (w: number) => String(w).padStart(2, "0");

  for (const entry of courseWeeks) {
    const w = entry.week;
    markers.push({
      kind: "overview",
      week: w,
      label: `Week ${w}`,
      detail: entry.topic,
      href: `/weeks/week-${pad(w)}/`,
      date: lectureDate(w),
    });
    markers.push({
      kind: "lecture",
      week: w,
      label: `Lecture ${w}`,
      detail: `${entry.topic} — with slides`,
      href: `/lectures/week-${pad(w)}/`,
      date: lectureDate(w),
    });
    markers.push({
      kind: "tutorial",
      week: w,
      label: `Tutorial ${w}`,
      detail: CHECKPOINT_WEEKS.includes(w)
        ? `Checkpoint ${CHECKPOINT_WEEKS.indexOf(w) + 1} of 10, 2 % — due 5 pm Friday`
        : "Ungraded practice",
      href: `/sessions/week-${pad(w)}/`,
      date: studioDateOrFallback(w),
    });
  }

  for (const a of assessments) {
    const isQuiz = a.id.startsWith("quiz-");
    const isCheckpoints = a.id === "tutorial-checkpoints";
    if (isCheckpoints) continue; // checkpoints show on the tutorial row, not as a fifth record
    markers.push({
      kind: isQuiz ? "quiz" : "assignment",
      week: a.week,
      label: isQuiz ? a.title.split(":")[0] : a.title,
      detail: `${a.weight} % — ${a.due.toISOString().slice(0, 10)}`,
      href: `/assessments/${a.id}/`,
      // A quiz is sat in its tutorial; an assignment sits on its own due date,
      // which for A2 is in the assessment period rather than in week 12.
      date: isQuiz ? studioDateOrFallback(a.week) : a.due.toISOString().slice(0, 10),
    });
  }
  return markers;
}

export { fridayOf };
