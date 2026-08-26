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
