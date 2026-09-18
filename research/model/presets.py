"""Preset site sets evaluated by site_model.py. Each design iteration adds a set rather
than editing an old one, so the critique log can point at before/after numbers."""

from site_model import Site

# v1: planning-chat draft mapped to the nearest long-record BoM station.
# Growable areas were not in the draft; these are the assumptions used to test it.
V1 = [
    Site("S1", "Cool-temperate suburban block", "070014", "detached house", 650, 300, 180),
    Site("S2", "Hot-arid rural lot", "015590", "rural house", 20000, 2000, 220),
    Site("S3", "Humid subtropical peri-urban", "040214", "detached house", 800, 400, 160),
    Site("S4", "Mediterranean townhouse", "023000", "townhouse", 250, 80, 110),
    Site("S5", "Cold upland rural lot", "056037", "rural house", 10000, 1500, 200),
]

# v2a: realistic lot/roof sizes (ABS lot sizes; ~230 m2 new-house floor area -> roof incl.
# garage and eaves ~250 m2), tropical wet-dry replaces the duplicate cool-temperate upland.
V2A = [
    Site("S1", "Cool-temperate inland suburban", "070014", "detached house + garage", 750, 300, 250),
    Site("S2", "Hot-arid rural-residential", "015590", "house + machinery shed", 20000, 600, 450, other_water_kl_year=150),
    Site("S3", "Humid subtropical suburban", "040214", "detached house", 810, 350, 240),
    Site("S4", "Mediterranean townhouse", "023000", "townhouse", 300, 90, 140),
    Site("S5", "Tropical wet-dry rural-residential", "014015", "elevated house + shed", 10000, 600, 350),
]

# v2b: same climates, dwelling types re-paired so the dense-urban case sits in the wettest
# temperate climate and the Mediterranean site is a standard suburban block.
V2B = [
    Site("S1", "Cool-temperate inland suburban", "070014", "detached house + garage", 750, 300, 250),
    Site("S2", "Hot-arid rural-residential", "015590", "house + machinery shed", 20000, 600, 450, other_water_kl_year=150),
    Site("S3", "Humid subtropical townhouse", "040214", "townhouse", 300, 90, 150),
    Site("S4", "Mediterranean suburban", "023000", "detached house", 700, 300, 250),
    Site("S5", "Tropical wet-dry rural-residential", "014015", "elevated house + shed", 10000, 600, 350),
]

PRESET_SETS = {
    "v1 — planning-chat draft": V1,
    "v2a — realistic sizes, Darwin replaces Armidale": V2A,
    "v2b — v2a with townhouse moved to the wet climate": V2B,
}

# v3: start from v2b (better balanced) and add the site inventory levers that real sites of
# each type commonly have: existing tanks, a capped bore allocation in the arid case, and a
# strata community garden for the townhouse.
V3 = [
    Site("S1", "Cool-temperate inland suburban", "070014", "detached house + garage", 750, 300, 250,
         existing_storage_kl=5),
    Site("S2", "Hot-arid rural-residential", "015590", "house + machinery shed", 20000, 600, 450,
         other_water_kl_year=100, existing_storage_kl=22),
    Site("S3", "Humid subtropical townhouse", "040214", "townhouse", 300, 90, 150,
         shared_growing_m2=60, existing_storage_kl=3),
    Site("S4", "Mediterranean suburban", "023000", "detached house", 700, 300, 250, existing_storage_kl=5),
    Site("S5", "Tropical wet-dry rural-residential", "014015", "elevated house + shed", 10000, 600, 350,
         existing_storage_kl=45),
]
PRESET_SETS["v3 — v2b plus site inventory (tanks, capped bore, strata garden)"] = V3

# v4: best balanced set from search_presets.py inside ordinary ranges for each site type.
# Physical levers alone cannot equalise these climates (ease spread stays ~1.4 SD); the
# set is chosen for no dominance and realistic inventories, and fairness moves to scoring.
V4 = [
    Site("S1", "Cool-temperate inland suburban", "070014", "detached house + garage + carport", 800, 450, 300,
         existing_storage_kl=5),
    Site("S2", "Hot-arid rural-residential", "015590", "house + machinery shed", 20000, 400, 350,
         other_water_kl_year=100, existing_storage_kl=22),
    Site("S3", "Humid subtropical townhouse", "040214", "townhouse", 300, 90, 170,
         shared_growing_m2=40, existing_storage_kl=3),
    Site("S4", "Mediterranean suburban", "023000", "detached house", 700, 250, 230, existing_storage_kl=5),
    Site("S5", "Tropical wet-dry rural-residential", "014015", "elevated house + shed", 10000, 500, 300,
         existing_storage_kl=45),
]
PRESET_SETS["v4 — search-balanced inventories"] = V4
