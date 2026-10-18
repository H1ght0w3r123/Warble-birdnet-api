"""
Where-to-look hints for birds the child hasn't found yet.

Shown on the note under the Collections book when an unfound card is at
the front, in place of the "Heard N times!" line a found bird gets. One
entry per bird in the UK 100: where to look, and one thing to listen or
look for, in a child's words.

At most HINT_MAX (60) characters, so the note fits the clear stretch of
table between the props on the smallest phones (about 3 short lines); the
check below fails at start-up if one runs over. The long versions (100-200
characters each) are in git history if they're ever wanted elsewhere.

KEYS MUST MATCH curated_species.py (and so BirdNET's output) EXACTLY.
A typo here doesn't raise - the bird just silently never gets a hint.
There's a test of this at the bottom of the file.
"""

HINT_MAX = 60

UNFOUND_HINTS = {
    "European Robin":
        "Look on fences and low branches. It sings all winter!",
    "Eurasian Blackbird":
        "Watch lawns at dawn for a black bird pulling up worms.",
    "House Sparrow":
        "Listen for noisy chirping in hedges near houses.",
    "Dunnock":
        "Look low under hedges for a shy brown-and-grey bird.",
    "European Starling":
        "Look on rooftops for shiny, speckled purple-green feathers.",
    "Common Wood-Pigeon":
        "A plump grey pigeon with a white neck patch. Coo-coo!",
    "Eurasian Collared-Dove":
        "A pale dove with a thin black collar on rooftops.",
    "Rock Pigeon":
        "Look in town squares, stations and on bridges.",
    "Eurasian Tree Sparrow":
        "Try farm hedges for a sparrow with a black cheek spot.",
    "European Turtle-Dove":
        "In summer, listen on farms for a soft purring turr-turr.",
    "Eurasian Blue Tit":
        "Watch feeders for a blue-and-yellow bird upside down!",
    "Great Tit":
        "Black head, white cheeks, yellow tummy. Teacher-teacher!",
    "Coal Tit":
        "Look in pine trees for a tiny tit with a white neck stripe.",
    "Long-tailed Tit":
        "A tiny pink ball with a long tail, in busy little gangs.",
    "Eurasian Nuthatch":
        "The only bird that climbs head-first DOWN tree trunks.",
    "Eurasian Treecreeper":
        "Watch tree trunks for a little brown bird spiralling up.",
    "Goldcrest":
        "Our smallest bird! Look in fir trees, listen for see-see.",
    "Eurasian Wren":
        "A tiny brown bird, tail up, with a super-loud song.",
    "Marsh Tit":
        "In woods, listen for a sneezy pitchoo! call.",
    "Willow Tit":
        "Try damp, bushy woods and listen for a buzzing call.",
    "Common Chaffinch":
        "Pink tummy, blue-grey head, white stripes on its wings.",
    "European Goldfinch":
        "Look on thistles for a finch with a red face.",
    "European Greenfinch":
        "A chunky green finch at feeders, with a wheezy call.",
    "Eurasian Linnet":
        "Look on bushy heaths and farms for pink-chested finches.",
    "Eurasian Bullfinch":
        "A shy round finch with a pink chest and a black cap.",
    "Eurasian Siskin":
        "In winter, look in birch and alder trees near water.",
    "Yellowhammer":
        "A bright yellow bird singing on top of farm hedges.",
    "Reed Bunting":
        "Look in reeds for a bird with a black head and white collar.",
    "Hawfinch":
        "Look high in old woods for a finch with a giant beak.",
    "Corn Bunting":
        "On farm fences its song sounds like jangling keys.",
    "Eurasian Blackcap":
        "Listen in spring woods. The boys wear a little black cap.",
    "Common Chiffchaff":
        "From March it sings its name: chiff-chaff-chiff-chaff!",
    "Willow Warbler":
        "In spring, listen for sweet notes tumbling down.",
    "Greater Whitethroat":
        "In summer, look on brambles for a bird with a white throat.",
    "Sedge Warbler":
        "In summer reeds, listen for loud, chattery singing.",
    "Eurasian Reed Warbler":
        "Deep in summer reeds, listen for a chugging song.",
    "European Stonechat":
        "On gorse bushes, its call sounds like two stones tapping.",
    "Common Redstart":
        "In old woods in summer, look for a shivering orange tail.",
    "Lesser Whitethroat":
        "Listen in thick hedges for a fast, rattly song.",
    "Common Firecrest":
        "A tiny bird with a fiery orange stripe on its head.",
    "Eurasian Magpie":
        "A black-and-white bird with a long tail. Look anywhere!",
    "Eurasian Jay":
        "In autumn woods, look for a flash of bright blue wing.",
    "Eurasian Jackdaw":
        "A small crow with pale eyes, calling chack! from chimneys.",
    "Carrion Crow":
        "An all-black crow, often alone, calling caw!",
    "Rook":
        "A crow with a pale face. Listen for noisy treetop nests.",
    "Common Raven":
        "Look on hills and cliffs for a huge crow going gronk!",
    "Great Spotted Woodpecker":
        "Listen in woods for fast drumming on a tree trunk.",
    "Eurasian Green Woodpecker":
        "In parks, listen for a loud laugh. It digs for ants!",
    "Lesser Spotted Woodpecker":
        "A tiny woodpecker, high up in old woods. Hard to find!",
    "Common Cuckoo":
        "In spring, listen for cuck-oo! across fields and heaths.",
    "Song Thrush":
        "Spotty tummy. It sings each tune twice or three times.",
    "Mistle Thrush":
        "A big spotty thrush singing on treetops, even in storms!",
    "Eurasian Skylark":
        "Look up over fields for a bird singing high in the sky.",
    "Ring-necked Pheasant":
        "On farm edges, a long-tailed bird with a red face.",
    "White Wagtail":
        "Near water and car parks, it wags its tail up and down.",
    "Gray Wagtail":
        "Look by fast streams for a bobbing bird with a yellow tummy.",
    "Meadow Pipit":
        "On moors, it flies up singing, then floats back down.",
    "Redwing":
        "In winter, look on berry bushes for a thrush with red sides.",
    "Gray Partridge":
        "At dawn on farms, a round bird with an orange face.",
    "Ring Ouzel":
        "On high hills, look for a blackbird with a white bib.",
    "Common Buzzard":
        "Look up for a big bird circling and calling pee-yoo!",
    "Eurasian Kestrel":
        "Watch roadsides for a small falcon hovering very still.",
    "Eurasian Sparrowhawk":
        "Watch feeders for a sudden dash after little birds.",
    "Red Kite":
        "Look up for a big reddish bird with a forked tail.",
    "Peregrine Falcon":
        "Look on cliffs and tall buildings. The fastest bird!",
    "Tawny Owl":
        "After dark in the woods, listen for twit-twoo!",
    "Barn Owl":
        "At dusk, look over fields for a white owl flying low.",
    "Little Owl":
        "Look on old farm buildings in daytime, bobbing its head.",
    "Eurasian Hobby":
        "In summer, a speedy falcon catching dragonflies.",
    "Long-eared Owl":
        "It hides in thick fir trees in the daytime. Hard to find!",
    "Mallard":
        "On any pond! The boys have a shiny green head.",
    "Mute Swan":
        "On park lakes, a huge white bird with an orange beak.",
    "Canada Goose":
        "A brown goose with a black neck and a white chin strap.",
    "Graylag Goose":
        "On lakes and fields, a grey goose with an orange beak.",
    "Eurasian Coot":
        "On lakes, a black bird with a white beak and forehead.",
    "Eurasian Moorhen":
        "By ponds, a dark bird with a red beak and flicking tail.",
    "Little Grebe":
        "A small round bird that keeps diving under the water.",
    "Great Crested Grebe":
        "On big lakes in spring, watch for a head-shaking dance.",
    "Common Kingfisher":
        "By quiet rivers, watch for a flash of electric blue!",
    "Common Eider":
        "At the seaside, listen for a duck going ooh! ooh!",
    "Gray Heron":
        "A tall grey bird standing very still in shallow water.",
    "Eurasian Oystercatcher":
        "On beaches, a black-and-white bird with an orange beak.",
    "Common Ringed Plover":
        "On sandy beaches, it runs, stops, then runs again.",
    "Sanderling":
        "On sandy beaches, it chases the waves in and out!",
    "Ruddy Turnstone":
        "On rocky shores, it flips over stones looking for food.",
    "Common Sandpiper":
        "By rivers and lakes, it bobs its tail as it walks.",
    "Common Snipe":
        "In marshes, look for a very, very long straight beak.",
    "Northern Lapwing":
        "On farms, a black-and-white bird with a wispy crest.",
    "Eurasian Curlew":
        "On mudflats, a huge curved beak and a bubbly call.",
    "Eurasian Woodcock":
        "At dusk in damp woods, listen for funny squeaks.",
    "Herring Gull":
        "At the seaside, a big noisy gull with pink legs.",
    "Black-headed Gull":
        "In summer it has a chocolate-brown head. Look on lakes.",
    "Common Gull":
        "On playing fields, a gentle gull with yellow-green legs.",
    "Great Black-backed Gull":
        "On the coast, the biggest gull, with a black back.",
    "Great Cormorant":
        "A big black bird drying its wings out wide by water.",
    "Common Tern":
        "In summer by water, it hovers then dives for fish.",
    "Barn Swallow":
        "In summer, it zooms low over fields with a forked tail.",
    "Common House-Martin":
        "In summer, look under roofs for little mud nests.",
    "Northern Gannet":
        "Big white seabirds diving straight into the sea.",
    "Razorbill":
        "On sea cliffs, a black-and-white bird with a thick beak.",
}


def _check_names():
    """Fails loudly at import time rather than silently dropping a hint."""
    from curated_species import PACKS
    curated = {n for p in PACKS.values() for n in p["common"] + p["rare"]}
    missing = curated - set(UNFOUND_HINTS)
    unknown = set(UNFOUND_HINTS) - curated
    if missing or unknown:
        raise ValueError(
            f"unfound_hints out of sync with curated_species - "
            f"missing: {sorted(missing)}, unknown: {sorted(unknown)}"
        )
    too_long = {n: len(h) for n, h in UNFOUND_HINTS.items() if len(h) > HINT_MAX}
    if too_long:
        raise ValueError(f"unfound_hints over {HINT_MAX} characters (the note under the book): {too_long}")


_check_names()
