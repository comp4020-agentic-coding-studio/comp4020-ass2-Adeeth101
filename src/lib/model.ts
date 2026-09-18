import model from "../data/course-model.json";

export type Level = "baseline" | "competent" | "excellent";
export const LEVELS: Level[] = ["baseline", "competent", "excellent"];

export type SiteRecord = (typeof model)["sites"][number];

export const courseModel = model;
export const sites = model.sites;
export const indicators = model.indicators;
export const constraints = model.constraints;
export const household = model.household;
export const schedule = model.schedule;

/** A site by its preset id (S1..S5). */
export function site(id: string): SiteRecord {
  const found = sites.find((s) => s.id === id);
  if (!found) throw new Error(`no preset site ${id}`);
  return found;
}

/** A site by the short place name used in prose ("Canberra"). */
export function siteByShort(short: string): SiteRecord {
  const found = sites.find((s) => s.short === short);
  if (!found) throw new Error(`no preset site called ${short}`);
  return found;
}

/** Percentages are a rounded *display* of the model's values. Bands are always
 *  evaluated on the unrounded number, so this must never be fed back into a
 *  threshold — see CLAUDE.md, Scoring. */
export const pct = (v: number): string =>
  v < 0.1 ? `${(v * 100).toFixed(1)} %` : `${Math.round(v * 100)} %`;

export const money = (v: number): string => `$${Math.round(v).toLocaleString("en-AU")}`;

export const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** Which site leads which week. Weeks 1 and 12 integrate all five.
 *  Each site leads once where its climate helps and once where it hurts. */
export const LEAD_SITES: Record<number, { id: string; role: "helps" | "hurts" } | null> = {
  1: null,
  2: { id: "S1", role: "helps" },
  3: { id: "S3", role: "helps" },
  4: { id: "S5", role: "helps" },
  5: { id: "S4", role: "hurts" },
  6: { id: "S4", role: "helps" },
  7: { id: "S2", role: "hurts" },
  8: { id: "S3", role: "hurts" },
  9: { id: "S5", role: "hurts" },
  10: { id: "S2", role: "helps" },
  11: { id: "S1", role: "hurts" },
  12: null,
};

/** The twelve topics, in the order one feeds the next. */
export const TOPICS: Record<number, string> = {
  1: "Loop thinking and the site sheet",
  2: "Perennial food systems and soil",
  3: "Mycology",
  4: "Insect farming",
  5: "Aquaponics",
  6: "Fermentation and cultured microbes",
  7: "Water sourcing",
  8: "Filtration and treatment",
  9: "Water security and storage",
  10: "Waste management",
  11: "Sanitation",
  12: "Integration",
};
