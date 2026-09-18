import { defineSiteConfig } from "astro-theme-university/types";
import { slopBranding } from "astro-theme-slop";
import { courseMeta } from "./course-config";

// Teaching sessions are design studios: students arrive with a sized system and
// leave with it changed. The collection and URL stay `sessions`.
export const sessionLabels = {
  singular: "Studio",
  plural: "Studios",
} as const;

export const graphCollections = ["sessions", "assessments", "lectures", "people"];

export const courseApiCollections = [
  ...graphCollections.map((key) => ({ key })),
  { key: "policies", dir: "pages/policies" },
];

export const siteConfig = defineSiteConfig({
  ...slopBranding,
  name: "Slop University",

  links: [
    { text: "Lectures", href: "/lectures/" },
    { text: sessionLabels.plural, href: "/sessions/" },
    { text: "Assessment", href: "/assessments/" },
    { text: "Sites", href: "/sites/" },
    { text: "Method", href: "/method/" },
    { text: "People", href: "/people/" },
    { text: "Policies", href: "/policies/" },
  ],

  licence: "CC-BY-NC-SA-4.0",
  // An image-free treatment: every figure on this site is a diagram drawn in the
  // page, from the same data the model produced. A photograph would be either
  // stock or invented, and neither belongs beside a costed design.
  socialImage: "/src/assets/images/card.png",
  socialImageAlt: `${courseMeta.code}: a closed-loop diagram of a household's food, water and waste streams, in the Slop palette`,
});
