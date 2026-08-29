"""
Collector species: 25 birds that can be held at all three rarity tiers.

For these, the collection keys on species AND tier, so hearing a Blackbird
that comes back Common near home and Visitor on holiday gives you two cards,
not one. Every other species stays one card, as before.

Why these 25: each is widespread enough that a child could plausibly meet it
in several parts of the UK, while having genuinely uneven regional record
density - so its tier really can differ from place to place. That density
reflects both real abundance and how heavily an area is recorded, which is
why even familiar garden birds can shift tier between a well-birded city and
somewhere rural.

Spread deliberately across all six habitat groups (8/5/4/4/2/2). An earlier
version was 13 garden birds with nothing coastal and no raptors at all,
which quietly made Globetrotter a garden-bird trophy and gave a child at the
seaside nothing to chase.

Names match BirdNET's output exactly, as everywhere else.
"""

COLLECTOR_SPECIES = {
    # Garden & Urban (8) - the birds a child meets almost anywhere, so the
    # tier difference between home and away is the whole point
    "European Robin",
    "Common Blackbird",
    "Great Tit",
    "Eurasian Blue Tit",
    "House Sparrow",
    "Common Starling",
    "Common Wood-Pigeon",
    "Eurasian Magpie",
    # Woodland (5) - patchier by region, so tier genuinely moves
    "Song Thrush",
    "Common Chiffchaff",
    "Eurasian Jay",
    "Eurasian Nuthatch",
    "Great Spotted Woodpecker",
    # Farmland & Hedgerow (4) - real regional abundance differences
    "Eurasian Skylark",
    "Yellowhammer",
    "Common Kestrel",
    "Common Pheasant",
    # Wetland & Water (4)
    "Grey Heron",
    "Mallard",
    "Barn Swallow",
    "Eurasian Curlew",
    # Coastal (2) - both are common inland as well as at the sea, which is
    # exactly the kind of swing the mechanic needs
    "Herring Gull",
    "Black-headed Gull",
    # Raptors & Others (2) - widespread enough to actually be heard
    "Common Cuckoo",
    "Peregrine Falcon",
}

TIERS = ["Common", "Visitor", "Rare"]
