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

