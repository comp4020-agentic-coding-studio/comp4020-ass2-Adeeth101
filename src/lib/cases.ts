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

/** Which home leads which week. Weeks 1 and 12 work with all five. */
export const LEAD_HOMES: Record<number, string | null> = {
  1: null,
  2: "S1",
  3: "S2",
  4: "S3",
  5: "S4",
  6: "S5",
  7: "S1",
  8: "S2",
  9: "S3",
  10: "S4",
  11: "S5",
  12: null,
};

/** The twelve topics, measurement first, design second. */
export const TOPICS: Record<number, string> = {
  1: "Client commission and intake",
  2: "Site survey, requirements and mass balances",
  3: "Water monitoring",
  4: "Soil, microclimate and crop demand",
  5: "Food, waste and nutrient audits",
  6: "Sampling, sensors, calibration and handover",
  7: "Specialist findings and uncertainty",
  8: "Water-system sizing",
  9: "Food-system selection",
  10: "Waste, sanitation and integrated balances",
  11: "Alternatives, optimisation and resilience",
  12: "Investment proposal and design review",
};

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
