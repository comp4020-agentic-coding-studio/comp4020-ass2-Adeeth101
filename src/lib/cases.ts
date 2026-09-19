import homesData from "../data/homes.json";
import releaseB from "../data/release-b.json";
import design from "../data/design.json";
import practice from "../data/practice.json";
import measurement from "../data/measurement.json";

export type Home = (typeof homesData)["homes"][number];
export type Findings = (typeof releaseB)["homes"]["S1"];

/** The five fixed client homes, in the order the course always lists them. */
export const homes: Home[] = homesData.homes;
export const findings = releaseB as typeof releaseB & { homes: Record<string, Findings> };
export { design, practice, measurement };

export function homeById(id: string): Home {
  const h = homes.find((x) => x.id === id);
  if (!h) throw new Error(`no client home ${id}`);
  return h;
}

export function homeByShort(short: string): Home {
  const h = homes.find((x) => x.short === short);
  if (!h) throw new Error(`no client home called ${short}`);
  return h;
}

export const findingsFor = (id: string): Findings => findings.homes[id as keyof typeof findings.homes] as Findings;

export const money = (v: number): string => `$${Math.round(v).toLocaleString("en-AU")}`;
export const kl = (v: number, dp = 1): string => `${v.toLocaleString("en-AU", { maximumFractionDigits: dp, minimumFractionDigits: 0 })} kL`;
export const m2 = (v: number, dp = 0): string => `${v.toLocaleString("en-AU", { maximumFractionDigits: dp })} m²`;

export const STATUS_LABEL: Record<string, string> = {
  known: "known",
  estimate: "estimate",
  unknown: "to be measured",
};

/** Month labels in calendar order. */
export const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
