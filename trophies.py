"""
Trophy definitions and the logic to check them.

Only the first 3 MVP trophies for now — Fledgling, Early Bird, Nomad.
The other 16 from the original design stay parked, same as always.
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
        "verb": "Go warbling", "unit": "times", "one": "once",
        "levels": [1, 15, 60, 100, 150, 250, 365],
        "citations": [
            "Your very first warble - welcome to the flock!",
            "Fifteen warbles in - this is a proper habit now.",
            "Sixty warbles. You're not a fledgling any more.",
            "A hundred warbles! You've got real wings now.",
            "A hundred and fifty. You're flying high.",
            "Two hundred and fifty warbles. What a birdwatcher!",
            "365 warbles - that's one for every day of the year!",
        ],
        "description": "This is where it all begins. Every birdwatcher remembers their first time listening properly - and you've kept coming back.",
    },
    "early_bird": {
        "name": "Early Bird", "emoji": "\U0001F305",
        "verb": "Warble before sunrise", "unit": "times", "one": "once",
        "levels": [1, 5, 15, 25, 40, 60, 80],
        "citations": [
            "Up before the birds - well, almost!",
            "Five sunrises beaten. That takes real getting up.",
            "Fifteen dawns. The birds must know you by now.",
            "Twenty-five sunrises. The sun's got competition!",
            "Forty dawns. You're a true morning bird.",
            "Sixty sunrises. The early bird really does get the worm.",
            "Eighty dawns. Nobody gets up earlier than you!",
        ],
        "description": "Dawn is when birds sing their loudest and best, to wake up the neighbourhood. Not many people hear it - you're one of the lucky ones.",
    },
    "nomad": {
        "name": "Nomad", "emoji": "\U0001F9ED",
        "verb": "Warble in", "unit": "different places",
        "levels": [10, 25, 50, 75, 100, 150, 200],
        "citations": [
            "Ten different spots, ten different adventures!",
            "Twenty-five places. You really do get about.",
            "Fifty different places. That's a proper explorer.",
            "Seventy-five places. Is there anywhere you haven't been?",
            "A hundred different places. Amazing!",
            "A hundred and fifty places. A true wanderer.",
            "Two hundred places. You've warbled everywhere!",
        ],
        "description": "Real birdwatchers know the best way to hear new birds is to go out listening for them - and that's exactly what you've been doing.",
    },
    "rooster": {
        "name": "Rooster", "emoji": "\U0001F413",
        "verb": "Warble", "unit": "times in the same place",
        "levels": [5, 20, 50, 75, 100, 150, 200],
        "citations": [
            "Same spot, five times - that's your patch now!",
            "Twenty visits. You know every tree in that place.",
            "Fifty visits to one spot. That's real devotion.",
            "Seventy-five visits. The birds there know your name!",
            "A hundred visits to one place. It's your kingdom now.",
            "A hundred and fifty visits. Nobody knows that spot like you.",
            "Two hundred visits. You ARE that place!",
        ],
        "description": "You know it now - the trees, the corners, the birds that live there. That's not luck, that's knowing your patch.",
    },
    "golden_eagle": {
        "name": "Golden Eagle", "emoji": "\U0001F985",
        "verb": "Hear", "unit": "Rare birds",
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
        "description": "These are the kind of sightings that make experienced birdwatchers gasp. You've got a brilliant ear.",
    },
    "dawn_chorus": {
        "name": "Dawn Chorus", "emoji": "\U0001F3B6",
        "verb": "Hear", "unit": "birds before sunrise in one warble",
        "levels": [5, 8, 12, 15, 18, 21, 25],
        "citations": [
            "Five songs, one sunrise - you caught the whole chorus!",
            "Eight birds before dawn. What a morning that was.",
            "Twelve birds in one dawn chorus. Extraordinary.",
            "Fifteen birds in one dawn. What an orchestra!",
            "Eighteen birds before sunrise. Brilliant listening!",
            "Twenty-one birds in one dawn chorus. Wow!",
            "Twenty-five birds in one dawn. The whole choir sang for you!",
        ],
        "description": "The dawn chorus is one of the most amazing sounds in nature, and you were there for it.",
    },
    "forager": {
        "name": "Forager", "emoji": "\U0001F33F",
        "verb": "Hear", "unit": "different birds",
        "levels": [20, 40, 70, 100, 130, 160, 200],
        "citations": [
            "Twenty different birds - that's a proper collection!",
            "Forty different birds. Your ear is getting sharp.",
            "Seventy different birds. That's a real naturalist.",
            "A hundred different birds! Superb.",
            "A hundred and thirty birds. You know so many songs!",
            "A hundred and sixty birds. An expert ear!",
            "Two hundred different birds. Unbelievable!",
        ],
        "description": "That's a huge range of songs to know by ear. You're building real knowledge of what's out there.",
    },
    "night_owl": {
        "name": "Night Owl", "emoji": "\U0001F989",
        "verb": "Hear", "unit": "night birds after dark",
        "levels": [5, 10, 20, 30, 45, 60, 80],
        "citations": [
            "Five night birds - you're not scared of the dark!",
            "Ten after dark. The night belongs to you.",
            "Twenty night birds. A true creature of the night.",
            "Thirty night birds. Owls must think you're one of them!",
            "Forty-five night birds. Spooky good listening!",
            "Sixty night birds. The moon is your friend.",
            "Eighty night birds. King of the night!",
        ],
        "description": "Owls, nightjars and woodcocks only come out at night. Hearing them takes proper dedication.",
    },
    "century": {
        "name": "Century", "emoji": "\U0001F4AF",
        "verb": "Hear", "unit": "birds from Warble's list",
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
        "description": "There are 100 birds on Warble's list. Working through them takes real skill, patience and a lot of listening.",
    },
    "globetrotter": {
        "name": "Globetrotter", "emoji": "\U0001F30D",
        "verb": "Complete", "unit": "collector packs", "one": "a collector pack",
        "levels": [1, 2, 3, 4, 6, 8, 10],
        "citations": [
            "A whole pack completed - every bird at every tier!",
            "Two packs finished. You've really covered the country.",
            "Three packs complete. You're a collector now!",
            "Four packs. Your collection is growing fast!",
            "Six packs complete. More than half way!",
            "Eight packs. Only two to go!",
            "Every collector pack complete. Nothing left to chase.",
        ],
        "description": "A bird everyone sees at home can be a special sight somewhere else. You had to travel to learn that.",
    },
    "summer_squad": {
        "name": "Summer Squad", "emoji": "\u2600\uFE0F",
        "verb": "Hear every summer visitor in", "unit": "summers", "one": "one summer",
        "levels": [1, 2, 3, 4, 5, 6, 7],
        "citations": [
            "Every summer bird, all in one summer - you didn't miss one!",
            "Two summers running. You know when they arrive now.",
            "Three summers complete. The migrants can't slip past you.",
            "Four summers. You're the swallows' best friend.",
            "Five summers! You always know when they're back.",
            "Six summers of every visitor. Amazing!",
            "Seven summers. You're part of their journey now!",
        ],
        "description": "Thirteen birds fly thousands of miles to spend the summer here, and every one of them leaves again. Catching all of them in a single season means being out there at the right time, again and again.",
    },
    "empty_nester": {
        "name": "Empty Nester", "emoji": "\U0001FAB9",
        "verb": "Go warbling", "unit": "times without hearing a bird",
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
        "description": "Every real birdwatcher knows that feeling. Coming back and trying again after a quiet day is the hardest part of all.",
    },
    "preener": {
        "name": "Preener", "emoji": "\U0001FAB6",
        "verb": "Collect", "unit": "Dress Up items",
        "levels": [10, 22, 40, 50, 60, 65, 70],
        "citations": [
            "Ten outfits and counting - looking sharp!",
            "Twenty-two items. Quite the wardrobe.",
            "Forty items. You could open your own shop!",
            "Fifty items. Best-dressed bird in town!",
            "Sixty items. What a collection!",
            "Sixty-five items. Nearly everything!",
            "Every single item. Nothing left to buy!",
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
        "description": "Birds change enormously through the year - who's singing, who's visiting, who's flown away.",
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
        "description": "Keeping a habit going is genuinely hard, and birds reward the people who show up again and again.",
    },
    "migrator": {
        "name": "Migrator", "emoji": "\U0001F5FA\uFE0F",
        "verb": "Hear", "unit": "birds in two places 5km apart",
        "one": "the same bird in two places 5km apart",
        "levels": [1, 5, 15, 20, 30, 40, 50],
        "citations": [
            "You heard the same bird miles from where you first met it!",
            "Five birds tracked across the miles.",
            "Fifteen birds heard far and wide. A real map-maker.",
            "Twenty birds heard far apart. You get around!",
            "Thirty birds across the miles. Like a migrating bird!",
            "Forty birds far and wide. A true traveller.",
            "Fifty birds heard far apart. You've mapped the country!",
        ],
        "description": "Birds move around far more than people realise, and now you've got the proof yourself.",
    },
    "skylark": {
        "name": "Skylark", "emoji": "\U0001F33E",
        "verb": "Hear", "unit": "farmland or hedgerow birds",
        "levels": [2, 3, 4, 6, 8, 9, 10],
        "citations": [
            "Two farmland birds - out in the open fields!",
            "Three farmland birds. Listen to those hedgerows!",
            "Four farmland birds. You know the open fields!",
            "Six farmland birds. The hedgerows are yours.",
            "Eight farmland birds. Brilliant!",
            "Nine! Just one farmland bird left to hear.",
            "Every farmland bird on the list. Remarkable.",
        ],
        "description": "These are some of the trickiest birds to hear, and many of them are getting rarer, so every one counts.",
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
        "description": "These are the hunters - the ones circling high overhead - and hearing them takes real patience.",
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
        "description": "A whole different world of birds lives around water - ponds, rivers, reedbeds and marshes.",
    },
    "brooder": {
        "name": "Brooder", "emoji": "\u2614",
        "verb": "Go warbling in the rain", "unit": "times", "one": "once",
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
        "description": "Most people stay inside, but plenty of birds keep right on singing - so you heard something most people never do.",
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
            "Eighty birds shared. Warble's best friend!",
        ],
        "description": "Birdwatchers have always told each other what they've heard, and now you're part of that too.",
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
