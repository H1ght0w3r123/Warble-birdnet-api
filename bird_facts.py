"""
Curated bird facts for the visual stats dashboard.

Real numbers, sourced from BTO BirdFacts (bto.org/learn/about-birds/birdfacts)
for weight, habitat, and conservation status — the same trusted source
already underpinning the app's rarity data. Wingspan and length come from
standard UK field-guide reference figures (consistently cited across
sources for these well-known species) rather than the same single BTO
page, since BTO's own biometric data uses "wing length" (a folded-wing
ringing measurement), not the tip-to-tip "wingspan" a kid would picture.

Size comparisons are written by hand, aimed at a 5-8 year old.

THIS LIST IS INTENTIONALLY SMALL SO FAR. Reaching the full ~100 species
target is a genuine ongoing content task, not a technical one — each
entry needs a real, checked source, not a guess. Add more species here
the same way, batch by batch.
"""

HABITAT_ICONS = {
    "Garden & Parks": "🌳",
    "Woodland": "🌲",
    "Wetland & Coast": "🌊",
    "Farmland": "🌾",
    "Towns & Cities": "🏘️",
}

BIRD_FACTS = {
    "European Robin": {
        "weight_g": 19,
        "wingspan_cm": 21,
        "length_cm": 14,
        "habitats": ["Garden & Parks", "Woodland"],
        "conservation_status": "Green",
        "size_comparison": "About as long as a school ruler.",
        "weight_comparison": "About as heavy as a AA battery.",
    },
    "Eurasian Blue Tit": {
        "weight_g": 10.9,
        "wingspan_cm": 18,
        "length_cm": 11.5,
        "habitats": ["Garden & Parks", "Woodland"],
        "conservation_status": "Green",
        "size_comparison": "Small enough to fit in the palm of your hand.",
        "weight_comparison": "Lighter than two pound coins.",
    },
    "Great Tit": {
        "weight_g": 18,
        "wingspan_cm": 24,
        "length_cm": 14,
        "habitats": ["Garden & Parks", "Woodland"],
        "conservation_status": "Green",
        "size_comparison": "About as long as a school ruler.",
        "weight_comparison": "About as heavy as a AA battery.",
    },
    "Common Blackbird": {
        "weight_g": 100,
        "wingspan_cm": 36,
        "length_cm": 25,
        "habitats": ["Garden & Parks", "Woodland", "Farmland"],
        "conservation_status": "Green",
        "size_comparison": "About as long as your forearm.",
        "weight_comparison": "About as heavy as a big apple.",
    },
    "Eurasian Wren": {
        "weight_g": 10,
        "wingspan_cm": 15,
        "length_cm": 9.5,
        "habitats": ["Garden & Parks", "Woodland"],
        "conservation_status": "Green",
        "size_comparison": "Tiny — barely longer than your thumb!",
        "weight_comparison": "Lighter than two pound coins.",
    },
    "House Sparrow": {
        "weight_g": 30,
        "wingspan_cm": 22,
        "length_cm": 15,
        "habitats": ["Garden & Parks", "Towns & Cities", "Farmland"],
        "conservation_status": "Red",
        "size_comparison": "About as long as a school ruler.",
        "weight_comparison": "About as heavy as five pound coins.",
    },
    "Common Starling": {
        "weight_g": 80,
        "wingspan_cm": 40,
        "length_cm": 21,
        "habitats": ["Garden & Parks", "Towns & Cities", "Farmland"],
        "conservation_status": "Red",
        "size_comparison": "About as long as your hand and wrist.",
        "weight_comparison": "About as heavy as a tennis ball.",
    },
    "Common Wood-Pigeon": {
        "weight_g": 500,
        "wingspan_cm": 76,
        "length_cm": 41,
        "habitats": ["Garden & Parks", "Woodland", "Farmland", "Towns & Cities"],
        "conservation_status": "Green",
        "size_comparison": "As long as your whole arm!",
        "weight_comparison": "About as heavy as a big bag of sugar... well, half of one!",
    },
    "Eurasian Magpie": {
        "weight_g": 220,
        "wingspan_cm": 56,
        "length_cm": 45,
        "habitats": ["Garden & Parks", "Farmland", "Towns & Cities"],
        "conservation_status": "Green",
        "size_comparison": "As long as your arm — but half of that is tail!",
        "weight_comparison": "About as heavy as a tin of beans.",
    },
    "European Goldfinch": {
        "weight_g": 16,
        "wingspan_cm": 23,
        "length_cm": 12,
        "habitats": ["Garden & Parks", "Farmland"],
        "conservation_status": "Green",
        "size_comparison": "Small enough to fit in the palm of your hand.",
        "weight_comparison": "About as heavy as three pound coins.",
    },
    "Common Chaffinch": {
        "weight_g": 24,
        "wingspan_cm": 26,
        "length_cm": 14.5,
        "habitats": ["Garden & Parks", "Woodland", "Farmland"],
        "conservation_status": "Green",
        "size_comparison": "About as long as a school ruler.",
        "weight_comparison": "About as heavy as four pound coins.",
    },
    "Dunnock": {
        "weight_g": 21,
        "wingspan_cm": 20,
        "length_cm": 14,
        "habitats": ["Garden & Parks", "Woodland", "Farmland"],
        "conservation_status": "Amber",
        "size_comparison": "About as long as a school ruler.",
        "weight_comparison": "About as heavy as a AA battery.",
    },
    "Song Thrush": {
        "weight_g": 83,
        "wingspan_cm": 34,
        "length_cm": 23,
        "habitats": ["Garden & Parks", "Woodland", "Farmland"],
        "conservation_status": "Amber",
        "size_comparison": "About as long as your forearm.",
        "weight_comparison": "About as heavy as a small apple.",
    },
    "Great Spotted Woodpecker": {
        "weight_g": 85,
        "wingspan_cm": 36,
        "length_cm": 23,
        "habitats": ["Woodland", "Garden & Parks"],
        "conservation_status": "Green",
        "size_comparison": "About as long as your forearm.",
        "weight_comparison": "About as heavy as a small apple.",
    },
    "Eurasian Jay": {
        "weight_g": 170,
        "wingspan_cm": 55,
        "length_cm": 34,
        "habitats": ["Woodland", "Garden & Parks"],
        "conservation_status": "Green",
        "size_comparison": "As long as your arm from elbow to fingertips.",
        "weight_comparison": "About as heavy as a big bag of crisps... times four!",
    },
}


def get_bird_facts(common_name: str):
    """Returns a dict of curated facts for this species, or None if we
    haven't researched it yet."""
    return BIRD_FACTS.get(common_name)
