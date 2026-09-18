import type { CourseMetaInput } from "astro-course-university";
import { z } from "astro/zod";

// The level digits ANU uses: 1000--4000 undergraduate, 6000 and 8000
// postgraduate. Both the code pattern and the level field derive from this.
const LEVELS = [1, 2, 3, 4, 6, 8] as const;
const allowedCode = new RegExp(`^SLOP[${LEVELS.join("")}]\\d{3}$`);

export const slopCourseMetaSchema = z
  .strictObject({
    code: z.string().regex(allowedCode, {
      message: "use SLOP plus a 1000–4000, 6000 or 8000 level code",
    }),
    title: z.string().trim().min(1).max(100),
    session: z.string().trim().min(1).max(40),
    year: z.number().int().min(2026).max(2200),
    level: z.literal(LEVELS),
    startDate: z.iso.date(),
    endDate: z.iso.date(),
    description: z.string().trim().min(80).max(300),
    tags: z.array(z.string().trim().min(2).max(24)).min(1).max(3),
  })
  .superRefine((course, ctx) => {
    const codeLevel = Number(course.code.at(4));
    if (course.level !== codeLevel) {
      ctx.addIssue({
        code: "custom",
        path: ["level"],
        message: `must match ${course.code}'s first digit (${codeLevel})`,
      });
    }
    if (course.startDate > course.endDate) {
      ctx.addIssue({
        code: "custom",
        path: ["startDate"],
        message: "must not be after endDate",
      });
    }
  });

// The single source of truth for the course record. The generated homepage,
// navigation label and /api/index.json all read this object.
//
// Dates: teaching runs 22 February to 28 May 2027 (twelve weeks, with a
// two-week mid-semester break from 29 March). `endDate` runs to 18 June
// because the capstone falls in the assessment period, and the course record's
// range has to contain every dated thing the course owns. `src/lib/calendar.ts`
// derives every week's dates from `startDate` so no page carries a typed date.
export const courseMeta = slopCourseMetaSchema.parse({
  code: "SLOP4761",
  title: "Designing the Closed-Loop Household I: Food, Water and Waste",
  session: "Semester 1",
  year: 2027,
  level: 4,
  startDate: "2027-02-22",
  endDate: "2027-06-18",
  description:
    "A household is not self-sufficient because it produces everything. It is " +
    "self-sufficient when the output of one system is the input to another. Twelve " +
    "weeks measuring how much of a food, water and waste loop one plot can honestly " +
    "close, on a fixed budget and energy allowance.",
  tags: ["closed-loop design", "water and sanitation", "food systems"],
}) satisfies CourseMetaInput;

/** The proposed sequel. Part I stops at the boundary of energy and shelter, and
 *  several pages need to say so in the same words, so the reference lives here.
 *  It is a proposal, not a catalogue entry: there is no page to link to. */
export const sequel = {
  code: "SLOP4762",
  title: "Designing the Closed-Loop Household II: Energy and Shelter",
  status: "proposed follow-on course",
  adds: "energy physics and introductory thermodynamics to the prerequisites",
} as const;

/** The prerequisites, worded identically wherever they appear. */
export const prerequisites = [
  "Introductory microbiology",
  "Soil science or plant biology",
  "Introductory chemistry",
  "An introductory environmental course",
  "Engineering design principles",
  "Some CAD and modelling experience",
] as const;
