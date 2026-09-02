"""
Weekly challenges: five per week, drawn from a pool, each worth feathers,
with a bonus for completing all five.

The five are chosen deterministically from the ISO week number, so they're
stable across reloads and devices without needing to be stored anywhere -
and they genuinely rotate rather than being random each time the page opens.

Every challenge's progress is computed from get_week_stats(), so adding one
means adding a "progress" function here and nothing else.
"""
import datetime
import random

# Each: id, text shown to the child, target, feathers, and how to measure it.
# "progress" takes the week-stats dict and returns a number to compare to target.
CHALLENGE_POOL = [
    {
        "id": "warble_3",
        "text": "Go warbling 3 times",
        "target": 3,
        "feathers": 8,
        "progress": lambda w: w["sessions"],
    },
    {
        "id": "two_days",
        "text": "Warble on 2 different days",
        "target": 2,
        "feathers": 5,
        "progress": lambda w: w["days"],
    },
    {
        "id": "two_places",
        "family": "places",
        "text": "Warble in 2 different places",
        "target": 2,
        "feathers": 6,
        "progress": lambda w: w["locations"],
    },
    {
        "id": "five_species",
        "family": "species",
        "text": "Find 5 different birds",
        "target": 5,
        "feathers": 8,
        "progress": lambda w: len(w["species"]),
    },
    {
        "id": "eight_species",
        "family": "species",
        "text": "Find 8 different birds",
        "target": 8,
        "feathers": 12,
        "progress": lambda w: len(w["species"]),
    },
    {
        "id": "three_in_one",
        "family": "one_session",
        "text": "Hear 3 birds in a single warble",
        "target": 3,
        "feathers": 6,
        "progress": lambda w: w["best_session_birds"],
    },
    {
        "id": "not_common",
        "text": "Find a Visitor or Rare bird",
        "target": 1,
        "feathers": 9,
        "progress": lambda w: 1 if (w["tiers"] & {"Visitor", "Rare"}) else 0,
    },
    {
        "id": "early_start",
        "text": "Go warbling before 9am",
        "target": 1,
        "feathers": 6,
        "progress": lambda w: 1 if (w["earliest_hour"] is not None and w["earliest_hour"] < 9) else 0,
    },
    {
        "id": "four_places",
        "family": "places",
        "text": "Warble in 3 different places",
        "target": 3,
        "feathers": 10,
        "progress": lambda w: w["locations"],
    },
    {
        "id": "big_session",
        "family": "one_session",
        "text": "Hear 5 birds in a single warble",
        "target": 5,
        "feathers": 10,
        "progress": lambda w: w["best_session_birds"],
    },
]

ALL_COMPLETE_BONUS = 20

# Always included, so the weekly rhythm the reward structure is built around
# is never absent - the other four rotate around it.
ANCHOR_ID = "warble_3"


def current_week_key(now: datetime.datetime = None) -> str:
    now = now or datetime.datetime.utcnow()
    return now.strftime("%G-W%V")


def get_week_challenges(now: datetime.datetime = None):
    """The five challenges for this week. Seeded by the ISO week so the same
    week always yields the same five, on any device, without storing them."""
    week = current_week_key(now)
    anchor = next(c for c in CHALLENGE_POOL if c["id"] == ANCHOR_ID)
    others = [c for c in CHALLENGE_POOL if c["id"] != ANCHOR_ID]
    rng = random.Random(week)
    # Some challenges are strictly easier versions of others ("2 places" vs
    # "3 places"). Picking both wastes a slot, since finishing the harder one
    # completes the easier one for free - so allow only one per family.
    rng.shuffle(others)
    picked, used_families = [], set()
    for ch in others:
        fam = ch.get("family")
        if fam and fam in used_families:
            continue
        picked.append(ch)
        if fam:
            used_families.add(fam)
        if len(picked) == 4:
            break
    return [anchor] + picked
