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
    # --- Gardeners
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

    # --- Crackers
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

    # --- Little Diggers
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

    # --- Swimmers
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

    # --- Mud Stompers
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

    # --- Wind Riders
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
