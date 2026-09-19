import { defineSiteConfig } from "astro-theme-university/types";
import { slopBranding } from "astro-theme-slop";
import { courseMeta } from "./course-config";

// Teaching sessions are tutorials: students arrive with their home's numbers and
// leave with the next piece of an assignment. The collection and URL stay `sessions`.
export const sessionLabels = {
  singular: "Tutorial",
  plural: "Tutorials",
} as const;

export const graphCollections = ["sessions", "assessments", "lectures", "people"];

export const courseApiCollections = [
  ...graphCollections.map((key) => ({ key })),
  { key: "policies", dir: "pages/policies" },
];

export const siteConfig = defineSiteConfig({
  ...slopBranding,
  name: "Slop University",

  // Three groups, in this order. `GroupedNav.astro` keeps these links in
  // semantic labelled groups at desktop and mobile widths.
  links: [
    // Weekly study
    { text: "Weeks", href: "/weeks/" },
    { text: "Lectures", href: "/lectures/" },
    { text: sessionLabels.plural, href: "/tutorials/" },
    { text: "Assessments", href: "/assessments/" },
    // Course reference
    { text: "Clients", href: "/clients/" },
    { text: "Programme & method", href: "/method/" },
    // People & policies
    { text: "People", href: "/people/" },
    { text: "Policies", href: "/policies/" },
  ],

  licence: "CC-BY-NC-SA-4.0",
  // The social card remains the course's data-derived loop diagram. Supplied
  // conceptual artwork appears in the site itself and is labelled as such.
  socialImage: "/src/assets/images/card.png",
  socialImageAlt: `${courseMeta.code}: a closed-loop diagram of a household's food, water and waste streams, in the Slop palette`,
});
