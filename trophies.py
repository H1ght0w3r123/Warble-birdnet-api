"""
Trophy definitions and the logic to check them.

Only the first 3 MVP trophies for now — Fledgling, Early Bird, Nomad.
The other 16 from the original design stay parked, same as always.
"""
import datetime

from astral import LocationInfo
from astral.sun import sun

TROPHY_DEFINITIONS = {
    "fledgling": {
        "name": "Fledgling",
        "requirement": "Finish your first warble",
        "emoji": "🥚",
        "citation": "Your very first warble — welcome to the flock!",
        "description": "This is where it all begins. You've had your first listening session, and that's a moment every birdwatcher remembers. Everything from here is new.",
    },
    "early_bird": {
        "name": "Early Bird",
        "requirement": "Warble before sunrise",
        "emoji": "🌅",
        "citation": "Up before the birds — well, almost!",
        "description": "You started warbling before sunrise. That's dawn chorus time, when birds sing their loudest and best songs to wake up the neighbourhood. Not many people hear this — you're one of the lucky ones.",
    },
    "nomad": {
        "name": "Nomad",
        "requirement": "Warble in 10 different places",
        "emoji": "🧭",
        "citation": "Ten different spots, ten different adventures!",
        "description": "You've gone warbling in 10 different places. Real birdwatchers know the best way to find new birds is to go looking for them — and that's exactly what you've been doing.",
    },
    "rooster": {
        "name": "Rooster",
        "requirement": "Warble 5 times in the same place",
        "emoji": "🐓",
        "citation": "Same spot, five times — that's your patch now!",
        "description": "You've warbled at the same place 5 times. You know it now — the trees, the corners, the birds that live there. That's not luck, that's knowing your patch.",
    },
    "golden_eagle": {
        "name": "Golden Eagle",
        "requirement": "Find 5 Rare birds",
        "emoji": "🦅",
        "citation": "You found birds that almost nobody finds here!",
        "description": "You discovered 5 birds that are seriously rare in the places you found them. These are the kind of sightings that make grown-up birdwatchers gasp. You've got a brilliant ear.",
    },
    "dawn_chorus": {
        "name": "Dawn Chorus",
        "requirement": "Hear 5 birds before sunrise in one warble",
        "emoji": "🎶",
        "citation": "Five songs, one sunrise — you caught the whole chorus!",
        "description": "In a single early morning session, you heard 5 different birds all singing before the sun came up. That's the dawn chorus — one of the most amazing sounds in nature, and you were there for it.",
    },
    "forager": {
        "name": "Forager",
        "requirement": "Find 20 different birds",
        "emoji": "🌿",
        "citation": "Twenty different birds — that's a proper collection!",
        "description": "You've now found 20 different kinds of birds. That's a huge range of songs to know by ear. You're building a real, proper knowledge of what's out there.",
    },
    "night_owl": {
        "name": "Night Owl",
        "requirement": "Find a night bird after 9pm",
        "emoji": "🦉",
        "citation": "You went out after dark and found a night bird!",
        "description": "You stayed out past 9pm with a grown-up and found an owl, nightjar or woodcock — birds that only come out at night. That's proper dedication. Well done, night owl.",
    },
    "century": {
        "name": "Century",
        "requirement": "Find all 100 birds on Warble's list",
        "emoji": "💯",
        "citation": "You've found every single bird on the list — outstanding!",
        "description": "There are 100 different birds on Warble's list, and you've found every single one of them. That's not luck — that's real skill, real patience, and a lot of listening. You're officially a master warbler.",
    },
    "empty_nester": {
        "name": "Empty Nester",
        "requirement": "Go warbling 20 times without hearing a bird",
        "emoji": "\U0001FAB9",
        "citation": "Twenty quiet warbles - and you kept going anyway!",
        "description": "Twenty times you went out, listened hard, and heard nothing at all. Every real birdwatcher knows that feeling. Coming back and trying again after a quiet day is the hardest part of all - and you did it twenty times.",
    },
    "preener": {
        "name": "Preener",
        "requirement": "Collect 10 Dress Up items",
        "emoji": "🪶",
        "citation": "Ten outfits and counting - looking sharp!",
        "description": "You've collected 10 different things for your bird to wear. Real birds preen their feathers every single day to keep them perfect, so you're in very good company.",
    },
    "evergreen": {
        "name": "Evergreen",
        "requirement": "Go warbling in all four seasons",
        "emoji": "🌲",
        "citation": "Spring, summer, autumn, winter - you warbled through them all!",
        "description": "You've been out warbling in every season of the year. Birds change enormously through the year - who's singing, who's visiting, who's flown away - and you've heard the whole cycle.",
    },
    "tailwind": {
        "name": "Tailwind",
        "requirement": "Go warbling three days in a row",
        "emoji": "🌬️",
        "citation": "Three days running - you're on a roll!",
        "description": "You went warbling three days in a row. Keeping a habit going is genuinely hard, and birds reward the people who show up again and again.",
    },
    "migrator": {
        "name": "Migrator",
        "requirement": "Find the same bird in two places 5km apart",
        "emoji": "🗺️",
        "citation": "You found the same bird miles from where you first met it!",
        "description": "You heard the same kind of bird in two places at least 5km apart. Birds move around far more than people realise, and now you've got the proof yourself.",
    },
    "skylark": {
        "name": "Skylark",
        "requirement": "Find 5 farmland or hedgerow birds",
        "emoji": "🌾",
        "citation": "Five farmland birds - you know the open fields!",
        "description": "You've found 5 birds that live out in farmland and hedgerows. These are some of the trickiest birds to hear, and many of them are getting rarer, so every one counts.",
    },
    "high_flyer": {
        "name": "High Flyer",
        "requirement": "Find 5 birds of prey",
        "emoji": "🦅",
        "citation": "Five birds of prey - you've been watching the skies!",
        "description": "You've found 5 birds of prey. These are the hunters - the ones circling high overhead - and hearing five different ones takes real patience and a very good ear.",
    },
    "still_water": {
        "name": "Still Water",
        "requirement": "Find 5 wetland or water birds",
        "emoji": "🌊",
        "citation": "Five water birds - you found the wet and wild ones!",
        "description": "You've found 5 birds that live around water - ponds, rivers, reedbeds and marshes. A whole different world of birds lives there, and you've been listening to it.",
    },
    "brooder": {
        "name": "Brooder",
        "requirement": "Go warbling in the rain",
        "emoji": "☔",
        "citation": "You went out in the rain - proper dedication!",
        "description": "You went warbling while it was actually raining. Most people stay inside, but plenty of birds keep right on singing - so you heard something most people never do.",
    },
    "wingman": {
        "name": "Wingman",
        "requirement": "Share one of your birds with someone",
        "emoji": "🤝",
        "citation": "You shared a bird - spreading the warble!",
        "description": "You shared one of your birds with someone else. Birdwatchers have always told each other what they've found, and now you're part of that too.",
    },
}

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
