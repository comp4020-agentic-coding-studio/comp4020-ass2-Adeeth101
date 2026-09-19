import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { describe, expect, it } from "vitest";

/**
 * SLOP4761's own spec.
 *
 * These test the built output and the generated data, not the source — what the
 * course must still be true about after any change, not how it was written. The
 * starter's `data-integrity.test.ts` is unchanged and sits alongside.
 *
 * What is deliberately NOT here: anything that pins prose. A test that greps for a
 * safety sentence passes the moment the sentence exists and says nothing about
 * whether the claim is correct, which is worse than no test because it looks like
 * verification. The claims themselves are checked in research/verification-log.md,
 * by reading primary sources. What is testable here is structure, arithmetic, and
 * agreement between the model and what the site published from it.
 */

interface ApiNode {
  id: string;
  type: string;
  title?: string;
  description?: string;
  related?: string[];
  meta?: Record<string, unknown>;
  body?: string;
}

interface CourseApi {
  canonicalUrl: string;
  course: {
    code: string;
    title: string;
    level: number;
    year: number;
    session: string;
    startDate: string;
    endDate: string;
    description: string;
    tags: string[];
  };
  nodes: ApiNode[];
}

const api = JSON.parse(readFileSync(resolve("dist/api/index.json"), "utf8")) as CourseApi;
const model = JSON.parse(readFileSync(resolve("src/data/course-model.json"), "utf8"));
const comparison = JSON.parse(readFileSync(resolve("src/data/comparison.json"), "utf8"));
const datasets = JSON.parse(readFileSync(resolve("src/data/datasets.json"), "utf8"));
const homes = JSON.parse(readFileSync(resolve("src/data/homes.json"), "utf8"));

/** Every built HTML page, for checks that must hold site-wide. */
function htmlFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) return htmlFiles(p);
    return p.endsWith(".html") ? [p] : [];
  });
}

const nodesOf = (type: string) => api.nodes.filter((n) => n.type === type);
/** Node ids are prefixed with their collection ("lectures/week-01"), which is also
 *  the built route, so the slug needs taking off the end. */
const slug = (n: ApiNode) => n.id.split("/").at(-1)!;
const week = (n: ApiNode) => Number(n.meta?.week);
const dateOnly = (v: unknown) => String(v).slice(0, 10);

const page = (route: string): string => {
  const p = resolve("dist", route, "index.html");
  if (!existsSync(p)) throw new Error(`no built page at /${route}/`);
  return readFileSync(p, "utf8");
};
/** Rendered text with tags and entities removed, for counting facts rather than markup. */
const text = (html: string): string =>
  html
    .replace(/<script[\s\S]*?<\/script>/g, " ")
    .replace(/<style[\s\S]*?<\/style>/g, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/\s+/g, " ");

// --------------------------------------------------------------------------
describe("identity", () => {
  it("keeps the repo's allocated code digits and a level that matches them", () => {
    expect(api.course.code).toMatch(/^SLOP\d761$/);
    expect(api.course.level).toBe(Number(api.course.code.at(4)));
  });

  it("publishes a course record complete enough for the catalogue", () => {
    expect(api.course.title.length).toBeGreaterThan(20);
    expect(api.course.description.length).toBeGreaterThanOrEqual(80);
    expect(api.course.tags.length).toBeGreaterThan(0);
    expect(api.course.session).toBeTruthy();
  });

  it("does not leave the Slop identity behind", () => {
    // The brand is fixed by the platform; the course sits inside it. The lockup is
    // markup rather than body copy, so this reads the raw HTML.
    expect(page("")).toContain("Slop");
    expect(api.canonicalUrl).toContain("slop.university");
    expect(api.canonicalUrl).toContain(api.course.code);
  });
});

// --------------------------------------------------------------------------
describe("the twelve weeks", () => {
  it("runs twelve lectures and twelve studios, one of each per week", () => {
    for (const type of ["lectures", "sessions"]) {
      const weeks = nodesOf(type).map(week).sort((a, b) => a - b);
      expect(weeks, `${type} weeks`).toEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
    }
  });

  it("gives every week a distinct topic rather than a template", () => {
    // A templated course reuses titles and descriptions. Requiring both to be
    // unique across 24 entries is a cheap structural guard against that.
    for (const type of ["lectures", "sessions"]) {
      const titles = nodesOf(type).map((n) => String(n.title ?? ""));
      expect(new Set(titles).size, `${type} titles`).toBe(12);
      expect(titles.every((t) => t.length > 8), `${type} titles are substantive`).toBe(true);
      const descs = nodesOf(type).map((n) => String(n.description ?? ""));
      expect(new Set(descs).size, `${type} descriptions`).toBe(12);
    }
  });

  it("keeps teaching dates in week order, Monday lectures and Thursday studios", () => {
    for (const [type, dow] of [["lectures", 1], ["sessions", 4]] as const) {
      const byWeek = [...nodesOf(type)].sort((a, b) => week(a) - week(b));
      let previous = "";
      for (const n of byWeek) {
        const d = dateOnly(n.meta?.date);
        expect(d > previous, `${n.id} is out of order`).toBe(true);
        expect(new Date(`${d}T00:00:00Z`).getUTCDay(), `${n.id} weekday`).toBe(dow);
        previous = d;
      }
    }
  });

  it("pairs each week's lecture and studio in the same teaching week", () => {
    for (let w = 1; w <= 12; w++) {
      const l = nodesOf("lectures").find((n) => week(n) === w)!;
      const s = nodesOf("sessions").find((n) => week(n) === w)!;
      const ld = new Date(`${dateOnly(l.meta?.date)}T00:00:00Z`).getTime();
      const sd = new Date(`${dateOnly(s.meta?.date)}T00:00:00Z`).getTime();
      const days = (sd - ld) / 86_400_000;
      expect(days, `week ${w} studio sits ${days} days after its lecture`).toBe(3);
    }
  });

  it("takes a mid-semester break rather than running twelve weeks straight", () => {
    const dates = [...nodesOf("lectures")]
      .sort((a, b) => week(a) - week(b))
      .map((n) => new Date(`${dateOnly(n.meta?.date)}T00:00:00Z`).getTime());
    const gaps = dates.slice(1).map((d, i) => (d - dates[i]) / 86_400_000);
    expect(gaps.filter((g) => g === 7).length, "ordinary week-to-week gaps").toBe(10);
    expect(Math.max(...gaps), "the break").toBeGreaterThan(7);
  });
});

// --------------------------------------------------------------------------
describe("assessment", () => {
  const assessments = () => nodesOf("assessments");

  it("totals exactly 100 %", () => {
    const total = assessments().reduce((s, n) => s + Number(n.meta?.weight ?? 0), 0);
    expect(total).toBe(100);
  });

  it("runs five quizzes at 8 % in weeks 3, 5, 8, 10 and 12", () => {
    const quizzes = assessments().filter((n) => slug(n).startsWith("quiz-"));
    expect(quizzes.length).toBe(5);
    expect(quizzes.map(week).sort((a, b) => a - b)).toEqual([3, 5, 8, 10, 12]);
    for (const q of quizzes) expect(Number(q.meta?.weight), q.id).toBe(8);
  });

  it("keeps the two design assessments at 20 % in week 7 and 40 % in the assessment period", () => {
    const design = assessments().filter((n) => !slug(n).startsWith("quiz-"));
    expect(design.length).toBe(2);
    const mid = design.find((n) => Number(n.meta?.weight) === 20)!;
    const capstone = design.find((n) => Number(n.meta?.weight) === 40)!;
    expect(mid, "a 20 % mid-semester assessment").toBeTruthy();
    expect(capstone, "a 40 % capstone").toBeTruthy();
    expect(week(mid)).toBe(7);

    // The capstone falls after teaching ends but inside the course record, which is
    // what lets the starter's date-range invariant hold without being weakened.
    const lastLecture = Math.max(
      ...nodesOf("lectures").map((n) => new Date(`${dateOnly(n.meta?.date)}T00:00:00Z`).getTime()),
    );
    const due = new Date(`${dateOnly(capstone.meta?.due)}T00:00:00Z`).getTime();
    expect(due, "capstone falls after the last lecture").toBeGreaterThan(lastLecture);
    expect(dateOnly(capstone.meta?.due) <= api.course.endDate).toBe(true);
  });

  it("does not schedule a quiz in the week the mid-semester design is due", () => {
    const mid = assessments().find((n) => Number(n.meta?.weight) === 20)!;
    const quizWeeks = assessments()
      .filter((n) => slug(n).startsWith("quiz-"))
      .map(week);
    expect(quizWeeks).not.toContain(week(mid));
  });

  it("states how every assessment is marked", () => {
    for (const a of assessments()) {
      expect(a.meta?.marking, `${a.id} has no marking model`).toBeTruthy();
    }
  });

  it("gives each quiz page real questions with explanations", () => {
    for (const q of nodesOf("assessments").filter((n) => slug(n).startsWith("quiz-"))) {
      const t = text(page(q.id));
      const questions = (t.match(/Answer and reasoning/g) ?? []).length;
      expect(questions, `${q.id} practice questions`).toBeGreaterThanOrEqual(5);
      // A static site cannot mark anything, and each quiz page has to say so.
      expect(t.toLowerCase(), `${q.id} is honest about collecting answers`).toMatch(
        /does not collect|not.{0,20}stored|no server/,
      );
    }
  });
});

// --------------------------------------------------------------------------
describe("site coverage", () => {
  const SITES = ["Canberra", "Alice Springs", "Brisbane", "Adelaide", "Darwin"];
  // Each site leads twice: once where its climate helps, once where it hurts.
  const LEADS: Record<string, number[]> = {
    Canberra: [2, 11],
    Brisbane: [3, 8],
    Darwin: [4, 9],
    Adelaide: [5, 6],
    "Alice Springs": [7, 10],
  };

  it("names all five sites in every topic week's lecture", () => {
    for (let w = 2; w <= 11; w++) {
      const node = nodesOf("lectures").find((n) => week(n) === w)!;
      const t = text(page(node.id));
      for (const s of SITES) {
        expect(t, `week ${w} does not mention ${s}`).toContain(s);
      }
    }
  });

  it("gives every site exactly two lead weeks, one helping and one hurting", () => {
    const all = Object.values(LEADS).flat().sort((a, b) => a - b);
    expect(all).toEqual([2, 3, 4, 5, 6, 7, 8, 9, 10, 11]);
    for (const [site, weeks] of Object.entries(LEADS)) {
      expect(weeks.length, `${site} lead weeks`).toBe(2);
    }
  });

  it("leads each week with the site that week's worked example is about", () => {
    // The lead site should be the most-mentioned of the five on its own page.
    for (const [site, weeks] of Object.entries(LEADS)) {
      for (const w of weeks) {
        const node = nodesOf("lectures").find((n) => week(n) === w)!;
        const t = text(page(node.id));
        const count = (s: string) => (t.match(new RegExp(s, "g")) ?? []).length;
        const mine = count(site);
        for (const other of SITES.filter((s) => s !== site)) {
          expect(
            mine >= count(other),
            `week ${w} should lead with ${site} but mentions ${other} more often`,
          ).toBe(true);
        }
      }
    }
  });

});

// --------------------------------------------------------------------------
describe("five fixed client homes", () => {
  const SLUGS = ["canberra", "alice-springs", "brisbane", "adelaide", "darwin"];

  it("has exactly five homes, the five presets, and nothing else", () => {
    expect(homes.homes.map((h: any) => h.slug)).toEqual(SLUGS);
    expect(homes.homes.map((h: any) => h.id)).toEqual(model.sites.map((s: any) => s.id));
  });

  it("publishes an intake dossier for every home and lists all five on the clients page", () => {
    const index = text(page("clients"));
    for (const h of homes.homes) {
      expect(index, `${h.short} missing from the clients page`).toContain(h.short);
      const t = text(page(`clients/${h.slug}`));
      expect(t, `${h.slug} dossier`).toContain("Release A");
      expect(t.toLowerCase(), `${h.slug} fiction label`).toContain("teaching fiction");
    }
  });

  it("offers no custom site anywhere", () => {
    expect(existsSync(resolve("dist/sites/index.html")), "the old /sites/ route still exists").toBe(false);
    const OFFERS = /propose your own site|custom[- ]site (request|approval)|custom sites? (may|can|are)|approval by (the end of )?week 3/i;
    for (const f of htmlFiles("dist")) {
      expect(readFileSync(f, "utf8"), `${f} offers a custom site`).not.toMatch(OFFERS);
    }
  });

  it("draws every home to scale and keys every feature it draws", () => {
    for (const h of homes.homes) {
      const html = page(`clients/${h.slug}`);
      const t = text(html);
      // a north arrow, a scale bar and the lot dimensions on the plan
      expect(html).toMatch(/<text[^>]*>N<\/text>/);
      expect(t, `${h.slug} lot width`).toContain(`${h.plan.extent[0]} m`);
      for (const r of h.plan.cover) expect(t, `${h.slug} key lacks ${r.id}`).toContain(r.label);
      for (const z of h.plan.zones) expect(t, `${h.slug} key lacks zone ${z.id}`).toContain(z.label);
      for (const room of h.floor.rooms) expect(t, `${h.slug} floor key lacks ${room.label}`).toContain(room.label);
    }
  });

  it("reconciles every plan with its case parameters", () => {
    for (const h of homes.homes) {
      const a = h.areas;
      const tol = (x: number, y: number) => Math.max(a.tolerance_abs_m2, a.tolerance_rel * Math.max(x, y));
      expect(Math.abs(a.roof_plan_m2 - a.preset_roof_m2), `${h.slug} roof`).toBeLessThanOrEqual(tol(a.roof_plan_m2, a.preset_roof_m2));
      expect(Math.abs(a.roof_zone_sum_m2 - a.roof_plan_m2), `${h.slug} zones`).toBeLessThanOrEqual(tol(a.roof_zone_sum_m2, a.roof_plan_m2));
      expect(Math.abs(a.growing_envelope_m2 - a.preset_growable_m2), `${h.slug} growing`).toBeLessThanOrEqual(tol(a.growing_envelope_m2, a.preset_growable_m2));
      expect(a.roof_plan_m2, `${h.slug} roof plan is footprint plus eaves`).toBeGreaterThan(a.footprint_m2);
      expect(a.other_m2, `${h.slug} parts exceed the drawn area`).toBeGreaterThanOrEqual(0);
      if (!h.parcel) expect(a.drawn_m2, `${h.slug} suburban plan is the whole lot`).toBeCloseTo(h.parcel_m2, 0);
      expect(a.existing_storage_kl).toBe(model.sites.find((s: any) => s.id === h.id).existing_storage_kl);
    }
  });

  it("keeps everything a household owns inside its boundary", () => {
    for (const h of homes.homes) {
      const [W, H] = h.plan.extent;
      const inside = (x: number, y: number, w: number, hh: number) =>
        x >= -0.01 && y >= -0.01 && x + w <= W + 0.01 && y + hh <= H + 0.01;
      for (const r of [...h.plan.cover, ...h.plan.roofover]) expect(inside(r.x, r.y, r.w, r.h), `${h.slug} ${r.id}`).toBe(true);
      for (const c of h.plan.circles.filter((c: any) => c.kind === "tank")) {
        const [w, hh] = c.w ? [c.w, c.h] : [2 * c.r, 2 * c.r];
        expect(inside(c.cx - w / 2, c.cy - hh / 2, w, hh), `${h.slug} tank ${c.id}`).toBe(true);
      }
    }
  });

  it("never adds Brisbane's shared-garden allocation to the lot", () => {
    const b = homes.homes.find((h: any) => h.slug === "brisbane");
    expect(b.parcel_m2).toBe(300);
    expect(b.areas.shared_allocation_m2).toBe(40);
    const lot = b.scheme.lots.find((l: any) => l.n === b.scheme.patel_lot);
    expect(lot.w * lot.h).toBe(300);
    const [ax, ay, aw, ah] = b.scheme.allocation;
    const outside = ax + aw <= lot.x || ax >= lot.x + lot.w || ay + ah <= lot.y || ay >= lot.y + lot.h;
    expect(outside, "allocation inside the lot").toBe(true);
    expect(text(page("clients/brisbane")).toLowerCase()).toContain("common property");
  });

  it("tags dossier facts as known, estimated or still to be measured", () => {
    for (const h of homes.homes) {
      const statuses = new Set([h.dossier.slope, ...h.dossier.services, ...h.dossier.constraints].map((f: any) => f.status));
      expect(statuses.has("known"), `${h.slug} has no known fact`).toBe(true);
      expect(statuses.has("estimate") || statuses.has("unknown"), `${h.slug} pretends to certainty`).toBe(true);
      expect(h.dossier.unknowns.length, `${h.slug} unknowns`).toBeGreaterThanOrEqual(4);
    }
  });

  it("gives every client attainable targets the existing home does not already meet", () => {
    for (const h of homes.homes) {
      expect(h.targets.length, `${h.slug} targets`).toBeGreaterThanOrEqual(4);
      expect(Object.values(h.existing_meets).some((v) => !v), `${h.slug} is already done`).toBe(true);
      expect(h.feasibility.budget_margin_at_least, `${h.slug} budget margin`).toBeGreaterThanOrEqual(5000);
      expect(h.feasibility.energy_margin_at_least, `${h.slug} energy margin`).toBeGreaterThanOrEqual(1);
      expect(text(page(`clients/${h.slug}`))).toContain(h.feasibility.budget_margin_at_least.toLocaleString("en-AU"));
    }
  });
});

// --------------------------------------------------------------------------
describe("prerequisites and the proposed sequel", () => {
  const SEQUEL = "SLOP4762";
  const MENTIONS = ["", "lectures/week-01", "lectures/week-12"];

  it("names the sequel on the home page, week 1 and week 12", () => {
    for (const route of MENTIONS) {
      expect(text(page(route)), `${route || "home"} does not name the sequel`).toContain(SEQUEL);
    }
  });

  it("labels the sequel a proposal rather than linking it as a real course", () => {
    for (const route of MENTIONS) {
      const html = page(route);
      expect(text(html).toLowerCase(), `${route || "home"}`).toMatch(
        /proposed follow-on|proposed sequel|a proposal/,
      );
      // A proposed course has no catalogue page, so it must not be linked as one.
      expect(html, `${route || "home"} links the sequel somewhere`).not.toMatch(
        new RegExp(`<a[^>]+href="[^"]*${SEQUEL}`, "i"),
      );
    }
  });

  it("states the prerequisites on the home page, all of them", () => {
    const home = text(page(""));
    for (const p of ["Engineering design", "Mass and energy balances", "statistics and measurement", "Spreadsheet", "CAD"]) {
      expect(home, `prerequisite "${p}" missing`).toContain(p);
    }
    expect(home).toMatch(/biological[^.]*helpful|helpful[^.]*biological/i);
  });

  it("makes no land-per-person claim on the home page", () => {
    const home = text(page(""));
    expect(home).not.toMatch(/372/);
    expect(home).not.toMatch(/largest site has 500/i);
  });
});

// --------------------------------------------------------------------------
describe("bands", () => {
  const LEVELS = ["baseline", "competent", "excellent"] as const;

  it("bands five indicators at five sites", () => {
    expect(model.indicators.length).toBe(5);
    for (const s of model.sites) {
      expect(Object.keys(s.bands).sort()).toEqual(
        model.indicators.map((i: { key: string }) => i.key).sort(),
      );
    }
  });

  it("orders every band baseline ≤ competent ≤ excellent", () => {
    for (const s of model.sites) {
      for (const [key, b] of Object.entries(s.bands) as [string, Record<string, number>][]) {
        expect(b.baseline, `${s.id} ${key}`).toBeLessThanOrEqual(b.competent);
        expect(b.competent, `${s.id} ${key}`).toBeLessThanOrEqual(b.excellent);
      }
    }
  });

  it("keeps every indicator inside 0 to 100 %, because closure is capped", () => {
    for (const s of model.sites) {
      for (const [key, b] of Object.entries(s.bands) as [string, Record<string, number>][]) {
        for (const l of LEVELS) {
          expect(b[l], `${s.id} ${key} ${l}`).toBeGreaterThanOrEqual(0);
          expect(b[l], `${s.id} ${key} ${l}`).toBeLessThanOrEqual(1);
        }
      }
    }
  });

  it("uses a single reference recipe at every site", () => {
    // Per-site thresholds must come from climate and inventory, never from a
    // different yardstick being applied to different students.
    expect(Object.keys(model.recipe).sort()).toEqual([...LEVELS].sort());
    for (const l of LEVELS) expect(model.recipe[l]).toBeTruthy();
  });

  it("keeps the recipe monotone on every lever", () => {
    const numeric = ["greywater", "production", "yield_mult", "n_recovery", "aquaponic_m2", "extra_catchment", "storage_budget"];
    for (const k of numeric) {
      expect(model.recipe.baseline[k], `${k} baseline→competent`).toBeLessThanOrEqual(model.recipe.competent[k]);
      expect(model.recipe.competent[k], `${k} competent→excellent`).toBeLessThanOrEqual(model.recipe.excellent[k]);
    }
    expect(model.recipe.excellent.demand).toBeLessThanOrEqual(model.recipe.baseline.demand);
  });

  it("publishes the thresholds the model produced, not retyped numbers", () => {
    const rendered = text(page("method"));
    // The table drops the per cent sign (the caption carries it once), so the
    // published triple is "baseline / competent / excellent" as bare numbers.
    const num = (v: number) => (v < 0.1 ? (v * 100).toFixed(1) : String(Math.round(v * 100)));
    for (const s of model.sites) {
      for (const key of ["water_closure", "garden_water_satisfaction", "nutrient_closure"] as const) {
        const b = s.bands[key];
        const triple = `${num(b.baseline)} / ${num(b.competent)} / ${num(b.excellent)}`;
        expect(
          rendered.replace(/\s+/g, " "),
          `${s.id} ${key} (${triple}) is not on the method page`,
        ).toContain(triple);
      }
    }
  });

  it("gives a band no path into a mark", () => {
    // The structural form of "bands are not grades": no marking criterion may be a
    // band, and the criteria already sum to 100 without one, so there is no weight
    // left for a band to occupy.
    for (const a of nodesOf("assessments")) {
      const marking = a.meta?.marking as
        | { mode: string; criteria?: { name: string; weight: number }[] }
        | undefined;
      if (marking?.mode !== "weighted") continue;
      const criteria = marking.criteria ?? [];
      expect(criteria.reduce((sum, c) => sum + c.weight, 0), `${a.id} criteria`).toBe(100);
      for (const c of criteria) {
        expect(c.name.toLowerCase(), `${a.id} criterion "${c.name}"`).not.toContain("band");
      }
    }
  });

  it("says so in prose wherever bands are explained", () => {
    const DISCLAIMED = ["not grades", "not a grade", "never an automatic grade", "not a score"];
    for (const route of ["method", "assessments/capstone-master-plan", "policies"]) {
      const t = text(page(route)).toLowerCase();
      expect(
        DISCLAIMED.some((phrase) => t.includes(phrase)),
        `${route} explains bands without saying they are not grades`,
      ).toBe(true);
    }
  });
});

// --------------------------------------------------------------------------
describe("the paired water indicators", () => {
  const WATER = "Water closure";
  const GARDEN = "Garden water satisfaction";

  it("bands both, so neither can be reported without the other having a threshold", () => {
    const keys = model.indicators.map((i: { key: string }) => i.key);
    expect(keys).toContain("water_closure");
    expect(keys).toContain("garden_water_satisfaction");
  });

  it("never publishes a water closure table without garden water satisfaction beside it", () => {
    for (const route of ["method", "clients"]) {
      const t = text(page(route));
      if (t.includes(WATER)) {
        expect(t, `${route} shows water closure alone`).toContain(GARDEN);
      }
    }
  });

  it("keeps the pair's reason visible: high closure with a dry garden is possible", () => {
    // Alice Springs is the worked case. If the model ever stops producing a site
    // where the two diverge sharply, the teaching example needs rewriting.
    const alice = model.sites.find((s: { short: string }) => s.short === "Alice Springs");
    expect(alice.bands.water_closure.excellent).toBeGreaterThan(0.9);
    expect(alice.bands.garden_water_satisfaction.excellent).toBeLessThan(0.3);
    expect(text(page("method"))).toContain(GARDEN);
  });

  it("does not band waste-stream recovery, and says why", () => {
    const keys = model.indicators.map((i: { key: string }) => i.key);
    expect(keys).not.toContain("waste_stream_recovery");
    expect(text(page("method")).toLowerCase()).toMatch(/not banded|no reference calculation/);
  });
});

// --------------------------------------------------------------------------
describe("hard constraints", () => {
  it("keeps the decided allowance, contingency and energy cap", () => {
    expect(model.constraints.budget_aud).toBe(30000);
    expect(model.constraints.contingency).toBeCloseTo(0.1, 5);
    expect(model.constraints.energy_cap_kwh_day).toBe(5);
  });

  it("demonstrates both constraints are satisfiable at every site and level", () => {
    // This is the check the course failed before the reference designs were
    // re-costed against the full schedule. It must not silently start failing.
    for (const s of model.sites) {
      for (const l of ["baseline", "competent", "excellent"] as const) {
        const r = s.reference[l];
        expect(r.fits_budget, `${s.id} ${l} costs $${r.cost_total}`).toBe(true);
        expect(r.cost_total, `${s.id} ${l}`).toBeLessThanOrEqual(model.constraints.budget_aud);
        expect(r.fits_energy, `${s.id} ${l} draws ${r.energy_declared_kwh_day} kWh/d`).toBe(true);
      }
    }
  });

  it("carries uncertain loads above the modelled figure, never below", () => {
    const allowance = model.constraints.uncertain_load_allowance_kwh_day;
    expect(allowance).toBeGreaterThan(0);
    for (const s of model.sites) {
      for (const l of ["baseline", "competent", "excellent"] as const) {
        const r = s.reference[l];
        expect(r.energy_declared_kwh_day, `${s.id} ${l}`).toBeCloseTo(
          r.energy_modelled_kwh_day + allowance,
          2,
        );
      }
    }
  });

  it("includes the contingency in every reference total", () => {
    for (const s of model.sites) {
      for (const l of ["baseline", "competent", "excellent"] as const) {
        const r = s.reference[l];
        expect(r.cost_contingency, `${s.id} ${l}`).toBe(
          Math.round(r.cost_subtotal * model.constraints.contingency),
        );
        expect(r.cost_total).toBe(r.cost_subtotal + r.cost_contingency);
      }
    }
  });

  it("does not claim comfortable compliance where the margin is thin", () => {
    // The tightest site clears the allowance by about a thousand dollars, which is
    // inside the noise of a schedule built from retail listings. The costing page
    // has to say so rather than presenting the fit as settled.
    const tightest = Math.min(...model.sites.map((s: any) => s.reference.excellent.cost_headroom));
    expect(tightest).toBeGreaterThan(0);
    if (tightest < 3000) {
      expect(text(page("method/costing")).toLowerCase()).toMatch(/noise|not that a real build|untested/);
    }
  });
});

// --------------------------------------------------------------------------
describe("the price schedule", () => {
  it("gives every line a basis, and uses only the two permitted ones", () => {
    expect(model.schedule.length).toBeGreaterThanOrEqual(15);
    for (const line of model.schedule) {
      expect(["indicative", "assumption"], `${line.key} basis`).toContain(line.basis);
      expect(line.price, `${line.key} price`).toBeGreaterThan(0);
      expect(line.description.length, `${line.key} description`).toBeGreaterThan(10);
    }
  });

  it("publishes both bases on the costing page, so a reader can tell them apart", () => {
    const t = text(page("method/costing"));
    expect(t).toContain("indicative");
    expect(t.toLowerCase()).toContain("course assumption");
  });

  it("does not pay for a bundled pump twice", () => {
    // The aquaponics line includes tank, pump and aeration. An additional bed on
    // the same system must cost the bundle less one pump line.
    const bundle = model.schedule.find((l: any) => l.key === "aquaponics_4m2").price;
    const pump = model.schedule.find((l: any) => l.key === "pump").price;
    expect(model.schedule_rules.extra_bed_aud).toBe(bundle - pump);
  });

  it("charges every reference bill from schedule lines only", () => {
    const prices = new Set<number>(model.schedule.map((l: any) => l.price));
    // Every line's unit cost must be derivable from a schedule price. Checking the
    // per-unit figure catches a hand-entered number appearing in a bill.
    for (const s of model.sites) {
      for (const row of s.reference.excellent.bill) {
        // Quantities are rounded for display, so a line matches if its cost is any
        // schedule price times its quantity, within that rounding.
        const ok =
          prices.has(row.cost) ||
          [...prices].some((p) => Math.abs(row.cost - p * row.qty) <= p) ||
          row.cost === model.schedule_rules.extra_bed_aud ||
          row.cost === bundlePlusExtra(model);
        expect(ok, `${s.id}: "${row.line}" at $${row.cost} for ${row.qty} ${row.unit}`).toBe(true);
      }
    }
  });

  it("publishes what the schedule does not price", () => {
    expect(model.schedule_rules.unpriced.length).toBeGreaterThanOrEqual(4);
    const t = text(page("method/costing"));
    for (const u of model.schedule_rules.unpriced) {
      expect(t, `unpriced item missing from the page: ${u}`).toContain(u.split(":")[0]);
    }
  });
});

function bundlePlusExtra(m: any): number {
  const bundle = m.schedule.find((l: any) => l.key === "aquaponics_4m2").price;
  return bundle + m.schedule_rules.extra_bed_aud;
}

// --------------------------------------------------------------------------
describe("published figures agree with the model that produced them", () => {
  it("renders the clients comparison from the case data", () => {
    const t = text(page("clients"));
    for (const h of homes.homes) {
      expect(t, `${h.short} roof`).toContain(`${Math.round(h.areas.roof_plan_m2).toLocaleString("en-AU")} m²`);
      const site = model.sites.find((x: any) => x.id === h.id);
      expect(t, `${h.short} rain`).toContain(`${site.climate.annual_rain_mm.toLocaleString("en-AU")} mm`);
    }
  });

  it("renders reference costs on the costing page", () => {
    const t = text(page("method/costing"));
    for (const s of model.sites) {
      const total = s.reference.excellent.cost_total.toLocaleString("en-AU");
      expect(t, `${s.short} excellent total $${total}`).toContain(total);
    }
  });

  it("publishes the worked comparison across all five sites", () => {
    const t = text(page("method/comparison"));
    expect(Object.keys(comparison.rows).length).toBe(5);
    for (const s of model.sites) expect(t, `${s.short} missing`).toContain(s.short);
    // The comparison's whole point is that the answer differs by site, so the
    // published spread must actually differ.
    const gains = Object.values(comparison.summary).map((s: any) => s.gain_water_closure);
    expect(Math.max(...gains) - Math.min(...gains)).toBeGreaterThan(0.02);
  });
});

// --------------------------------------------------------------------------
describe("synthetic data is labelled as such", () => {
  it("labels the dataset file itself", () => {
    expect(datasets.label.toUpperCase()).toContain("SYNTHETIC");
    expect(datasets.drought_years.what_it_is_not.length).toBeGreaterThan(20);
    expect(datasets.aquaponic_log.what_it_is_not.length).toBeGreaterThan(20);
  });

  it("labels it on the page a student reads", () => {
    const t = text(page("method/datasets")).toLowerCase();
    expect(t).toContain("synthetic");
    expect(t).toMatch(/not a measurement|none of it is a measurement/);
    expect(t).toMatch(/not a historical drought|historical drought/);
  });

  it("names every published dataset file so its filename carries the label", () => {
    for (const f of [
      "SYNTHETIC-aquaponic-cycling-log.csv",
      "SYNTHETIC-dry-year-canberra.csv",
      "SYNTHETIC-dry-year-alice-springs.csv",
      "SYNTHETIC-dry-year-brisbane.csv",
      "SYNTHETIC-dry-year-adelaide.csv",
      "SYNTHETIC-dry-year-darwin.csv",
    ]) {
      const p = resolve("dist/data", f);
      expect(existsSync(p), `${f} was not published`).toBe(true);
      expect(readFileSync(p, "utf8").split("\n")[0].toUpperCase()).toContain("SYNTHETIC");
    }
  });

  it("gives the troubleshooting log a fault a student can actually diagnose", () => {
    // Without a diagnosable signature the dataset is decoration. The signature is
    // nitrite rising while ammonia stays low, with hardness falling ahead of both.
    const rows = datasets.aquaponic_log.rows as {
      day: number;
      ph: number;
      kh_mg_l_caco3: number;
      ammonia_mg_l: number;
      nitrite_mg_l: number;
    }[];
    expect(rows.length).toBe(60);
    const settled = rows.find((r) => r.day === 24)!;
    const faulted = rows.find((r) => r.day === 45)!;
    expect(settled.nitrite_mg_l).toBeLessThan(0.5);
    expect(faulted.nitrite_mg_l).toBeGreaterThan(3);
    expect(faulted.ammonia_mg_l).toBeLessThan(1);
    expect(faulted.kh_mg_l_caco3).toBeLessThan(settled.kh_mg_l_caco3);
    expect(faulted.ph).toBeLessThan(6.5);
    const recovered = rows.at(-1)!;
    expect(recovered.nitrite_mg_l).toBeLessThan(0.5);
  });
});

// --------------------------------------------------------------------------
describe("scope", () => {
  it("links a real deck from at least one lecture", () => {
    const withDecks = nodesOf("lectures").filter((n) => typeof n.meta?.slides === "string");
    expect(withDecks.length).toBeGreaterThanOrEqual(1);
    for (const l of withDecks) {
      const slug = String(l.meta?.slides).replace(/^\/decks\/|\/$/g, "");
      const html = page(`decks/${slug}`);
      // A real deck, not a stub: several slides with actual content.
      expect(text(html).length, `${slug} is too short to be a real deck`).toBeGreaterThan(1200);
    }
  });

  it("ships no interactive calculator", () => {
    // The course's position is that students compute and the site publishes. The
    // theme's site-wide search box is platform furniture and is excluded; what must
    // not appear is a control that takes a design parameter and returns a result.
    for (const route of ["method", "method/costing", "method/comparison", "clients", ""]) {
      const html = page(route).replace(/<input[^>]*type="search"[^>]*>/gi, "");
      expect(html, `${route || "home"} has a form`).not.toMatch(/<form[\s>]/i);
      expect(html, `${route || "home"} has a numeric input`).not.toMatch(
        /<input[^>]*type="(number|range)"/i,
      );
      expect(html, `${route || "home"} has an unexpected input`).not.toMatch(/<input[\s>]/i);
      expect(html, `${route || "home"} wires an event handler`).not.toMatch(
        /\son(input|change|click)=/i,
      );
    }
  });

  it("keeps energy and shelter out of scope and says where they went", () => {
    const t = text(page("lectures/week-12")).toLowerCase();
    expect(t).toMatch(/biogas/);
    expect(t).toMatch(/not credited|earns you nothing|recorded and not credited/);
  });
});

// --------------------------------------------------------------------------
describe("the weekly map", () => {
  // The course previously carried a second week order in a second module, so the
  // home page advertised "water monitoring" over a mushroom lecture. These check
  // the published pages agree with each other, which is the failure that hurt.
  const LEAD: Record<number, string> = {
    2: "Canberra", 3: "Brisbane", 4: "Darwin", 5: "Adelaide", 6: "Adelaide",
    7: "Alice Springs", 8: "Brisbane", 9: "Darwin", 10: "Alice Springs", 11: "Canberra",
  };
  const pad = (w: number) => String(w).padStart(2, "0");

  it("publishes an overview for every teaching week, and an index of them", () => {
    const index = text(page("weeks"));
    for (let w = 1; w <= 12; w++) {
      const t = text(page(`weeks/week-${pad(w)}`));
      expect(t, `week ${w} overview does not name its week`).toContain(`Week ${w}`);
      expect(index, `the weeks index omits week ${w}`).toContain(`Week ${w}`);
    }
  });

  it("links each overview to that week's own lecture and tutorial, not another's", () => {
    for (let w = 1; w <= 12; w++) {
      const html = page(`weeks/week-${pad(w)}`);
      for (const route of [`lectures/week-${pad(w)}/`, `sessions/week-${pad(w)}/`]) {
        expect(html, `week ${w} overview does not link ${route}`).toContain(route);
      }
      for (let other = 1; other <= 12; other++) {
        if (other === w || other === w - 1 || other === w + 1) continue;
        expect(html, `week ${w} overview links week ${other}'s lecture`).not.toContain(
          `lectures/week-${pad(other)}/`,
        );
      }
    }
  });

  it("gives every week one topic, used identically on the home page and its overview", () => {
    const home = text(page(""));
    const index = text(page("weeks"));
    const topics = new Set<string>();
    for (let w = 1; w <= 12; w++) {
      // The overview's <title> is "Week N: <topic>", which is the canonical wording.
      const title = page(`weeks/week-${pad(w)}`).match(/<title>([^<]*)<\/title>/)![1];
      const topic = title.split(/Week \d+:\s*/)[1].split("|")[0].trim();
      expect(topic.length, `week ${w} topic`).toBeGreaterThan(8);
      expect(topics.has(topic), `week ${w} reuses another week's topic`).toBe(false);
      topics.add(topic);
      expect(home, `the home timeline does not carry week ${w}'s topic`).toContain(topic);
      expect(index, `the weeks index does not carry week ${w}'s topic`).toContain(topic);
    }
  });

  it("names the same lead home on the overview as the lecture works its example at", () => {
    const ALL = ["Canberra", "Alice Springs", "Brisbane", "Adelaide", "Darwin"];
    for (const [w, site] of Object.entries(LEAD)) {
      const t = text(page(`weeks/week-${pad(Number(w))}`));
      expect(t, `week ${w} overview should lead with ${site}`).toContain(site);
      // An overview that named a second home would be describing a different
      // week's worked example, which is exactly the drift this guards against.
      for (const other of ALL.filter((s) => s !== site)) {
        expect(t, `week ${w} overview names ${other} as well as ${site}`).not.toContain(other);
      }
    }
  });

  it("states what the tutorial produces, on every week", () => {
    for (let w = 1; w <= 12; w++) {
      const t = text(page(`weeks/week-${pad(w)}`));
      expect(t, `week ${w} overview does not say what you leave with`).toContain(
        "What you leave with",
      );
    }
  });
});
