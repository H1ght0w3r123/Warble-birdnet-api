"""
Trophy definitions and the logic to check them.

Only the first 3 MVP trophies for now — Fledgling, Early Bird, Nomad.
The other 16 from the original design stay parked, same as always.
"""
import datetime

from astral import LocationInfo
from astral.sun import sun

# Every trophy has three levels. The context never changes - only how much of
# it is required - which means new challenge can be added by extending a
# levels list rather than inventing a new idea each time.
#
# "unit" completes the sentence "Find/Warble ... {n} <unit>", so requirement
# text is generated rather than written out three times per trophy.
TROPHY_DEFINITIONS = {
    "fledgling": {
        "name": "Fledgling", "emoji": "\U0001F95A",
        "verb": "Go warbling", "unit": "times",
        "levels": [1, 15, 60],
        "citations": [
            "Your very first warble - welcome to the flock!",
            "Fifteen warbles in - this is a proper habit now.",
            "Sixty warbles. You're not a fledgling any more.",
        ],
        "description": "This is where it all begins. Every birdwatcher remembers their first time listening properly - and you've kept coming back.",
    },
    "early_bird": {
        "name": "Early Bird", "emoji": "\U0001F305",
        "verb": "Warble before sunrise", "unit": "times",
        "levels": [1, 5, 15],
        "citations": [
            "Up before the birds - well, almost!",
            "Five sunrises beaten. That takes real getting up.",
            "Fifteen dawns. The birds must know you by now.",
        ],
        "description": "Dawn is when birds sing their loudest and best, to wake up the neighbourhood. Not many people hear it - you're one of the lucky ones.",
    },
    "nomad": {
        "name": "Nomad", "emoji": "\U0001F9ED",
        "verb": "Warble in", "unit": "different places",
        "levels": [10, 25, 50],
        "citations": [
            "Ten different spots, ten different adventures!",
            "Twenty-five places. You really do get about.",
            "Fifty different places. That's a proper explorer.",
        ],
        "description": "Real birdwatchers know the best way to find new birds is to go looking for them - and that's exactly what you've been doing.",
    },
    "rooster": {
        "name": "Rooster", "emoji": "\U0001F413",
        "verb": "Warble", "unit": "times in the same place",
        "levels": [5, 20, 50],
        "citations": [
            "Same spot, five times - that's your patch now!",
            "Twenty visits. You know every tree in that place.",
            "Fifty visits to one spot. That's real devotion.",
        ],
        "description": "You know it now - the trees, the corners, the birds that live there. That's not luck, that's knowing your patch.",
    },
    "golden_eagle": {
        "name": "Golden Eagle", "emoji": "\U0001F985",
        "verb": "Find", "unit": "Rare birds",
        "levels": [5, 15, 40],
        "citations": [
            "You found birds that almost nobody finds here!",
            "Fifteen rare finds. That's a seriously good ear.",
            "Forty rare birds. Grown-up birdwatchers would be jealous.",
        ],
        "description": "These are the kind of sightings that make experienced birdwatchers gasp. You've got a brilliant ear.",
    },
    "dawn_chorus": {
        "name": "Dawn Chorus", "emoji": "\U0001F3B6",
        "verb": "Hear", "unit": "birds before sunrise in one warble",
        "levels": [5, 8, 12],
        "citations": [
            "Five songs, one sunrise - you caught the whole chorus!",
            "Eight birds before dawn. What a morning that was.",
            "Twelve birds in one dawn chorus. Extraordinary.",
        ],
        "description": "The dawn chorus is one of the most amazing sounds in nature, and you were there for it.",
    },
    "forager": {
        "name": "Forager", "emoji": "\U0001F33F",
        "verb": "Find", "unit": "different birds",
        "levels": [20, 40, 70],
        "citations": [
            "Twenty different birds - that's a proper collection!",
            "Forty different birds. Your ear is getting sharp.",
            "Seventy different birds. That's a real naturalist.",
        ],
        "description": "That's a huge range of songs to know by ear. You're building real knowledge of what's out there.",
    },
    "night_owl": {
        "name": "Night Owl", "emoji": "\U0001F989",
        "verb": "Find", "unit": "night birds after dark",
        "levels": [5, 10, 20],
        "citations": [
            "Five night birds - you're not scared of the dark!",
            "Ten after dark. The night belongs to you.",
            "Twenty night birds. A true creature of the night.",
        ],
        "description": "Owls, nightjars and woodcocks only come out at night. Finding them takes proper dedication.",
    },
    "century": {
        "name": "Century", "emoji": "\U0001F4AF",
        "verb": "Find", "unit": "birds from Warble's list",
        "levels": [25, 60, 100],
        "citations": [
            "A quarter of the list already!",
            "Sixty of the hundred. The end is in sight.",
            "All 100 birds. You've completed Warble.",
        ],
        "description": "There are 100 birds on Warble's list. Working through them takes real skill, patience and a lot of listening.",
    },
    "globetrotter": {
        "name": "Globetrotter", "emoji": "\U0001F30D",
        "verb": "Complete", "unit": "collector packs",
        "levels": [1, 2, 3],
        "citations": [
            "A whole pack completed - every bird at every tier!",
            "Two packs finished. You've really covered the country.",
            "Every collector pack complete. Nothing left to chase.",
        ],
        "description": "A bird everyone sees at home can be a special sight somewhere else. You had to travel to learn that.",
    },
    "summer_squad": {
        "name": "Summer Squad", "emoji": "\u2600\uFE0F",
        "verb": "Find every summer visitor in", "unit": "summers",
        "levels": [1, 2, 3],
        "citations": [
            "Every summer bird, all in one summer - you didn't miss one!",
            "Two summers running. You know when they arrive now.",
            "Three summers complete. The migrants can't slip past you.",
        ],
        "description": "Thirteen birds fly thousands of miles to spend the summer here, and every one of them leaves again. Catching all of them in a single season means being out there at the right time, again and again.",
    },
    "empty_nester": {
        "name": "Empty Nester", "emoji": "\U0001FAB9",
        "verb": "Go warbling", "unit": "times without hearing a bird",
        "levels": [20, 50, 100],
        "citations": [
            "Twenty quiet warbles - and you kept going anyway!",
            "Fifty quiet days, and you're still here.",
            "A hundred silent warbles. Nothing puts you off.",
        ],
        "description": "Every real birdwatcher knows that feeling. Coming back and trying again after a quiet day is the hardest part of all.",
    },
    "preener": {
        "name": "Preener", "emoji": "\U0001FAB6",
        "verb": "Collect", "unit": "Dress Up items",
        "levels": [10, 22, 40],
        "citations": [
            "Ten outfits and counting - looking sharp!",
            "Twenty-two items. Quite the wardrobe.",
            "Every single item. Nothing left to buy!",
        ],
        "description": "Real birds preen their feathers every single day to keep them perfect, so you're in very good company.",
    },
    "evergreen": {
        "name": "Evergreen", "emoji": "\U0001F332",
        "verb": "Warble in", "unit": "different seasons",
        "levels": [2, 3, 4],
        "citations": [
            "Two seasons in - you've seen the birds change!",
            "Three seasons. Only one left to go.",
            "Spring, summer, autumn, winter - you warbled through them all!",
        ],
        "description": "Birds change enormously through the year - who's singing, who's visiting, who's flown away.",
    },
    "tailwind": {
        "name": "Tailwind", "emoji": "\U0001F32C\uFE0F",
        "verb": "Go warbling", "unit": "days in a row",
        "levels": [3, 7, 14],
        "citations": [
            "Three days running - you're on a roll!",
            "A whole week without missing a day!",
            "Fourteen days straight. Astonishing.",
        ],
        "description": "Keeping a habit going is genuinely hard, and birds reward the people who show up again and again.",
    },
    "migrator": {
        "name": "Migrator", "emoji": "\U0001F5FA\uFE0F",
        "verb": "Find", "unit": "birds in two places 5km apart",
        "levels": [1, 5, 15],
        "citations": [
            "You found the same bird miles from where you first met it!",
            "Five birds tracked across the miles.",
            "Fifteen birds found far and wide. A real map-maker.",
        ],
        "description": "Birds move around far more than people realise, and now you've got the proof yourself.",
    },
    "skylark": {
        "name": "Skylark", "emoji": "\U0001F33E",
        "verb": "Find", "unit": "farmland or hedgerow birds",
        "levels": [5, 9, 14],
        "citations": [
            "Five farmland birds - you know the open fields!",
            "Nine farmland birds. The hedgerows are yours.",
            "Every farmland bird on the list. Remarkable.",
        ],
        "description": "These are some of the trickiest birds to hear, and many of them are getting rarer, so every one counts.",
    },
    "high_flyer": {
        "name": "High Flyer", "emoji": "\U0001F9BF",
        "verb": "Find", "unit": "birds of prey",
        "levels": [3, 6, 10],
        "citations": [
            "Three birds of prey - you've been watching the skies!",
            "Six hunters found. Sharp eyes and sharper ears.",
            "Every bird of prey on the list. Outstanding.",
        ],
        "description": "These are the hunters - the ones circling high overhead - and hearing them takes real patience.",
    },
    "still_water": {
        "name": "Still Water", "emoji": "\U0001F30A",
        "verb": "Find", "unit": "wetland or water birds",
        "levels": [5, 12, 20],
        "citations": [
            "Five water birds - you found the wet and wild ones!",
            "Twelve water birds. The reedbeds know you.",
            "Every water bird on the list. Astonishing.",
        ],
        "description": "A whole different world of birds lives around water - ponds, rivers, reedbeds and marshes.",
    },
    "brooder": {
        "name": "Brooder", "emoji": "\u2614",
        "verb": "Go warbling in the rain", "unit": "times",
        "levels": [1, 5, 15],
        "citations": [
            "You went out in the rain - proper dedication!",
            "Five rainy warbles. Weather doesn't stop you.",
            "Fifteen soggy sessions. Nothing keeps you in.",
        ],
        "description": "Most people stay inside, but plenty of birds keep right on singing - so you heard something most people never do.",
    },
    "wingman": {
        "name": "Wingman", "emoji": "\U0001F91D",
        "verb": "Share", "unit": "birds with someone",
        "levels": [1, 5, 15],
        "citations": [
            "You shared a bird - spreading the warble!",
            "Five birds shared. You're spreading the word.",
            "Fifteen shared. A proper ambassador for birds.",
        ],
        "description": "Birdwatchers have always told each other what they've found, and now you're part of that too.",
    },
}


def requirement_text(key: str, level_index: int) -> str:
    """Generates 'Find 10 night birds after dark' from the trophy's own verb,
    threshold and unit - so the wording can't drift out of step with the
    numbers the way three hand-written strings would."""
    t = TROPHY_DEFINITIONS[key]
    return f"{t['verb']} {t['levels'][level_index]} {t['unit']}".replace("  ", " ")


# UK species that are genuinely nocturnal — used for the Night Owl trophy.
# Deliberately narrow: only birds that are specifically known for being
# active after dark, not just "sometimes heard in the evening".
NOCTURNAL_SPECIES = {
    "Tawny Owl", "Barn Owl", "Little Owl", "Long-eared Owl",
    "Short-eared Owl", "European Nightjar", "Eurasian Woodcock",
}


def is_before_sunrise(lat: float, lng: float, moment_utc: datetime.datetime) -> bool:
    """
    Works entirely in UTC to avoid needing to know the location's local
    timezone name — comparing a UTC moment against a UTC sunrise time is
    just as correct, and sidesteps a whole extra dependency.
    """
    try:
        location = LocationInfo("", "", "UTC", lat, lng)
        s = sun(location.observer, date=moment_utc.date(), tzinfo=datetime.timezone.utc)
        return moment_utc < s["sunrise"]
    except Exception as e:
        # Can fail near the poles (permanent day/night) — default to False
        # rather than incorrectly awarding the trophy.
        print(f"Warning: sunrise calculation failed for ({lat}, {lng}): {e}")
        return False
