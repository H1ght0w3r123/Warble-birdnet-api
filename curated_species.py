"""
Warble's curated bird list — 100 real UK species, hand-picked as the
app's actual "collection goal."

IMPORTANT: this is deliberately NOT used to filter what BirdNET can
detect. Detection stays fully open (geographic + seasonal filtering
already narrows it to what's genuinely plausible). This list only
powers the "Century" trophy and the Collection's completion tracker —
a target to chase, not a restriction on what the app will hear.

Species names use BirdNET's own naming convention (confirmed from
BirdNET's official labels format, e.g. "Turdus merula_Common
Blackbird") - formal English names, not casual shorthand. A handful
may need a small correction once tested against real live detections,
since the exact label file isn't something this could be checked
against directly - trivial to fix here if so, it's just one string.

Organised by habitat for readability, and because a habitat tag per
species is likely useful for future trophy work (e.g. High Flyer).
"""

CURATED_SPECIES = {
    "Garden & Urban": [
        "European Robin", "Eurasian Blue Tit", "Great Tit", "Common Blackbird",
        "House Sparrow", "Eurasian Wren", "Common Starling", "Eurasian Blackcap",
        "Common Chaffinch", "European Goldfinch", "Eurasian Magpie", "Carrion Crow",
        "Rock Pigeon", "Common Wood-Pigeon", "Eurasian Collared-Dove",
        "Western Jackdaw", "Coal Tit", "Long-tailed Tit", "European Greenfinch",
        "Dunnock", "White Wagtail",
    ],
    "Woodland": [
        "Song Thrush", "Mistle Thrush", "Great Spotted Woodpecker",
        "European Green Woodpecker", "Eurasian Nuthatch", "Eurasian Treecreeper",
        "Common Chiffchaff", "Willow Warbler", "Eurasian Jay", "Common Firecrest",
        "Goldcrest", "Common Redstart", "Eurasian Sparrowhawk", "Common Buzzard",
        "Tawny Owl", "European Turtle-Dove", "Hawfinch", "Marsh Tit",
        "Willow Tit", "European Nightjar",
    ],
    "Farmland & Hedgerow": [
        "Yellowhammer", "Common Linnet", "Eurasian Skylark", "Grey Partridge",
        "Common Pheasant", "Corn Bunting", "European Stonechat",
        "Common Whitethroat", "Lesser Whitethroat", "Eurasian Tree Sparrow",
        "Common Kestrel", "Red Kite", "Barn Owl", "Little Owl",
    ],
    "Wetland & Water": [
        "Grey Heron", "Mute Swan", "Canada Goose", "Greylag Goose", "Mallard",
        "Eurasian Coot", "Common Moorhen", "Common Kingfisher", "Sand Martin",
        "Barn Swallow", "Common House-Martin", "Reed Bunting",
        "Eurasian Reed Warbler", "Sedge Warbler", "Little Grebe",
        "Great Crested Grebe", "Common Sandpiper", "Common Snipe",
        "Eurasian Curlew", "Grey Wagtail",
    ],
    "Coastal": [
        "Herring Gull", "Black-headed Gull", "Common Gull",
        "Great Black-backed Gull", "Northern Gannet", "European Shag",
        "Great Cormorant", "Common Eider", "Eurasian Oystercatcher",
        "Common Ringed Plover", "Sanderling", "Ruddy Turnstone", "Common Tern",
        "Arctic Tern", "Razorbill",
    ],
    "Raptors & Others": [
        "Peregrine Falcon", "Common Cuckoo", "Eurasian Hobby", "Osprey",
        "White-tailed Eagle", "Golden Eagle", "Merlin", "Hen Harrier",
        "Long-eared Owl", "Short-eared Owl",
    ],
}

# Flattened for actual lookups - the category grouping above is for
# readability and future habitat-tag use, not needed at query time.
ALL_CURATED_SPECIES = {name for species_list in CURATED_SPECIES.values() for name in species_list}
