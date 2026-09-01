"""
Warble's curated UK bird list: 10 collector packs of 10 birds each.

This is the game's main collection mechanic. Packs are grouped by behaviour
and characteristics rather than habitat, so they cut across where birds live.

Each pack has 8 common birds and 2 rare ones. RARITY IS A FIXED PROPERTY OF
THE SPECIES, based on genuine UK scarcity - not something derived from local
record density. A Hawfinch is rare whether you're in Kent or Argyll.

A few rare birds are deliberately regional - Ring Ouzel needs uplands,
Razorbill needs coastal cliffs. Those packs are meant to require going
somewhere, not just listening harder at home.

This list is UK-specific. Other markets would get their own list of the same
shape, which is why nothing here assumes British species beyond the data.
"""

PACKS = {
    "garden_regulars": {
        "name": "Garden Regulars",
        "blurb": "The birds you'll meet on almost any doorstep.",
        "emoji": "\U0001F3E1",
        "common": [
            "European Robin", "Common Blackbird", "House Sparrow", "Dunnock",
            "Common Starling", "Common Wood-Pigeon", "Eurasian Collared-Dove",
            "Rock Pigeon",
        ],
        "rare": ["Eurasian Tree Sparrow", "European Turtle-Dove"],
    },
    "tits_and_climbers": {
        "name": "Tits & Climbers",
        "blurb": "Tiny acrobats that hang upside down and run up tree trunks.",
        "emoji": "\U0001F343",
        "common": [
            "Eurasian Blue Tit", "Great Tit", "Coal Tit", "Long-tailed Tit",
            "Eurasian Nuthatch", "Eurasian Treecreeper", "Goldcrest", "Eurasian Wren",
        ],
        "rare": ["Marsh Tit", "Willow Tit"],
    },
    "seed_eaters": {
        "name": "Finches & Seed-Eaters",
        "blurb": "Stout beaks built for cracking seeds open.",
        "emoji": "\U0001F33B",
        "common": [
            "Common Chaffinch", "European Goldfinch", "European Greenfinch",
            "Common Linnet", "Eurasian Bullfinch", "Eurasian Siskin",
            "Yellowhammer", "Reed Bunting",
        ],
        "rare": ["Hawfinch", "Corn Bunting"],
    },
    "small_singers": {
        "name": "Warblers & Small Singers",
        "blurb": "Little brown birds with surprisingly big voices.",
        "emoji": "\U0001F3B5",
        "common": [
            "Eurasian Blackcap", "Common Chiffchaff", "Willow Warbler",
            "Common Whitethroat", "Sedge Warbler", "Eurasian Reed Warbler",
            "European Stonechat", "Common Redstart",
        ],
        "rare": ["Lesser Whitethroat", "Common Firecrest"],
    },
    "tricksters": {
        "name": "Tricksters & Drummers",
        "blurb": "The cleverest birds around - and the ones that drum on trees.",
        "emoji": "\u2728",
        "common": [
            "Eurasian Magpie", "Eurasian Jay", "Western Jackdaw", "Carrion Crow",
            "Rook", "Northern Raven", "Great Spotted Woodpecker",
            "European Green Woodpecker",
        ],
        "rare": ["Lesser Spotted Woodpecker", "Common Cuckoo"],
    },
    "ground_feeders": {
        "name": "Thrushes & Ground Feeders",
        "blurb": "Birds that hop and probe about on the ground.",
        "emoji": "\U0001F33E",
        "common": [
            "Song Thrush", "Mistle Thrush", "Eurasian Skylark", "Common Pheasant",
            "White Wagtail", "Grey Wagtail", "Meadow Pipit", "Redwing",
        ],
        "rare": ["Grey Partridge", "Ring Ouzel"],
    },
    "hunters": {
        "name": "Hunters",
        "blurb": "Sharp eyes, sharp talons - the hunters of day and night.",
        "emoji": "\U0001F985",
        "common": [
            "Common Buzzard", "Common Kestrel", "Eurasian Sparrowhawk", "Red Kite",
            "Peregrine Falcon", "Tawny Owl", "Barn Owl", "Little Owl",
        ],
        "rare": ["Eurasian Hobby", "Long-eared Owl"],
    },
    "water_birds": {
        "name": "Water Birds",
        "blurb": "Swimmers, divers and dabblers.",
        "emoji": "\U0001F986",
        "common": [
            "Mallard", "Mute Swan", "Canada Goose", "Greylag Goose",
            "Eurasian Coot", "Common Moorhen", "Little Grebe", "Great Crested Grebe",
        ],
        "rare": ["Common Kingfisher", "Common Eider"],
    },
    "waders": {
        "name": "Waders & Long-legs",
        "blurb": "Long legs and long bills, built for mud and shallows.",
        "emoji": "\U0001FAB6",
        "common": [
            "Grey Heron", "Eurasian Oystercatcher", "Common Ringed Plover",
            "Sanderling", "Ruddy Turnstone", "Common Sandpiper", "Common Snipe",
            "Northern Lapwing",
        ],
        "rare": ["Eurasian Curlew", "Eurasian Woodcock"],
    },
    "sky_and_sea": {
        "name": "Sky & Sea",
        "blurb": "Birds of the open air and the open water.",
        "emoji": "\U0001F30A",
        "common": [
            "Herring Gull", "Black-headed Gull", "Common Gull",
            "Great Black-backed Gull", "Great Cormorant", "Common Tern",
            "Barn Swallow", "Common House-Martin",
        ],
        "rare": ["Northern Gannet", "Razorbill"],
    },
}

# --- Derived lookups -------------------------------------------------------

ALL_CURATED_SPECIES = {
    s for p in PACKS.values() for s in (p["common"] + p["rare"])
}

# Fixed rarity per species. Only two tiers now - a bird is either common or
# rare, and that never changes with where you are.
SPECIES_RARITY = {}
for _p in PACKS.values():
    for _s in _p["common"]:
        SPECIES_RARITY[_s] = "Common"
    for _s in _p["rare"]:
        SPECIES_RARITY[_s] = "Rare"

PACK_FOR_SPECIES = {
    s: key for key, p in PACKS.items() for s in (p["common"] + p["rare"])
}

TIERS = ["Common", "Rare"]


def rarity_of(common_name: str):
    """Fixed rarity for a species, or None if it isn't on Warble's list."""
    return SPECIES_RARITY.get(common_name)


def pack_for_species(common_name: str):
    return PACK_FOR_SPECIES.get(common_name)
