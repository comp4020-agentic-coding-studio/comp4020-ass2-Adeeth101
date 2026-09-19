import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import climate from "../research/model/data/climate_stations.json";
import datasets from "../src/data/datasets.json";
import { generateAll, SITE_KEYS } from "../src/lib/dataset-generator";

// The Datasets page regenerates the published files in the browser. That promise
// only holds if the port writes exactly what research/model/make_datasets.py wrote.
const sites = SITE_KEYS.map((s) => ({
  ...s,
  rain: (climate.stations as Record<string, { rain: number[] }>)[s.station].rain,
}));
const published = (name: string) =>
  readFileSync(resolve("public/data", name), "utf8").replace(/\r\n/g, "\n");

describe("in-browser dataset generator", () => {
  const { dry, files } = generateAll(sites);

  it("reproduces every published CSV byte for byte with the default seeds", () => {
    expect(files).toHaveLength(6);
    for (const file of files) {
      expect(file.text.replace(/\r\n/g, "\n"), file.name).toBe(published(file.name));
    }
  });

  it("reproduces the dry-year summary the page renders", () => {
    for (const d of dry) {
      const want = datasets.drought_years.sites[d.sid as keyof typeof datasets.drought_years.sites];
      expect(d.dry_year_mm).toEqual(want.dry_year_mm);
      expect([d.mean_annual_mm, d.dry_annual_mm, d.share_of_mean]).toEqual([
        want.mean_annual_mm,
        want.dry_annual_mm,
        want.share_of_mean,
      ]);
    }
  });

  it("gives a different, still labelled, set for a different seed", () => {
    const other = generateAll(sites, 1, 2).files;
    expect(other.map((f) => f.text)).not.toEqual(files.map((f) => f.text));
    for (const file of other) expect(file.text.startsWith('"# SYNTHETIC DATA') || file.text.startsWith("# SYNTHETIC DATA")).toBe(true);
  });
});
