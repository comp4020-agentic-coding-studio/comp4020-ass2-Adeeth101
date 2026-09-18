import { courseMeta } from "../course-config";

/** Teaching weeks 1–12 derive from the course record's start date, so a date is
 *  never typed twice. Week 1 begins on `courseMeta.startDate`; a two-week
 *  mid-semester break falls after week 5, which is why week 6 is not simply
 *  five weeks on. */
export const BREAK_AFTER_WEEK = 5;
export const BREAK_WEEKS = 2;
export const TEACHING_WEEKS = 12;

const DAY = 86_400_000;

function mondayOf(week: number): Date {
  const start = new Date(`${courseMeta.startDate}T00:00:00Z`);
  const skipped = week > BREAK_AFTER_WEEK ? BREAK_WEEKS : 0;
  return new Date(start.getTime() + (week - 1 + skipped) * 7 * DAY);
}

const iso = (d: Date): string => d.toISOString().slice(0, 10);

/** Monday of a teaching week: when that week's lecture runs. */
export const lectureDate = (week: number): string => iso(mondayOf(week));

/** Thursday of a teaching week: when that week's studio runs. */
export const studioDate = (week: number): string =>
  iso(new Date(mondayOf(week).getTime() + 3 * DAY));

/** Friday of a teaching week, used for work due at the end of a week. */
export const fridayOf = (week: number): string =>
  iso(new Date(mondayOf(week).getTime() + 4 * DAY));

/** The mid-semester break, as an inclusive pair of dates. */
export const midSemesterBreak = {
  from: iso(new Date(mondayOf(BREAK_AFTER_WEEK).getTime() + 7 * DAY)),
  to: iso(new Date(mondayOf(BREAK_AFTER_WEEK).getTime() + (7 * BREAK_WEEKS + 6) * DAY)),
};

/** Teaching ends on the Friday of week 12; the course record runs past it to
 *  contain the assessment period, where the capstone falls. */
export const teachingEnds = fridayOf(TEACHING_WEEKS);
export const assessmentPeriodEnds = courseMeta.endDate;

export const weeks = Array.from({ length: TEACHING_WEEKS }, (_, i) => i + 1);
