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
        "emoji": "🥚",
        "citation": "Your very first warble — welcome to the flock!",
        "description": "This is where it all begins. You've had your first listening session, and that's a moment every birdwatcher remembers. Everything from here is new.",
    },
    "early_bird": {
        "name": "Early Bird",
        "emoji": "🌅",
        "citation": "Up before the birds — well, almost!",
        "description": "You started warbling before sunrise. That's dawn chorus time, when birds sing their loudest and best songs to wake up the neighbourhood. Not many people hear this — you're one of the lucky ones.",
    },
    "nomad": {
        "name": "Nomad",
        "emoji": "🧭",
        "citation": "Ten different spots, ten different adventures!",
        "description": "You've gone warbling in 10 different places. Real birdwatchers know the best way to find new birds is to go looking for them — and that's exactly what you've been doing.",
    },
    "rooster": {
        "name": "Rooster",
        "emoji": "🐓",
        "citation": "Same spot, five times — that's your patch now!",
        "description": "You've warbled at the same place 5 times. You know it now — the trees, the corners, the birds that live there. That's not luck, that's knowing your patch.",
    },
    "golden_eagle": {
        "name": "Golden Eagle",
        "emoji": "🦅",
        "citation": "You found birds that almost nobody finds here!",
        "description": "You discovered 5 birds that are seriously rare in the places you found them. These are the kind of sightings that make grown-up birdwatchers gasp. You've got a brilliant ear.",
    },
    "dawn_chorus": {
        "name": "Dawn Chorus",
        "emoji": "🎶",
        "citation": "Five songs, one sunrise — you caught the whole chorus!",
        "description": "In a single early morning session, you heard 5 different birds all singing before the sun came up. That's the dawn chorus — one of the most amazing sounds in nature, and you were there for it.",
    },
    "forager": {
        "name": "Forager",
        "emoji": "🌿",
        "citation": "Twenty different birds — that's a proper collection!",
        "description": "You've now found 20 different kinds of birds. That's a huge range of songs to know by ear. You're building a real, proper knowledge of what's out there.",
    },
    "night_owl": {
        "name": "Night Owl",
        "emoji": "🦉",
        "citation": "You went out after dark and found a night bird!",
        "description": "You stayed out past 9pm with a grown-up and found an owl, nightjar or woodcock — birds that only come out at night. That's proper dedication. Well done, night owl.",
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
