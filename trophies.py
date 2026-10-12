"""
Trophy definitions and the logic to check them.

18 trophies of seven levels each. Dawn Chorus, Globetrotter and Skylark were
removed (October 2026); levels a child had won on them no longer count as
leaves, but the feathers they paid were kept.
"""
import datetime

from astral import LocationInfo
from astral.sun import sun

# Every trophy has seven levels. The context never changes - only how much of
# it is required - which means new challenge can be added by extending a
# levels list rather than inventing a new idea each time.
#
# On the trophy itself: level 1 shows its three leaf sockets empty, levels 2-4
# fill them with green leaves one by one, and levels 5-7 turn those leaves
# gold one by one. (The first three thresholds of most trophies are the old
# three levels unchanged; the ones that count birds from one pack, all 100
# birds or seasons were re-laddered, as their counts stop at 10, 100 or 4.)
#
# "unit" completes the sentence "Hear/Warble ... {n} <unit>", so requirement
# text is generated rather than written out three times per trophy.
# A trophy with a level of 1 also has "one": what follows the verb at that
# level, so it reads "Go warbling once" rather than "Go warbling 1 times".
TROPHY_DEFINITIONS = {
    "fledgling": {
        "name": "Fledgling", "emoji": "\U0001F95A",
        "verb": "Just get out there", "unit": "times", "one": "once",
        "levels": [1, 15, 60, 100, 150, 250, 350],
        "citations": [
            "Congratulations on your very first warble. Welcome to the flock. Spread your wings!",
            "Getting the hang of this now? 15 warbles and counting.",
            "Sixty warbles. You're not a fledgling any more.",
            "A hundred warbles! Now you've got your wings.",
            "A hundred and fifty. Flying high!",
            "Two hundred and fifty warbles. You are soaring now!",
            "You've hit the 350 mark! You're out of sight!",
        ],
        "description": "This is where it all begins. Every birdwatcher remembers their first time listening properly - and you've kept coming back.",
    },
    "early_bird": {
        "name": "Early Bird", "emoji": "\U0001F305",
        # It counts early warbles that heard a bird, so it says so.
        "verb": "Hear birds before sunrise", "unit": "times", "one": "once",
        "levels": [1, 5, 10, 15, 20, 30, 45],
        "citations": [
            "Up before the birds. Well...almost!",
            "Five sunrises beaten. Get up and Go!",
            "10 early rises. Go catch that worm!",
            "Warbling before dawn fifteen times! This is becoming a habit.",
            "Twenty dawns. Who's waking who up at this point?",
            "Thirty sunrises. You've definitely earned chocolate for breakfast!",
            "Forty-five dawns. You are indeed THE early bird!",
        ],
        "description": "Dawn is when birds sing their loudest and best. Hear them as you're waking up? Then make the most of it!",
    },
    "nomad": {
        "name": "Nomad", "emoji": "\U0001F9ED",
        "verb": "Travel to", "unit": "different places",
        "levels": [5, 10, 25, 40, 75, 100, 150],
        "citations": [
            "Five different locations. You're getting around!",
            "10 unique places. Really mixing it up now. Good for you!",
            "Twenty-five locations now. Keep on trucking!",
            "You've travelled to forty different places now.",
            "Seventy-five locations! A travelling warbler.",
            "A hundred places. Are you ever at home?!",
            "A hundred and fifty unique locations. Incredible effort!",
        ],
        "description": "The best way to hear new birds is to try in lots of different places. This trophy rewards those that keep on moving.",
    },
    "rooster": {
        "name": "Rooster", "emoji": "\U0001F413",
        "verb": "Warble", "unit": "times in the same place",
        "levels": [5, 20, 50, 75, 100, 150, 200],
        "citations": [
            "Same spot, five times. Claiming that patch!",
            "Twenty visits. Laying down roots!",
            "Fifty visits to one spot. That's real devotion.",
            "Seventy-five visits. The birds there know your name!",
            "A hundred visits to one place. This is your domain!",
            "A hundred and fifty visits. Nobody knows that spot like you.",
            "Two hundred visits to the same place. Such dedication. Good for you!",
        ],
        "description": "You've found a purple patch and you're sticking to it. Good for you! Are any birds nesting in your hair yet?",
    },
    "golden_eagle": {
        "name": "Golden Eagle", "emoji": "\U0001F985",
        "verb": "Hear", "unit": "rare birds",
        "levels": [5, 15, 40, 60, 80, 100, 125],
        "citations": [
            "You heard birds that almost nobody hears here!",
            "Fifteen rare birds heard. That's a seriously good ear.",
            "Forty rare birds. Grown-up birdwatchers would be jealous.",
            "Sixty rare birds. You find the special ones!",
            "Eighty rare birds. Your ears are pure gold.",
            "A hundred rare birds. Incredible!",
            "A hundred and twenty-five rare birds. A real legend!",
        ],
        "description": "Rare birds are the hardest of the bunch to hear. You have a brilliant ear, and a knack for being in the right place at the right time.",
    },
    "forager": {
        "name": "Forager", "emoji": "\U0001F33F",
        "verb": "Add", "unit": "birds to your flock",
        # Capped at 100, Warble's own list - higher levels could only be
        # reached with birds outside it, which have no cards.
        "levels": [20, 35, 50, 65, 80, 90, 100],
        "citations": [
            "Twenty different birds - that's a proper collection!",
            "Thirty-five different birds. Your ear is getting sharp.",
            "Fifty different birds. That's a real naturalist.",
            "Sixty-five different birds. You know so many songs!",
            "Eighty different birds. An expert ear!",
            "Ninety different birds. Hardly anything gets past you!",
            "A hundred different birds. Unbelievable!",
        ],
        "description": "This trophy rewards a full and varied flock! Keep on adding to it to level up.",
    },
    "night_owl": {
        "name": "Night Owl", "emoji": "\U0001F989",
        # Every bird heard after dark counts, owl or not - each bird in each
        # warble, so a robin singing under a streetlight three evenings
        # running is three. "After dark" is after dusk or before dawn
        # (is_after_dark), not just after sunset, when it's still light.
        "verb": "Hear", "unit": "birds after dark",
        "levels": [5, 10, 20, 30, 45, 60, 80],
        "citations": [
            "Five birds after dark - you're not scared of the dark!",
            "Ten after dark. The night belongs to you.",
            "Twenty birds after dark. A true creature of the night.",
            "Thirty birds after dark. Owls must think you're one of them!",
            "Forty-five birds after dark. Spooky good listening!",
            "Sixty birds after dark. The moon is your friend.",
            "Eighty birds after dark. King of the night!",
        ],
        "description": "Most birds go quiet when it gets dark, but not all of them and some are just waking up. Take a grown-up on a nighttime warble. Who knows what you'll hear!",
    },
    "century": {
        "name": "Century", "emoji": "\U0001F4AF",
        "verb": "Collect", "unit": "birds from the UK's top 100",
        "levels": [10, 25, 40, 60, 75, 90, 100],
        "citations": [
            "Ten of the hundred already - a brilliant start!",
            "A quarter of the list already!",
            "Forty of the hundred. Keep going!",
            "Sixty of the hundred. The end is in sight.",
            "Seventy-five. Three quarters done!",
            "Ninety! Only ten left to find.",
            "All 100 birds. You've completed Warble.",
        ],
        "description": "How many of the UK's top 100 birds can you hear? Completing this trophy takes real skill, patience and a lot of listening.",
    },
    "empty_nester": {
        "name": "Empty Nester", "emoji": "\U0001FAB9",
        "verb": "Listen for a whole minute", "unit": "times without hearing a bird",
        "levels": [20, 50, 100, 150, 200, 300, 400],
        "citations": [
            "Twenty quiet warbles - and you kept going anyway!",
            "Fifty quiet days, and you're still here.",
            "A hundred silent warbles. Nothing puts you off.",
            "A hundred and fifty quiet warbles. So patient!",
            "Two hundred. Patience is your superpower.",
            "Three hundred quiet warbles. You never give up!",
            "Four hundred. The most patient birdwatcher ever!",
        ],
        "description": "Sometimes the birds just don't feel like singing. But they'll be back, and so will you! Going again after a quiet session shows determination. Great effort!",
    },
    "preener": {
        "name": "Preener", "emoji": "\U0001FAB6",
        "verb": "Collect", "unit": "accessories in the Hoot-tique",
        # Round numbers, and never "the whole shop": that number moves every
        # time the Hoot-tique restocks (or loses an item), and the top level
        # would quietly stop meaning what it says - or stop being possible.
        # main.py checks the top level is below the number of items there are.
        "levels": [5, 10, 20, 30, 40, 50, 60],
        "citations": [
            "Five things to wear - looking sharp!",
            "Ten items. Quite the wardrobe.",
            "Twenty items. You could open your own shop!",
            "Thirty items. Best-dressed bird in town!",
            "Forty items. What a collection!",
            "Fifty items. The Hoot-tique knows your name!",
            "Sixty items. The best-dressed bird in Warble!",
        ],
        "description": "Real birds preen their feathers every single day to keep them perfect, so you're in very good company.",
    },
    "evergreen": {
        "name": "Evergreen", "emoji": "\U0001F332",
        "verb": "Warble in", "unit": "different seasons",
        "levels": [2, 3, 4, 6, 8, 12, 16],
        "citations": [
            "Two seasons in - you've seen the birds change!",
            "Three seasons. Only one left to go.",
            "Spring, summer, autumn, winter - you warbled through them all!",
            "Six seasons. A whole year and a half of birds!",
            "Eight seasons - two whole years of warbling!",
            "Twelve seasons. Three years of birds!",
            "Sixteen seasons. Four whole years - you're evergreen!",
        ],
        "description": "The birds around you change enormously through the year. Stick at it through every season and you learn who stays and who flies away.",
    },
    "tailwind": {
        "name": "Tailwind", "emoji": "\U0001F32C\uFE0F",
        "verb": "Go warbling", "unit": "days in a row",
        "levels": [3, 7, 14, 21, 30, 45, 60],
        "citations": [
            "Three days running - you're on a roll!",
            "A whole week without missing a day!",
            "Fourteen days straight. Astonishing.",
            "Three weeks in a row. Unstoppable!",
            "Thirty days running - a whole month!",
            "Forty-five days in a row. Incredible!",
            "Sixty days running. A true champion!",
        ],
        "description": "Creating a habit and keeping it up can be really hard. Well done, you're showing real commitment. Showing up day after day proves you're reliable and people can count on you! It does help when it's this fun though!",
    },
    "migrator": {
        "name": "Migrator", "emoji": "\U0001F5FA\uFE0F",
        "verb": "Hear", "unit": "birds in two places 5km apart",
        "one": "the same bird in two places 5km apart",
        "levels": [1, 2, 5, 10, 20, 35, 50],
        "citations": [
            "You heard the same bird miles from where you first met it!",
            "Two birds tracked across the miles.",
            "Five birds heard far and wide. A real map-maker.",
            "Ten birds heard far apart. You get around!",
            "Twenty birds across the miles. Like a migrating bird!",
            "Thirty-five birds far and wide. A true traveller.",
            "Fifty birds heard far apart. You've mapped the country!",
        ],
        "description": "Birds move around far more than people realise. Those who max out the Migrator trophy become expert trackers.",
    },
    "high_flyer": {
        "name": "High Flyer", "emoji": "\U0001F9BF",
        "verb": "Hear", "unit": "birds of prey",
        "levels": [2, 3, 4, 6, 8, 9, 10],
        "citations": [
            "Two birds of prey - you've been watching the skies!",
            "Three hunters heard. Keep looking up!",
            "Four birds of prey. Sharp eyes and sharper ears.",
            "Six hunters. The skies hold no secrets from you.",
            "Eight birds of prey. Fantastic!",
            "Nine! Just one bird of prey left to hear.",
            "Every bird of prey on the list. Outstanding.",
        ],
        "description": "These are the hunters who circle high overhead. You'll have to travel to some pretty interesting places to level up this trophy!",
    },
    "still_water": {
        "name": "Still Water", "emoji": "\U0001F30A",
        "verb": "Hear", "unit": "wetland or water birds",
        "levels": [2, 3, 4, 6, 8, 9, 10],
        "citations": [
            "Two water birds - you heard the wet and wild ones!",
            "Three water birds. Splash!",
            "Four water birds. The reedbeds know you.",
            "Six water birds. A real water-watcher!",
            "Eight water birds. Superb!",
            "Nine! Just one water bird left to hear.",
            "Every water bird on the list. Astonishing.",
        ],
        "description": "A whole different world of birds lives around ponds, rivers, reedbeds and marshes. Hearing these birds takes patience, cunning and often complete silence!",
    },
    "brooder": {
        "name": "Brooder", "emoji": "\u2614",
        "verb": "Hear birds in the rain", "unit": "times", "one": "once",
        "levels": [1, 5, 15, 25, 40, 60, 80],
        "citations": [
            "You went out in the rain - proper dedication!",
            "Five rainy warbles. Weather doesn't stop you.",
            "Fifteen soggy sessions. Nothing keeps you in.",
            "Twenty-five rainy warbles. Who needs an umbrella?",
            "Forty soggy sessions. You love a puddle!",
            "Sixty rainy warbles. Rain or shine, you're out there.",
            "Eighty rainy warbles. The bravest birdwatcher of all!",
        ],
        "description": "Most people try to stay out of the rain. But you don't, and by the sounds of it, neither do the birds!",
    },
    "high_five": {
        "name": "High Five", "emoji": "\u270B",
        "verb": "Finish all five weekly challenges in", "unit": "weeks", "one": "a week",
        "levels": [1, 3, 6, 10, 15, 25, 40],
        "citations": [
            "All five challenges in one week - high five!",
            "Three full weeks. You love a challenge!",
            "Six weeks of all five. Nothing stops you.",
            "Ten perfect weeks. That's a whole term!",
            "Fifteen weeks of five. Brilliant birding!",
            "Twenty-five weeks. Half a year of high fives!",
            "Forty weeks of all five. A true champion!",
        ],
        "description": "Five challenges every week, and you finished the lot. Maxing out your feather count week after week!",
    },
    "wingman": {
        "name": "Wingman", "emoji": "\U0001F91D",
        "verb": "Share", "unit": "birds with someone", "one": "a bird with someone",
        "levels": [1, 5, 15, 25, 40, 60, 80],
        "citations": [
            "You shared a bird - spreading the warble!",
            "Five birds shared. You're spreading the word.",
            "Fifteen shared. A proper ambassador for birds.",
            "Twenty-five shared. Everyone's learning from you!",
            "Forty shared birds. A true bird teacher!",
            "Sixty shared. You've got everyone listening.",
            "Eighty birds shared. Thanks for spreading the word!",
        ],
        "description": "Sharing is caring! Hit the share button on any bird you hear so your friends know how brilliant you are!",
    },
}


def requirement_text(key: str, level_index: int) -> str:
    """Generates 'Hear 10 night birds after dark' from the trophy's own verb,
    threshold and unit - so the wording can't drift out of step with the
    numbers the way three hand-written strings would."""
    t = TROPHY_DEFINITIONS[key]
    n = t['levels'][level_index]
    rest = t['one'] if n == 1 and 'one' in t else f"{n} {t['unit']}"
    return f"{t['verb']} {rest}".replace("  ", " ")


def is_after_dark(lat: float, lng: float, moment_utc: datetime.datetime) -> bool:
    """Night Owl's "after dark": after dusk or before dawn. Civil dusk and
    dawn - the sun 6 degrees below the horizon, about when streetlights come
    on - rather than sunset, after which it stays light for half an hour or
    more. In UTC throughout, like is_before_sunrise."""
    if moment_utc.tzinfo is None:
        moment_utc = moment_utc.replace(tzinfo=datetime.timezone.utc)
    try:
        location = LocationInfo("", "", "UTC", lat, lng)
        s = sun(location.observer, date=moment_utc.date(), tzinfo=datetime.timezone.utc)
        return moment_utc < s["dawn"] or moment_utc > s["dusk"]
    except Exception:
        # No dusk at all: a northern summer night that never gets properly
        # dark (Shetland in June). Nothing counts as after dark then.
        return False


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


# Birder rank: what all the trophies add up to. Every trophy level is a leaf,
# and the leaves together give the child a title - its badge sits in the top
# bar beside the feathers on every screen, and opens the whole ladder. Thresholds are
# total leaves (147 in all). Each rank has its own look in the page
# (rankSeal), and a painting, when one arrives, as icon-rank-<key>.
BIRDER_RANKS = [
    (0, "Hatchling"), (5, "Lark"), (12, "Eavesdropper"), (25, "Trill Seeker"),
    (40, "Glider"), (60, "Flockstar"), (85, "Elder"), (115, "Warbler"),
]


def rank_key(name: str) -> str:
    """"Master Birder" -> "master-birder": the name of the rank's picture."""
    return name.lower().replace(" ", "-")


def birder_rank(leaves: int) -> dict:
    """The rank for a number of leaves, how far it is to the next, and the
    whole ladder - so the page never keeps a copy of the thresholds."""
    i = max(k for k, (need, _) in enumerate(BIRDER_RANKS) if leaves >= need)
    nxt = BIRDER_RANKS[i + 1] if i + 1 < len(BIRDER_RANKS) else None
    to_go = (nxt[0] - leaves) if nxt else 0
    return {"name": BIRDER_RANKS[i][1], "key": rank_key(BIRDER_RANKS[i][1]),
            "index": i, "leaves": leaves,
            "leaves_total": sum(len(t["levels"]) for t in TROPHY_DEFINITIONS.values()),
            "next_name": nxt[1] if nxt else None,
            "next_at": nxt[0] if nxt else None,
            "to_go": to_go,
            # How to climb, in the child's words (shown on the ladder).
            "message": (f"Win {to_go} more {'leaf' if to_go == 1 else 'leaves'} to be "
                        f"{'an' if nxt[1][0] in 'AEIOU' else 'a'} {nxt[1]}. "
                        "Every trophy level wins a leaf.") if nxt
                       else f"You're a {BIRDER_RANKS[-1][1]} - the very top!",
            "ladder": [{"name": n, "key": rank_key(n), "at": need} for need, n in BIRDER_RANKS]}
