"""
Collector packs: themed sets of 5 birds from the curated UK 100.

These are the ONLY birds that carry a rarity tier. Every other bird in the
100 is simply found or not found - no Common/Visitor/Rare. That keeps rarity
meaningful rather than being noise attached to every sighting.

A pack bird can be held at all three tiers, so a pack is 15 cards, completed
by finding every tier of all five. Tier comes from local NBN Atlas record
density, so that genuinely means hearing the same birds in very different
parts of the country - a pack is a long-haul goal, not a weekend one.

Packs are themed rather than habitat-based, so they deliberately cut across
the habitat groups the 100 is otherwise divided into.
"""

COLLECTOR_PACKS = {
    "hedge_hoppers": {
        "name": "Hedge Hoppers",
        "blurb": "Tiny birds that dart about in bushes - easy to hear, hard to see.",
        "emoji": "\U0001F33F",
        "species": [
            "Eurasian Wren",
            "Dunnock",
            "Common Chiffchaff",
            "Willow Warbler",
            "Eurasian Blackcap",
        ],
    },
    "hunters": {
        "name": "Hunters",
        "blurb": "Birds of prey - the sharp-eyed hunters of the sky and the night.",
        "emoji": "\U0001F985",
        "species": [
            "Common Buzzard",
            "Common Kestrel",
            "Eurasian Sparrowhawk",
            "Tawny Owl",
            "Barn Owl",
        ],
    },
    "bright_sparks": {
        "name": "Bright Sparks",
        "blurb": "The cleverest, noisiest birds around - and some brilliant mimics.",
        "emoji": "\u2728",
        "species": [
            "Eurasian Magpie",
            "Eurasian Jay",
            "Carrion Crow",
            "Western Jackdaw",
            # Not a corvid, but a famously clever mimic - it earns its place
            # here on behaviour rather than family.
            "Common Starling",
        ],
    },
}

TIERS = ["Common", "Visitor", "Rare"]

# Flat lookup: every species that carries a rarity tier.
COLLECTOR_SPECIES = {s for p in COLLECTOR_PACKS.values() for s in p["species"]}


def pack_for_species(common_name: str):
    """Which pack a bird belongs to, or None if it isn't a collector bird."""
    for key, pack in COLLECTOR_PACKS.items():
        if common_name in pack["species"]:
            return key
    return None
