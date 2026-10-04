"""
Every bird in the UK 100, in one place.

This replaces the old split between bird_facts.py (rich data for 31 researched
species) and bird_stats.py (universal data for all 100). Keeping both meant the
same bird had its weight and length recorded twice, and they had already drifted
apart in four places - Blue Tit was 10.9g in one file and 11g in the other. One
file, one value.

Every bird has: length_cm, weight_g, speed_kmh, uk_pop, song, brains, habitat,
diet. Those drive the stat tiles and the Top Trumps ratings, so no card is ever
missing them.

Researched birds additionally have: wingspan_cm, conservation_status,
habitat_tags and the kid-friendly size/weight comparisons. Where a researched
figure disagreed with the general one, the researched value was kept - it came
from a real source.

Ratings out of 100 are computed by RANKING each bird against the other 99, not
by scaling raw values. Population spans five orders of magnitude; scaled
linearly, every small bird would score 1 and only the swan would move.

Honest sourcing note: lengths, weights and populations are standard reference
figures. Flight speeds are published values where known and reasoned estimates
from body size and wing shape where not. Song and brains are informed
judgements, not measurements.
"""

import math

HABITAT_ICONS = {'Garden & Parks': '🌳', 'Woodland': '🌲', 'Wetland & Coast': '🌊', 'Farmland': '🌾', 'Towns & Cities': '🏘️'}

STAT_LABELS = {
    "size": "Size", "speed": "Speed", "population": "Population",
    "song": "Song", "brains": "Brains",
}

BIRDS = {
    # --- Locals
    'European Robin': {
        "length_cm": 14, "weight_g": 19,
        "speed_kmh": 30, "uk_pop": 13000000, "song": 9, "brains": 5,
        "habitat": 'Gardens & parks', "diet": 'Insects & worms',
        "wingspan_cm": 21, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Woodland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Common Blackbird': {
        "length_cm": 25, "weight_g": 100,
        "speed_kmh": 38, "uk_pop": 15000000, "song": 10, "brains": 5,
        "habitat": 'Gardens & woodland', "diet": 'Worms & berries',
        "wingspan_cm": 36, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Woodland', 'Farmland'],
        "size_comparison": 'About as long as your forearm.',
        "weight_comparison": 'About as heavy as a big apple.',
    },
    'House Sparrow': {
        "length_cm": 15, "weight_g": 30,
        "speed_kmh": 38, "uk_pop": 10000000, "song": 3, "brains": 5,
        "habitat": 'Towns & farms', "diet": 'Seeds & scraps',
        "wingspan_cm": 22, "conservation_status": 'Red',
        "habitat_tags": ['Garden & Parks', 'Towns & Cities', 'Farmland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as five pound coins.',
    },
    'Dunnock': {
        "length_cm": 14, "weight_g": 21,
        "speed_kmh": 30, "uk_pop": 5000000, "song": 6, "brains": 4,
        "habitat": 'Hedges & gardens', "diet": 'Insects & seeds',
        "wingspan_cm": 20, "conservation_status": 'Amber',
        "habitat_tags": ['Garden & Parks', 'Woodland', 'Farmland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Common Starling': {
        "length_cm": 21, "weight_g": 80,
        "speed_kmh": 60, "uk_pop": 5000000, "song": 7, "brains": 8,
        "habitat": 'Towns & farmland', "diet": 'Insects & fruit',
        "wingspan_cm": 40, "conservation_status": 'Red',
        "habitat_tags": ['Garden & Parks', 'Towns & Cities', 'Farmland'],
        "size_comparison": 'About as long as your hand and wrist.',
        "weight_comparison": 'About as heavy as a tennis ball.',
    },
    'Common Wood-Pigeon': {
        "length_cm": 41, "weight_g": 500,
        "speed_kmh": 60, "uk_pop": 10000000, "song": 4, "brains": 4,
        "habitat": 'Woods & gardens', "diet": 'Leaves & seeds',
        "wingspan_cm": 76, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Woodland', 'Farmland', 'Towns & Cities'],
        "size_comparison": 'As long as your whole arm!',
        "weight_comparison": 'About as heavy as a big bag of sugar... well, half of one!',
    },
    'Eurasian Collared-Dove': {
        "length_cm": 32, "weight_g": 200,
        "speed_kmh": 55, "uk_pop": 2000000, "song": 4, "brains": 4,
        "habitat": 'Towns & gardens', "diet": 'Seeds & grain',
        "wingspan_cm": 51, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Towns & Cities'],
        "size_comparison": 'About as long as your forearm.',
        "weight_comparison": 'About as heavy as a big apple.',
    },
    'Rock Pigeon': {
        "length_cm": 33, "weight_g": 350,
        "speed_kmh": 70, "uk_pop": 1000000, "song": 3, "brains": 7,
        "habitat": 'Towns & cliffs', "diet": 'Seeds & scraps',
        "wingspan_cm": 65, "conservation_status": 'Green',
        "habitat_tags": ['Towns & Cities'],
        "size_comparison": 'About as long as your forearm.',
        "weight_comparison": 'About as heavy as a big apple.',
    },
    'Eurasian Tree Sparrow': {
        "length_cm": 14, "weight_g": 22,
        "speed_kmh": 36, "uk_pop": 450000, "song": 3, "brains": 5,
        "habitat": 'Farmland hedges', "diet": 'Seeds & insects',
        "wingspan_cm": 21, "conservation_status": 'Red',
        "habitat_tags": ['Farmland', 'Garden & Parks'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as three pound coins.',
    },
    'European Turtle-Dove': {
        "length_cm": 27, "weight_g": 150,
        "speed_kmh": 60, "uk_pop": 6000, "song": 5, "brains": 4,
        "habitat": 'Farmland & scrub', "diet": 'Seeds',
    },

    # --- Acrobats
    'Eurasian Blue Tit': {
        "length_cm": 11.5, "weight_g": 10.9,
        "speed_kmh": 30, "uk_pop": 15000000, "song": 6, "brains": 7,
        "habitat": 'Woods & gardens', "diet": 'Insects & seeds',
        "wingspan_cm": 18, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Woodland'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'Lighter than two pound coins.',
    },
    'Great Tit': {
        "length_cm": 14, "weight_g": 18,
        "speed_kmh": 32, "uk_pop": 10000000, "song": 7, "brains": 7,
        "habitat": 'Woods & gardens', "diet": 'Insects & seeds',
        "wingspan_cm": 24, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Woodland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Coal Tit': {
        "length_cm": 11, "weight_g": 9,
        "speed_kmh": 28, "uk_pop": 3000000, "song": 6, "brains": 6,
        "habitat": 'Conifer woods', "diet": 'Insects & seeds',
        "wingspan_cm": 19, "conservation_status": 'Green',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'Lighter than two pound coins.',
    },
    'Long-tailed Tit': {
        "length_cm": 14, "weight_g": 8,
        "speed_kmh": 27, "uk_pop": 1900000, "song": 4, "brains": 6,
        "habitat": 'Hedges & woods', "diet": 'Tiny insects',
        "wingspan_cm": 18, "conservation_status": 'Green',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'Tiny - and over half of it is tail!',
        "weight_comparison": 'Lighter than two pound coins.',
    },
    'Eurasian Nuthatch': {
        "length_cm": 14, "weight_g": 24,
        "speed_kmh": 32, "uk_pop": 500000, "song": 6, "brains": 7,
        "habitat": 'Mature woodland', "diet": 'Nuts & insects',
        "wingspan_cm": 25, "conservation_status": 'Green',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as four pound coins.',
    },
    'Eurasian Treecreeper': {
        "length_cm": 13, "weight_g": 10,
        "speed_kmh": 26, "uk_pop": 400000, "song": 5, "brains": 5,
        "habitat": 'Woodland trunks', "diet": 'Insects in bark',
        "wingspan_cm": 19, "conservation_status": 'Green',
        "habitat_tags": ['Woodland'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'Lighter than two pound coins.',
    },
    'Goldcrest': {
        "length_cm": 9, "weight_g": 6,
        "speed_kmh": 25, "uk_pop": 1300000, "song": 5, "brains": 4,
        "habitat": 'Conifer woods', "diet": 'Tiny insects',
        "wingspan_cm": 14, "conservation_status": 'Green',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'The smallest bird in Britain - tinier than your thumb!',
        "weight_comparison": 'About as heavy as six paperclips.',
    },
    'Eurasian Wren': {
        "length_cm": 9.5, "weight_g": 10,
        "speed_kmh": 28, "uk_pop": 11000000, "song": 9, "brains": 5,
        "habitat": 'Hedges & woods', "diet": 'Insects & spiders',
        "wingspan_cm": 15, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Woodland'],
        "size_comparison": 'Tiny — barely longer than your thumb!',
        "weight_comparison": 'Lighter than two pound coins.',
    },
    'Marsh Tit': {
        "length_cm": 12, "weight_g": 12,
        "speed_kmh": 28, "uk_pop": 82000, "song": 5, "brains": 7,
        "habitat": 'Damp woodland', "diet": 'Insects & seeds',
    },
    'Willow Tit': {
        "length_cm": 12, "weight_g": 11,
        "speed_kmh": 28, "uk_pop": 5000, "song": 5, "brains": 7,
        "habitat": 'Wet scrubby woods', "diet": 'Insects & seeds',
    },

    # --- Nutcrackers
    'Common Chaffinch': {
        "length_cm": 14.5, "weight_g": 24,
        "speed_kmh": 35, "uk_pop": 12000000, "song": 7, "brains": 5,
        "habitat": 'Woods & gardens', "diet": 'Seeds & insects',
        "wingspan_cm": 26, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Woodland', 'Farmland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as four pound coins.',
    },
    'European Goldfinch': {
        "length_cm": 12, "weight_g": 16,
        "speed_kmh": 35, "uk_pop": 3000000, "song": 7, "brains": 5,
        "habitat": 'Gardens & weeds', "diet": 'Small seeds',
        "wingspan_cm": 23, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Farmland'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'About as heavy as three pound coins.',
    },
    'European Greenfinch': {
        "length_cm": 15, "weight_g": 28,
        "speed_kmh": 35, "uk_pop": 1000000, "song": 5, "brains": 5,
        "habitat": 'Gardens & hedges', "diet": 'Seeds & buds',
        "wingspan_cm": 26, "conservation_status": 'Red',
        "habitat_tags": ['Garden & Parks', 'Woodland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as five pound coins.',
    },
    'Common Linnet': {
        "length_cm": 13, "weight_g": 18,
        "speed_kmh": 35, "uk_pop": 1800000, "song": 6, "brains": 5,
        "habitat": 'Heath & farmland', "diet": 'Small seeds',
        "wingspan_cm": 23, "conservation_status": 'Red',
        "habitat_tags": ['Farmland', 'Garden & Parks'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'About as heavy as three pound coins.',
    },
    'Eurasian Bullfinch': {
        "length_cm": 16, "weight_g": 25,
        "speed_kmh": 32, "uk_pop": 500000, "song": 4, "brains": 5,
        "habitat": 'Woods & hedges', "diet": 'Buds & seeds',
        "wingspan_cm": 26, "conservation_status": 'Amber',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as four pound coins.',
    },
    'Eurasian Siskin': {
        "length_cm": 12, "weight_g": 14,
        "speed_kmh": 33, "uk_pop": 850000, "song": 6, "brains": 5,
        "habitat": 'Conifer woods', "diet": 'Conifer seeds',
        "wingspan_cm": 22, "conservation_status": 'Green',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'Lighter than three pound coins.',
    },
    'Yellowhammer': {
        "length_cm": 16, "weight_g": 27,
        "speed_kmh": 32, "uk_pop": 1200000, "song": 7, "brains": 5,
        "habitat": 'Farmland hedges', "diet": 'Seeds & insects',
        "wingspan_cm": 26, "conservation_status": 'Red',
        "habitat_tags": ['Farmland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as four pound coins.',
    },
    'Reed Bunting': {
        "length_cm": 15, "weight_g": 20,
        "speed_kmh": 30, "uk_pop": 500000, "song": 5, "brains": 5,
        "habitat": 'Reeds & marsh', "diet": 'Seeds & insects',
        "wingspan_cm": 23, "conservation_status": 'Amber',
        "habitat_tags": ['Wetland & Coast', 'Farmland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Hawfinch': {
        "length_cm": 18, "weight_g": 55,
        "speed_kmh": 40, "uk_pop": 2000, "song": 3, "brains": 6,
        "habitat": 'Mature woodland', "diet": 'Hard seeds & stones',
    },
    'Corn Bunting': {
        "length_cm": 18, "weight_g": 45,
        "speed_kmh": 32, "uk_pop": 22000, "song": 4, "brains": 4,
        "habitat": 'Open farmland', "diet": 'Seeds & insects',
    },

    # --- Little Loudmouths
    'Eurasian Blackcap': {
        "length_cm": 14, "weight_g": 18,
        "speed_kmh": 32, "uk_pop": 3000000, "song": 10, "brains": 5,
        "habitat": 'Woods & gardens', "diet": 'Insects & berries',
        "wingspan_cm": 23, "conservation_status": 'Green',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Common Chiffchaff': {
        "length_cm": 11, "weight_g": 9,
        "speed_kmh": 28, "uk_pop": 1800000, "song": 6, "brains": 5,
        "habitat": 'Woods & scrub', "diet": 'Small insects',
        "wingspan_cm": 19, "conservation_status": 'Green',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'Lighter than two pound coins.',
    },
    'Willow Warbler': {
        "length_cm": 11, "weight_g": 9,
        "speed_kmh": 28, "uk_pop": 4000000, "song": 8, "brains": 5,
        "habitat": 'Young woodland', "diet": 'Small insects',
        "wingspan_cm": 19, "conservation_status": 'Amber',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'Lighter than two pound coins.',
    },
    'Common Whitethroat': {
        "length_cm": 14, "weight_g": 16,
        "speed_kmh": 30, "uk_pop": 2000000, "song": 7, "brains": 5,
        "habitat": 'Hedges & scrub', "diet": 'Insects & berries',
        "wingspan_cm": 21, "conservation_status": 'Green',
        "habitat_tags": ['Farmland', 'Garden & Parks'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'Lighter than three pound coins.',
    },
    'Sedge Warbler': {
        "length_cm": 13, "weight_g": 12,
        "speed_kmh": 29, "uk_pop": 500000, "song": 7, "brains": 5,
        "habitat": 'Reeds & marsh', "diet": 'Insects',
        "wingspan_cm": 19, "conservation_status": 'Green',
        "habitat_tags": ['Wetland & Coast'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'Lighter than two pound coins.',
    },
    'Eurasian Reed Warbler': {
        "length_cm": 13, "weight_g": 13,
        "speed_kmh": 29, "uk_pop": 260000, "song": 6, "brains": 5,
        "habitat": 'Reedbeds', "diet": 'Insects',
        "wingspan_cm": 19, "conservation_status": 'Green',
        "habitat_tags": ['Wetland & Coast'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'Lighter than two pound coins.',
    },
    'European Stonechat': {
        "length_cm": 12, "weight_g": 15,
        "speed_kmh": 30, "uk_pop": 120000, "song": 5, "brains": 5,
        "habitat": 'Heath & coast', "diet": 'Insects',
    },
    'Common Redstart': {
        "length_cm": 14, "weight_g": 15,
        "speed_kmh": 32, "uk_pop": 200000, "song": 7, "brains": 5,
        "habitat": 'Upland woods', "diet": 'Insects',
        "wingspan_cm": 22, "conservation_status": 'Amber',
        "habitat_tags": ['Woodland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Lesser Whitethroat': {
        "length_cm": 13, "weight_g": 13,
        "speed_kmh": 30, "uk_pop": 74000, "song": 6, "brains": 5,
        "habitat": 'Thick hedges', "diet": 'Insects & berries',
    },
    'Common Firecrest': {
        "length_cm": 9, "weight_g": 6,
        "speed_kmh": 25, "uk_pop": 1700, "song": 5, "brains": 4,
        "habitat": 'Conifer woods', "diet": 'Tiny insects',
    },

    # --- Mischiefs
    'Eurasian Magpie': {
        "length_cm": 45, "weight_g": 220,
        "speed_kmh": 45, "uk_pop": 1300000, "song": 3, "brains": 9,
        "habitat": 'Towns & farmland', "diet": 'Almost anything',
        "wingspan_cm": 56, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Farmland', 'Towns & Cities'],
        "size_comparison": 'As long as your arm — but half of that is tail!',
        "weight_comparison": 'About as heavy as a tin of beans.',
    },
    'Eurasian Jay': {
        "length_cm": 34, "weight_g": 170,
        "speed_kmh": 45, "uk_pop": 340000, "song": 3, "brains": 9,
        "habitat": 'Oak woodland', "diet": 'Acorns & insects',
        "wingspan_cm": 55, "conservation_status": 'Green',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'As long as your arm from elbow to fingertips.',
        "weight_comparison": 'About as heavy as a big bag of crisps... times four!',
    },
    'Western Jackdaw': {
        "length_cm": 34, "weight_g": 240,
        "speed_kmh": 55, "uk_pop": 3000000, "song": 3, "brains": 9,
        "habitat": 'Towns & cliffs', "diet": 'Almost anything',
        "wingspan_cm": 70, "conservation_status": 'Green',
        "habitat_tags": ['Towns & Cities', 'Farmland', 'Woodland'],
        "size_comparison": 'As long as your arm from elbow to fingertips.',
        "weight_comparison": 'About as heavy as a tin of beans.',
    },
    'Carrion Crow': {
        "length_cm": 47, "weight_g": 540,
        "speed_kmh": 50, "uk_pop": 2000000, "song": 2, "brains": 10,
        "habitat": 'Almost anywhere', "diet": 'Almost anything',
        "wingspan_cm": 95, "conservation_status": 'Green',
        "habitat_tags": ['Garden & Parks', 'Farmland', 'Towns & Cities', 'Woodland'],
        "size_comparison": 'As long as your whole arm!',
        "weight_comparison": 'About as heavy as a big tin of paint.',
    },
    'Rook': {
        "length_cm": 45, "weight_g": 480,
        "speed_kmh": 50, "uk_pop": 2000000, "song": 2, "brains": 9,
        "habitat": 'Farmland & rookeries', "diet": 'Worms & grain',
        "wingspan_cm": 90, "conservation_status": 'Green',
        "habitat_tags": ['Farmland', 'Woodland'],
        "size_comparison": 'As long as your whole arm!',
        "weight_comparison": 'About as heavy as a big tin of paint.',
    },
    'Northern Raven': {
        "length_cm": 64, "weight_g": 1200,
        "speed_kmh": 55, "uk_pop": 30000, "song": 3, "brains": 10,
        "habitat": 'Cliffs & moors', "diet": 'Carrion & anything',
    },
    'Great Spotted Woodpecker': {
        "length_cm": 23, "weight_g": 85,
        "speed_kmh": 40, "uk_pop": 400000, "song": 4, "brains": 7,
        "habitat": 'Woodland', "diet": 'Grubs in wood',
        "wingspan_cm": 36, "conservation_status": 'Green',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'About as long as your forearm.',
        "weight_comparison": 'About as heavy as a small apple.',
    },
    'European Green Woodpecker': {
        "length_cm": 32, "weight_g": 190,
        "speed_kmh": 40, "uk_pop": 130000, "song": 4, "brains": 7,
        "habitat": 'Parks & grassland', "diet": 'Ants',
    },
    'Lesser Spotted Woodpecker': {
        "length_cm": 15, "weight_g": 22,
        "speed_kmh": 35, "uk_pop": 2000, "song": 3, "brains": 7,
        "habitat": 'Old woodland', "diet": 'Grubs in wood',
    },
    'Common Cuckoo': {
        "length_cm": 33, "weight_g": 110,
        "speed_kmh": 55, "uk_pop": 30000, "song": 8, "brains": 6,
        "habitat": 'Woods & moors', "diet": 'Hairy caterpillars',
        "wingspan_cm": 60, "conservation_status": 'Red',
        "habitat_tags": ['Woodland', 'Farmland'],
        "size_comparison": 'As long as your arm from elbow to fingertips.',
        "weight_comparison": 'About as heavy as a small apple.',
    },

    # --- Diggers
    'Song Thrush': {
        "length_cm": 23, "weight_g": 83,
        "speed_kmh": 40, "uk_pop": 2400000, "song": 10, "brains": 6,
        "habitat": 'Gardens & woods', "diet": 'Snails & worms',
        "wingspan_cm": 34, "conservation_status": 'Amber',
        "habitat_tags": ['Garden & Parks', 'Woodland', 'Farmland'],
        "size_comparison": 'About as long as your forearm.',
        "weight_comparison": 'About as heavy as a small apple.',
    },
    'Mistle Thrush': {
        "length_cm": 27, "weight_g": 130,
        "speed_kmh": 45, "uk_pop": 340000, "song": 8, "brains": 6,
        "habitat": 'Parks & woods', "diet": 'Berries & worms',
        "wingspan_cm": 45, "conservation_status": 'Red',
        "habitat_tags": ['Woodland', 'Garden & Parks'],
        "size_comparison": 'About as long as your forearm.',
        "weight_comparison": 'About as heavy as a big apple.',
    },
    'Eurasian Skylark': {
        "length_cm": 18, "weight_g": 38,
        "speed_kmh": 35, "uk_pop": 3000000, "song": 10, "brains": 5,
        "habitat": 'Open farmland', "diet": 'Seeds & insects',
        "wingspan_cm": 32, "conservation_status": 'Red',
        "habitat_tags": ['Farmland'],
        "size_comparison": 'About as long as your hand and wrist.',
        "weight_comparison": 'About as heavy as six pound coins.',
    },
    'Common Pheasant': {
        "length_cm": 65, "weight_g": 1200,
        "speed_kmh": 45, "uk_pop": 4000000, "song": 2, "brains": 4,
        "habitat": 'Farmland & woods', "diet": 'Seeds & shoots',
        "wingspan_cm": 80, "conservation_status": 'Green',
        "habitat_tags": ['Farmland', 'Woodland'],
        "size_comparison": 'Longer than your whole arm - and most of that is tail!',
        "weight_comparison": 'About as heavy as a big bag of sugar.',
    },
    'White Wagtail': {
        "length_cm": 18, "weight_g": 21,
        "speed_kmh": 35, "uk_pop": 900000, "song": 4, "brains": 5,
        "habitat": 'Open ground & water', "diet": 'Insects',
        "wingspan_cm": 27, "conservation_status": 'Green',
        "habitat_tags": ['Towns & Cities', 'Wetland & Coast'],
        "size_comparison": 'About as long as your hand and wrist - with a very waggy tail!',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Grey Wagtail': {
        "length_cm": 19, "weight_g": 18,
        "speed_kmh": 35, "uk_pop": 76000, "song": 4, "brains": 5,
        "habitat": 'Fast streams', "diet": 'Insects',
    },
    'Meadow Pipit': {
        "length_cm": 15, "weight_g": 18,
        "speed_kmh": 32, "uk_pop": 4000000, "song": 6, "brains": 4,
        "habitat": 'Moors & grassland', "diet": 'Insects',
        "wingspan_cm": 24, "conservation_status": 'Amber',
        "habitat_tags": ['Farmland'],
        "size_comparison": 'About as long as a school ruler.',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Redwing': {
        "length_cm": 21, "weight_g": 63,
        "speed_kmh": 45, "uk_pop": 700000, "song": 6, "brains": 5,
        "habitat": 'Fields & hedges', "diet": 'Berries & worms',
        "wingspan_cm": 34, "conservation_status": 'Amber',
        "habitat_tags": ['Woodland', 'Farmland'],
        "size_comparison": 'About as long as your hand and wrist.',
        "weight_comparison": 'About as heavy as a small apple.',
    },
    'Grey Partridge': {
        "length_cm": 30, "weight_g": 390,
        "speed_kmh": 45, "uk_pop": 74000, "song": 3, "brains": 4,
        "habitat": 'Open farmland', "diet": 'Seeds & shoots',
    },
    'Ring Ouzel': {
        "length_cm": 24, "weight_g": 110,
        "speed_kmh": 45, "uk_pop": 12000, "song": 8, "brains": 5,
        "habitat": 'Upland crags', "diet": 'Worms & berries',
    },

    # --- Sky Divers
    'Common Buzzard': {
        "length_cm": 54, "weight_g": 780,
        "speed_kmh": 45, "uk_pop": 250000, "song": 3, "brains": 7,
        "habitat": 'Farmland & woods', "diet": 'Rabbits & carrion',
        "wingspan_cm": 120, "conservation_status": 'Green',
        "habitat_tags": ['Farmland', 'Woodland'],
        "size_comparison": 'Wings wider than you can stretch your arms!',
        "weight_comparison": 'About as heavy as a big bag of flour.',
    },
    'Common Kestrel': {
        "length_cm": 34, "weight_g": 190,
        "speed_kmh": 55, "uk_pop": 90000, "song": 2, "brains": 7,
        "habitat": 'Farmland & verges', "diet": 'Voles & insects',
        "wingspan_cm": 76, "conservation_status": 'Amber',
        "habitat_tags": ['Farmland', 'Towns & Cities'],
        "size_comparison": 'As long as your arm from elbow to fingertips.',
        "weight_comparison": 'About as heavy as a tin of beans.',
    },
    'Eurasian Sparrowhawk': {
        "length_cm": 33, "weight_g": 220,
        "speed_kmh": 50, "uk_pop": 100000, "song": 2, "brains": 7,
        "habitat": 'Woods & gardens', "diet": 'Small birds',
    },
    'Red Kite': {
        "length_cm": 63, "weight_g": 1000,
        "speed_kmh": 45, "uk_pop": 12000, "song": 2, "brains": 7,
        "habitat": 'Farmland & woods', "diet": 'Carrion & scraps',
    },
    'Peregrine Falcon': {
        "length_cm": 46, "weight_g": 750,
        "speed_kmh": 65, "uk_pop": 4500, "song": 2, "brains": 7,
        "habitat": 'Cliffs & cities', "diet": 'Birds in flight',
        "wingspan_cm": 105, "conservation_status": 'Green',
        "habitat_tags": ['Towns & Cities', 'Wetland & Coast'],
        "size_comparison": 'About as long as your whole arm.',
        "weight_comparison": 'About as heavy as a big tin of paint.',
    },
    'Tawny Owl': {
        "length_cm": 38, "weight_g": 440,
        "speed_kmh": 40, "uk_pop": 100000, "song": 7, "brains": 7,
        "habitat": 'Woodland', "diet": 'Voles & birds',
    },
    'Barn Owl': {
        "length_cm": 34, "weight_g": 330,
        "speed_kmh": 35, "uk_pop": 12000, "song": 3, "brains": 6,
        "habitat": 'Farmland & barns', "diet": 'Voles & mice',
    },
    'Little Owl': {
        "length_cm": 22, "weight_g": 180,
        "speed_kmh": 40, "uk_pop": 8000, "song": 4, "brains": 6,
        "habitat": 'Farmland & orchards', "diet": 'Insects & voles',
    },
    'Eurasian Hobby': {
        "length_cm": 32, "weight_g": 210,
        "speed_kmh": 60, "uk_pop": 2800, "song": 3, "brains": 7,
        "habitat": 'Heath & farmland', "diet": 'Dragonflies & swallows',
    },
    'Long-eared Owl': {
        "length_cm": 36, "weight_g": 290,
        "speed_kmh": 40, "uk_pop": 3500, "song": 4, "brains": 6,
        "habitat": 'Conifer woods', "diet": 'Voles & mice',
    },

    # --- Waterwings
    'Mallard': {
        "length_cm": 58, "weight_g": 1100,
        "speed_kmh": 60, "uk_pop": 1000000, "song": 3, "brains": 6,
        "habitat": 'Ponds & rivers', "diet": 'Plants & insects',
        "wingspan_cm": 90, "conservation_status": 'Amber',
        "habitat_tags": ['Wetland & Coast', 'Garden & Parks'],
        "size_comparison": 'About as long as your whole arm.',
        "weight_comparison": 'About as heavy as a big bag of sugar.',
    },
    'Mute Swan': {
        "length_cm": 150, "weight_g": 11000,
        "speed_kmh": 55, "uk_pop": 75000, "song": 2, "brains": 6,
        "habitat": 'Lakes & rivers', "diet": 'Water plants',
    },
    'Canada Goose': {
        "length_cm": 95, "weight_g": 4500,
        "speed_kmh": 60, "uk_pop": 200000, "song": 2, "brains": 6,
        "habitat": 'Parks & lakes', "diet": 'Grass & water plants',
    },
    'Greylag Goose': {
        "length_cm": 84, "weight_g": 3300,
        "speed_kmh": 60, "uk_pop": 150000, "song": 3, "brains": 6,
        "habitat": 'Lakes & marshes', "diet": 'Grass & grain',
    },
    'Eurasian Coot': {
        "length_cm": 38, "weight_g": 800,
        "speed_kmh": 40, "uk_pop": 200000, "song": 2, "brains": 5,
        "habitat": 'Lakes & ponds', "diet": 'Water plants',
    },
    'Common Moorhen': {
        "length_cm": 33, "weight_g": 320,
        "speed_kmh": 35, "uk_pop": 250000, "song": 3, "brains": 5,
        "habitat": 'Ponds & ditches', "diet": 'Plants & insects',
        "wingspan_cm": 52, "conservation_status": 'Green',
        "habitat_tags": ['Wetland & Coast', 'Garden & Parks'],
        "size_comparison": 'About as long as your forearm.',
        "weight_comparison": 'About as heavy as a tin of beans.',
    },
    'Little Grebe': {
        "length_cm": 27, "weight_g": 150,
        "speed_kmh": 40, "uk_pop": 16000, "song": 4, "brains": 5,
        "habitat": 'Ponds & canals', "diet": 'Small fish & insects',
    },
    'Great Crested Grebe': {
        "length_cm": 48, "weight_g": 1000,
        "speed_kmh": 50, "uk_pop": 19000, "song": 3, "brains": 5,
        "habitat": 'Lakes & reservoirs', "diet": 'Fish',
    },
    'Common Kingfisher': {
        "length_cm": 17, "weight_g": 40,
        "speed_kmh": 45, "uk_pop": 14000, "song": 2, "brains": 6,
        "habitat": 'Clear rivers', "diet": 'Small fish',
    },
    'Common Eider': {
        "length_cm": 60, "weight_g": 2200,
        "speed_kmh": 70, "uk_pop": 60000, "song": 3, "brains": 5,
        "habitat": 'Rocky coasts', "diet": 'Mussels & crabs',
    },

    # --- Mucky Puddles
    'Grey Heron': {
        "length_cm": 95, "weight_g": 1600,
        "speed_kmh": 45, "uk_pop": 40000, "song": 2, "brains": 7,
        "habitat": 'Rivers & lakes', "diet": 'Fish & frogs',
        "wingspan_cm": 185, "conservation_status": 'Green',
        "habitat_tags": ['Wetland & Coast', 'Garden & Parks'],
        "size_comparison": 'Almost as tall as a five-year-old!',
        "weight_comparison": 'About as heavy as a big bag of sugar and a half.',
    },
    'Eurasian Oystercatcher': {
        "length_cm": 43, "weight_g": 540,
        "speed_kmh": 55, "uk_pop": 340000, "song": 4, "brains": 5,
        "habitat": 'Coasts & fields', "diet": 'Shellfish & worms',
        "wingspan_cm": 83, "conservation_status": 'Amber',
        "habitat_tags": ['Wetland & Coast', 'Farmland'],
        "size_comparison": 'About as long as your whole arm.',
        "weight_comparison": 'About as heavy as a tin of beans.',
    },
    'Common Ringed Plover': {
        "length_cm": 19, "weight_g": 64,
        "speed_kmh": 55, "uk_pop": 15000, "song": 4, "brains": 4,
        "habitat": 'Shingle beaches', "diet": 'Insects & worms',
    },
    'Sanderling': {
        "length_cm": 20, "weight_g": 55,
        "speed_kmh": 60, "uk_pop": 20000, "song": 3, "brains": 4,
        "habitat": 'Sandy beaches', "diet": 'Sand shrimps',
    },
    'Ruddy Turnstone': {
        "length_cm": 23, "weight_g": 110,
        "speed_kmh": 55, "uk_pop": 48000, "song": 3, "brains": 5,
        "habitat": 'Rocky shores', "diet": 'Anything under stones',
    },
    'Common Sandpiper': {
        "length_cm": 20, "weight_g": 50,
        "speed_kmh": 50, "uk_pop": 15000, "song": 5, "brains": 4,
        "habitat": 'Upland rivers', "diet": 'Insects & worms',
    },
    'Common Snipe': {
        "length_cm": 26, "weight_g": 110,
        "speed_kmh": 55, "uk_pop": 76000, "song": 6, "brains": 4,
        "habitat": 'Marsh & bog', "diet": 'Worms in mud',
    },
    'Northern Lapwing': {
        "length_cm": 30, "weight_g": 220,
        "speed_kmh": 45, "uk_pop": 140000, "song": 6, "brains": 5,
        "habitat": 'Wet farmland', "diet": 'Worms & insects',
    },
    'Eurasian Curlew': {
        "length_cm": 55, "weight_g": 800,
        "speed_kmh": 50, "uk_pop": 125000, "song": 9, "brains": 5,
        "habitat": 'Moors & estuaries', "diet": 'Worms & crabs',
        "wingspan_cm": 90, "conservation_status": 'Red',
        "habitat_tags": ['Wetland & Coast', 'Farmland'],
        "size_comparison": 'About as long as your whole arm.',
        "weight_comparison": 'About as heavy as a big tin of paint.',
    },
    'Eurasian Woodcock': {
        "length_cm": 34, "weight_g": 300,
        "speed_kmh": 45, "uk_pop": 55000, "song": 4, "brains": 4,
        "habitat": 'Damp woodland', "diet": 'Worms in soil',
    },

    # --- Wind Surfers
    'Herring Gull': {
        "length_cm": 60, "weight_g": 900,
        "speed_kmh": 50, "uk_pop": 140000, "song": 3, "brains": 8,
        "habitat": 'Coasts & towns', "diet": 'Fish & scraps',
        "wingspan_cm": 145, "conservation_status": 'Red',
        "habitat_tags": ['Wetland & Coast', 'Towns & Cities'],
        "size_comparison": 'Wings wider than you can stretch your arms!',
        "weight_comparison": 'About as heavy as a big bag of sugar.',
    },
    'Black-headed Gull': {
        "length_cm": 37, "weight_g": 300,
        "speed_kmh": 45, "uk_pop": 400000, "song": 3, "brains": 7,
        "habitat": 'Coasts & inland', "diet": 'Insects & scraps',
        "wingspan_cm": 105, "conservation_status": 'Amber',
        "habitat_tags": ['Wetland & Coast', 'Towns & Cities', 'Garden & Parks'],
        "size_comparison": 'As long as your arm from elbow to fingertips.',
        "weight_comparison": 'About as heavy as a big apple.',
    },
    'Common Gull': {
        "length_cm": 43, "weight_g": 400,
        "speed_kmh": 45, "uk_pop": 100000, "song": 3, "brains": 7,
        "habitat": 'Coasts & fields', "diet": 'Worms & fish',
    },
    'Great Black-backed Gull': {
        "length_cm": 70, "weight_g": 1700,
        "speed_kmh": 50, "uk_pop": 34000, "song": 2, "brains": 8,
        "habitat": 'Rocky coasts', "diet": 'Fish & seabirds',
    },
    'Great Cormorant': {
        "length_cm": 90, "weight_g": 2500,
        "speed_kmh": 60, "uk_pop": 62000, "song": 2, "brains": 6,
        "habitat": 'Coasts & lakes', "diet": 'Fish',
    },
    'Common Tern': {
        "length_cm": 34, "weight_g": 120,
        "speed_kmh": 55, "uk_pop": 24000, "song": 3, "brains": 5,
        "habitat": 'Coasts & gravel pits', "diet": 'Small fish',
    },
    'Barn Swallow': {
        "length_cm": 19, "weight_g": 19,
        "speed_kmh": 55, "uk_pop": 1400000, "song": 6, "brains": 6,
        "habitat": 'Farmland & barns', "diet": 'Flying insects',
        "wingspan_cm": 33, "conservation_status": 'Green',
        "habitat_tags": ['Farmland', 'Wetland & Coast'],
        "size_comparison": 'About as long as your hand and wrist - half of it tail!',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Common House-Martin': {
        "length_cm": 13, "weight_g": 18,
        "speed_kmh": 50, "uk_pop": 1000000, "song": 4, "brains": 5,
        "habitat": 'Towns & villages', "diet": 'Flying insects',
        "wingspan_cm": 28, "conservation_status": 'Red',
        "habitat_tags": ['Towns & Cities', 'Farmland'],
        "size_comparison": 'Small enough to fit in the palm of your hand.',
        "weight_comparison": 'About as heavy as a AA battery.',
    },
    'Northern Gannet': {
        "length_cm": 92, "weight_g": 3000,
        "speed_kmh": 65, "uk_pop": 600000, "song": 2, "brains": 6,
        "habitat": 'Sea cliffs', "diet": 'Fish',
        "wingspan_cm": 175, "conservation_status": 'Amber',
        "habitat_tags": ['Wetland & Coast'],
        "size_comparison": 'Wings wider than a grown-up is tall!',
        "weight_comparison": 'About as heavy as three bags of sugar.',
    },
    'Razorbill': {
        "length_cm": 40, "weight_g": 700,
        "speed_kmh": 65, "uk_pop": 200000, "song": 2, "brains": 5,
        "habitat": 'Sea cliffs', "diet": 'Fish',
    },
}


def _ranked(values: dict) -> dict:
    """Rank birds against each other and scale to 1-100."""
    ordered = sorted(values.items(), key=lambda kv: kv[1])
    n = len(ordered)
    return {name: max(1, round((i + 1) / n * 100)) for i, (name, _) in enumerate(ordered)}


def _build_ratings():
    by = lambda f: {k: f(v) for k, v in BIRDS.items()}
    ranked = {
        "size": _ranked(by(lambda v: v["length_cm"])),
        "speed": _ranked(by(lambda v: v["speed_kmh"])),
        # log first, so "ten times as many" is a consistent step up the scale
        "population": _ranked(by(lambda v: math.log10(max(v["uk_pop"], 1)))),
        "song": _ranked(by(lambda v: v["song"])),
        "brains": _ranked(by(lambda v: v["brains"])),
    }
    for name, bird in BIRDS.items():
        bird["ratings"] = {stat: ranked[stat][name] for stat in ranked}


_build_ratings()


# --- About -------------------------------------------------------------------
# One or two sentences on each bird, for the top of its card. Paraphrased from
# what Wikipedia's article on the bird says, in words a five-to-eight-year-old
# can read along with: short sentences, one memorable thing each, nothing
# grisly. Merged into BIRDS below so every bird carries its own "about".
ABOUT = {
    'European Robin': "Robins sing all year round, even in winter, and both boys and girls sing. They are brave little birds that often follow gardeners to grab worms from the freshly dug soil.",
    'Common Blackbird': "Only the boy blackbird is black - the girl is brown. The boy has a bright orange beak and a lovely, slow, fluty song you can hear at dusk.",
    'House Sparrow': "House sparrows love living near people and nest in holes in buildings. They chatter in noisy groups and like to take dust baths.",
    'Dunnock': "The dunnock is a shy brown bird that creeps along the ground under bushes like a little mouse. It is easy to mistake for a sparrow, but it has a thin beak for eating insects.",
    'Common Starling': "Starlings look black from far away, but up close their feathers shine purple and green with tiny white spots. In winter thousands fly together in swirling clouds called murmurations.",
    'Common Wood-Pigeon': "The wood pigeon is the biggest pigeon in Britain, with a white patch on its neck. Its soft cooing song sounds like it is saying 'my toe hurts, Betty'.",
    'Eurasian Collared-Dove': "Collared doves have a thin black stripe on the back of their neck, like a collar. They only started living in Britain about seventy years ago, and now they are everywhere.",
    'Rock Pigeon': "The pigeons in town squares come from wild rock doves that live on sea cliffs. They are very good at finding their way home, so people once used them to carry messages.",
    'Eurasian Tree Sparrow': "The tree sparrow looks like a house sparrow but has a chocolate-brown cap and a black spot on each white cheek. It is much rarer, and likes farmland and the edges of woods.",
    'European Turtle-Dove': "Turtle doves fly all the way from Africa to spend the summer here, and their gentle purring song is a sound of summer. They have become very rare and need our help.",
    'Eurasian Blue Tit': "Blue tits are tiny acrobats with blue caps and yellow tummies. They can hang upside down to find caterpillars, and they love nest boxes.",
    'Great Tit': "The great tit is the biggest tit, with a black stripe down its yellow tummy like a tie. Its song sounds like 'teacher, teacher'.",
    'Coal Tit': "The coal tit is a small tit with a black cap and a white patch on the back of its head. It hides seeds to eat later, so it often flies off with food from bird feeders.",
    'Long-tailed Tit': "Long-tailed tits look like little fluffy balls with a very long tail. They build a stretchy nest out of moss, spider silk and hundreds of feathers.",
    'Eurasian Nuthatch': "The nuthatch is the only British bird that can climb down a tree head-first. It wedges nuts into bark and hammers them open with its strong beak.",
    'Eurasian Treecreeper': "The treecreeper is a little brown bird that climbs up tree trunks in a spiral, like a mouse. It uses its thin curved beak to pick insects out of cracks in the bark.",
    'Goldcrest': "The goldcrest is Britain's smallest bird and weighs about the same as a 20p coin. It has a bright yellow stripe on its head.",
    'Eurasian Wren': "The wren is one of Britain's tiniest birds, but it has one of the loudest songs. It often holds its little tail straight up in the air.",
    'Marsh Tit': "Despite its name, the marsh tit lives in woods, not marshes. It has a shiny black cap and says 'pitchoo!' when it calls.",
    'Willow Tit': "The willow tit looks almost exactly like the marsh tit, so the best way to tell them apart is by their calls. It digs its own nest hole in soft, rotten wood.",
    'Common Chaffinch': "The boy chaffinch has a pink tummy and a blue-grey head, and both boys and girls have white stripes on their wings. Its song runs down like a bowler running up to bowl.",
    'European Goldfinch': "Goldfinches have red faces and flashes of bright gold on their wings. A group of goldfinches is called a charm, and they love eating thistle seeds.",
    'European Greenfinch': "The greenfinch is a chunky green bird with yellow on its wings and tail. It has a strong beak for cracking open seeds, and it sometimes sounds like it is wheezing.",
    'Common Linnet': "In spring, the boy linnet gets a rosy red chest and a red patch on his head. Linnets like heaths and farmland, where they feed on small seeds.",
    'Eurasian Bullfinch': "The boy bullfinch has a bright pink chest and a black cap. Bullfinch pairs often stay together all year.",
    'Eurasian Siskin': "The siskin is a small, stripy yellow-green finch. It loves the seeds of pine and alder trees, and it can hang upside down to reach them.",
    'Yellowhammer': "The boy yellowhammer has a bright yellow head. His song is said to sound like 'a little bit of bread and no cheese!'",
    'Reed Bunting': "In spring, the boy reed bunting has a black head and a white collar. Reed buntings live in reed beds and wet places, and sit on top of reeds to sing.",
    'Hawfinch': "The hawfinch is Britain's biggest finch, and its huge beak can crack open cherry stones. It is shy and hard to spot, high up in the treetops.",
    'Corn Bunting': "The corn bunting is a plump brown bird of farm fields. Its song sounds like a jangle of keys, and it often lets its legs dangle as it flies.",
    'Eurasian Blackcap': "The boy blackcap has a black cap and the girl has a brown one. It has such a beautiful song that it is sometimes called the northern nightingale.",
    'Common Chiffchaff': "The chiffchaff is named after its song, which goes 'chiff-chaff-chiff-chaff'. It is one of the first summer birds to arrive each spring.",
    'Willow Warbler': "The willow warbler looks almost the same as the chiffchaff, but its song is a sweet tumble of notes going down the scale. It flies here from Africa for the summer.",
    'Common Whitethroat': "The whitethroat has a fluffy white throat that it puffs out as it sings. It sings a scratchy song from the top of hedges, and sometimes leaps into the air to sing.",
    'Sedge Warbler': "The sedge warbler sings a fast, chattering song from the reeds, full of copied sounds. It has a pale stripe over its eye like an eyebrow.",
    'Eurasian Reed Warbler': "The reed warbler weaves a deep cup-shaped nest between reed stems. Its chattering song sounds a bit like a sewing machine.",
    'European Stonechat': "The stonechat's call sounds like two stones being tapped together. It likes to perch on top of gorse bushes, flicking its wings.",
    'Common Redstart': "The redstart has a bright orange-red tail that it shivers up and down. It spends the summer in old woods and flies back to Africa for the winter.",
    'Lesser Whitethroat': "The lesser whitethroat is a shy little warbler with a dark patch around its eye like a bandit's mask. It often hides deep inside hedges.",
    'Common Firecrest': "The firecrest is one of Britain's two smallest birds, with a fiery orange stripe on its head and a white stripe over each eye. It is rare and very special to see.",
    'Eurasian Magpie': "Magpies are black and white with long tails that shimmer blue and green in the sun. They are very clever, and can even recognise themselves in a mirror.",
    'Eurasian Jay': "The jay is a colourful crow with bright blue patches on its wings. In autumn it buries thousands of acorns, and the ones it forgets grow into new oak trees.",
    'Western Jackdaw': "The jackdaw is the smallest crow, with pale silvery eyes. Jackdaws are clever and chatty, and they often nest in chimneys.",
    'Carrion Crow': "Carrion crows are big, all-black, and very clever. Some have learned to drop nuts onto roads so cars crack them open.",
    'Rook': "Rooks are crows with a bare, pale face around their beak. They live together in noisy treetop nesting groups called rookeries.",
    'Northern Raven': "The raven is one of the biggest crows in the world. It is very clever, can copy sounds, and sometimes does somersaults in the air just for fun.",
    'Great Spotted Woodpecker': "The great spotted woodpecker is black and white with a red patch under its tail. In spring it drums on trees so fast it sounds like a machine.",
    'European Green Woodpecker': "The green woodpecker is a big green bird with a red cap. It spends lots of time on lawns licking up ants with its long sticky tongue, and its laughing call is called a yaffle.",
    'Lesser Spotted Woodpecker': "The lesser spotted woodpecker is only about the size of a sparrow. It is rare and hard to spot, high in the branches of old trees.",
    'Common Cuckoo': "The cuckoo is named after its 'cuck-oo' call. The mother lays her eggs in other birds' nests, and those birds raise her chicks for her.",
    'Song Thrush': "The song thrush sings each line of its song two or three times. It smashes snail shells on a favourite stone, called an anvil, to get at the snail inside.",
    'Mistle Thrush': "The mistle thrush is a big spotty thrush that loves mistletoe berries. It sings from treetops even on windy, rainy days, so it is also called the stormcock.",
    'Eurasian Skylark': "The skylark rises high into the sky, singing all the way up without stopping. It can sing for many minutes while it hovers far above the fields.",
    'Common Pheasant': "The boy pheasant has a shiny copper body, a green head, red face patches and a very long tail. The girl is brown so she can hide on her nest.",
    'White Wagtail': "In Britain it's called the pied wagtail - a black and white bird that wags its long tail up and down all the time. In winter, lots of them sleep together in town centres where it is warmer.",
    'Grey Wagtail': "Despite its name, the grey wagtail has a bright yellow tummy. It lives by fast streams and wags its very long tail as it hunts for insects.",
    'Meadow Pipit': "The meadow pipit is a small, stripy brown bird of hills and moors. It flutters up into the air to sing, then parachutes back down.",
    'Redwing': "The redwing is a small thrush with a cream stripe over its eye and red under its wings. Redwings fly here from the far north to spend the winter.",
    'Grey Partridge': "The grey partridge is a round farmland bird with an orange face. Families stay together in groups called coveys.",
    'Ring Ouzel': "The ring ouzel looks like a blackbird wearing a white bib. It lives on wild mountains and moors, and is sometimes called the mountain blackbird.",
    'Common Buzzard': "The buzzard is Britain's most common bird of prey. It circles high in the sky on wide wings and makes a call like a cat's mew.",
    'Common Kestrel': "The kestrel can hover in one spot in the air, keeping its head perfectly still. It is watching the grass below for mice and voles.",
    'Eurasian Sparrowhawk': "The sparrowhawk is a fast, sneaky hunter that zooms along hedges to surprise small birds. The girl is much bigger than the boy.",
    'Red Kite': "The red kite has a forked tail and twists it to steer as it glides. Red kites nearly disappeared from Britain, but now there are lots again.",
    'Peregrine Falcon': "The peregrine falcon is the fastest animal in the world. When it dives through the sky it can go faster than a racing car.",
    'Tawny Owl': "The tawny owl is the owl that goes 'twit-twoo' - the girl calls 'ke-wick' and the boy answers 'hoo-hoo'. It hunts at night in woods and parks.",
    'Barn Owl': "The barn owl has a white heart-shaped face and flies without making a sound. It can find mice in the dark just by listening.",
    'Little Owl': "The little owl is a small owl with fierce-looking yellow eyes. It often hunts in the daytime and bobs its head up and down when it is curious.",
    'Eurasian Hobby': "The hobby is a small, speedy falcon that catches dragonflies in mid-air and eats them as it flies. It spends the summer here and the winter in Africa.",
    'Long-eared Owl': "The long-eared owl has long feather tufts on its head that look like ears, and bright orange eyes. It hides so well in trees that it is very hard to spot.",
    'Mallard': "The mallard is the most common duck. The boy has a shiny green head, and it is the girl who makes the loud 'quack'.",
    'Mute Swan': "The mute swan is one of the heaviest flying birds in the world. It is called mute, meaning silent, because it is quieter than other swans - but it does hiss and snort.",
    'Canada Goose': "Canada geese have a black head and neck with a white chinstrap. They came from North America and fly in a V shape, honking as they go.",
    'Greylag Goose': "The greylag is a big grey goose with an orange beak. Most farmyard geese are related to the greylag.",
    'Eurasian Coot': "The coot is a black water bird with a white beak and a white patch on its forehead. Instead of webbed feet, it has funny lobed toes for swimming.",
    'Common Moorhen': "The moorhen has a red and yellow beak and flicks its white tail as it swims. It can also walk across floating leaves on its long green toes.",
    'Little Grebe': "The little grebe, or dabchick, is a small round diving bird. It can sink slowly under the water like a tiny submarine.",
    'Great Crested Grebe': "The great crested grebe has a fancy crest and frills on its head. In spring, pairs do a dance on the water, shaking their heads and offering each other weed.",
    'Common Kingfisher': "The kingfisher is a flash of bright blue and orange by the river. It dives head-first into the water to catch little fish.",
    'Common Eider': "The eider is a big sea duck. The mum lines her nest with her own super-soft feathers, called eiderdown.",
    'Grey Heron': "The grey heron is a very tall bird that stands perfectly still in the water, waiting to spear a fish with its long beak. Herons build big stick nests high in trees.",
    'Eurasian Oystercatcher': "The oystercatcher is a black and white shore bird with a long bright orange beak. It uses its beak to open mussels and dig up worms.",
    'Common Ringed Plover': "The ringed plover has a black collar and runs about on beaches in little dashes. To protect its eggs, it pretends to have a broken wing to lead danger away.",
    'Sanderling': "Sanderlings are small, pale shore birds that run up and down at the water's edge as the waves come and go. They look like little clockwork toys.",
    'Ruddy Turnstone': "The turnstone does just what its name says - it flips over stones and seaweed on the beach to find food hiding underneath.",
    'Common Sandpiper': "The common sandpiper bobs its tail up and down as it walks along rivers and lakes. It flies low over the water with stiff, flickering wings.",
    'Common Snipe': "The snipe has a very long, straight beak for probing in mud. When it dives through the air, its tail feathers make a buzzing sound called drumming.",
    'Northern Lapwing': "The lapwing has a wispy crest and shiny green feathers. It does tumbling flights in spring and calls 'pee-wit', which is another of its names.",
    'Eurasian Curlew': "The curlew is a big wading bird with a long, curved beak. Its haunting call, 'cur-lee', is one of the most beautiful sounds of the moors.",
    'Eurasian Woodcock': "The woodcock's brown feathers look just like dead leaves, so it is almost impossible to spot. Its eyes are set so far back it can see behind itself.",
    'Herring Gull': "The herring gull is the big noisy seagull of the seaside. Its chicks peck at the red spot on their parent's beak to ask for food.",
    'Black-headed Gull': "In summer the black-headed gull has a chocolate-brown hood, not a black one - and in winter it is just a small dark spot behind its eye.",
    'Common Gull': "The common gull looks like a smaller, gentler herring gull with a thin yellow-green beak. Despite its name, it isn't the most common gull.",
    'Great Black-backed Gull': "The great black-backed gull is the biggest gull in the world. It has a black back and wings and a huge yellow beak.",
    'Great Cormorant': "The cormorant is a big dark diving bird that catches fish underwater. Afterwards it stands with its wings held out to dry them.",
    'Common Tern': "The common tern is a graceful white seabird with a black cap and a red beak. It hovers over the water, then plunges in to catch fish.",
    'Barn Swallow': "The swallow has a long forked tail and swoops low to catch flies. Every spring it flies thousands of miles from Africa to nest in our barns.",
    'Common House-Martin': "The house martin builds a cup-shaped nest out of little mud pellets under the edges of house roofs. It has a bright white bottom you can see as it flies.",
    'Northern Gannet': "The gannet is a big white seabird with black wingtips. It dives into the sea from high up, folding its wings back like an arrow.",
    'Razorbill': "The razorbill is a black and white seabird with a thick, flat beak. It is a great swimmer and uses its wings to fly underwater.",
}

for _name, _text in ABOUT.items():
    BIRDS[_name]["about"] = _text


def bird_data(common_name: str):
    """Everything known about a bird, or None if it isn't one of the 100."""
    return BIRDS.get(common_name)


# --- Seasonality -----------------------------------------------------------
# Which months each bird is actually in the UK. Only the migrants are listed;
# everything else is here all year and defaults to all twelve.
#
# Chiffchaff and Blackcap are deliberately NOT listed: both increasingly
# overwinter here, so calling them summer-only would be out of date.
#
# Stored as explicit month numbers rather than a start/end range, because
# Redwing runs October to March and wraps the year end - a range would need
# special-casing that a list simply doesn't.
ALL_YEAR = list(range(1, 13))

SEASONAL_MONTHS = {
    # Summer visitors, here to breed
    "Barn Swallow":           [4, 5, 6, 7, 8, 9],
    "Common House-Martin":    [4, 5, 6, 7, 8, 9],
    "Common Tern":            [4, 5, 6, 7, 8, 9],
    "Willow Warbler":         [4, 5, 6, 7, 8],
    "Common Whitethroat":     [4, 5, 6, 7, 8],
    "Sedge Warbler":          [4, 5, 6, 7, 8],
    "Common Redstart":        [4, 5, 6, 7, 8],
    "Ring Ouzel":             [4, 5, 6, 7, 8],
    "Lesser Whitethroat":     [5, 6, 7, 8],
    "Eurasian Reed Warbler":  [5, 6, 7, 8],
    "European Turtle-Dove":   [5, 6, 7, 8],
    "Eurasian Hobby":         [5, 6, 7, 8, 9],
    # Cuckoos leave early - adults are often gone by July, long before the
    # other summer birds
    "Common Cuckoo":          [4, 5, 6, 7],
    # Winter visitor
    "Redwing":                [10, 11, 12, 1, 2, 3],
}

SUMMER_VISITORS = [n for n, ms in SEASONAL_MONTHS.items() if 6 in ms]
# Fixed order so the What's Here list doesn't reshuffle between loads
SEASONAL_ORDER = sorted(SEASONAL_MONTHS)

from curated_species import pack_for_species, pack_color_for_species

for _name, _bird in BIRDS.items():
    _bird["is_migratory"] = _name in SEASONAL_MONTHS
    # Which of the 10 collector packs this species belongs to, and that
    # pack's fixed colour - the same small coloured marker every card for
    # this species shows, wherever it appears in the app.
    _bird["pack"] = pack_for_species(_name)
    _bird["pack_color"] = pack_color_for_species(_name)


def months_for(common_name: str):
    return SEASONAL_MONTHS.get(common_name, ALL_YEAR)


def is_seasonal(common_name: str) -> bool:
    return common_name in SEASONAL_MONTHS


MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


def season_state(common_name: str, month: int):
    """Where a bird is in its year: here, leaving, arriving or away, with a
    label a child can read. Residents always come back as 'here' with no
    label, so nothing is cluttered by birds that never leave."""
    months = months_for(common_name)
    seasonal = is_seasonal(common_name)
    here = month in months
    nxt = (month % 12) + 1
    here_next = nxt in months

    if not seasonal:
        return {"state": "here", "seasonal": False, "label": None}
    if here and not here_next:
        return {"state": "leaving", "seasonal": True, "label": "Leaving soon!"}
    if here:
        return {"state": "here", "seasonal": True, "label": "Here right now"}
    if here_next:
        return {"state": "arriving", "seasonal": True,
                "label": f"Arriving in {MONTH_NAMES[nxt]}"}
    # Away - find the next month it returns, so the label is a promise rather
    # than just a refusal
    for step in range(2, 13):
        m = ((month - 1 + step) % 12) + 1
        if m in months:
            return {"state": "away", "seasonal": True,
                    "label": f"Back in {MONTH_NAMES[m]}"}
    return {"state": "away", "seasonal": True, "label": "Away"}
