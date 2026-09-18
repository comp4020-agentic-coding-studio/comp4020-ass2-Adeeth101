"""The five fixed client properties: personas, intake dossiers and scaled plan geometry.

Everything in this file is FICTIONAL CASE MATERIAL for SLOP4761, invented for teaching
and labelled as such on the site. It must be internally consistent, not survey-accurate:

  * every area on a plan is computed from its geometry, never typed;
  * roof plan area is derived from footprint plus eaves, never asserted;
  * the preset site parameters (presets.py, set v4) are reproduced within a stated
    rounding tolerance;
  * nothing a household owns sits outside its own boundary, and nothing overlaps.

Three quantities the course keeps apart, because the first draft ran them together:

  * footprint        the ground a building covers;
  * roof plan area   the horizontal projection of the roof, i.e. footprint plus eaves,
                     plus any roof over hardstand (carport, verandah). This is the area
                     that collects rain: 1 mm on 1 m2 of plan area is 1 L, whatever the
                     pitch;
  * roof surface     larger again on a pitched roof, and the wrong number for catchment.

Coordinates are metres, x east and y north, origin at the south-west corner of the drawn
plan. Suburban plans draw the whole lot. Rural plans draw a working area inside a larger
parcel, and the parcel is drawn separately at a smaller scale.

Run:  python case.py   -> self-checks every plan and prints the area reconciliation.
"""

import os
import sys
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))

# Plans are drawn to round dimensions, so their parts reproduce the preset totals only
# approximately. This is the published tolerance: the larger of 15 m2 or 4 per cent.
TOL_ABS_M2 = 15.0
TOL_REL = 0.04

# Status of a dossier fact. The course asks students to tell these apart.
KNOWN, ESTIMATE, UNKNOWN = "known", "estimate", "unknown"


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------
@dataclass
class Rect:
    """Axis-aligned rectangle in plan metres. `eaves` is (west, east, south, north)."""
    id: str
    x: float
    y: float
    w: float
    h: float
    label: str
    kind: str                 # building | roofover | hardstand | growing | recreation | other
    note: str = ""
    eaves: tuple = (0.0, 0.0, 0.0, 0.0)

    @property
    def area(self) -> float:
        return self.w * self.h

    @property
    def roof(self) -> tuple:
        """The roof outline as (x, y, w, h), eaves included."""
        we, ee, se, ne = self.eaves
        return (self.x - we, self.y - se, self.w + we + ee, self.h + se + ne)

    @property
    def roof_area(self) -> float:
        _, _, w, h = self.roof
        return w * h

    def as_dict(self) -> dict:
        d = {"id": self.id, "x": self.x, "y": self.y, "w": self.w, "h": self.h,
             "label": self.label, "kind": self.kind, "note": self.note,
             "area": round(self.area, 1)}
        if any(self.eaves):
            rx, ry, rw, rh = self.roof
            d["roof"] = {"x": round(rx, 2), "y": round(ry, 2), "w": round(rw, 2), "h": round(rh, 2),
                         "area": round(self.roof_area, 1)}
        return d


def E(e):
    """Uniform eaves shorthand."""
    return (e, e, e, e)


@dataclass
class Circle:
    """A tank or a tree canopy. Tanks carry a capacity; trees may be off-site."""
    id: str
    cx: float
    cy: float
    r: float
    label: str
    kind: str                 # tank | tree | bore | septic
    note: str = ""
    kl: float = 0.0
    offsite: bool = False
    w: float = 0.0            # a slimline tank is drawn as a w x h box centred on (cx, cy)
    h: float = 0.0

    @property
    def box(self) -> tuple:
        if self.w:
            return (self.cx - self.w / 2, self.cy - self.h / 2, self.w, self.h)
        return (self.cx - self.r, self.cy - self.r, 2 * self.r, 2 * self.r)

    def as_dict(self) -> dict:
        d = {"id": self.id, "cx": self.cx, "cy": self.cy, "r": self.r, "label": self.label,
             "kind": self.kind, "note": self.note}
        if self.w:
            d["w"], d["h"] = self.w, self.h
        if self.kl:
            d["kl"] = self.kl
        if self.offsite:
            d["offsite"] = True
        return d


@dataclass
class Zone:
    """A separately connectable roof catchment zone, with where its downpipes land."""
    id: str
    label: str
    rect: tuple               # (x, y, w, h) part of a roof outline
    downpipes: list           # [(x, y)]
    connected_now: bool
    gutter: bool = True
    note: str = ""

    @property
    def plan_m2(self) -> float:
        return self.rect[2] * self.rect[3]

    def as_dict(self) -> dict:
        x, y, w, h = self.rect
        return {"id": self.id, "label": self.label, "x": x, "y": y, "w": w, "h": h,
                "plan_m2": round(self.plan_m2), "downpipes": [list(p) for p in self.downpipes],
                "connected_now": self.connected_now, "gutter": self.gutter, "note": self.note}


@dataclass
class Point:
    """A service point or spot level."""
    id: str
    x: float
    y: float
    label: str
    kind: str                 # service | level | access | overflow
    status: str = KNOWN
    note: str = ""

    def as_dict(self) -> dict:
        return {"id": self.id, "x": self.x, "y": self.y, "label": self.label, "kind": self.kind,
                "status": self.status, "note": self.note}


@dataclass
class Fact:
    text: str
    status: str = KNOWN


@dataclass
class Home:
    sid: str
    slug: str
    short: str
    family: str
    household: str            # names, fictional
    place: str
    dwelling: str
    tenure: str
    parcel_m2: float
    plan_extent: tuple        # (W, H) of the drawn plan
    cover: list               # Rect: buildings, hardstand, growing, recreation (non-overlapping)
    roofover: list            # Rect: roofs over hardstand (carports, verandahs); not ground cover
    circles: list             # Circle: tanks, trees, bores
    zones: list               # Zone
    points: list              # Point
    easements: list           # Rect-like dicts drawn as hatched overlays
    floor_extent: tuple
    rooms: list               # Rect, kind wet|room|service
    floor_points: list        # Point, in floor-plan coordinates
    slope: Fact
    services: list            # (service, Fact)
    inventory: list           # Fact
    observations: list        # str, the homeowner's words
    priorities: list          # str, ranked
    constraints: list         # Fact
    unknowns: list            # str
    # machine-readable client constraints, consumed by scenario.py
    permitted_tank_uses: tuple
    bore_uses: tuple = ()
    retained_within_envelope_m2: float = 0.0
    max_new_storage_kl: float = 0.0
    storage_kind: str = "round"      # round | slimline
    maintenance_h_week: float = 3.0
    min_attendance_days: int = 1     # shortest attendance interval the household can keep
    unattended_days: int = 0         # longest absence systems must survive
    excluded_modules: tuple = ()
    existing_irrigated_m2: float = 0.0
    existing_irrigation: str = ""    # mains_sprinkler | mains_drip | tank_gravity | tank_drip
    existing_pressure_pump: bool = False
    existing_garden_pump: bool = False
    existing_tank_uses: tuple = ("garden",)
    priority_zones: tuple = ()       # (zone id, m2): where the existing plantings the client keeps are
    zone_quality: dict = field(default_factory=dict)   # relative productivity, revealed in Release B
    shared_allocation_m2: float = 0.0
    priority_perennial_share: float = 0.0   # share of the existing plantings that are trees or perennials
    existing_timer_share: float = 0.0       # existing condition: share of the plantings' need a tap timer draws before the house
    mains: bool = True
    parcel: dict = field(default_factory=dict)
    scheme: dict = field(default_factory=dict)
    presets: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# S1 Canberra — the Taylor family
# ---------------------------------------------------------------------------
CANBERRA = Home(
    sid="S1", slug="canberra", short="Canberra", family="Taylor",
    household="Alex and Morgan Taylor and their two children, aged 9 and 12",
    place="Canberra, ACT",
    dwelling="Single-storey brick-veneer house (1978) with a detached garage, carport and garden shed",
    tenure="Owner-occupied residential lease. No body corporate.",
    parcel_m2=800, plan_extent=(20.0, 40.0),
    cover=[
        Rect("B1", 1.2, 6.0, 11.6, 14.5, "House", "building", "single storey, tiled roof", E(0.6)),
        Rect("B2", 14.0, 22.0, 6.0, 6.0, "Garage", "building", "boundary wall to the east, steel roof", (0.3, 0.0, 0.3, 0.3)),
        Rect("B3", 0.5, 36.3, 3.0, 2.5, "Shed", "building", "steel, no gutter", E(0.2)),
        Rect("H1", 16.6, 0.0, 3.4, 22.0, "Driveway", "hardstand", "concrete, falls to the street"),
        Rect("H2", 1.2, 20.5, 11.6, 3.0, "Terrace", "hardstand", "paved, north of the house"),
        Rect("G1", 0.0, 0.0, 16.6, 6.0, "Front garden", "growing", "lawn and shrubs; the house shades it from May to August"),
        Rect("G2", 12.8, 6.0, 3.8, 14.5, "East side bed", "growing", "morning sun; meters and hot-water unit on this wall"),
        Rect("G3", 0.0, 23.5, 14.0, 9.5, "Back lawn", "growing", "where the children play; the family keeps at least 100 m² of it as lawn"),
        Rect("G4", 4.0, 33.0, 10.0, 7.0, "North beds", "growing", "warmest aspect; the two raised beds are here"),
        Rect("G5", 14.0, 28.0, 6.0, 12.0, "Orchard strip", "growing", "apple, pear and plum"),
        Rect("G6", 0.0, 33.0, 4.0, 3.3, "Herb strip", "growing", "beside the shed; the neighbour's eucalypt shades it after 2 pm"),
    ],
    roofover=[
        Rect("V1", 16.6, 7.0, 3.4, 7.0, "Carport", "roofover", "steel roof over the driveway", (0.2, 0.0, 0.2, 0.2)),
        Rect("V2", 4.0, 21.1, 6.0, 2.4, "Verandah", "roofover", "polycarbonate over part of the terrace", (0.2, 0.2, 0.0, 0.2)),
    ],
    circles=[
        Circle("T1", 15.0, 29.1, 0.9, "Existing 5 kL tank", "tank", "poly, 2009, garage roof only, gravity tap", kl=5),
        Circle("E1", 17.2, 31.0, 2.1, "Apple", "tree", "mature"),
        Circle("E2", 17.2, 35.0, 1.9, "Pear", "tree", "mature"),
        Circle("E3", 17.3, 38.4, 1.5, "Plum", "tree", "partly shaded by the pear"),
        Circle("E4", -2.5, 31.0, 5.0, "Neighbour's eucalypt", "tree", "off-site; shades the west of the back garden from about 2 pm", offsite=True),
        Circle("E5", 7.5, 36.5, 0.0, "", "tree"),  # placeholder removed below
    ],
    zones=[
        Zone("R1", "House, north plane", (0.6, 13.25, 12.8, 7.85), [(0.6, 21.1), (13.4, 21.1)], False,
             note="gutters renewed 2021; both downpipes go to stormwater"),
        Zone("R2", "House, south plane", (0.6, 5.4, 12.8, 7.85), [(0.6, 5.4), (13.4, 5.4)], False,
             note="downpipes at the two front corners"),
        Zone("R3", "Garage", (13.7, 21.7, 6.3, 6.6), [(14.9, 28.3)], True,
             note="the only zone plumbed to the 5 kL tank"),
        Zone("R4", "Carport", (16.4, 6.8, 3.6, 7.4), [(16.4, 14.2)], False, note="drains onto the driveway"),
        Zone("R5", "Verandah", (3.8, 21.1, 6.4, 2.6), [(3.8, 23.7)], False, note="gutter to a garden bed"),
        Zone("R6", "Shed", (0.3, 36.1, 3.4, 2.9), [], False, gutter=False, note="no gutter fitted"),
    ],
    points=[
        Point("P1", 16.2, 0.4, "Water meter", "service"),
        Point("P2", 16.2, 9.0, "Gas meter and hot-water unit", "service"),
        Point("P3", 12.9, 11.0, "Switchboard", "service"),
        Point("P4", 2.0, 5.5, "Sewer connection (approximate)", "service", UNKNOWN,
              "the house drain is assumed to leave the south-west corner; not located"),
        Point("P5", 18.3, 0.3, "Stormwater to kerb", "service"),
        Point("L1", 10.0, 0.5, "RL 100.0", "level", ESTIMATE),
        Point("L2", 10.0, 39.5, "RL 101.2", "level", ESTIMATE),
        Point("A1", 18.3, 1.0, "Vehicle access", "access"),
    ],
    easements=[
        {"id": "X1", "x": 0.0, "y": 38.2, "w": 20.0, "h": 1.8, "label": "Sewer easement",
         "note": "1.8 m along the rear boundary on the title; main depth and alignment not verified",
         "status": ESTIMATE},
    ],
    floor_extent=(11.6, 14.5),
    rooms=[
        Rect("F1", 0.0, 0.0, 3.9, 4.2, "Bedroom 2", "room"),
        Rect("F2", 3.9, 0.0, 3.9, 4.2, "Bedroom 3", "room"),
        Rect("F3", 7.8, 0.0, 3.8, 4.2, "Bedroom 1", "room"),
        Rect("F4", 0.0, 4.2, 11.6, 1.2, "Hall", "room"),
        Rect("F5", 0.0, 5.4, 2.8, 3.6, "Bathroom", "wet", "shower over bath, basin"),
        Rect("F6", 2.8, 5.4, 1.4, 3.6, "WC", "wet"),
        Rect("F7", 4.2, 5.4, 4.8, 3.6, "Study", "room"),
        Rect("F8", 9.0, 5.4, 2.6, 3.6, "Laundry", "wet", "tub and washing machine; door to the east side"),
        Rect("F9", 0.0, 9.0, 7.6, 5.5, "Living and dining", "room"),
        Rect("F10", 7.6, 9.0, 4.0, 5.5, "Kitchen", "wet", "sink and dishwasher on the east wall"),
    ],
    floor_points=[
        Point("Q1", 11.6, 7.2, "Laundry door", "access"),
        Point("Q2", 11.6, 3.0, "Hot-water unit (external)", "service"),
    ],
    slope=Fact("Falls about 1.2 m from the rear fence to the street, roughly 3 per cent, estimated from the ACT contour map. Enough for gravity from the back garden towards the street, not the reverse.", ESTIMATE),
    services=[
        ("Water", Fact("Mains water, 20 mm meter at the street on the east side.")),
        ("Sewer", Fact("Connected. The main is on the title in the rear easement, but where the house drain runs has not been located.", UNKNOWN)),
        ("Power", Fact("Overhead supply, 63 A single phase.")),
        ("Gas", Fact("Natural gas; storage hot-water unit on the east wall.")),
        ("Stormwater", Fact("Roof and driveway both discharge to the street kerb.")),
    ],
    inventory=[
        Fact("5 kL poly rainwater tank (2009), fed by the garage roof, gravity garden tap, no pump."),
        Fact("Two timber raised beds, about 9 m² in total, in the north beds."),
        Fact("Apple, pear and plum trees, mature, in the orchard strip."),
        Fact("One 220 L compost tumbler."),
        Fact("Hose and oscillating sprinkler on a tap timer, run from the mains in summer over the beds and fruit trees, about 45 m²."),
    ],
    observations=[
        "“The tank is empty by January most years and we water off the mains all summer.”",
        "“The back lawn is where the kids actually play. We are not digging all of it up.”",
        "“Nobody is home to look at anything between Monday and Friday.”",
        "“The herb strip never does much. I assumed it was the soil.”",
        "“Whatever we do has to keep working through July, when everything here freezes.”",
    ],
    priorities=[
        "Keep the fruit trees and the raised beds productive through summer without watering from the mains.",
        "Make whatever is installed work reliably through a Canberra winter, including frosts.",
        "Keep a real lawn for the children: at least 100 m² of the back lawn stays lawn.",
        "Nothing that needs attention on a weekday.",
    ],
    constraints=[
        Fact("Retained lawn: at least 100 m² of the back lawn (G3) stays lawn, so at most 33 m² of it may be cultivated."),
        Fact("Maintenance: up to 2 hours a week, on one weekend day only. Nothing may need attention more often than every 7 days."),
        Fact("Installation zones: new tanks only on the east side of the house (G2 and the driveway edge) or in the orchard strip clear of the tree canopies. Nothing in the sewer easement, nothing forward of the house."),
        Fact("Disruption: up to five working days on site. No internal plumbing work during school term."),
        Fact("Permitted uses of rainwater: garden irrigation, toilet flushing and laundry. The family does not want rainwater for drinking, cooking or bathing."),
    ],
    unknowns=[
        "Where the house drain and the sewer main actually run, and how deep they are.",
        "Soil texture, pH and organic matter in each growing zone.",
        "Why the herb strip underperforms: shade, root competition from the eucalypt, or soil.",
        "How much water the household uses indoors, month by month, and how it splits between uses.",
        "Whether the house gutters can be connected to storage without regrading them.",
        "How cold the ground and any exposed pipework get on the worst July nights.",
    ],
    permitted_tank_uses=("toilet", "laundry", "garden"),
    retained_within_envelope_m2=100.0,
    max_new_storage_kl=20.0,
    maintenance_h_week=2.0,
    min_attendance_days=7,
    unattended_days=21,
    excluded_modules=(),
    existing_irrigated_m2=45.0,
    existing_irrigation="mains_sprinkler",
    priority_zones=(("G4", 15.0), ("G5", 30.0)),
    zone_quality={"G1": 0.70, "G2": 0.80, "G3": 0.95, "G4": 1.00, "G5": 0.85, "G6": 0.45},
    priority_perennial_share=0.67,
    mains=True,
)
CANBERRA.circles = [c for c in CANBERRA.circles if c.label]

# ---------------------------------------------------------------------------
# S2 Alice Springs — the Nguyen family
# ---------------------------------------------------------------------------
ALICE = Home(
    sid="S2", slug="alice-springs", short="Alice Springs", family="Nguyen",
    household="Linh and David Nguyen and their two children, aged 10 and 13",
    place="Alice Springs, NT (rural-residential)",
    dwelling="Blockwork house (1994) with deep verandahs and a steel machinery shed on a 2 ha block",
    tenure="Owner-occupied freehold, rural-residential zoning.",
    parcel_m2=20000, plan_extent=(50.0, 40.0),
    cover=[
        Rect("B1", 8.0, 18.0, 12.0, 14.0, "House", "building", "blockwork, steel roof", E(0.5)),
        Rect("B2", 32.0, 6.0, 8.0, 10.0, "Machinery shed", "building", "steel", E(0.3)),
        Rect("H1", 21.0, 0.0, 10.5, 15.0, "Gravel turning area", "hardstand", "unsealed; sheet drains east"),
        Rect("H2", 7.5, 15.0, 13.0, 2.5, "South verandah slab", "hardstand", "concrete, under the verandah"),
        Rect("H3", 40.3, 6.0, 7.0, 5.0, "Shed apron", "hardstand", "concrete"),
        Rect("G1", 8.0, 35.5, 12.0, 4.5, "Shade-house garden", "growing", "50 per cent shadecloth over about 40 m²"),
        Rect("G2", 25.0, 20.0, 12.0, 14.0, "Main garden", "growing", "drip on a manual tap timer, no filtration"),
        Rect("G3", 1.0, 17.0, 5.0, 18.0, "Windbreak strip", "growing", "established olives and figs"),
        Rect("G4", 39.0, 20.0, 8.0, 12.0, "Trial plot", "growing", "bare since last summer's melons failed"),
        Rect("C1", 8.0, 2.0, 11.0, 10.0, "Shaded yard", "recreation", "under the river red gum; kept as it is"),
    ],
    roofover=[
        Rect("V1", 7.5, 15.0, 13.0, 2.5, "South verandah", "roofover", "steel, guttered", (0, 0, 0, 0)),
        Rect("V2", 7.5, 32.5, 13.0, 2.5, "North verandah", "roofover", "steel, guttered", (0, 0, 0, 0)),
    ],
    circles=[
        Circle("T1", 22.8, 25.8, 1.8, "Existing 22 kL tank", "tank", "steel-lined, 2014, house east plane, pressure pump", kl=22),
        Circle("W1", 47.5, 37.0, 0.6, "Bore", "bore", "licensed, 100 kL/yr, metered"),
        Circle("E1", 3.5, 20.5, 2.5, "Olive", "tree", "windbreak"),
        Circle("E2", 3.5, 29.0, 2.5, "Fig", "tree", "windbreak"),
        Circle("E3", 13.5, 7.0, 4.5, "River red gum", "tree", "shades the yard from mid-afternoon"),
    ],
    zones=[
        Zone("R1", "House, east plane", (14.0, 17.5, 6.5, 15.0), [(20.5, 24.0), (20.5, 27.5)], True,
             note="plumbed to the 22 kL tank"),
        Zone("R2", "House, west plane", (7.5, 17.5, 6.5, 15.0), [(7.5, 20.0), (7.5, 30.0)], False,
             note="gutter present; downpipes discharge to the windbreak"),
        Zone("R3", "South verandah", (7.5, 15.0, 13.0, 2.5), [(20.5, 15.0)], False, note="gutter to the turning area"),
        Zone("R4", "North verandah", (7.5, 32.5, 13.0, 2.5), [(20.5, 35.0)], False, note="gutter to the shade house"),
        Zone("R5", "Shed, north plane", (31.7, 11.0, 8.6, 5.3), [(40.3, 16.3)], False, note="gutter to the apron"),
        Zone("R6", "Shed, south plane", (31.7, 5.7, 8.6, 5.3), [], False, gutter=False, note="no gutter"),
    ],
    points=[
        Point("P1", 44.0, 38.0, "Bore meter", "service"),
        Point("P2", 21.0, 30.5, "Pressure pump and cartridge filter", "service"),
        Point("P3", 5.8, 21.0, "Septic tank (approximate)", "service", ESTIMATE),
        Point("P4", 20.0, 14.2, "Switchboard and shed submain", "service"),
        Point("P5", 22.0, 21.0, "Carted-water fill point", "service"),
        Point("L1", 25.0, 0.5, "RL 100.0", "level", ESTIMATE),
        Point("L2", 25.0, 39.5, "RL 100.4", "level", ESTIMATE),
        Point("A1", 25.5, 0.6, "Access from the road", "access"),
    ],
    easements=[
        {"id": "X1", "x": 0.5, "y": 3.0, "w": 6.5, "h": 12.5, "label": "Septic trench exclusion",
         "note": "trenches drawn from the 1994 approval; position not verified on the ground", "status": ESTIMATE},
    ],
    floor_extent=(12.0, 14.0),
    rooms=[
        Rect("F1", 0.0, 0.0, 4.4, 5.0, "Kitchen", "wet", "sink and dishwasher"),
        Rect("F2", 4.4, 0.0, 2.8, 5.0, "Laundry", "wet", "tub and machine; door to the south verandah"),
        Rect("F3", 7.2, 0.0, 2.6, 3.0, "Bathroom", "wet", "shower and basin"),
        Rect("F4", 7.2, 3.0, 2.6, 2.0, "WC", "wet"),
        Rect("F5", 9.8, 0.0, 2.2, 5.0, "Store and hot-water cylinder", "service", "solar hot water on the north roof"),
        Rect("F6", 0.0, 5.0, 7.0, 5.0, "Living and dining", "room"),
        Rect("F7", 7.0, 5.0, 5.0, 5.0, "Bedroom 1 and ensuite", "wet", "second shower"),
        Rect("F8", 0.0, 10.0, 4.0, 4.0, "Bedroom 2", "room"),
        Rect("F9", 4.0, 10.0, 4.0, 4.0, "Bedroom 3", "room"),
        Rect("F10", 8.0, 10.0, 4.0, 4.0, "Office", "room"),
    ],
    floor_points=[Point("Q1", 5.8, 0.0, "Laundry door", "access")],
    slope=Fact("Nearly level: about 0.4 m of fall across the working area, from a handheld level survey. The wider parcel falls gently to a sandy swale along its eastern boundary.", ESTIMATE),
    services=[
        ("Water", Fact("No reticulated supply. The house runs on the tank and the bore, topped up by a water carrier who fills the tank.")),
        ("Sewer", Fact("Not connected. Septic tank and absorption trenches south-west of the house; their age and exact position are not known.", UNKNOWN)),
        ("Power", Fact("Overhead single phase, 80 A; submain to the shed.")),
        ("Gas", Fact("Bottled LPG for cooking.")),
        ("Stormwater", Fact("Sheet flow to the swale. No piped drainage.")),
    ],
    inventory=[
        Fact("22 kL steel-lined tank (2014) on the house east plane, with a pressure pump and a cartridge filter to the house."),
        Fact("Licensed bore with a meter and a submersible pump; allocation 100 kL a year. Bore water is pumped into the same tank."),
        Fact("Shade house over about 40 m², 50 per cent cloth, ten years old."),
        Fact("Drip lines on the shade-house vegetables (40 m²) and a 50 m² fruit block of citrus, pomegranate and grapes in the main garden, from the tank through the pressure pump, manual tap timer, no filter."),
        Fact("Two 1,000 L IBC totes, not plumbed."),
        Fact("Olives and figs established on the windbreak."),
    ],
    observations=[
        "“We cart water most summers. That is the thing I actually want to stop.”",
        "“If a part fails I want to buy it in town, not wait two weeks for a courier.”",
        "“The drip lines block up. I do not know what with.”",
        "“The trial plot cooked. Melons in January was not clever.”",
    ],
    priorities=[
        "Cart as little water as possible, and none at all in an ordinary year if that can be done.",
        "Never exceed the 100 kL bore allocation, with the meter as the evidence.",
        "Equipment the family can maintain with parts sold in Alice Springs.",
        "Get the shade-house vegetables and the drip-watered fruit block, about 90 m² together, producing reliably.",
    ],
    constraints=[
        Fact("The bore allocation is 100 kL a year and is not exceeded. The course's draw rule is at most one-twelfth of the allocation in any month."),
        Fact("Maintenance: up to 4 hours a week. The household is comfortable with mechanical work and daily checks."),
        Fact("Installation zones: new tanks on the gravel turning area or the shed apron. Nothing in the septic exclusion zone."),
        Fact("Disruption: the shed stays usable throughout; up to ten working days on site."),
        Fact("Permitted uses: all household uses from the tank, as now, and garden irrigation. Carted water is delivered into the tank by a licensed potable-water carrier."),
        Fact("Common parts: every pump, filter and fitting must be a type stocked in Alice Springs. Specialist modules are acceptable only with a local service arrangement."),
    ],
    unknowns=[
        "What blocks the drip emitters: bore-water hardness, biofilm, or sediment from the tank.",
        "Bore-water quality: hardness, dissolved solids and iron.",
        "How the bore draw actually splits month by month against the allocation.",
        "Where the septic trenches are and whether they still work.",
        "How much light the shade house lets through after ten years.",
        "The household's real indoor use when nobody is rationing it.",
    ],
    permitted_tank_uses=("toilet", "laundry", "shower", "kitchen", "other", "garden"),
    bore_uses=("toilet", "laundry", "shower", "kitchen", "other", "garden"),
    max_new_storage_kl=90.0,
    maintenance_h_week=4.0,
    min_attendance_days=1,
    unattended_days=14,
    excluded_modules=("aquaponics",),
    existing_irrigated_m2=90.0,
    existing_irrigation="tank_drip",
    existing_pressure_pump=True,
    existing_garden_pump=False,
    existing_tank_uses=("toilet", "laundry", "shower", "kitchen", "other", "garden"),
    priority_zones=(("G1", 40.0), ("G2", 50.0)),
    zone_quality={"G1": 0.90, "G2": 0.85, "G3": 0.50, "G4": 0.70},
    priority_perennial_share=0.55,
    existing_timer_share=0.30,
    mains=False,
    parcel={
        "extent": (100.0, 200.0),
        "working_area": (25.0, 5.0, 50.0, 40.0),
        "features": [
            {"id": "K1", "x": 0.0, "y": 197.0, "w": 100.0, "h": 3.0, "label": "Access easement (3 m) in favour of the lot to the north", "kind": "easement"},
            {"id": "K2", "x": 90.0, "y": 0.0, "w": 10.0, "h": 197.0, "label": "Sandy swale", "kind": "drainage"},
            {"id": "K3", "x": 0.0, "y": 45.0, "w": 90.0, "h": 152.0, "label": "Native vegetation, not available", "kind": "retained"},
        ],
        "road": "south",
        "note": "Only the working area is available for the design. The rest of the parcel is retained native vegetation under the zoning, a case assumption.",
    },
)

# ---------------------------------------------------------------------------
# S3 Brisbane — the Patel family
# ---------------------------------------------------------------------------
BRISBANE = Home(
    sid="S3", slug="brisbane", short="Brisbane", family="Patel",
    household="Priya and Rohan Patel and their two children, aged 9 and 11",
    place="Brisbane, Queensland",
    dwelling="Two-storey townhouse (2006) with an internal garage, in a nine-lot community titles scheme",
    tenure="Owner-occupied lot. Body corporate consent is needed for anything visible, attached or changing stormwater.",
    parcel_m2=300, plan_extent=(10.0, 30.0),
    cover=[
        Rect("B1", 0.0, 5.0, 9.2, 14.0, "Townhouse", "building", "two storey; party wall on the west boundary", (0.0, 0.4, 0.4, 0.4)),
        Rect("B2", 7.2, 22.0, 2.0, 2.0, "Store", "building", "steel, no gutter", E(0.2)),
        Rect("H1", 0.0, 0.0, 3.5, 5.0, "Driveway apron", "hardstand", "meets the scheme's common driveway"),
        Rect("H2", 9.2, 5.0, 0.8, 25.0, "Side path", "hardstand", "0.8 m between wall and fence; 600 mm clear past the meter box and downpipes"),
        Rect("H3", 0.0, 19.0, 7.2, 5.0, "Courtyard", "hardstand", "paved; the family's outdoor room"),
        Rect("H4", 7.2, 19.0, 2.0, 3.0, "Courtyard, east", "hardstand", "paved"),
        Rect("G1", 3.5, 0.0, 6.5, 5.0, "Front bed", "growing", "visible from the common driveway"),
        Rect("G2", 0.0, 24.0, 9.2, 6.0, "Rear garden", "growing", "morning sun; shaded after about 11 am by the neighbour's poinciana"),
    ],
    roofover=[
        Rect("V1", 0.0, 19.4, 5.0, 3.6, "Patio roof", "roofover", "polycarbonate over the sitting area", (0.0, 0.2, 0.0, 0.2)),
    ],
    circles=[
        Circle("T1", 7.3, 19.4, 0.0, "Existing 3 kL slimline tank", "tank", "poly, 2018, rear roof plane, gravity tap", kl=3, w=2.4, h=0.6),
        Circle("E1", 4.5, 33.5, 4.5, "Neighbour's poinciana", "tree", "off-site; canopy over the rear garden", offsite=True),
        Circle("E2", 6.2, 2.2, 0.6, "Dwarf citrus (pot)", "tree", "movable"),
    ],
    zones=[
        Zone("R1", "Townhouse, front plane", (0.0, 4.6, 9.6, 7.4), [(9.6, 4.6)], False,
             note="to the scheme's driveway drain"),
        Zone("R2", "Townhouse, rear plane", (0.0, 12.0, 9.6, 7.4), [(9.6, 19.4)], True,
             note="the only zone on the 3 kL slimline tank"),
        Zone("R3", "Patio roof", (0.0, 19.4, 5.2, 3.8), [(5.2, 23.2)], False, note="gutter to the courtyard drain"),
        Zone("R4", "Store", (7.0, 21.8, 2.4, 2.4), [], False, gutter=False, note="no gutter"),
    ],
    points=[
        Point("P1", 9.6, 5.6, "Meter box and water meter", "service"),
        Point("P2", 0.6, 23.4, "Sewer connection (lot)", "service", KNOWN, "scheme drain inspection point"),
        Point("P4", 3.6, 23.6, "Courtyard drain to common stormwater", "service"),
        Point("L1", 5.0, 0.4, "RL 100.0", "level", ESTIMATE),
        Point("L2", 5.0, 29.6, "RL 100.2", "level", ESTIMATE),
        Point("A1", 9.6, 1.0, "Pedestrian access: side path only", "access"),
    ],
    easements=[
        {"id": "X1", "x": 0.0, "y": 28.5, "w": 9.2, "h": 1.5, "label": "Common-property services easement",
         "note": "scheme services cross the rear 1.5 m; no structures", "status": KNOWN},
    ],
    floor_extent=(9.2, 14.0),
    rooms=[
        Rect("F1", 0.0, 0.0, 3.4, 6.0, "Garage", "room", "single car; water heater on the rear wall"),
        Rect("F2", 3.4, 0.0, 3.0, 3.0, "Entry and stair", "room"),
        Rect("F3", 6.4, 0.0, 2.8, 3.0, "Meter cupboard and riser", "service"),
        Rect("F4", 3.4, 3.0, 2.4, 3.0, "Laundry", "wet", "internal, no external door"),
        Rect("F5", 5.8, 3.0, 1.6, 3.0, "WC", "wet", "ground floor"),
        Rect("F6", 7.4, 3.0, 1.8, 3.0, "Store", "room"),
        Rect("F7", 0.0, 6.0, 5.2, 8.0, "Living and dining", "room"),
        Rect("F8", 5.2, 6.0, 4.0, 8.0, "Kitchen", "wet", "sink and dishwasher; bathroom above"),
    ],
    floor_points=[Point("Q1", 7.2, 14.0, "Stack from the first-floor bathroom", "service")],
    slope=Fact("Essentially level: the lot falls about 0.2 m to the common driveway, which is its only drainage outlet. Levels are from the 2006 scheme plan.", ESTIMATE),
    services=[
        ("Water", Fact("Mains, individually metered in the meter box beside the side path.")),
        ("Sewer", Fact("Connected to the scheme's common drain; the lot's inspection point is in the courtyard.")),
        ("Power", Fact("Underground supply, 40 A single phase, individually metered.")),
        ("Gas", Fact("None.")),
        ("Stormwater", Fact("Roof and courtyard drain to the common system. Any change needs body corporate consent.")),
    ],
    inventory=[
        Fact("3 kL slimline poly tank (2018) on the rear roof plane, beside the courtyard, gravity tap."),
        Fact("Four self-watering planter boxes and about 10 m² of the rear garden in vegetables, 12 m² in all, watered from the tank tap."),
        Fact("Dwarf citrus in a pot."),
        Fact("Worm farm, 60 L."),
        Fact("An exclusive-use allocation of 40 m² in the scheme's shared garden (common property, outside the lot)."),
    ],
    observations=[
        "“Whatever we do has to get past the body corporate, and it cannot be loud.”",
        "“The side path is 600 mm clear. Everything has to come through it.”",
        "“The back garden gets sun until about eleven and then nothing.”",
        "“We have 40 m² in the shared garden but we do not own it.”",
    ],
    priorities=[
        "Grow something worthwhile in a small space without losing the courtyard.",
        "Nothing the body corporate will refuse, and nothing audible at the boundary at night.",
        "Compact equipment that fits through a 600 mm path.",
        "Use the shared-garden allocation well, without installing anything on it.",
    ],
    constraints=[
        Fact("Body corporate consent is needed for any external attachment, any tank over 1.8 m tall, and any change to stormwater. Assume consent is refused for plant audible above 45 dB(A) at a boundary at night."),
        Fact("Retained courtyard: the 20 m² sitting area under the patio roof stays clear."),
        Fact("Maintenance: up to 3 hours a week."),
        Fact("Installation zones: inside the lot, and only where a component can come through a 600 mm path. No plant on common property."),
        Fact("Permitted uses of rainwater: garden irrigation and toilet flushing. The laundry is internal and the family will not open walls for it."),
        Fact("The 40 m² shared-garden allocation may be cultivated and hand-watered from the scheme's garden tap, but nothing may be installed on it. The allocation can be revoked by the body corporate."),
    ],
    unknowns=[
        "How much usable light the rear garden and the front bed get through the year.",
        "Whether the body corporate will consent to connecting the front roof plane to storage.",
        "The level of the common drain, which limits any gravity overflow.",
        "Soil depth and quality in the front bed and rear garden, which sit on 2006 fill.",
        "Whether the shared-garden tap is metered to the scheme or to the lots.",
    ],
    permitted_tank_uses=("toilet", "garden"),
    max_new_storage_kl=4.0,
    storage_kind="slimline",
    maintenance_h_week=3.0,
    min_attendance_days=2,
    unattended_days=14,
    excluded_modules=("digester",),
    existing_irrigated_m2=12.0,
    existing_irrigation="tank_gravity",
    priority_zones=(("G2", 12.0),),
    zone_quality={"G1": 0.80, "G2": 0.55, "SG": 0.90},
    shared_allocation_m2=40.0,
    mains=True,
    scheme={
        "extent": (62.0, 66.0),
        "lots": [{"n": n, "x": (n - 1) * 10.0, "y": 36.0, "w": 10.0, "h": 30.0} for n in range(1, 6)]
                + [{"n": n, "x": (n - 6) * 10.0, "y": 0.0, "w": 10.0, "h": 30.0} for n in range(6, 10)],
        "patel_lot": 4,
        "driveway": (0.0, 30.0, 62.0, 6.0),
        "parking": (40.0, 0.0, 10.0, 30.0),
        "garden": (50.0, 0.0, 12.0, 30.0),
        "allocation": (52.0, 20.0, 8.0, 5.0),
        "street": "east",
        "note": "Scheme plan, schematic and not to survey. Lots 1 to 9 are private. The common driveway, visitor parking and the 360 m² shared garden are common property. The Patel allocation is 40 m² of the shared garden, held by body corporate resolution, and is not part of their 300 m² lot (lot 4).",
    },
)

# ---------------------------------------------------------------------------
# S4 Adelaide — the Rossi family
# ---------------------------------------------------------------------------
ADELAIDE = Home(
    sid="S4", slug="adelaide", short="Adelaide", family="Rossi",
    household="Elena and Marco Rossi and their two children, aged 10 and 12",
    place="Adelaide, South Australia",
    dwelling="Double-brick house (1965) with a detached garage reached by a side driveway",
    tenure="Owner-occupied freehold. No body corporate.",
    parcel_m2=700, plan_extent=(17.5, 40.0),
    cover=[
        Rect("B1", 1.2, 7.0, 11.0, 15.0, "House", "building", "double brick, tiled roof", E(0.5)),
        Rect("B2", 12.5, 26.0, 5.0, 6.0, "Garage", "building", "boundary wall to the east, tiled roof", (0.4, 0.0, 0.4, 0.4)),
        Rect("H1", 13.6, 0.0, 3.9, 26.0, "Driveway", "hardstand", "concrete, falls to the street"),
        Rect("H2", 1.2, 22.5, 10.0, 3.5, "Pergola terrace", "hardstand", "open vine pergola, no roof"),
        Rect("G1", 0.0, 0.0, 13.6, 7.0, "Front garden", "growing", "roses and shrubs; full sun"),
        Rect("G2", 0.0, 7.0, 1.2, 15.5, "West border", "growing", "narrow; afternoon sun"),
        Rect("G3", 9.0, 26.0, 3.5, 7.5, "Vegetable beds", "growing", "four raised beds in use"),
        Rect("G4", 12.5, 32.0, 5.0, 8.0, "Orchard corner", "growing", "lemon, almond, apricot"),
        Rect("G5", 0.0, 33.5, 12.5, 6.5, "North bed", "growing", "best aspect"),
        Rect("C1", 0.0, 26.0, 9.0, 7.5, "Back lawn", "recreation", "kept as lawn"),
    ],
    roofover=[],
    circles=[
        Circle("T1", 12.5, 24.9, 0.9, "Existing 5 kL tank", "tank", "poly, 2011, garage roof, 0.4 kW pump to two garden taps", kl=5),
        Circle("E1", 15.0, 34.5, 1.9, "Lemon", "tree", "productive"),
        Circle("E2", 15.0, 38.0, 1.7, "Almond", "tree", "old, mostly dead"),
        Circle("E3", 2.2, 37.0, 1.8, "Apricot", "tree", ""),
    ],
    zones=[
        Zone("R1", "House, north plane", (0.7, 14.5, 12.0, 8.0), [(0.7, 22.5), (12.7, 22.5)], False, note="to the street gutter"),
        Zone("R2", "House, south plane", (0.7, 6.5, 12.0, 8.0), [(0.7, 6.5), (12.7, 6.5)], False, note="to the street gutter"),
        Zone("R3", "Garage", (12.1, 25.6, 5.4, 6.8), [(12.1, 25.6)], True, note="the only zone on the 5 kL tank"),
    ],
    points=[
        Point("P1", 13.9, 0.4, "Water meter", "service"),
        Point("P2", 12.7, 12.0, "Electric storage hot-water unit", "service"),
        Point("P3", 12.7, 9.0, "Switchboard and 5 kW solar inverter", "service"),
        Point("P4", 1.0, 6.8, "Sewer connection (approximate)", "service", ESTIMATE, "drain assumed to leave the south-west corner"),
        Point("P5", 17.1, 1.6, "Stormwater to kerb", "service"),
        Point("L1", 7.0, 0.5, "RL 100.0", "level", ESTIMATE),
        Point("L2", 7.0, 39.5, "RL 100.9", "level", ESTIMATE),
        Point("A1", 15.5, 1.0, "Vehicle access", "access"),
    ],
    easements=[],
    floor_extent=(11.0, 15.0),
    rooms=[
        Rect("F1", 0.0, 0.0, 3.8, 4.4, "Bedroom 2", "room"),
        Rect("F2", 3.8, 0.0, 3.6, 4.4, "Bedroom 3", "room"),
        Rect("F3", 7.4, 0.0, 3.6, 4.4, "Bedroom 1", "room"),
        Rect("F4", 0.0, 4.4, 11.0, 1.2, "Hall", "room"),
        Rect("F5", 0.0, 5.6, 5.5, 4.4, "Living", "room"),
        Rect("F6", 5.5, 5.6, 2.6, 4.4, "Bathroom", "wet", "shower and bath"),
        Rect("F7", 8.1, 5.6, 1.3, 4.4, "WC", "wet", "cistern on the east external wall"),
        Rect("F8", 9.4, 5.6, 1.6, 4.4, "Laundry", "wet", "tub and machine; external door east"),
        Rect("F9", 0.0, 10.0, 6.0, 5.0, "Dining", "room"),
        Rect("F10", 6.0, 10.0, 5.0, 5.0, "Kitchen", "wet", "sink and dishwasher"),
    ],
    floor_points=[Point("Q1", 11.0, 7.8, "Laundry door", "access")],
    slope=Fact("Falls about 0.9 m from the rear fence to the street, roughly 2 per cent, estimated from council contours. The back garden is the high end.", ESTIMATE),
    services=[
        ("Water", Fact("Mains, 20 mm meter at the front boundary.")),
        ("Sewer", Fact("Connected; the main is in the street. Where the house drain leaves has not been checked.", ESTIMATE)),
        ("Power", Fact("Overhead, 63 A single phase, with a 5 kW rooftop solar system.")),
        ("Gas", Fact("Natural gas for cooking.")),
        ("Stormwater", Fact("Roof and driveway to the street kerb.")),
    ],
    inventory=[
        Fact("5 kL poly tank (2011) on the garage roof, with a 0.4 kW pump to two garden taps."),
        Fact("Four raised vegetable beds, about 22 m² in total, in use."),
        Fact("Lemon, almond and apricot trees."),
        Fact("Two 220 L compost bins."),
        Fact("Drip line on the vegetable beds, fed from the mains through a tap timer."),
        Fact("Unglazed greenhouse frame, 4 m²."),
    ],
    observations=[
        "“Every January the beds go backwards and the water bill goes up. Both annoy me.”",
        "“I want to know what it costs to run before I agree to it.”",
        "“The almond is mostly dead. I would replace it if something better grows here.”",
        "“We keep the back lawn. That is not negotiable.”",
    ],
    priorities=[
        "Reliable summer irrigation for the beds and fruit trees without a rising water bill.",
        "A food garden that stays manageable across the year instead of peaking and collapsing.",
        "Running costs that are low, predictable and stated in dollars a year.",
    ],
    constraints=[
        Fact("Retained recreation: the 67.5 m² back lawn stays."),
        Fact("Maintenance: up to 3 hours a week. Routine work yes; fault-finding no."),
        Fact("Installation zones: new tanks along the driveway edge beside the house or behind the garage. Nothing forward of the house; the driveway must stay 3 m clear."),
        Fact("Disruption: up to seven working days. The family will not open any internal wall."),
        Fact("Permitted uses of rainwater: garden irrigation and laundry; toilet flushing if the cistern can be supplied without opening an internal wall."),
        Fact("Running cost: the family asks for new running costs under $250 a year, and a stated reason if that is exceeded."),
    ],
    unknowns=[
        "Whether the January decline is water, heat or nitrogen.",
        "Soil pH and salinity in the vegetable beds after decades of mains water.",
        "How the 12-month water use splits between indoors and the garden.",
        "Whether the WC cistern can be supplied from outside.",
        "The existing drip line's flow rate and uniformity.",
    ],
    permitted_tank_uses=("toilet", "laundry", "garden"),
    max_new_storage_kl=15.0,
    maintenance_h_week=3.0,
    min_attendance_days=2,
    unattended_days=14,
    excluded_modules=(),
    existing_irrigated_m2=56.0,
    existing_irrigation="mains_drip",
    existing_garden_pump=True,
    priority_zones=(("G3", 26.0), ("G4", 30.0)),
    zone_quality={"G1": 0.95, "G2": 0.70, "G3": 0.85, "G4": 0.80, "G5": 1.00},
    priority_perennial_share=0.54,
    mains=True,
)

# ---------------------------------------------------------------------------
# S5 Darwin — the Williams family
# ---------------------------------------------------------------------------
DARWIN = Home(
    sid="S5", slug="darwin", short="Darwin", family="Williams",
    household="Kate and Josh Williams and their two children, aged 9 and 13",
    place="Darwin rural area, NT",
    dwelling="Elevated steel-frame house (2008) and a steel shed on a 1 ha block",
    tenure="Owner-occupied freehold, rural-residential zoning.",
    parcel_m2=10000, plan_extent=(60.0, 40.0),
    cover=[
        Rect("B1", 12.0, 16.0, 13.0, 15.0, "Elevated house", "building", "on piers; shaded storage slab underneath", E(0.9)),
        Rect("B2", 36.0, 8.0, 6.0, 8.0, "Shed", "building", "steel", E(0.3)),
        Rect("H1", 26.0, 0.0, 9.0, 14.0, "Gravel drive and turnaround", "hardstand", "unsealed"),
        Rect("H2", 42.5, 9.0, 6.0, 6.0, "Shed apron", "hardstand", "concrete"),
        Rect("G1", 12.0, 33.0, 14.0, 7.0, "North garden", "growing", "productive in the wet, marginal in the dry"),
        Rect("G2", 31.0, 18.0, 12.0, 16.0, "Main garden", "growing", "banana, pawpaw, cassava, sweet potato"),
        Rect("G3", 2.0, 15.0, 8.0, 18.0, "West orchard", "growing", "mango and citrus"),
        Rect("G4", 46.0, 18.0, 8.0, 9.0, "Nursery area", "growing", "shadecloth frame over about 20 m²"),
        Rect("C1", 12.0, 3.0, 10.0, 9.0, "Shaded yard", "recreation", "under the native fig; kept"),
    ],
    roofover=[],
    circles=[
        Circle("T1", 28.3, 21.8, 1.8, "Existing tank 1 (22.5 kL)", "tank", "poly, 2016", kl=22.5),
        Circle("T2", 28.3, 26.3, 1.8, "Existing tank 2 (22.5 kL)", "tank", "poly, 2016", kl=22.5),
        Circle("E1", 5.5, 19.5, 3.5, "Mango", "tree", "large, dense shade"),
        Circle("E2", 5.5, 28.0, 2.5, "Citrus", "tree", ""),
        Circle("E3", 17.0, 7.5, 4.0, "Native fig", "tree", "shades the yard"),
    ],
    zones=[
        Zone("R1", "House, east plane", (18.5, 15.1, 7.4, 16.8), [(25.9, 20.0), (25.9, 28.0)], True,
             note="plumbed to both tanks; carries the 6.6 kW solar array"),
        Zone("R2", "House, west plane", (11.1, 15.1, 7.4, 16.8), [(11.1, 18.0), (11.1, 29.0)], False,
             note="gutter present; downpipes discharge beside the piers"),
        Zone("R3", "Shed, north plane", (35.7, 12.0, 6.6, 4.3), [(42.3, 16.3)], False, note="gutter fitted"),
        Zone("R4", "Shed, south plane", (35.7, 7.7, 6.6, 4.3), [(42.3, 7.7)], False, note="gutter fitted"),
    ],
    points=[
        Point("P1", 27.0, 19.0, "Pressure pump and cartridge filter", "service"),
        Point("P2", 25.9, 30.5, "Switchboard and inverter", "service"),
        Point("P3", 33.0, 35.5, "Septic tank (approximate)", "service", ESTIMATE),
        Point("P4", 30.5, 23.5, "Carted-water fill point", "service"),
        Point("O1", 30.2, 28.5, "Tank overflow (current)", "overflow", KNOWN, "discharges beside the piers"),
        Point("L1", 5.0, 39.0, "RL 100.8", "level", ESTIMATE),
        Point("L2", 55.0, 1.0, "RL 100.0", "level", ESTIMATE),
        Point("A1", 30.5, 0.6, "Access from the road", "access"),
    ],
    easements=[
        {"id": "X1", "x": 27.0, "y": 34.5, "w": 12.0, "h": 5.5, "label": "Septic trench exclusion",
         "note": "trench position from the 2008 approval plan; not verified", "status": ESTIMATE},
    ],
    floor_extent=(13.0, 15.0),
    rooms=[
        Rect("F1", 0.0, 0.0, 4.4, 5.0, "Kitchen", "wet", "sink and dishwasher"),
        Rect("F2", 4.4, 0.0, 3.0, 5.0, "Laundry", "wet", "tub and machine; external stair"),
        Rect("F3", 7.4, 0.0, 3.0, 2.8, "Bathroom", "wet", "shower"),
        Rect("F4", 7.4, 2.8, 3.0, 2.2, "WC", "wet"),
        Rect("F5", 10.4, 0.0, 2.6, 5.0, "Store", "service", "solar hot water on the roof"),
        Rect("F6", 0.0, 5.0, 7.0, 5.5, "Open living", "room", "louvred, cross-ventilated"),
        Rect("F7", 7.0, 5.0, 6.0, 5.5, "Bedroom 1 and ensuite", "wet", "second shower"),
        Rect("F8", 0.0, 10.5, 4.3, 4.5, "Bedroom 2", "room"),
        Rect("F9", 4.3, 10.5, 4.3, 4.5, "Bedroom 3", "room"),
        Rect("F10", 8.6, 10.5, 4.4, 4.5, "Verandah room", "room"),
    ],
    floor_points=[Point("Q1", 5.9, 0.0, "Laundry stair", "access")],
    slope=Fact("The working area falls about 0.8 m to the south-east, where wet-season sheet flow crosses the drive. Estimated from the NT contour layer; not surveyed.", ESTIMATE),
    services=[
        ("Water", Fact("No reticulated supply. Tank water, with carted top-ups delivered into the tanks in the late dry season.")),
        ("Sewer", Fact("Not connected. Septic tank and trenches north-east of the house; trench position unverified.", ESTIMATE)),
        ("Power", Fact("Overhead single phase, 80 A, with a 6.6 kW solar array on the east roof plane.")),
        ("Gas", Fact("Bottled LPG.")),
        ("Stormwater", Fact("Sheet flow. Tank overflow currently discharges beside the house piers.")),
    ],
    inventory=[
        Fact("Two 22.5 kL poly tanks, 45 kL in total (2016), on the house east plane, with a pressure pump and cartridge filter."),
        Fact("Shadecloth frame over about 20 m² in the nursery area."),
        Fact("Mango and citrus; banana, pawpaw, cassava and sweet potato in the main garden."),
        Fact("Two timber compost bays, about 1.5 m³ each."),
        Fact("Drip and micro-sprays on the main garden, manual valves."),
        Fact("6.6 kW solar array on the east roof plane."),
    ],
    observations=[
        "“In the wet the tanks overflow for weeks. In October we buy water. It is absurd.”",
        "“We are away for four weeks every July and things have to keep running.”",
        "“The overflow washes out under the house. I want that dealt with.”",
        "“Anything I cannot service myself in the wet is no use to me.”",
    ],
    priorities=[
        "Carry enough of the wet season into the dry to stop buying water.",
        "Systems that run unattended through a four-week absence in July.",
        "Overflow sent somewhere deliberate instead of under the house.",
        "Keep the fruit trees and the main garden producing through the dry.",
    ],
    constraints=[
        Fact("Retained recreation: the 90 m² shaded yard stays."),
        Fact("Maintenance: up to 4 hours a week when home. Nothing may need attention during the four-week July absence."),
        Fact("Installation zones: new tanks on the gravel turnaround or the shed apron. Nothing in the septic exclusion zone and nothing under the house."),
        Fact("Disruption: up to ten working days. The solar array must not be disturbed."),
        Fact("Permitted uses: all household uses from the tanks, as now, and garden irrigation. Carted water is delivered by a licensed potable-water carrier."),
        Fact("Overflow must go to a nominated discharge point away from the piers. This is a requirement, not an option."),
    ],
    unknowns=[
        "How far into the dry season the existing 45 kL lasts, month by month.",
        "How much overflows in the wet, and where it goes.",
        "Whether the west gutter falls the right way for new downpipes.",
        "Soil infiltration at a possible overflow discharge point.",
        "Tank water quality after a wet season of leaf litter.",
    ],
    permitted_tank_uses=("toilet", "laundry", "shower", "kitchen", "other", "garden"),
    max_new_storage_kl=120.0,
    maintenance_h_week=4.0,
    min_attendance_days=1,
    unattended_days=28,
    excluded_modules=(),
    existing_irrigated_m2=120.0,
    existing_irrigation="tank_drip",
    existing_pressure_pump=True,
    existing_tank_uses=("toilet", "laundry", "shower", "kitchen", "other", "garden"),
    priority_zones=(("G2", 120.0),),
    zone_quality={"G1": 0.90, "G2": 0.95, "G3": 0.60, "G4": 0.80},
    priority_perennial_share=0.60,
    mains=False,
    parcel={
        "extent": (80.0, 125.0),
        "working_area": (10.0, 5.0, 60.0, 40.0),
        "features": [
            {"id": "K1", "x": 58.0, "y": 0.0, "w": 22.0, "h": 30.0, "label": "Seasonal drainage line", "kind": "drainage"},
            {"id": "K2", "x": 0.0, "y": 45.0, "w": 80.0, "h": 80.0, "label": "Savanna woodland, not available", "kind": "retained"},
        ],
        "road": "south",
        "note": "Only the working area is available for the design. The woodland north of it is retained, a case assumption.",
    },
)

HOMES = [CANBERRA, ALICE, BRISBANE, ADELAIDE, DARWIN]
BY_SID = {h.sid: h for h in HOMES}
HOUSEHOLD = "two adults and two children aged 9 to 13"


# ---------------------------------------------------------------------------
# Derived areas and self-checks
# ---------------------------------------------------------------------------
def _overlap(a, b) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ox = min(ax + aw, bx + bw) - max(ax, bx)
    oy = min(ay + ah, by + bh) - max(ay, by)
    return ox * oy if ox > 0 and oy > 0 else 0.0


def _r(rect: Rect) -> tuple:
    return (rect.x, rect.y, rect.w, rect.h)


def totals(home: Home) -> dict:
    by = lambda k: [r for r in home.cover if r.kind == k]
    footprint = sum(r.area for r in by("building"))
    roof_plan = sum(r.roof_area for r in by("building")) + sum(r.roof_area for r in home.roofover)
    zone_sum = sum(z.plan_m2 for z in home.zones)
    connected = sum(z.plan_m2 for z in home.zones if z.connected_now)
    guttered = sum(z.plan_m2 for z in home.zones if z.gutter)
    hardstand = sum(r.area for r in by("hardstand"))
    growing = sum(r.area for r in by("growing"))
    recreation = sum(r.area for r in by("recreation"))
    W, H = home.plan_extent
    drawn = W * H
    residual = drawn - footprint - hardstand - growing - recreation
    cultivable = growing - home.retained_within_envelope_m2
    return {
        "parcel_m2": home.parcel_m2,
        "drawn_m2": round(drawn, 1),
        "footprint_m2": round(footprint, 1),
        "roof_plan_m2": round(roof_plan, 1),
        "roof_zone_sum_m2": round(zone_sum, 1),
        "roof_connected_now_m2": round(connected, 1),
        "roof_guttered_m2": round(guttered, 1),
        "eaves_and_overhead_m2": round(roof_plan - footprint, 1),
        "hardstand_m2": round(hardstand, 1),
        "growing_envelope_m2": round(growing, 1),
        "retained_within_envelope_m2": home.retained_within_envelope_m2,
        "cultivable_max_m2": round(cultivable, 1),
        "recreation_m2": round(recreation, 1),
        "other_m2": round(residual, 1),
        "floor_rooms_m2": round(sum(r.area for r in home.rooms), 1),
        "floor_envelope_m2": round(home.floor_extent[0] * home.floor_extent[1], 1),
        "existing_storage_kl": sum(c.kl for c in home.circles if c.kind == "tank"),
    }


def _close(a, b, what):
    tol = max(TOL_ABS_M2, TOL_REL * max(abs(a), abs(b)))
    return abs(a - b) <= tol, f"{what}: {a:.1f} vs {b:.1f} (tolerance {tol:.1f})"


def check(home: Home) -> list:
    """Every inconsistency a careful reader of the plan could find."""
    t = totals(home)
    p = home.presets
    bad = []
    for ok, msg in (
        _close(t["roof_plan_m2"], p["roof_m2"], f"{home.sid} roof plan vs preset"),
        _close(t["roof_zone_sum_m2"], t["roof_plan_m2"], f"{home.sid} roof zones vs roof plan"),
        _close(t["growing_envelope_m2"], p["growable_m2"], f"{home.sid} growing envelope vs preset"),
    ):
        if not ok:
            bad.append(msg)
    if abs(t["floor_rooms_m2"] - t["floor_envelope_m2"]) > 0.5:
        bad.append(f"{home.sid} rooms {t['floor_rooms_m2']} do not tile the floor {t['floor_envelope_m2']}")
    house = next(r for r in home.cover if r.kind == "building")
    if abs(home.floor_extent[0] - house.w) > 0.01 or abs(home.floor_extent[1] - house.h) > 0.01:
        bad.append(f"{home.sid} floor plan {home.floor_extent} does not match the house footprint {house.w}x{house.h}")
    if abs(t["existing_storage_kl"] - p["existing_storage_kl"]) > 0.01:
        bad.append(f"{home.sid} drawn tanks {t['existing_storage_kl']} kL vs preset {p['existing_storage_kl']}")
    if home.parcel_m2 <= 1000 and abs(t["drawn_m2"] - home.parcel_m2) > 0.5:
        bad.append(f"{home.sid} suburban plan {t['drawn_m2']} m2 is not the whole {home.parcel_m2} m2 lot")
    if t["other_m2"] < -0.01:
        bad.append(f"{home.sid} parts exceed the drawn area by {-t['other_m2']:.1f} m2")

    W, H = home.plan_extent
    inside = lambda x, y, w, h: x >= -0.01 and y >= -0.01 and x + w <= W + 0.01 and y + h <= H + 0.01
    for r in home.cover + home.roofover:
        if not inside(*_r(r)):
            bad.append(f"{home.sid} '{r.label}' leaves the plan")
        if any(r.eaves) and not inside(*r.roof):
            bad.append(f"{home.sid} roof of '{r.label}' overhangs the boundary")
    for c in home.circles:
        if not c.offsite and not inside(*c.box):
            bad.append(f"{home.sid} '{c.label}' leaves the plan")
    for z in home.zones:
        if not inside(*z.rect):
            bad.append(f"{home.sid} roof zone {z.id} leaves the plan")

    # Ground cover must not overlap itself.
    for i, a in enumerate(home.cover):
        for b in home.cover[i + 1:]:
            o = _overlap(_r(a), _r(b))
            if o > 0.01:
                bad.append(f"{home.sid} '{a.label}' overlaps '{b.label}' by {o:.2f} m2")
    # Tanks sit on hardstand, other ground or in a growing zone, never on a building or another tank.
    tanks = [c for c in home.circles if c.kind == "tank"]
    for c in tanks:
        box = c.box
        for r in home.cover:
            if r.kind == "building" and _overlap(box, _r(r)) > 0.01:
                bad.append(f"{home.sid} tank '{c.label}' sits on '{r.label}'")
    for i, a in enumerate(tanks):
        for b in tanks[i + 1:]:
            if _overlap(a.box, b.box) > 0.01:
                bad.append(f"{home.sid} tanks '{a.label}' and '{b.label}' overlap")
    # Roof zones must lie inside a roof outline and not overlap one another.
    outlines = [r.roof for r in home.cover if r.kind == "building"] + [r.roof for r in home.roofover]
    for z in home.zones:
        covered = sum(_overlap(z.rect, o) for o in outlines)
        if covered < z.plan_m2 * 0.98:
            bad.append(f"{home.sid} roof zone {z.id} is not on a roof ({covered:.1f} of {z.plan_m2:.1f} m2)")
    for i, a in enumerate(home.zones):
        for b in home.zones[i + 1:]:
            if _overlap(a.rect, b.rect) > 0.05:
                bad.append(f"{home.sid} roof zones {a.id} and {b.id} overlap")
    # Easements stay inside the plan.
    for e in home.easements:
        if not inside(e["x"], e["y"], e["w"], e["h"]):
            bad.append(f"{home.sid} easement '{e['label']}' leaves the plan")
    # The working area of a rural parcel must sit inside the parcel.
    if home.parcel:
        PW, PH = home.parcel["extent"]
        x, y, w, h = home.parcel["working_area"]
        if (w, h) != home.plan_extent or x < 0 or y < 0 or x + w > PW or y + h > PH:
            bad.append(f"{home.sid} working area does not fit the parcel")
        if abs(PW * PH - home.parcel_m2) > 1:
            bad.append(f"{home.sid} parcel extent {PW}x{PH} is not {home.parcel_m2} m2")
    # A strata scheme: the household's lot is the drawn lot, and the allocation is
    # common property inside the shared garden, never inside a lot.
    if home.scheme:
        sch = home.scheme
        lot = next(l for l in sch["lots"] if l["n"] == sch["patel_lot"])
        if abs(lot["w"] * lot["h"] - home.parcel_m2) > 0.5:
            bad.append(f"{home.sid} scheme lot is not the {home.parcel_m2} m2 lot")
        ax, ay, aw, ah = sch["allocation"]
        gx, gy, gw, gh = sch["garden"]
        if not (ax >= gx and ay >= gy and ax + aw <= gx + gw and ay + ah <= gy + gh):
            bad.append(f"{home.sid} allocation is not inside the shared garden")
        if abs(aw * ah - home.shared_allocation_m2) > 0.5:
            bad.append(f"{home.sid} allocation is {aw * ah} m2, not {home.shared_allocation_m2}")
        for l in sch["lots"]:
            if _overlap((l["x"], l["y"], l["w"], l["h"]), sch["allocation"]) > 0:
                bad.append(f"{home.sid} allocation overlaps lot {l['n']}")
    return bad


def attach_presets():
    from presets import V4
    for s in V4:
        BY_SID[s.sid].presets = {
            "plot_m2": s.plot_m2, "growable_m2": s.growable_m2, "roof_m2": s.roof_m2,
            "shared_growing_m2": s.shared_growing_m2, "existing_storage_kl": s.existing_storage_kl,
            "other_water_kl_year": s.other_water_kl_year, "station": s.station, "label": s.label,
        }


attach_presets()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    problems = []
    for h in HOMES:
        t = totals(h)
        p = h.presets
        bad = check(h)
        problems += bad
        print(f"{h.sid} {h.family:9} parcel {h.parcel_m2:>6.0f}  footprint {t['footprint_m2']:>6.1f}  "
              f"roof {t['roof_plan_m2']:>6.1f} (preset {p['roof_m2']:.0f}, zones {t['roof_zone_sum_m2']:.1f})  "
              f"growing {t['growing_envelope_m2']:>6.1f} (preset {p['growable_m2']:.0f})  "
              f"cultivable {t['cultivable_max_m2']:>6.1f}  connected {t['roof_connected_now_m2']:>5.1f}  "
              f"other {t['other_m2']:>6.1f}")
        for b in bad:
            print("   !", b)
    print("\ngeometry problems:", len(problems) or "none")
