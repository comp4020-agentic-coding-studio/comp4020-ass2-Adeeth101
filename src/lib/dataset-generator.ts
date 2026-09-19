/** A browser port of research/model/make_datasets.py.
 *
 *  It reproduces the Python generator exactly, not approximately: the same
 *  Mersenne Twister, seeded the way Python's `random.seed(int)` seeds it, the
 *  same `round()` (half to even on the exact binary value) and the same CSV
 *  dialect. With the default seeds it writes files byte-identical to the ones
 *  in public/data/, which spec/dataset-generator.test.ts checks. Anyone can
 *  therefore regenerate the published sets from the page, and a different seed
 *  gives a different, equally labelled, synthetic set.
 */

export const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] as const;
export const DROUGHT_SEED = 4761;
export const LOG_SEED = 589;

export interface GeneratorSite {
  sid: string;
  label: string;
  file: string;
  station: string;
  /** Long-record mean monthly rainfall, Jan–Dec, mm. */
  rain: number[];
}

/** Sites in the order the Python generator iterates them (presets.V4). */
export const SITE_KEYS = [
  { sid: "S1", label: "Canberra", file: "canberra", station: "070014" },
  { sid: "S2", label: "Alice Springs", file: "alice-springs", station: "015590" },
  { sid: "S3", label: "Brisbane", file: "brisbane", station: "040214" },
  { sid: "S4", label: "Adelaide", file: "adelaide", station: "023000" },
  { sid: "S5", label: "Darwin", file: "darwin", station: "014015" },
] as const;

// ---------------------------------------------------------------------------
// Python's random module: MT19937 with init_by_array seeding and 53-bit floats.

export class PyRandom {
  private mt = new Uint32Array(624);
  private mti = 625;

  constructor(seed: number) {
    // random.seed(n) for a non-negative int n feeds its 32-bit words to init_by_array.
    let n = BigInt(Math.abs(Math.trunc(seed)));
    const key: number[] = [];
    do {
      key.push(Number(n & 0xffffffffn));
      n >>= 32n;
    } while (n > 0n);
    this.initByArray(key);
  }

  private initGenrand(s: number) {
    const mt = this.mt;
    mt[0] = s >>> 0;
    for (let i = 1; i < 624; i++) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = (Math.imul(1812433253, prev) + i) >>> 0;
    }
    this.mti = 624;
  }

  private initByArray(key: number[]) {
    const mt = this.mt;
    this.initGenrand(19650218);
    let i = 1;
    let j = 0;
    for (let k = Math.max(624, key.length); k > 0; k--) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = ((mt[i] ^ Math.imul(prev, 1664525)) + key[j] + j) >>> 0;
      i++;
      j++;
      if (i >= 624) {
        mt[0] = mt[623];
        i = 1;
      }
      if (j >= key.length) j = 0;
    }
    for (let k = 623; k > 0; k--) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = ((mt[i] ^ Math.imul(prev, 1566083941)) - i) >>> 0;
      i++;
      if (i >= 624) {
        mt[0] = mt[623];
        i = 1;
      }
    }
    mt[0] = 0x80000000;
  }

  private int32(): number {
    const mt = this.mt;
    if (this.mti >= 624) {
      for (let k = 0; k < 624; k++) {
        const y = (mt[k] & 0x80000000) | (mt[(k + 1) % 624] & 0x7fffffff);
        mt[k] = mt[(k + 397) % 624] ^ (y >>> 1) ^ (y & 1 ? 0x9908b0df : 0);
      }
      this.mti = 0;
    }
    let y = mt[this.mti++];
    y ^= y >>> 11;
    y ^= (y << 7) & 0x9d2c5680;
    y ^= (y << 15) & 0xefc60000;
    y ^= y >>> 18;
    return y >>> 0;
  }

  random(): number {
    const a = this.int32() >>> 5;
    const b = this.int32() >>> 6;
    return (a * 67108864 + b) / 2 ** 53;
  }

  uniform(a: number, b: number): number {
    return a + (b - a) * this.random();
  }
}

// ---------------------------------------------------------------------------
// Python's round(): correctly rounded, ties to even, on the exact double value.

export function pyRound(x: number, ndigits = 0): number {
  const neg = x < 0;
  // toFixed(100) is the exact decimal expansion for the magnitudes used here.
  const exact = Math.abs(x).toFixed(100);
  const [intPart, frac] = exact.split(".");
  const digits = intPart + frac.slice(0, ndigits);
  const rest = frac.slice(ndigits);
  let up = false;
  if (rest[0] > "5") up = true;
  else if (rest[0] === "5") {
    up = /[1-9]/.test(rest.slice(1)) || Number(digits[digits.length - 1]) % 2 === 1;
  }
  let n = BigInt(digits) + (up ? 1n : 0n);
  if (neg) n = -n;
  return Number(n) / 10 ** ndigits;
}

/** A value that Python would print as a float (always with a decimal point). */
class PyFloat {
  constructor(readonly value: number) {}
  toString() {
    return Number.isInteger(this.value) ? this.value.toFixed(1) : String(this.value);
  }
}

type Cell = number | string | PyFloat;
const f = (x: number, nd: number) => new PyFloat(pyRound(x, nd));
const cellText = (c: Cell) => (c instanceof PyFloat ? c.toString() : String(c));

// ---------------------------------------------------------------------------
// The two datasets, line for line with make_datasets.py.

export interface DryYear {
  sid: string;
  site: string;
  file: string;
  station: string;
  mean_year_mm: number[];
  dry_year_mm: number[];
  mean_annual_mm: number;
  dry_annual_mm: number;
  share_of_mean: number;
}

export function droughtYears(sites: GeneratorSite[], seed = DROUGHT_SEED): DryYear[] {
  const rng = new PyRandom(seed);
  return sites.map((site) => {
    const rain = site.rain.slice(0, 12);
    // Python's sort is stable, as is Array.prototype.sort.
    const order = [...Array(12).keys()].sort((a, b) => rain[a] - rain[b]);
    const driest = new Set(order.slice(0, 4));
    const dry = rain.map((r, m) => {
      const factor = driest.has(m) ? rng.uniform(0.2, 0.45) : rng.uniform(0.5, 0.8);
      return pyRound(r * factor, 1);
    });
    const total = dry.reduce((s, v) => s + v, 0);
    const meanTotal = rain.reduce((s, v) => s + v, 0);
    return {
      sid: site.sid,
      site: site.label,
      file: site.file,
      station: site.station,
      mean_year_mm: rain.map((r) => pyRound(r, 1)),
      dry_year_mm: dry,
      mean_annual_mm: pyRound(meanTotal),
      dry_annual_mm: pyRound(total),
      share_of_mean: pyRound(total / meanTotal, 2),
    };
  });
}

export const LOG_COLUMNS = [
  "day", "temp_c", "ph", "kh_mg_l_caco3", "ammonia_mg_l", "nitrite_mg_l", "nitrate_mg_l", "note",
] as const;

export type LogRow = Record<(typeof LOG_COLUMNS)[number], Cell>;

export function aquaponicLog(seed = LOG_SEED): LogRow[] {
  const rng = new PyRandom(seed);
  const rows: LogRow[] = [];
  for (let d = 1; d <= 60; d++) {
    let nh3: number, no2: number, no3: number, kh: number;
    if (d <= 8) {
      nh3 = 0.4 + 0.42 * d;
      no2 = 0.05 * d;
      no3 = 0.5 + 0.3 * d;
      kh = 82 - 1.1 * d;
    } else if (d <= 16) {
      nh3 = Math.max(0.15, 3.8 - 0.42 * (d - 8));
      no2 = 0.4 + 0.55 * (d - 8);
      no3 = 2.9 + 1.4 * (d - 8);
      kh = 73 - 1.6 * (d - 8);
    } else if (d <= 24) {
      nh3 = Math.max(0.05, 0.45 - 0.05 * (d - 16));
      no2 = Math.max(0.05, 4.8 - 0.62 * (d - 16));
      no3 = 14 + 2.1 * (d - 16);
      kh = 60 - 2.2 * (d - 16);
    } else if (d <= 45) {
      nh3 = 0.06 + 0.012 * (d - 24);
      no2 = 0.08 + 0.29 * (d - 24);
      no3 = 31 + 0.5 * (d - 24);
      kh = Math.max(8, 42 - 1.7 * (d - 24));
    } else {
      nh3 = Math.max(0.04, 0.32 - 0.02 * (d - 45));
      no2 = Math.max(0.05, 6.2 - 0.42 * (d - 45));
      no3 = 41 + 1.6 * (d - 45);
      kh = Math.min(78, 12 + 4.6 * (d - 45));
    }

    // Draw order matches the Python exactly: ph, temp, then the row's fields.
    const ph = 6.0 + 0.0135 * kh + rng.uniform(-0.04, 0.04);
    const temp = 22.4 + 1.5 * (0.5 - Math.abs((d % 14) - 7) / 14) + rng.uniform(-0.35, 0.35);
    let note = "";
    if (d === 1) note = "system started; 12 fish stocked, feeding 40 g/day";
    else if (d === 25) note = "feed increased to 60 g/day";
    else if (d === 46) note = "operator added carbonate buffer";
    rows.push({
      day: d,
      temp_c: f(temp, 1),
      ph: f(ph, 2),
      kh_mg_l_caco3: pyRound(Math.max(4, kh + rng.uniform(-1.5, 1.5))),
      ammonia_mg_l: f(Math.max(0.02, nh3 + rng.uniform(-0.03, 0.03)), 2),
      nitrite_mg_l: f(Math.max(0.02, no2 + rng.uniform(-0.06, 0.06)), 2),
      nitrate_mg_l: f(Math.max(0.3, no3 + rng.uniform(-0.7, 0.7)), 1),
      note,
    });
  }
  return rows;
}

// ---------------------------------------------------------------------------
// CSV output in Python's csv.writer default dialect: minimal quoting, CRLF.

function csvLine(cells: Cell[]): string {
  return cells
    .map((c) => {
      const s = cellText(c);
      return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
    })
    .join(",") + "\r\n";
}

export function logCsv(rows: LogRow[]): string {
  return (
    csvLine(["# SYNTHETIC DATA - generated, not measured. SLOP4761."]) +
    csvLine([...LOG_COLUMNS]) +
    rows.map((r) => csvLine(LOG_COLUMNS.map((c) => r[c]))).join("")
  );
}

export function dryYearCsv(d: DryYear): string {
  return (
    csvLine([`# SYNTHETIC DATA - derived from BoM station ${d.station} statistics, not an observed year. SLOP4761.`]) +
    csvLine(["month", "mean_year_rain_mm", "dry_year_rain_mm"]) +
    MONTHS.map((m, i) => csvLine([m, new PyFloat(d.mean_year_mm[i]), new PyFloat(d.dry_year_mm[i])])).join("")
  );
}

export const LOG_FILE = "SYNTHETIC-aquaponic-cycling-log.csv";
export const dryYearFile = (d: { file: string }) => `SYNTHETIC-dry-year-${d.file}.csv`;

/** Every file the Python generator writes to public/data/, by filename. */
export function generateAll(sites: GeneratorSite[], droughtSeed = DROUGHT_SEED, logSeed = LOG_SEED) {
  const dry = droughtYears(sites, droughtSeed);
  const log = aquaponicLog(logSeed);
  const files: { name: string; text: string }[] = [
    { name: LOG_FILE, text: logCsv(log) },
    ...dry.map((d) => ({ name: dryYearFile(d), text: dryYearCsv(d) })),
  ];
  return { dry, log, files };
}
