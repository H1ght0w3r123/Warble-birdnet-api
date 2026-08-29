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

Names match BirdNET's output exactly, as everywhere else.
"""

COLLECTOR_SPECIES = {
    # Garden and urban birds - tier moves mostly with recording effort
    "European Robin",
    "Common Blackbird",
    "Great Tit",
    "Eurasian Blue Tit",
    "Common Chaffinch",
    "Eurasian Wren",
    "House Sparrow",
    "Common Starling",
    "Common Wood-Pigeon",
    "Eurasian Magpie",
    "Carrion Crow",
    "European Goldfinch",
    "Dunnock",
    "Song Thrush",
    # Woodland - patchier, so more regional swing
    "Common Chiffchaff",
    "Willow Warbler",
    "Eurasian Jay",
    "Great Spotted Woodpecker",
    "Eurasian Nuthatch",
    # Farmland, upland and water - the genuinely regional ones, where tier
    # tracks real abundance rather than recorder density
    "Eurasian Skylark",
    "Yellowhammer",
    "Common Kestrel",
    "Barn Swallow",
    "Eurasian Curlew",
    "Grey Heron",
}

TIERS = ["Common", "Visitor", "Rare"]
