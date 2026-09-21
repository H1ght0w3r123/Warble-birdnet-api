"""
Where-to-look hints for birds the child hasn't found yet.

Shown under the fan on the Collections screen when an unfound card is
hovered or selected, in place of the "Found N times!" line a found bird
gets. One entry per bird in the UK 100.

KEYS MUST MATCH curated_species.py (and so BirdNET's output) EXACTLY.
A typo here doesn't raise - the bird just silently never gets a hint.
There's a test of this at the bottom of the file.
"""

UNFOUND_HINTS = {
    "European Robin":
        "Look on garden fences and low branches any time of year \u2014 robins don't migrate and they'll often follow you if you're digging! Listen for a thin, sweet song even on winter mornings.",
    "Common Blackbird":
        "Check lawns and flowerbeds at dawn or dusk, when they hop about tugging worms from the grass. Males are glossy black with an orange-yellow beak \u2014 hard to miss.",
    "House Sparrow":
        "Listen for noisy chirping from hedges and roof gutters near houses \u2014 they love living close to people. You'll usually spot a whole chattering little gang together.",
    "Dunnock":
        "Look low down, right under hedges and bushes, where this shy brown-and-grey bird shuffles about quietly. It's often mistaken for a sparrow, but its thin beak and quiet 'tseep' give it away.",
    "Common Starling":
        "Watch rooftops and playing fields for a bird with glossy, speckled feathers that shimmer purple and green in the sun. In winter evenings, look up for huge swirling flocks called murmurations.",
    "Common Wood-Pigeon":
        "Spot this plump grey pigeon with a white neck patch on garden lawns or tree branches almost anywhere. Its soft, five-note coo is one of the most familiar sounds in a British garden.",
    "Eurasian Collared-Dove":
        "Look for a pale sandy-grey dove with a thin black half-collar, often perched on rooftops, telegraph wires or garden feeders. Its call sounds like it's saying 'u-NI-ted' over and over.",
    "Rock Pigeon":
        "Check town squares, station ledges and bridges \u2014 these are the grey pigeons with a dark head and shiny green-purple neck that gather wherever people drop crumbs.",
    "Eurasian Tree Sparrow":
        "This one's trickier than House Sparrow \u2014 look for it around farmland hedgerows and orchards, and check for a neat chestnut cap and a black cheek spot to tell them apart.",
    "European Turtle-Dove":
        "A real summer rarity now \u2014 try farmland with scrubby hedges in June or July and listen for a soft, purring 'turr-turr' call. Seeing one is a proper birding achievement.",
    "Eurasian Blue Tit":
        "Watch garden feeders and hanging fat balls for a small yellow-and-blue acrobat that hangs upside down while it feeds. Its call is a bright, scolding 'see-see-see-tchurr'.",
    "Great Tit":
        "Look for the biggest of the garden tits \u2014 black head, white cheeks and a bold yellow belly with a black stripe down the middle. Its song sounds like a squeaky bicycle pump: 'tea-cher, tea-cher'.",
    "Coal Tit":
        "Check conifer trees and pine woods, where this small tit with a white stripe down the back of its head darts quickly through the needles. It visits feeders too, grabbing a seed and dashing off to hide it.",
    "Long-tailed Tit":
        "Listen for a soft 'tsirrup' contact call and look for a tiny round pink-and-black bird with a tail longer than its body, usually travelling in a chattering little troupe through hedges and treetops.",
    "Eurasian Nuthatch":
        "Look on tree trunks in woodland or park \u2014 it's the only common bird here that can climb head-first down a trunk. Blue-grey above with a black eye-stripe and rusty flanks.",
    "Eurasian Treecreeper":
        "Watch tree trunks closely \u2014 this streaky brown bird spirals upward from the base, probing bark with a thin curved bill, then flies down to the next tree and starts again.",
    "Goldcrest":
        "Britain's smallest bird \u2014 check conifers and yew trees for constant fidgety movement and listen for an extremely high, thin 'see-see-see' song, almost too high for some ears to hear.",
    "Eurasian Wren":
        "Look low in dense undergrowth for a tiny round brown bird with its tail cocked straight up. For its size its song is astonishingly loud and fast, trilling from a low perch.",
    "Marsh Tit":
        "A woodland bird that looks a lot like Willow Tit \u2014 glossy black cap, plain brown wings, no pale wing patch. Listen for a sharp, sneezy 'pitchoo' call to help tell it apart.",
    "Willow Tit":
        "Very similar to Marsh Tit but prefers damp, scrubby woodland \u2014 its cap is duller black and it has a pale wing panel. Its call is a nasal, buzzing 'zi-zi-chair-chair'.",
    "Common Chaffinch":
        "Look on garden lawns and woodland edges for a bird with a blue-grey head, pink breast and bold white wing-bars. Its song ends with a cheerful downward flourish, like a bowler's run-up.",
    "European Goldfinch":
        "Check thistle patches and garden niger-seed feeders for a red-faced finch with bold black-and-yellow wings. A flock is called a 'charm', and you'll hear their tinkling, liquid call before you see them.",
    "European Greenfinch":
        "Look for a chunky yellowish-green finch at garden feeders, listening for its wheezy, buzzing 'dzzzweee' call. In spring, males do a slow, fluttery display flight over gardens and hedges.",
    "Common Linnet":
        "Search scrubby farmland, heaths and coastal bushes for small flocks feeding on weed seeds \u2014 males show a rosy-pink breast and forehead in summer. Their song is a fast, musical twittering.",
    "Eurasian Bullfinch":
        "Look in hedgerows and woodland edges for a shy, round finch \u2014 the male's rosy-pink breast and black cap stand out. Its call is a soft, mournful 'peu' whistle, often heard before the bird is seen.",
    "Eurasian Siskin":
        "Check alder and birch trees near water, especially in winter when flocks join garden feeders. A small streaky yellow-green finch with a forked tail and a wheezy, twittering call.",
    "Yellowhammer":
        "Scan hedgerows along farmland tracks for a bright yellow-headed bunting perched up singing. Its song is famous for sounding like 'a-little-bit-of-bread-and-no-cheese'.",
    "Reed Bunting":
        "Look in reedbeds and damp scrub, where the male's smart black head and white collar stand out against the reeds. It sings a simple, scratchy little song from a swaying reed stem.",
    "Hawfinch":
        "A shy, hard-to-find rare finch \u2014 try old woodland with hornbeam or cherry trees in winter, scanning treetops for its huge, powerful beak built for cracking cherry stones.",
    "Corn Bunting":
        "Search open arable farmland for a large, plain brown bunting singing from a fence post or wire \u2014 its song is often compared to jangling keys.",
    "Eurasian Blackcap":
        "Listen in woodland and scrubby gardens for a rich, fluty warbling song. The male has a neat black cap; the female's cap is chestnut-brown.",
    "Common Chiffchaff":
        "One of the first summer migrants to arrive \u2014 listen from March in woods and parks for its own name sung over and over: 'chiff-chaff-chiff-chaff'.",
    "Willow Warbler":
        "Similar to Chiffchaff but with a gentle, descending song like a sweet cascade of notes. Look in open woodland and scrub with young trees in spring and summer.",
    "Common Whitethroat":
        "Check brambles and scrubby hedgerows in summer for a bird that pops up to sing a scratchy little song, then dives back into cover \u2014 its white throat flashes as it sings.",
    "Sedge Warbler":
        "Search reedbeds and damp scrub near water in summer for a streaky brown warbler with a bold pale eyebrow, belting out a scratchy, chattering song, sometimes even at night.",
    "Eurasian Reed Warbler":
        "Listen deep in reedbeds in summer for a steady, chugging song repeating short phrases. It's plainer than Sedge Warbler, with no eyebrow stripe, and usually stays hidden in the reeds.",
    "European Stonechat":
        "Look on heathland and coastal scrub for a bird perched prominently on top of a gorse bush \u2014 the male has a black head and orange breast. Its call sounds like two pebbles being knocked together.",
    "Common Redstart":
        "Check open woodland with old trees in spring and summer, and watch for a constantly quivering rusty-orange tail \u2014 that's how it gets its name.",
    "Lesser Whitethroat":
        "Trickier than Common Whitethroat \u2014 look in dense hedgerows and scrub for a grey-headed warbler and listen for a fast, rattling song, quite different from its cousin's scratchy warble.",
    "Common Firecrest":
        "Even rarer than its cousin Goldcrest \u2014 check conifers and holly bushes for a tiny bird with a bold black-and-white eye-stripe and a flame-orange crown stripe.",
    "Eurasian Magpie":
        "Look almost anywhere \u2014 parks, gardens, roadsides \u2014 for a bold black-and-white bird with a long tail that flashes green and purple in the light. Its harsh chattering call carries a long way.",
    "Eurasian Jay":
        "Check woodland edges, especially in autumn when jays are busy burying acorns. Look for a pinkish-brown bird with a flash of bright blue on the wing as it flies off, usually shrieking loudly.",
    "Western Jackdaw":
        "Look for small, sociable black crows with pale silvery-grey eyes and a soft grey nape, often nesting in chimneys or old buildings and calling a sharp, metallic 'chack'.",
    "Carrion Crow":
        "Look for an all-black crow, usually alone or in a pair rather than a big flock, with a harsh, flat 'caw' call \u2014 common in almost any open space, from parks to farmland.",
    "Rook":
        "Check farmland near noisy treetop colonies called rookeries \u2014 Rooks look like Carrion Crows but have a pale, bare patch of skin around the base of the beak and shaggy 'trouser' feathers on the legs.",
    "Northern Raven":
        "Look to upland and coastal areas for the biggest crow of all \u2014 a huge black bird with a deep, croaking 'gronk' call and a diamond-shaped tail, often seen tumbling and rolling in flight.",
    "Great Spotted Woodpecker":
        "Listen in woodland and even leafy gardens for a sharp 'kick' call and a fast drumming roll on tree trunks \u2014 look for a black-and-white bird with a flash of red under the tail.",
    "European Green Woodpecker":
        "Check grassy parkland and woodland edges, where this green woodpecker often feeds on the ground, probing for ants. Its loud, laughing call gave it the old nickname 'yaffle'.",
    "Lesser Spotted Woodpecker":
        "Britain's smallest and shyest woodpecker \u2014 a real challenge to find. Scan high in old broadleaf woodland for a sparrow-sized bird with black-and-white barred wings, best located by its faint, fast drumming.",
    "Common Cuckoo":
        "Listen across heathland, farmland and open woodland from April, for the unmistakable two-note 'cuck-oo' call \u2014 far easier to hear than to actually spot, since it rarely shows itself for long.",
    "Song Thrush":
        "Look on lawns and woodland floors for a thrush with warm brown upperparts and neat dark spots below, often smashing snail shells against a favourite stone. Its song repeats each musical phrase two or three times.",
    "Mistle Thrush":
        "Larger and greyer than Song Thrush, with bolder spotting \u2014 look high in a treetop, even in stormy weather, where it earned the old name 'stormcock' for singing through wind and rain.",
    "Eurasian Skylark":
        "Look up over open farmland and grassland \u2014 Skylarks sing a long, tumbling stream of notes while hovering high overhead, sometimes for minutes at a time, before dropping back to the ground.",
    "Common Pheasant":
        "Check farmland edges and woodland margins for a large, long-tailed bird \u2014 the male is unmistakable with a glossy green head and red face wattle. Listen for a loud, explosive crowing call.",
    "White Wagtail":
        "Look near water, car parks and farm buildings for a slim black-and-white bird constantly bobbing its long tail up and down as it walks \u2014 the UK's own form is called the Pied Wagtail.",
    "Grey Wagtail":
        "Despite the name, look for a bird with a bright yellow belly, found bobbing along fast-flowing streams and rivers, especially near weirs and bridges.",
    "Meadow Pipit":
        "Scan open moorland, rough grassland and coastal fields for a small streaky brown bird that flies up singing, then parachutes back down on stiff wings \u2014 a classic upland sound.",
    "Redwing":
        "A winter visitor \u2014 check hedgerows, parks and berry bushes from October to March for a small thrush with a bold cream eyebrow stripe and reddish flanks, often arriving in large flocks.",
    "Grey Partridge":
        "Search open arable farmland at dawn or dusk for a plump, orange-faced bird that prefers to run rather than fly, usually in a small family covey scuttling along field edges.",
    "Ring Ouzel":
        "A true upland specialist \u2014 check high moorland and rocky hillsides in spring or autumn for a blackbird-lookalike with a bold white crescent across its chest.",
    "Common Buzzard":
        "Look up on almost any drive through the countryside for a broad-winged bird soaring in lazy circles, calling a thin, mewing 'pee-yoo' \u2014 Britain's most common bird of prey.",
    "Common Kestrel":
        "Watch over roadside verges and farmland for a small falcon hovering perfectly still in mid-air, head fixed on the ground below, scanning for voles.",
    "Eurasian Sparrowhawk":
        "Look for a fast, low flight straight through gardens and along hedgerows \u2014 a sudden dash after small birds at a feeder is often the giveaway that a Sparrowhawk is nearby.",
    "Red Kite":
        "Scan the sky over woodland and farmland for a large reddish-brown bird of prey with a deeply forked tail, tilting and twisting in flight far more than a Buzzard does.",
    "Peregrine Falcon":
        "Check tall cliffs, quarries and even city buildings and cathedral towers, where pairs now nest. Watch for an incredibly fast, powerful dive \u2014 the fastest animal on Earth.",
    "Tawny Owl":
        "Listen after dark in woodland and leafy parks for the classic 'twit-twoo' \u2014 actually two owls calling back and forth, a sharp 'kewick' answered by a soft, quavering hoot.",
    "Barn Owl":
        "Watch rough grassland and farmland at dusk for a pale, heart-faced owl flying low and silent over the grass, hunting for voles in the fading light.",
    "Little Owl":
        "Check old farm buildings, orchards and hedgerow trees in daylight \u2014 unlike most owls, Little Owl is often active by day, perched upright and bobbing its head when alert.",
    "Eurasian Hobby":
        "A fast, elegant falcon to look for over wetlands and heathland in summer, often hunting dragonflies and swallows on the wing with astonishing speed and agility.",
    "Long-eared Owl":
        "One of the trickiest owls to find \u2014 check dense conifer plantations by day, where it roosts pressed tight against the trunk, and listen for a low, mournful hoot after dark.",
    "Mallard":
        "Look on almost any pond, river or park lake \u2014 the male has a glossy green head and yellow bill, while the female is mottled brown. Britain's most familiar duck.",
    "Mute Swan":
        "Check park lakes, canals and slow rivers for a huge white bird with an orange bill and black knob at the base \u2014 despite the name, it does hiss loudly if you get too close to its nest.",
    "Canada Goose":
        "Look on park lakes, reservoirs and riverside grass for a large brown goose with a black neck and a bold white chinstrap marking, often in noisy honking flocks.",
    "Greylag Goose":
        "Check lakes, reservoirs and farmland for a large, plain grey-brown goose with an orange bill and pink legs \u2014 the wild ancestor of the farmyard goose.",
    "Eurasian Coot":
        "Look on lakes and slow rivers for an all-black waterbird with a bright white bill and forehead shield \u2014 quite aggressive, often seen chasing other coots across the water.",
    "Common Moorhen":
        "Check pond and river edges for a dark waterbird with a red-and-yellow bill and a flicking white tail, walking on long-toed feet across lily pads and waterside vegetation.",
    "Little Grebe":
        "Look for a small, round, dumpy waterbird diving frequently on ponds and slow rivers, often disappearing underwater for long stretches \u2014 listen for its trilling, whinnying call.",
    "Great Crested Grebe":
        "Check larger lakes and reservoirs, especially in spring, for an elegant waterbird with head plumes and a stunning head-shaking courtship dance performed by pairs face to face.",
    "Common Kingfisher":
        "Watch quiet stretches of river or canal for a flash of electric blue skimming low and fast over the water \u2014 a lucky sighting is often just a blur before it's gone.",
    "Common Eider":
        "Look along rocky and sandy coasts for a large, chunky sea duck \u2014 the male is bold black-and-white, and its deep, crooning 'ooh' call is a classic seaside sound.",
    "Grey Heron":
        "Check riverbanks, lake edges and even garden ponds for a tall, still grey bird standing statue-like in shallow water, waiting to spear a fish with a sudden strike.",
    "Eurasian Oystercatcher":
        "Look along beaches, estuaries and riverbanks for a bold black-and-white wader with a long, bright orange-red bill, and listen for its loud, piping 'kleep' call.",
    "Common Ringed Plover":
        "Check sandy and shingle beaches for a small, plump wader with a black breast-band and orange legs, running in short bursts then stopping suddenly to peck at the sand.",
    "Sanderling":
        "Watch the very edge of the waves on sandy beaches for a small pale wader chasing the tide in and out on quick, scurrying legs, like a little clockwork toy.",
    "Ruddy Turnstone":
        "Look on rocky and pebbly shorelines for a stocky wader with orange legs, doing exactly what its name says \u2014 flipping stones and seaweed with its bill to find food underneath.",
    "Common Sandpiper":
        "Check riverbanks, lake edges and reservoir margins for a small wader bobbing its tail constantly as it walks, and flying low over the water on stiff, bowed wings.",
    "Common Snipe":
        "Look in damp marshes and wet grassland for a stocky, camouflaged wader with an extremely long, straight bill, most often flushed suddenly from the grass in a fast zigzag flight.",
    "Northern Lapwing":
        "Check farmland and wet meadows for a striking black-and-white bird with a wispy head crest and rounded, floppy wings \u2014 its display flight includes tumbling dives and a wheezy 'pee-wit' call.",
    "Eurasian Curlew":
        "Look on estuaries, coastal mudflats and upland moors for Britain's largest wader, with a very long, down-curved bill and a beautiful, bubbling call that carries a long way.",
    "Eurasian Woodcock":
        "A very hard bird to spot by day \u2014 check damp woodland at dusk from spring, listening for a strange, croaking-then-squeaking flight display known as 'roding' over the treetops.",
    "Herring Gull":
        "Look almost anywhere on the coast, and in many town centres too, for a large gull with a grey back, pink legs and a red spot on the bill \u2014 its laughing call is a classic seaside sound.",
    "Black-headed Gull":
        "Check park lakes, playing fields and coasts for a small gull with a chocolate-brown head in summer (not actually black) and white head with a dark ear-spot in winter.",
    "Common Gull":
        "Look on playing fields, coasts and reservoirs for a gull smaller and gentler-looking than Herring Gull, with a rounder head, yellow-green legs and a plain yellow bill.",
    "Great Black-backed Gull":
        "Check coastal cliffs, harbours and large rivers for the biggest gull in the world, with a very dark, almost black back and a deep, booming call.",
    "Great Cormorant":
        "Look on rivers, reservoirs and coasts for a large black waterbird, often seen perched with wings held out wide to dry after diving for fish.",
    "Common Tern":
        "Check coasts, gravel pits and rivers in summer for a slender, elegant seabird with a forked tail, hovering then plunge-diving headfirst for small fish.",
    "Barn Swallow":
        "Watch farmland and open skies from April to September for a fast-flying bird with a deeply forked tail and rusty-red throat, often skimming low for insects near livestock and water.",
    "Common House-Martin":
        "Look under the eaves of houses and barns in summer for a bird with a glossy blue-black back and a bold white rump, building a neat mud-cup nest against the wall.",
    "Northern Gannet":
        "Check the coast, especially near big seabird cliffs, for a huge white seabird with black wingtips and a dagger bill, folding its wings into a spectacular vertical dive for fish.",
    "Razorbill":
        "Look on sheer coastal cliffs and offshore waters in the breeding season for a black-and-white seabird with a thick, blunt bill marked with a white stripe, nesting in tight, noisy colonies.",
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


_check_names()
