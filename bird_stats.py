"""
Top Trumps style stats for all 100 birds.

Each bird has REAL underlying values, not hand-picked scores out of 100. The
0-100 ratings are worked out by ranking every bird against the other 99 for
each stat, so a rating always means "how does this bird compare to the rest
of the collection" rather than an arbitrary number.

Raw fields per bird:
  length_cm    body length, bill to tail
  weight_g     typical adult weight
  speed_kmh    typical flight speed (not maximum dive speed)
  uk_pop       rough UK population, individuals - log-scaled for the rating,
               since it spans from a few hundred to tens of millions
  song         how impressive the voice is, 1-10
  brains       problem-solving and tool use, 1-10
  habitat      one short phrase for the stat box
  diet         one short phrase for the stat box

Honest note on sourcing: lengths and weights are standard reference figures.
Populations are approximate orders of magnitude from BTO/RSPB estimates.
Flight speeds are typical published values where known and reasoned estimates
from body size and wing shape where not. Song and brains are informed
judgements rather than measurements - they're there to be fun and roughly
right, not authoritative.
"""

# name: (length_cm, weight_g, speed_kmh, uk_pop, song, brains, habitat, diet)
RAW = {
    # --- Gardeners
    "European Robin":        (14, 19, 30, 13000000, 9, 5, "Gardens & parks", "Insects & worms"),
    "Common Blackbird":      (25, 100, 38, 15000000, 10, 5, "Gardens & woodland", "Worms & berries"),
    "House Sparrow":         (15, 30, 38, 10000000, 3, 5, "Towns & farms", "Seeds & scraps"),
    "Dunnock":               (14, 21, 30, 5000000, 6, 4, "Hedges & gardens", "Insects & seeds"),
    "Common Starling":       (21, 80, 60, 5000000, 7, 8, "Towns & farmland", "Insects & fruit"),
    "Common Wood-Pigeon":    (41, 500, 60, 10000000, 4, 4, "Woods & gardens", "Leaves & seeds"),
    "Eurasian Collared-Dove":(32, 200, 55, 2000000, 4, 4, "Towns & gardens", "Seeds & grain"),
    "Rock Pigeon":           (33, 350, 70, 1000000, 3, 7, "Towns & cliffs", "Seeds & scraps"),
    "Eurasian Tree Sparrow": (14, 22, 36, 450000, 3, 5, "Farmland hedges", "Seeds & insects"),
    "European Turtle-Dove":  (27, 150, 60, 6000, 5, 4, "Farmland & scrub", "Seeds"),
    # --- Acrobats
    "Eurasian Blue Tit":     (12, 11, 30, 15000000, 6, 7, "Woods & gardens", "Insects & seeds"),
    "Great Tit":             (14, 18, 32, 10000000, 7, 7, "Woods & gardens", "Insects & seeds"),
    "Coal Tit":              (11, 9, 28, 3000000, 6, 6, "Conifer woods", "Insects & seeds"),
    "Long-tailed Tit":       (14, 8, 27, 1900000, 4, 6, "Hedges & woods", "Tiny insects"),
    "Eurasian Nuthatch":     (14, 24, 32, 500000, 6, 7, "Mature woodland", "Nuts & insects"),
    "Eurasian Treecreeper":  (13, 10, 26, 400000, 5, 5, "Woodland trunks", "Insects in bark"),
    "Goldcrest":             (9, 6, 25, 1300000, 5, 4, "Conifer woods", "Tiny insects"),
    "Eurasian Wren":         (10, 10, 28, 11000000, 9, 5, "Hedges & woods", "Insects & spiders"),
    "Marsh Tit":             (12, 12, 28, 82000, 5, 7, "Damp woodland", "Insects & seeds"),
    "Willow Tit":            (12, 11, 28, 5000, 5, 7, "Wet scrubby woods", "Insects & seeds"),
    # --- Crackers
    "Common Chaffinch":      (15, 24, 35, 12000000, 7, 5, "Woods & gardens", "Seeds & insects"),
    "European Goldfinch":    (12, 16, 35, 3000000, 7, 5, "Gardens & weeds", "Small seeds"),
    "European Greenfinch":   (15, 28, 35, 1000000, 5, 5, "Gardens & hedges", "Seeds & buds"),
    "Common Linnet":         (13, 18, 35, 1800000, 6, 5, "Heath & farmland", "Small seeds"),
    "Eurasian Bullfinch":    (16, 25, 32, 500000, 4, 5, "Woods & hedges", "Buds & seeds"),
    "Eurasian Siskin":       (12, 14, 33, 850000, 6, 5, "Conifer woods", "Conifer seeds"),
    "Yellowhammer":          (16, 27, 32, 1200000, 7, 5, "Farmland hedges", "Seeds & insects"),
    "Reed Bunting":          (15, 20, 30, 500000, 5, 5, "Reeds & marsh", "Seeds & insects"),
    "Hawfinch":              (18, 55, 40, 2000, 3, 6, "Mature woodland", "Hard seeds & stones"),
    "Corn Bunting":          (18, 45, 32, 22000, 4, 4, "Open farmland", "Seeds & insects"),
    # --- Little Loudmouths
    "Eurasian Blackcap":     (14, 18, 32, 3000000, 10, 5, "Woods & gardens", "Insects & berries"),
    "Common Chiffchaff":     (11, 9, 28, 1800000, 6, 5, "Woods & scrub", "Small insects"),
    "Willow Warbler":        (11, 9, 28, 4000000, 8, 5, "Young woodland", "Small insects"),
    "Common Whitethroat":    (14, 16, 30, 2000000, 7, 5, "Hedges & scrub", "Insects & berries"),
    "Sedge Warbler":         (13, 12, 29, 500000, 7, 5, "Reeds & marsh", "Insects"),
    "Eurasian Reed Warbler": (13, 13, 29, 260000, 6, 5, "Reedbeds", "Insects"),
    "European Stonechat":    (12, 15, 30, 120000, 5, 5, "Heath & coast", "Insects"),
    "Common Redstart":       (14, 15, 32, 200000, 7, 5, "Upland woods", "Insects"),
    "Lesser Whitethroat":    (13, 13, 30, 74000, 6, 5, "Thick hedges", "Insects & berries"),
    "Common Firecrest":      (9, 6, 25, 1700, 5, 4, "Conifer woods", "Tiny insects"),
    # --- Mischiefs
    "Eurasian Magpie":       (45, 220, 45, 1300000, 3, 9, "Towns & farmland", "Almost anything"),
    "Eurasian Jay":          (34, 170, 45, 340000, 3, 9, "Oak woodland", "Acorns & insects"),
    "Western Jackdaw":       (34, 240, 55, 3000000, 3, 9, "Towns & cliffs", "Almost anything"),
    "Carrion Crow":          (47, 540, 50, 2000000, 2, 10, "Almost anywhere", "Almost anything"),
    "Rook":                  (45, 480, 50, 2000000, 2, 9, "Farmland & rookeries", "Worms & grain"),
    "Northern Raven":        (64, 1200, 55, 30000, 3, 10, "Cliffs & moors", "Carrion & anything"),
    "Great Spotted Woodpecker":(23, 85, 40, 400000, 4, 7, "Woodland", "Grubs in wood"),
    "European Green Woodpecker":(32, 190, 40, 130000, 4, 7, "Parks & grassland", "Ants"),
    "Lesser Spotted Woodpecker":(15, 22, 35, 2000, 3, 7, "Old woodland", "Grubs in wood"),
    "Common Cuckoo":         (33, 110, 55, 30000, 8, 6, "Woods & moors", "Hairy caterpillars"),
    # --- Little Diggers
    "Song Thrush":           (23, 83, 40, 2400000, 10, 6, "Gardens & woods", "Snails & worms"),
    "Mistle Thrush":         (27, 130, 45, 340000, 8, 6, "Parks & woods", "Berries & worms"),
    "Eurasian Skylark":      (18, 38, 35, 3000000, 10, 5, "Open farmland", "Seeds & insects"),
    "Common Pheasant":       (65, 1200, 45, 4000000, 2, 4, "Farmland & woods", "Seeds & shoots"),
    "White Wagtail":         (18, 21, 35, 900000, 4, 5, "Open ground & water", "Insects"),
    "Grey Wagtail":          (19, 18, 35, 76000, 4, 5, "Fast streams", "Insects"),
    "Meadow Pipit":          (15, 18, 32, 4000000, 6, 4, "Moors & grassland", "Insects"),
    "Redwing":               (21, 63, 45, 700000, 6, 5, "Fields & hedges", "Berries & worms"),
    "Grey Partridge":        (30, 390, 45, 74000, 3, 4, "Open farmland", "Seeds & shoots"),
    "Ring Ouzel":            (24, 110, 45, 12000, 8, 5, "Upland crags", "Worms & berries"),
    # --- Sky Divers
    "Common Buzzard":        (54, 780, 45, 250000, 3, 7, "Farmland & woods", "Rabbits & carrion"),
    "Common Kestrel":        (34, 190, 55, 90000, 2, 7, "Farmland & verges", "Voles & insects"),
    "Eurasian Sparrowhawk":  (33, 220, 50, 100000, 2, 7, "Woods & gardens", "Small birds"),
    "Red Kite":              (63, 1000, 45, 12000, 2, 7, "Farmland & woods", "Carrion & scraps"),
    "Peregrine Falcon":      (46, 750, 65, 4500, 2, 7, "Cliffs & cities", "Birds in flight"),
    "Tawny Owl":             (38, 440, 40, 100000, 7, 7, "Woodland", "Voles & birds"),
    "Barn Owl":              (34, 330, 35, 12000, 3, 6, "Farmland & barns", "Voles & mice"),
    "Little Owl":            (22, 180, 40, 8000, 4, 6, "Farmland & orchards", "Insects & voles"),
    "Eurasian Hobby":        (32, 210, 60, 2800, 3, 7, "Heath & farmland", "Dragonflies & swallows"),
    "Long-eared Owl":        (36, 290, 40, 3500, 4, 6, "Conifer woods", "Voles & mice"),
    # --- Swimmers
    "Mallard":               (58, 1100, 60, 1000000, 3, 6, "Ponds & rivers", "Plants & insects"),
    "Mute Swan":             (150, 11000, 55, 75000, 2, 6, "Lakes & rivers", "Water plants"),
    "Canada Goose":          (95, 4500, 60, 200000, 2, 6, "Parks & lakes", "Grass & water plants"),
    "Greylag Goose":         (84, 3300, 60, 150000, 3, 6, "Lakes & marshes", "Grass & grain"),
    "Eurasian Coot":         (38, 800, 40, 200000, 2, 5, "Lakes & ponds", "Water plants"),
    "Common Moorhen":        (33, 320, 35, 250000, 3, 5, "Ponds & ditches", "Plants & insects"),
    "Little Grebe":          (27, 150, 40, 16000, 4, 5, "Ponds & canals", "Small fish & insects"),
    "Great Crested Grebe":   (48, 1000, 50, 19000, 3, 5, "Lakes & reservoirs", "Fish"),
    "Common Kingfisher":     (17, 40, 45, 14000, 2, 6, "Clear rivers", "Small fish"),
    "Common Eider":          (60, 2200, 70, 60000, 3, 5, "Rocky coasts", "Mussels & crabs"),
    # --- Mud Stompers
    "Grey Heron":            (95, 1600, 45, 40000, 2, 7, "Rivers & lakes", "Fish & frogs"),
    "Eurasian Oystercatcher":(43, 540, 55, 340000, 4, 5, "Coasts & fields", "Shellfish & worms"),
    "Common Ringed Plover":  (19, 64, 55, 15000, 4, 4, "Shingle beaches", "Insects & worms"),
    "Sanderling":            (20, 55, 60, 20000, 3, 4, "Sandy beaches", "Sand shrimps"),
    "Ruddy Turnstone":       (23, 110, 55, 48000, 3, 5, "Rocky shores", "Anything under stones"),
    "Common Sandpiper":      (20, 50, 50, 15000, 5, 4, "Upland rivers", "Insects & worms"),
    "Common Snipe":          (26, 110, 55, 76000, 6, 4, "Marsh & bog", "Worms in mud"),
    "Northern Lapwing":      (30, 220, 45, 140000, 6, 5, "Wet farmland", "Worms & insects"),
    "Eurasian Curlew":       (55, 800, 50, 125000, 9, 5, "Moors & estuaries", "Worms & crabs"),
    "Eurasian Woodcock":     (34, 300, 45, 55000, 4, 4, "Damp woodland", "Worms in soil"),
    # --- Wind Riders
    "Herring Gull":          (60, 900, 50, 140000, 3, 8, "Coasts & towns", "Fish & scraps"),
    "Black-headed Gull":     (37, 300, 45, 400000, 3, 7, "Coasts & inland", "Insects & scraps"),
    "Common Gull":           (43, 400, 45, 100000, 3, 7, "Coasts & fields", "Worms & fish"),
    "Great Black-backed Gull":(70, 1700, 50, 34000, 2, 8, "Rocky coasts", "Fish & seabirds"),
    "Great Cormorant":       (90, 2500, 60, 62000, 2, 6, "Coasts & lakes", "Fish"),
    "Common Tern":           (34, 120, 55, 24000, 3, 5, "Coasts & gravel pits", "Small fish"),
    "Barn Swallow":          (19, 19, 55, 1400000, 6, 6, "Farmland & barns", "Flying insects"),
    "Common House-Martin":   (13, 18, 50, 1000000, 4, 5, "Towns & villages", "Flying insects"),
    "Northern Gannet":       (92, 3000, 65, 600000, 2, 6, "Sea cliffs", "Fish"),
    "Razorbill":             (40, 700, 65, 200000, 2, 5, "Sea cliffs", "Fish"),
}

STAT_LABELS = {
    "size": "Size", "speed": "Speed", "population": "Population",
    "song": "Song", "brains": "Brains",
}

import math


def _rank_scores(values: dict) -> dict:
    """Turn raw values into 1-100 by rank against every other bird. Rank
    rather than raw scaling, because population spans five orders of
    magnitude and a Wren would otherwise score 1 on everything."""
    ordered = sorted(values.items(), key=lambda kv: kv[1])
    n = len(ordered)
    return {name: max(1, round((i + 1) / n * 100)) for i, (name, _) in enumerate(ordered)}


def _build():
    size = {k: v[0] for k, v in RAW.items()}
    speed = {k: v[2] for k, v in RAW.items()}
    # log first, so "ten times as many" is a consistent step up the scale
    pop = {k: math.log10(max(v[3], 1)) for k, v in RAW.items()}
    song = {k: v[4] for k, v in RAW.items()}
    brains = {k: v[5] for k, v in RAW.items()}

    ranked = {
        "size": _rank_scores(size), "speed": _rank_scores(speed),
        "population": _rank_scores(pop), "song": _rank_scores(song),
        "brains": _rank_scores(brains),
    }
    out = {}
    for name, v in RAW.items():
        out[name] = {
            "length_cm": v[0], "weight_g": v[1],
            "habitat": v[6], "diet": v[7],
            "ratings": {stat: ranked[stat][name] for stat in ranked},
        }
    return out


BIRD_STATS = _build()


def stats_for(common_name: str):
    """Stats and 0-100 ratings for a bird, or None if it isn't one of the 100."""
    return BIRD_STATS.get(common_name)
