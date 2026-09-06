# Migration routes for Warble's 14 seasonal species. Each entry backs the
# "Migrator" card - a real map (Wikimedia Commons' "Continents vide couleurs",
# CC BY-SA 3.0/GFDL, cropped to Europe/Africa/Middle East) with each bird's
# route drawn on top.
#
# Researched individually against RSPB/BTO and published tracking studies
# rather than guessed, since this is factual content in a children's app.
#
# Coordinates are pixel positions in the cropped map image (560x780,
# /static/migration-map-base.webp), not raw lat/lng - the frontend never has
# to do map projection. They were derived by measuring Africa's actual pixel
# bounding box in the source image (mainland Africa's real-world extremes:
# lng -17.5 to 51.4, lat -34.8 to 37.5) and fitting a linear transform from
# that - not eyeballed - then cross-checked against where each named place
# actually falls in the cropped image.
UK_POINT = [74, 168]

MIGRATION_INFO = {
    "Barn Swallow": {
        "direction": "departs",
        "destination_name": "South Africa",
        "route": [UK_POINT, [67, 249], [55, 300], [156, 375], [219, 479], [245, 646]],
        "fact": "Barn Swallows fly over 9,000km to reach South Africa - one of the longest journeys of any bird that visits Britain.",
    },
    "Common House-Martin": {
        "direction": "departs",
        "destination_name": "Central Africa",
        "route": [UK_POINT, [67, 249], [156, 375], [219, 467]],
        "fact": "Nobody knows exactly where House Martins spend the winter - despite hundreds of thousands being ringed, almost none have ever been found in Africa. It's one of British birdwatching's great mysteries.",
    },
    "Common Tern": {
        "direction": "departs",
        "destination_name": "The coast of West Africa",
        "route": [UK_POINT, [67, 249], [55, 300], [80, 450]],
        "fact": "Common Terns hug the coastline the whole way, following the shore of Spain and West Africa - some carry on as far south as the tip of South Africa.",
    },
    "Willow Warbler": {
        "direction": "departs",
        "destination_name": "West Africa (Ivory Coast & Ghana)",
        "route": [UK_POINT, [67, 249], [156, 375], [74, 444]],
        "fact": "This tiny bird weighs less than a £1 coin but flies over 15,000km there and back to West Africa every single year.",
    },
    "Common Whitethroat": {
        "direction": "departs",
        "destination_name": "The Sahel, West Africa",
        "route": [UK_POINT, [67, 249], [156, 375], [42, 398]],
        "fact": "Whitethroats winter in the dry Sahel region, just south of the Sahara. A terrible drought there in the late 1960s wiped out 90% of Britain's whitethroats in a single year.",
    },
    "Sedge Warbler": {
        "direction": "departs",
        "destination_name": "West Africa, south of the Sahara",
        "route": [UK_POINT, [67, 249], [156, 375], [29, 410]],
        "fact": "Before the big flight over the Sahara, Sedge Warblers gorge on aphids at south-coast reedbeds to build up enough fat to fuel the journey.",
    },
    "Common Redstart": {
        "direction": "departs",
        "destination_name": "West Africa",
        "route": [UK_POINT, [67, 249], [156, 375], [55, 421]],
        "fact": "Redstarts trade Britain's woodlands for the dry savannah of West Africa every autumn, then fly all the way back to breed again in spring.",
    },
    "Ring Ouzel": {
        "direction": "departs",
        "destination_name": "The Atlas Mountains, Morocco",
        "route": [UK_POINT, [67, 249], [55, 300]],
        "fact": "Unlike most of Britain's summer visitors, Ring Ouzels don't cross the Sahara at all - they winter much closer, up in Morocco's mountains.",
    },
    "Lesser Whitethroat": {
        "direction": "departs",
        "destination_name": "East Africa",
        "route": [UK_POINT, [232, 237], [295, 254], [314, 300], [333, 450]],
        "fact": "Most British migrants head south-west towards Spain. Lesser Whitethroats do the opposite, flying south-east via the Balkans and Turkey instead.",
    },
    "Eurasian Reed Warbler": {
        "direction": "departs",
        "destination_name": "West Africa, south of the Sahara",
        "route": [UK_POINT, [67, 249], [156, 375], [36, 433]],
        "fact": "Reed Warblers are the bird most often tricked into raising a baby Cuckoo - and they still make this huge migration to Africa and back every year regardless.",
    },
    "European Turtle-Dove": {
        "direction": "departs",
        "destination_name": "The Inner Niger Delta, Mali",
        "route": [UK_POINT, [67, 249], [156, 375], [67, 392]],
        "fact": "Turtle-Doves head for a huge wetland called the Inner Niger Delta - a green, watery oasis right in the middle of the Sahara desert.",
    },
    "Eurasian Hobby": {
        "direction": "departs",
        "destination_name": "Southern Africa",
        "route": [UK_POINT, [67, 249], [156, 375], [219, 479], [264, 582]],
        "fact": "This speedy little falcon crosses the entire Sahara AND the equatorial rainforest to reach southern Africa, hunting dragonflies along the way.",
    },
    "Common Cuckoo": {
        "direction": "departs",
        "destination_name": "The Congo Rainforest",
        "route": [UK_POINT, [67, 249], [156, 375], [219, 479]],
        "fact": "Scientists have fitted real satellite tags to UK cuckoos and tracked them all the way to the Congo rainforest - one famous tagged cuckoo was named 'Chris'.",
    },
    "Redwing": {
        "direction": "arrives",
        "destination_name": "Iceland, Norway & Sweden",
        "route": [UK_POINT, [156, 116]],
        "fact": "Redwings do the opposite of most of the birds on this list - they breed far north in Iceland and Scandinavia, and only come to Britain for the winter.",
    },
}


def get_migration_info(common_name: str):
    return MIGRATION_INFO.get(common_name)
