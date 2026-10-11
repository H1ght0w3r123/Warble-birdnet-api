"""
Weekly challenges: five per week, drawn from a pool. Feathers come only from
finishing the whole week - all five done is ALL_COMPLETE_BONUS, and a
challenge on its own pays nothing. One clear prize for the week, rather than a
trickle that makes the last few challenges feel optional.

The five are chosen deterministically from the ISO week number, so they're
stable across reloads and devices without needing to be stored anywhere -
and they genuinely rotate rather than being random each time the page opens.

Every challenge's progress is computed from get_week_stats(), so adding one
means adding a "progress" function here and nothing else.
"""
import datetime
import random

# Each: id, text shown to the child, target, and how to measure it.
# "progress" takes the week-stats dict and returns a number to compare to target.
CHALLENGE_POOL = [
    {
        "id": "warble_3",
        "text": "Go warbling 3 times",
        "target": 3,
        "progress": lambda w: w["sessions"],
    },
    {
        "id": "two_days",
        "text": "Warble on 2 different days",
        "target": 2,
        "progress": lambda w: w["days"],
    },
    {
        "id": "two_places",
        "family": "places",
        "text": "Warble in 2 different places",
        "target": 2,
        "progress": lambda w: w["locations"],
    },
    {
        "id": "five_species",
        "family": "species",
        "text": "Hear 5 different birds",
        "target": 5,
        "progress": lambda w: len(w["species"]),
    },
    {
        "id": "eight_species",
        "family": "species",
        "text": "Hear 8 different birds",
        "target": 8,
        "progress": lambda w: len(w["species"]),
    },
    {
        "id": "three_in_one",
        "family": "one_session",
        "text": "Hear 3 birds in a single warble",
        "target": 3,
        "progress": lambda w: w["best_session_birds"],
    },
    {
        "id": "new_bird",
        "text": "Hear a new bird",
        "target": 1,
        "progress": lambda w: min(1, len(w["new_species"])),
        # Only while new birds are still turning up for this child. Once
        # the ones near home are all found it can't be done, and as one of
        # the five it would quietly stop the whole week (and High Five).
        "needs_new_birds": True,
    },
    {
        "id": "game_star",
        "text": "Win a star in Guess the Song",
        "target": 1,
        "progress": lambda w: min(1, w["game_stars"]),
        # Only for a child who can play it, and only from the week after it
        # was added - so the week it arrived in didn't reshuffle mid-week.
        "needs_game": True,
        "from_week": "2026-W42",
    },
    {
        # Birds sing most in the morning. It was "before 9am", which a child
        # at school only manages at the weekend, if then - typical children
        # never finished it. Any warble before midday, UK time, now counts.
        "id": "early_start",
        "text": "Go warbling in the morning",
        "target": 1,
        "progress": lambda w: 1 if (w["earliest_uk_hour"] is not None and w["earliest_uk_hour"] < 12) else 0,
    },
    {
        # A third place in one week is a family outing, not something a
        # child can choose - so it's no longer picked. Kept here, with
        # until_week, so the week it was retired in didn't reshuffle.
        "id": "four_places",
        "family": "places",
        "text": "Warble in 3 different places",
        "target": 3,
        "progress": lambda w: w["locations"],
        "until_week": "2026-W42",
    },
    {
        # Was 5, which depends more on the garden than on the child.
        "id": "big_session",
        "family": "one_session",
        "text": "Hear 4 birds in a single warble",
        "target": 4,
        "progress": lambda w: w["best_session_birds"],
    },
]

ALL_COMPLETE_BONUS = 25   # the only feathers the challenges pay

# Always included, so the weekly rhythm the reward structure is built around
# is never absent - the other four rotate around it.
ANCHOR_ID = "warble_3"


def current_week_key(now: datetime.datetime = None) -> str:
    now = now or datetime.datetime.utcnow()
    return now.strftime("%G-W%V")


CHALLENGES_BY_ID = {c["id"]: c for c in CHALLENGE_POOL}


def get_week_challenges(now: datetime.datetime = None, can_play_game: bool = True,
                        finding_new_birds: bool = True):
    """The five challenges for this week. Seeded by the ISO week so the same
    week always yields the same five for the same child. The caller keeps
    the five it was given for the rest of the week (main.week_challenges),
    so a game opening mid-week can't swap them about."""
    week = current_week_key(now)
    anchor = next(c for c in CHALLENGE_POOL if c["id"] == ANCHOR_ID)
    others = [c for c in CHALLENGE_POOL if c["id"] != ANCHOR_ID
              and week >= c.get("from_week", "")
              and week < c.get("until_week", "9999")
              and (can_play_game or not c.get("needs_game"))
              and (finding_new_birds or not c.get("needs_new_birds"))]
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
