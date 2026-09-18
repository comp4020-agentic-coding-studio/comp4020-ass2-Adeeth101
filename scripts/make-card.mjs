// Draws the link-preview card from the same loop the course teaches, in the
// Slop palette, and rasterises it with the `sharp` the build already depends on.
// Run: node scripts/make-card.mjs
//
// The card is generated rather than drawn by hand so the four stream colours and
// the palette stay in one place: src/components/LoopDiagram.astro uses the same
// five node labels, and a change here is a change there.
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const GOLD = "#b97d1c";
const BRONZE = "#8a5c13";
const GREY = "#6b6154";
const INK = "#2e2822";
const PAPER = "#fefcf9";
const PANEL = "#f7f1e6";

const W = 1200;
const H = 630;

// Five nodes around an ellipse: the loop, in the order the course teaches it.
const NODES = [
  "Garden",
  "Kitchen",
  "Waste",
  "Nutrients",
  "Water",
];
const cx = 905;
const cy = 330;
const rx = 205;
const ry = 175;
const pt = (i) => {
  const a = -Math.PI / 2 + (i * 2 * Math.PI) / NODES.length;
  return [cx + rx * Math.cos(a), cy + ry * Math.sin(a)];
};

const arcs = NODES.map((_, i) => {
  const [x1, y1] = pt(i);
  const [x2, y2] = pt((i + 1) % NODES.length);
  // Pull each chord toward the centre so the ring reads as flow, not a pentagon.
  const mx = (x1 + x2) / 2 + (cx - (x1 + x2) / 2) * 0.22;
  const my = (y1 + y2) / 2 + (cy - (y1 + y2) / 2) * 0.22;
  return `<path d="M ${x1.toFixed(1)} ${y1.toFixed(1)} Q ${mx.toFixed(1)} ${my.toFixed(1)} ${x2.toFixed(1)} ${y2.toFixed(1)}"
      fill="none" stroke="${i % 2 ? BRONZE : GOLD}" stroke-width="7" stroke-linecap="round"
      marker-end="url(#a)" opacity="0.92"/>`;
}).join("\n    ");

const nodes = NODES.map((label, i) => {
  const [x, y] = pt(i);
  return `<g><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="46" fill="${PAPER}" stroke="${GOLD}" stroke-width="4"/>
      <text x="${x.toFixed(1)}" y="${(y + 6).toFixed(1)}" text-anchor="middle"
        font-family="Georgia, serif" font-size="20" fill="${INK}">${label}</text></g>`;
}).join("\n    ");

// The leak: the part the course refuses to hide.
const leak = `<g>
      <path d="M ${cx + 40} ${cy + ry + 34} l 92 46" stroke="${GREY}" stroke-width="6"
        stroke-dasharray="11 9" stroke-linecap="round" marker-end="url(#g)"/>
      <text x="${cx + 146}" y="${cy + ry + 96}" text-anchor="middle" font-family="Georgia, serif"
        font-size="19" fill="${GREY}">imports</text>
    </g>`;

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="${BRONZE}"/>
    </marker>
    <marker id="g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="${GREY}"/>
    </marker>
  </defs>
  <rect width="${W}" height="${H}" fill="${PAPER}"/>
  <rect x="0" y="0" width="${W}" height="14" fill="${GOLD}"/>
  <rect x="640" y="0" width="560" height="${H}" fill="${PANEL}" opacity="0.55"/>

  <text x="72" y="140" font-family="Georgia, serif" font-size="30" fill="${BRONZE}" letter-spacing="3">SLOP4761</text>
  <text x="72" y="216" font-family="Georgia, serif" font-size="52" fill="${INK}">Designing the</text>
  <text x="72" y="278" font-family="Georgia, serif" font-size="52" fill="${INK}">Closed-Loop Household I</text>
  <text x="72" y="336" font-family="Georgia, serif" font-size="34" fill="${GOLD}">Food, Water and Waste</text>

  <line x1="72" y1="382" x2="536" y2="382" stroke="${GOLD}" stroke-width="3"/>
  <text x="72" y="432" font-family="Georgia, serif" font-size="25" fill="${INK}">One plot. $30,000. 5 kWh a day.</text>
  <text x="72" y="474" font-family="Georgia, serif" font-size="25" fill="${GREY}">How much of the loop closes,</text>
  <text x="72" y="510" font-family="Georgia, serif" font-size="25" fill="${GREY}">honestly counted?</text>
  <text x="72" y="566" font-family="Georgia, serif" font-size="20" fill="${GREY}">Slop University &#183; Semester 1, 2027</text>

  <g>
    ${arcs}
    ${leak}
    ${nodes}
  </g>
</svg>`;

const out = fileURLToPath(new URL("../src/assets/images/card.png", import.meta.url));
const svgOut = fileURLToPath(new URL("../src/assets/images/loop-card.svg", import.meta.url));
writeFileSync(svgOut, svg);
await sharp(Buffer.from(svg)).png().toFile(out);
console.log("wrote src/assets/images/card.png and loop-card.svg");
