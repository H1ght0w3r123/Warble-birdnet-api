"""
Dress Up catalog - 55 items across 6 categories, real design art
(Warble art pass 02). Each accessory overlays the 100x100 avatar
illustration (see avatarSvg() in the frontend). tile_viewbox is the
cropped viewBox used to render this item inside a 96px carousel tile,
so the art fills the tile regardless of which zone it sits in.

Hats carry their tilt baked into a <g transform> wrapper (translate +
rotate around a 50,26 pivot) rather than a CSS transform, since the
app has no per-item CSS-transform pipeline for these overlays - this
is the SVG-native equivalent, same visual result.

Glasses (art pass 03) are real raster art rather than hand-coded paths -
each is a photo/AI-generated pair of glasses, cut out with an alpha matte
and referenced via an SVG <image> tag at a fixed x/y/width/height within
the same 100x100 avatar space, sized to the 56-unit span between the
avatar's two eyes (at x=39.5 and x=60.5, y=51) and vertically centered on
the eye line. The monocle is the one exception - asymmetric by design, so
it's narrower and sits over the right eye only rather than spanning both.
"""

# Price ladder. Costs come from named bands rather than being picked ad hoc,
# so the spread stays deliberate and any new item has an obvious price.
#
# Sized against what the economy actually pays: roughly 150 feathers a week for
# a child warbling a few times and finishing some challenges, up to ~310 in a
# very strong week. Previously everything cost 20-110, which meant the dearest
# item was under one week's income and there was nothing left to want. The top
# band is now about a month of saving.
PRICE_TIERS = {
    "starter": 5,      # a session or two
    "everyday": 10,    # a few sessions
    "special": 20,     # about a week
    "prestige": 40,    # a fortnight - a real goal
    "legendary": 75,   # a month or so - the things to dream about
}

ACCESSORIES = {
    "top_hat": {
        "name": "Top Hat",
        "emoji": "🎩",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "11.95 -33.75 73.07 73.07",
        "svg": '<g transform="rotate(-8 50 26)"><image xlink:href="/static/accessories/hat_top_hat.webp" href="/static/accessories/hat_top_hat.webp" x="23.23" y="-16.89" width="57.00" height="39.39"/></g>',
    },
    "golden_crown": {
        "name": "Golden Crown",
        "emoji": "👑",
        "cost": 75,
        "category": "hats",
        "tile_viewbox": "21.43 -25.74 64.71 64.71",
        "svg": '<g transform="rotate(6 50 26)"><image xlink:href="/static/accessories/hat_golden_crown.webp" href="/static/accessories/hat_golden_crown.webp" x="26.23" y="-13.36" width="51.00" height="39.36"/></g>',
    },
    "flower_crown": {
        "name": "Flower Crown",
        "emoji": "🌸",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "13.26 -28.42 73.90 73.90",
        "svg": '<g transform="rotate(-5 50 26)"><image xlink:href="/static/accessories/hat_flower_crown.webp" href="/static/accessories/hat_flower_crown.webp" x="21.73" y="-7.77" width="60.00" height="32.77"/></g>',
    },
    "deerstalker_hat": {
        "name": "Deerstalker Hat",
        "emoji": "🔍",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "16.52 -25.62 66.59 66.59",
        "svg": '<g transform="rotate(-6 50 26)"><image xlink:href="/static/accessories/hat_deerstalker_hat.webp" href="/static/accessories/hat_deerstalker_hat.webp" x="25.33" y="-11.00" width="52.80" height="37.50"/></g>',
    },
    "baseball_cap": {
        "name": "Baseball Cap",
        "emoji": "🧢",
        "cost": 10,
        "category": "hats",
        "tile_viewbox": "12.46 -14.21 65.36 65.36",
        # clipPath trims the side-panel tips that would otherwise hang below
        # the bill as a disconnected dark sliver, since the head is narrower
        # there than the cap art - they'd be hidden by the head's curve on
        # a real 3D head, so they're not something a front view should show.
        "svg": '<g transform="rotate(-9 50 26)"><defs><clipPath id="cap-underside-clip" clipPathUnits="objectBoundingBox"><polygon points="0,0 1,0 1,0.80 0.86,1 0.14,1 0,0.80"/></clipPath></defs><image clip-path="url(#cap-underside-clip)" xlink:href="/static/accessories/hat_baseball_cap.webp" href="/static/accessories/hat_baseball_cap.webp" x="23.03" y="2.44" width="51.00" height="32.06"/></g>',
    },
    "sun_hat": {
        "name": "Sun Hat",
        "emoji": "👒",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "21.55 -17.67 62.54 62.54",
        "svg": '<g transform="rotate(5 50 26)"><image xlink:href="/static/accessories/hat_sun_hat.webp" href="/static/accessories/hat_sun_hat.webp" x="26.23" y="0.81" width="51.00" height="25.19"/></g>',
    },
    "party_hat": {
        "name": "Party Hat",
        "emoji": "🥳",
        "cost": 10,
        "category": "hats",
        "tile_viewbox": "33.79 -14.11 41.98 41.98",
        "svg": '<g transform="rotate(9 50 26)"><image xlink:href="/static/accessories/hat_party_hat.webp" href="/static/accessories/hat_party_hat.webp" x="36.73" y="-9.27" width="30.00" height="31.27"/></g>',
    },
    "wizard_hat": {
        "name": "Wizard Hat",
        "emoji": "🧙",
        "cost": 75,
        "category": "hats",
        "tile_viewbox": "17.32 -22.04 65.03 65.03",
        "svg": '<g transform="rotate(-7 50 26)"><image xlink:href="/static/accessories/hat_wizard_hat.webp" href="/static/accessories/hat_wizard_hat.webp" x="26.23" y="-7.86" width="51.00" height="36.86"/></g>',
    },
    "pirate_hat": {
        "name": "Pirate Hat",
        "emoji": "🏴",
        "cost": 40,
        "category": "hats",
        "tile_viewbox": "18.55 -26 71.03 71.03",
        "svg": '<g transform="rotate(8 50 26)"><image xlink:href="/static/accessories/hat_pirate_hat.webp" href="/static/accessories/hat_pirate_hat.webp" x="24.13" y="-10.76" width="55.20" height="39.76"/></g>',
    },
    "explorer_helmet": {
        "name": "Explorer Helmet",
        "emoji": "🪖",
        "cost": 40,
        "category": "hats",
        "tile_viewbox": "18.28 -20.89 63.77 63.77",
        "svg": '<g transform="rotate(-6 50 26)"><image xlink:href="/static/accessories/hat_explorer_helmet.webp" href="/static/accessories/hat_explorer_helmet.webp" x="26.23" y="-4.81" width="51.00" height="31.81"/></g>',
    },
    "ski_hat": {
        "name": "Ski Hat",
        "emoji": "🎿",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "21.10 -27.89 66.37 66.37",
        "svg": '<g transform="rotate(7 50 26)"><image xlink:href="/static/accessories/hat_ski_hat.webp" href="/static/accessories/hat_ski_hat.webp" x="26.23" y="-18.14" width="51.00" height="46.14"/></g>',
    },
    "cozy_beanie": {
        "name": "Cozy Beanie",
        "emoji": "🧶",
        "cost": 10,
        "category": "hats",
        "tile_viewbox": "20.90 -29.78 68.66 68.66",
        "svg": '<g transform="rotate(-4 50 26)"><image xlink:href="/static/accessories/hat_cozy_beanie.webp" href="/static/accessories/hat_cozy_beanie.webp" x="29.13" y="-17.76" width="55.20" height="44.76"/></g>',
    },
    "cosy_scarf": {
        "name": "Cosy Scarf",
        "emoji": "🧣",
        "cost": 10,
        "category": "neck",
        "tile_viewbox": "25.83 43.50 51.81 51.81",
        "svg": '<image xlink:href="/static/accessories/neck_cosy_scarf.webp" href="/static/accessories/neck_cosy_scarf.webp" x="29.78" y="50.2" width="43.91" height="38.42"/>',
    },
    "fancy_bow": {
        "name": "Fancy Bow",
        "emoji": "🎀",
        "cost": 5,
        "category": "neck",
        "tile_viewbox": "28.08 45.76 47.31 47.31",
        "svg": '<image xlink:href="/static/accessories/neck_fancy_bow.webp" href="/static/accessories/neck_fancy_bow.webp" x="31.69" y="50.2" width="40.09" height="38.42"/>',
    },
    "bow_tie": {
        "name": "Bow Tie",
        "emoji": "🎗️",
        "cost": 5,
        "category": "neck",
        "tile_viewbox": "18.39 33.56 66.67 66.67",
        "svg": '<image xlink:href="/static/accessories/neck_bow_tie.webp" href="/static/accessories/neck_bow_tie.webp" x="23.48" y="50.2" width="56.5" height="33.39"/>',
    },
    "beaded_necklace": {
        "name": "Beaded Necklace",
        "emoji": "📿",
        "cost": 10,
        "category": "neck",
        "tile_viewbox": "18.82 36.49 65.84 65.84",
        "svg": '<image xlink:href="/static/accessories/neck_beaded_necklace.webp" href="/static/accessories/neck_beaded_necklace.webp" x="23.84" y="50.2" width="55.8" height="38.42"/>',
    },
    "golden_medal": {
        "name": "Golden Medal",
        "emoji": "🏅",
        "cost": 75,
        "category": "neck",
        "tile_viewbox": "28.71 46.38 46.07 46.07",
        "svg": '<image xlink:href="/static/accessories/neck_golden_medal.webp" href="/static/accessories/neck_golden_medal.webp" x="32.22" y="50.2" width="39.04" height="38.42"/>',
    },
    "pearl_necklace": {
        "name": "Pearl Necklace",
        "emoji": "🤍",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "19.07 36.74 65.34 65.34",
        "svg": '<image xlink:href="/static/accessories/neck_pearl_necklace.webp" href="/static/accessories/neck_pearl_necklace.webp" x="24.05" y="50.2" width="55.37" height="38.42"/>',
    },
    "striped_scarf": {
        "name": "Striped Scarf",
        "emoji": "🧣",
        "cost": 10,
        "category": "neck",
        "tile_viewbox": "25.40 43.08 52.66 52.66",
        "svg": '<image xlink:href="/static/accessories/neck_striped_scarf.webp" href="/static/accessories/neck_striped_scarf.webp" x="29.42" y="50.2" width="44.63" height="38.42"/>',
    },
    "star_necklace": {
        "name": "Star Necklace",
        "emoji": "⭐",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "25.96 43.63 51.55 51.55",
        "svg": '<image xlink:href="/static/accessories/neck_star_necklace.webp" href="/static/accessories/neck_star_necklace.webp" x="29.89" y="50.2" width="43.69" height="38.42"/>',
    },
    "flower_lei": {
        "name": "Flower Lei",
        "emoji": "🌺",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "24.64 42.31 54.20 54.20",
        "svg": '<image xlink:href="/static/accessories/neck_flower_lei.webp" href="/static/accessories/neck_flower_lei.webp" x="28.77" y="50.2" width="45.93" height="38.42"/>',
    },
    "cape": {
        "name": "Cape",
        "emoji": "🦸",
        "cost": 40,
        "category": "neck",
        "tile_viewbox": "18.39 29.68 66.67 66.67",
        "svg": '<image xlink:href="/static/accessories/neck_cape.webp" href="/static/accessories/neck_cape.webp" x="23.48" y="50.2" width="56.5" height="25.63"/>',
    },
    "explorer_backpack": {
        "name": "Explorer Backpack",
        "emoji": "🎒",
        "cost": 40,
        "category": "gear",
        "tile_viewbox": "9.17 18.90 81.66 81.66",
        "svg": '<g transform="translate(0,-12.8)"><path d="M15.4 61 C15.4 58.6 17 57 19.6 57 L26 57 C27.4 57 28 58 28 59.4 L28 73 C28 75 26.6 76 24.4 76 L19.6 76 C17 76 15.4 74.4 15.4 72 Z" fill="#7EC8A4"></path><path d="M24 57.4 C26.6 58 28 59 28 60.6 L28 73 C28 75 26.6 76 24.4 76 C25.4 74 25.6 71.6 25.4 68.6 C25 64.6 24.6 61 24 57.4 Z" fill="#3F7C5C"></path><path d="M84.6 61 C84.6 58.6 83 57 80.4 57 L74 57 C72.6 57 72 58 72 59.4 L72 73 C72 75 73.4 76 75.6 76 L80.4 76 C83 76 84.6 74.4 84.6 72 Z" fill="#7EC8A4"></path><path d="M76 57.4 C73.4 58 72 59 72 60.6 L72 73 C72 75 73.4 76 75.6 76 C74.6 74 74.4 71.6 74.6 68.6 C75 64.6 75.4 61 76 57.4 Z" fill="#3F7C5C"></path><path d="M37.6 61 C39.6 60.4 42.4 60.4 44.4 61 C45.4 69.6 46 78.6 46 87.6 C44 88.2 41.4 88.2 39.4 87.6 C39.4 78.6 38.6 69.6 37.6 61 Z" fill="#3F7C5C"></path><path d="M62.4 61 C60.4 60.4 57.6 60.4 55.6 61 C54.6 69.6 54 78.6 54 87.6 C56 88.2 58.6 88.2 60.6 87.6 C60.6 78.6 61.4 69.6 62.4 61 Z" fill="#3F7C5C"></path><path d="M43 60.6 C44 60.7 44.4 60.8 44.4 61 C45.4 69.6 46 78.6 46 87.6 C45.4 87.8 44.8 88 44.2 88 C44.2 78.6 43.6 69.4 43 60.6 Z" fill="#7EC8A4" opacity="0.5"></path><path d="M57 60.6 C56 60.7 55.6 60.8 55.6 61 C54.6 69.6 54 78.6 54 87.6 C54.6 87.8 55.2 88 55.8 88 C55.8 78.6 56.4 69.4 57 60.6 Z" fill="#7EC8A4" opacity="0.5"></path><path d="M39 71.6 L46 71.6 L46 76.4 L39 76.4 Z" fill="#F2C94C"></path><path d="M54 71.6 L61 71.6 L61 76.4 L54 76.4 Z" fill="#F2C94C"></path><path d="M41 73 L44 73 L44 75 L41 75 Z" fill="#B8901F"></path><path d="M56 73 L59 73 L59 75 L56 75 Z" fill="#B8901F"></path></g>',
    },
    "round_specs": {
        "name": "Round Wire Specs",
        "emoji": "👓",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "14.39 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_round_wire_specs.webp" href="/static/accessories/glasses_round_wire_specs.webp" x="20.09" y="23.12" width="63.28" height="24.2"/>',
    },
    "explorer_goggles": {
        "name": "Explorer Goggles",
        "emoji": "🥽",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "14.39 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_explorer_goggles.webp" href="/static/accessories/glasses_explorer_goggles.webp" x="20.09" y="23.89" width="63.28" height="22.65"/>',
    },
    "sunglasses": {
        "name": "Aviator Sunglasses",
        "emoji": "🕶️",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "14.39 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_aviator_sunglasses.webp" href="/static/accessories/glasses_aviator_sunglasses.webp" x="20.09" y="23.62" width="63.28" height="23.2"/>',
    },
    "star_glasses": {
        "name": "Star Glasses",
        "emoji": "⭐",
        "cost": 75,
        "category": "glasses",
        "tile_viewbox": "14.39 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_star_glasses.webp" href="/static/accessories/glasses_star_glasses.webp" x="20.09" y="22.96" width="63.28" height="24.52"/>',
    },
    "black_browline": {
        "name": "Browline Glasses",
        "emoji": "🤓",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "14.39 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_black_browline.webp" href="/static/accessories/glasses_black_browline.webp" x="20.09" y="25.21" width="63.28" height="20.02"/>',
    },
    "cat_eye": {
        "name": "Cat-Eye Glasses",
        "emoji": "😼",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "14.39 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_cat_eye.webp" href="/static/accessories/glasses_cat_eye.webp" x="20.09" y="24.79" width="63.28" height="20.85"/>',
    },
    "heart_glasses": {
        "name": "Heart Glasses",
        "emoji": "💗",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "14.39 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_heart_glasses.webp" href="/static/accessories/glasses_heart_glasses.webp" x="20.09" y="24.05" width="63.28" height="22.34"/>',
    },
    "movie_3d": {
        "name": "3D Movie Glasses",
        "emoji": "🎬",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "14.39 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_movie_3d.webp" href="/static/accessories/glasses_movie_3d.webp" x="20.09" y="24.99" width="63.28" height="20.45"/>',
    },
    "monocle": {
        "name": "Monocle",
        "emoji": "🧐",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "48.48 13.88 42.67 42.67",
        "svg": '<image xlink:href="/static/accessories/glasses_monocle.webp" href="/static/accessories/glasses_monocle.webp" x="51.73" y="25.2" width="36.16" height="20.03"/>',
    },
    "rainbow_holo": {
        "name": "Rainbow Holo Sunglasses",
        "emoji": "🌈",
        "cost": 75,
        "category": "glasses",
        "tile_viewbox": "14.39 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_rainbow_holo.webp" href="/static/accessories/glasses_rainbow_holo.webp" x="20.09" y="24.82" width="63.28" height="20.8"/>',
    },
    "wellies": {
        "name": "Wellies",
        "emoji": "👢",
        "cost": 10,
        "category": "shoes",
        "tile_viewbox": "29.94 63.27 40.12 40.12",
        "svg": '<image xlink:href="/static/accessories/shoe_wellies.webp" href="/static/accessories/shoe_wellies.webp" x="33" y="66.76" width="34" height="33.14"/>',
    },
    "trainers": {
        "name": "Trainers",
        "emoji": "👟",
        "cost": 20,
        "category": "shoes",
        "tile_viewbox": "29.94 69.03 40.12 40.12",
        "svg": '<image xlink:href="/static/accessories/shoe_trainers.webp" href="/static/accessories/shoe_trainers.webp" x="33" y="78.28" width="34" height="21.62"/>',
    },
    "hiking_boots": {
        "name": "Hiking Boots",
        "emoji": "🥾",
        "cost": 40,
        "category": "shoes",
        "tile_viewbox": "29.94 67.06 40.12 40.12",
        "svg": '<image xlink:href="/static/accessories/shoe_hiking_boots.webp" href="/static/accessories/shoe_hiking_boots.webp" x="33" y="74.35" width="34" height="25.55"/>',
    },
    "roller_skates": {
        "name": "Roller Skates",
        "emoji": "🛼",
        "cost": 75,
        "category": "shoes",
        "tile_viewbox": "29.94 64.68 40.12 40.12",
        "svg": '<image xlink:href="/static/accessories/shoe_roller_skates.webp" href="/static/accessories/shoe_roller_skates.webp" x="33" y="69.58" width="34" height="30.32"/>',
    },
    "cowboy_boots": {
        "name": "Cowboy Boots",
        "emoji": "🤠",
        "cost": 20,
        "category": "shoes",
        "tile_viewbox": "26.84 57.12 46.31 46.31",
        "svg": '<image xlink:href="/static/accessories/shoe_cowboy_boots.webp" href="/static/accessories/shoe_cowboy_boots.webp" x="33" y="60.65" width="34" height="39.25"/>',
    },
    "ballet_slippers": {
        "name": "Ballet Slippers",
        "emoji": "🩰",
        "cost": 10,
        "category": "shoes",
        "tile_viewbox": "29.94 65.37 40.12 40.12",
        "svg": '<image xlink:href="/static/accessories/shoe_ballet_slippers.webp" href="/static/accessories/shoe_ballet_slippers.webp" x="33" y="70.96" width="34" height="28.94"/>',
    },
    "flip_flops": {
        "name": "Flip-Flops",
        "emoji": "🩴",
        "cost": 5,
        "category": "shoes",
        "tile_viewbox": "29.94 69.10 40.12 40.12",
        "svg": '<image xlink:href="/static/accessories/shoe_flip_flops.webp" href="/static/accessories/shoe_flip_flops.webp" x="33" y="78.43" width="34" height="21.47"/>',
    },
    "football_boots": {
        "name": "Football Boots",
        "emoji": "⚽",
        "cost": 20,
        "category": "shoes",
        "tile_viewbox": "29.94 68 40.12 40.12",
        "svg": '<image xlink:href="/static/accessories/shoe_football_boots.webp" href="/static/accessories/shoe_football_boots.webp" x="33" y="76.23" width="34" height="23.67"/>',
    },
    "snow_boots": {
        "name": "Snow Boots",
        "emoji": "❄️",
        "cost": 20,
        "category": "shoes",
        "tile_viewbox": "29.94 68.07 40.12 40.12",
        "svg": '<image xlink:href="/static/accessories/shoe_snow_boots.webp" href="/static/accessories/shoe_snow_boots.webp" x="33" y="76.36" width="34" height="23.54"/>',
    },
    "ice_skates": {
        "name": "Ice Skates",
        "emoji": "⛸️",
        "cost": 40,
        "category": "shoes",
        "tile_viewbox": "29.94 68.88 40.12 40.12",
        "svg": '<image xlink:href="/static/accessories/shoe_ice_skates.webp" href="/static/accessories/shoe_ice_skates.webp" x="33" y="77.97" width="34" height="21.93"/>',
    },
    "ice_cream": {
        "name": "Ice Cream",
        "emoji": "🍦",
        "cost": 10,
        "category": "held",
        "tile_viewbox": "58.16 46.61 41.61 41.61",
        "svg": '<g transform="rotate(14 78 63)"><path d="M73.5 65 L86.5 65 L80 83 Z" fill="#D9A441"></path><path d="M73.5 65 L86.5 65 L80 83 Z" fill="#1A1128" opacity="0.12"></path><circle cx="76.3" cy="61.5" r="5.2" fill="#E87EA1"></circle><circle cx="83.7" cy="61.5" r="5.2" fill="#F5EDD6"></circle><circle cx="80" cy="56.5" r="5.4" fill="#7EC8A4"></circle></g>',
    },
    "walkie_talkie": {
        "name": "Walkie Talkie",
        "emoji": "📻",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "57.85 43.82 43.21 43.21",
        "svg": '<g transform="rotate(14 78 63)"><rect x="72.5" y="58" width="15" height="24" rx="2.5" fill="#2D1B69"></rect><rect x="75.5" y="61" width="9" height="6" rx="1" fill="#7EC8A4"></rect><circle cx="77.5" cy="72" r="1.7" fill="#C4BFDF"></circle><circle cx="82.5" cy="72" r="1.7" fill="#C4BFDF"></circle><circle cx="77.5" cy="77" r="1.7" fill="#C4BFDF"></circle><circle cx="82.5" cy="77" r="1.7" fill="#C4BFDF"></circle><rect x="83" y="48" width="2.6" height="11" rx="1.3" fill="#1A1128"></rect></g>',
    },
    "microphone": {
        "name": "Microphone",
        "emoji": "🎤",
        "cost": 75,
        "category": "held",
        "tile_viewbox": "58.80 49.32 39.49 39.49",
        "svg": '<g transform="rotate(14 78 63)"><rect x="78.4" y="65" width="3.2" height="18" rx="1.6" fill="#2B2B2B"></rect><circle cx="80" cy="60.5" r="7.2" fill="#8E87B8"></circle><circle cx="80" cy="60.5" r="4.8" fill="#C4BFDF"></circle><rect x="76" y="81" width="8" height="3.2" rx="1.6" fill="#1A1128"></rect></g>',
    },
    "lollipop": {
        "name": "Lollipop",
        "emoji": "🍭",
        "cost": 5,
        "category": "held",
        "tile_viewbox": "58.45 47.02 40.98 40.98",
        "svg": '<g transform="rotate(14 78 63)"><rect x="78.8" y="63" width="2.6" height="20" rx="1.3" fill="#F5EDD6"></rect><circle cx="80" cy="59.5" r="8.2" fill="#E87EA1"></circle><circle cx="80" cy="59.5" r="5.4" fill="#F5EDD6"></circle><circle cx="80" cy="59.5" r="2.7" fill="#E87EA1"></circle></g>',
    },
    "drumsticks": {
        "name": "Drumsticks",
        "emoji": "🥁",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "58.41 48.16 40.58 40.58",
        "svg": '<g transform="rotate(14 78 63)"><g transform="rotate(-11 75.5 69)"><rect x="74" y="57" width="3" height="26" rx="1.5" fill="#D9A441"></rect><circle cx="75.5" cy="56" r="2.8" fill="#B8901F"></circle></g><g transform="rotate(11 84.5 69)"><rect x="83" y="57" width="3" height="26" rx="1.5" fill="#D9A441"></rect><circle cx="84.5" cy="56" r="2.8" fill="#B8901F"></circle></g></g>',
    },
    "magnifying_glass": {
        "name": "Magnifying Glass",
        "emoji": "🔍",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "59.12 48.36 39.37 39.37",
        "svg": '<g transform="rotate(14 78 63)"><circle cx="80" cy="60" r="7.6" fill="#C4BFDF" opacity="0.55"></circle><circle cx="80" cy="60" r="7.6" fill="none" stroke="#8B5A2B" stroke-width="3"></circle><rect x="78.5" y="67" width="3" height="16" rx="1.5" fill="#8B5A2B"></rect></g>',
    },
    "water_bottle": {
        "name": "Water Bottle",
        "emoji": "🍶",
        "cost": 5,
        "category": "held",
        "tile_viewbox": "58.94 47.33 40.06 40.06",
        "svg": '<g transform="rotate(14 78 63)"><rect x="76" y="51" width="8" height="5.5" rx="1.5" fill="#3F7C5C"></rect><rect x="74" y="56" width="12" height="27" rx="3.5" fill="#7EC8A4"></rect><rect x="74" y="64" width="12" height="6.5" fill="#F5EDD6"></rect><rect x="76.4" y="59" width="2.5" height="20" rx="1.2" fill="#FFFFFF" opacity="0.35"></rect></g>',
    },
    "binoculars": {
        "name": "Binoculars",
        "emoji": "🔭",
        "cost": 75,
        "category": "gear",
        "tile_viewbox": "37.19 31.64 33.63 33.63",
        "svg": '<g transform="translate(0,-12.8)"><path d="M42 47 L56 65 L66 47" fill="none" stroke="#3D2A85" stroke-width="2.5" stroke-linecap="round"></path><rect x="47.5" y="63" width="17" height="12.5" rx="2.2" fill="#2D1B69"></rect><circle cx="51.5" cy="69.2" r="3.6" fill="#1A1128"></circle><circle cx="60.5" cy="69.2" r="3.6" fill="#1A1128"></circle><circle cx="51.5" cy="69.2" r="2" fill="#5B93C4"></circle><circle cx="60.5" cy="69.2" r="2" fill="#5B93C4"></circle></g>',
    },
    "camera": {
        "name": "Camera",
        "emoji": "📷",
        "cost": 75,
        "category": "gear",
        "tile_viewbox": "36.59 31.55 34.81 34.81",
        "svg": '<g transform="translate(0,-12.8)"><path d="M42 47 L56 65 L66 47" fill="none" stroke="#2B2B2B" stroke-width="2.5" stroke-linecap="round"></path><rect x="46.5" y="63" width="19" height="13.5" rx="2.5" fill="#2B2B2B"></rect><circle cx="56" cy="69.8" r="4.8" fill="#5B93C4"></circle><circle cx="56" cy="69.8" r="2.5" fill="#1A1128"></circle><rect x="61" y="60.2" width="4.2" height="3.2" rx="1" fill="#2B2B2B"></rect></g>',
    },
    "compass": {
        "name": "Compass",
        "emoji": "🧭",
        "cost": 40,
        "category": "gear",
        "tile_viewbox": "35.89 31.44 36.23 36.23",
        "svg": '<g transform="translate(0,-12.8)"><path d="M42 47 L56 65 L66 47" fill="none" stroke="#8B5A2B" stroke-width="2.5" stroke-linecap="round"></path><circle cx="56" cy="69.5" r="8.2" fill="#F5EDD6"></circle><circle cx="56" cy="69.5" r="8.2" fill="none" stroke="#8B5A2B" stroke-width="2"></circle><path d="M56 63 L58.6 69.5 L56 76 L53.4 69.5 Z" fill="#C0392B"></path></g>',
    },
    "field_notebook": {
        "name": "Field Notebook",
        "emoji": "📓",
        "cost": 10,
        "category": "gear",
        "tile_viewbox": "34.23 31.19 39.53 39.53",
        "svg": '<g transform="translate(0,-12.8)"><path d="M42 47 L56 65 L66 47" fill="none" stroke="#8B5A2B" stroke-width="2.5" stroke-linecap="round"></path><rect x="48" y="63" width="16" height="17.5" rx="1.5" fill="#F5EDD6"></rect><rect x="48" y="63" width="16" height="17.5" rx="1.5" fill="none" stroke="#8B5A2B" stroke-width="1.5"></rect><path d="M51 68 L61 68 M51 72 L61 72 M51 76 L61 76" stroke="#8E87B8" stroke-width="1"></path></g>',
    },
    "satchel": {
        "name": "Satchel",
        "emoji": "👜",
        "cost": 10,
        "category": "gear",
        "tile_viewbox": "36.30 31.50 35.40 35.40",
        "svg": '<g transform="translate(0,-12.8)"><path d="M42 47 L56 65 L66 47" fill="none" stroke="#B85A36" stroke-width="2.5" stroke-linecap="round"></path><rect x="46" y="63" width="20" height="14" rx="2.5" fill="#E8845C"></rect><path d="M46 63 L66 63 L66 69 C66 70.2 65 70.6 64 70.6 L48 70.6 C47 70.6 46 70.2 46 69 Z" fill="#B85A36"></path><rect x="53" y="67" width="6" height="4.6" rx="1.2" fill="#F2C94C"></rect></g>',
    },
}

# Each category carries its own 24x24 icon inline. Previously icons lived in a
# separate parallel list matched by index - fragile, and easy to silently
# mismatch when reordering or adding a category, which this change does both of.
CATEGORIES = [
    {"id": "hats", "name": "Hats", "icon_svg": '<path d="M8.6 4.4 L15.4 4.4 L16.4 13.6 L7.6 13.6 Z" fill="#2D1B69"></path><path d="M7.6 10.6 L16.4 10.6 L16.4 13.6 L7.6 13.6 Z" fill="#E8845C"></path><path d="M3.6 14.4 C7 13 17 13 20.4 14.4 C20.4 16.4 17 17.6 12 17.6 C7 17.6 3.6 16.4 3.6 14.4 Z" fill="#2D1B69"></path>'},
    {"id": "glasses", "name": "Glasses", "icon_svg": '<circle cx="7.4" cy="12.4" r="4.6" fill="#1A1128"></circle><circle cx="16.6" cy="12.4" r="4.6" fill="#1A1128"></circle><circle cx="7.4" cy="12.4" r="2.9" fill="#F5EDD6"></circle><circle cx="16.6" cy="12.4" r="2.9" fill="#F5EDD6"></circle><path d="M10.6 10.6 C11.4 10.1 12.6 10.1 13.4 10.6 L13.4 12 C12.6 11.5 11.4 11.5 10.6 12 Z" fill="#1A1128"></path><path d="M2.8 11 C2 11.2 1.4 11.8 1 12.4 L2 13.4 C2.4 12.9 2.8 12.6 3.4 12.5 Z" fill="#1A1128"></path><path d="M21.2 11 C22 11.2 22.6 11.8 23 12.4 L22 13.4 C21.6 12.9 21.2 12.6 20.6 12.5 Z" fill="#1A1128"></path>'},
    {"id": "neck", "name": "Neck", "icon_svg": '<path d="M3.6 7 C6 8 9 9.8 10.8 12 C9 14.2 6 16 3.6 17 C4.4 13.6 4.4 10.4 3.6 7 Z" fill="#E87EA1"></path><path d="M20.4 7 C18 8 15 9.8 13.2 12 C15 14.2 18 16 20.4 17 C19.6 13.6 19.6 10.4 20.4 7 Z" fill="#E87EA1"></path><path d="M10.2 9.4 C11.4 9 12.6 9 13.8 9.4 C14.2 10.8 14.2 13.2 13.8 14.6 C12.6 15 11.4 15 10.2 14.6 C9.8 13.2 9.8 10.8 10.2 9.4 Z" fill="#B85A36"></path>'},
    {"id": "gear", "name": "Gear", "icon_svg": '<path d="M4 8.4 C4 6.8 5 6 7 6 C9 6 10 6.8 10 8.4 L10.4 15.6 C10.4 17.8 9 19 7 19 C5 19 3.6 17.8 3.6 15.6 Z" fill="#2D1B69"></path><path d="M14 8.4 C14 6.8 15 6 17 6 C19 6 20 6.8 20 8.4 L20.4 15.6 C20.4 17.8 19 19 17 19 C15 19 13.6 17.8 13.6 15.6 Z" fill="#2D1B69"></path><path d="M10.2 9.6 C11 9.2 13 9.2 13.8 9.6 L13.8 12.4 C13 12.8 11 12.8 10.2 12.4 Z" fill="#3D2A85"></path><circle cx="7" cy="15.4" r="2.4" fill="#C4BFDF"></circle><circle cx="17" cy="15.4" r="2.4" fill="#C4BFDF"></circle>'},
    {"id": "held", "name": "Held", "icon_svg": '<path d="M5 13 C5 10 7 8 10 8 L14 8 C17 8 19 10 19 13 L19 15 C19 17.6 17 19 14 19 L10 19 C7 19 5 17.6 5 15 Z" fill="#8E87B8"></path><circle cx="12" cy="13.4" r="3.2" fill="#F5EDD6"></circle><path d="M9 8 L9 5.4 C9 4.4 9.8 3.8 10.8 3.8 L13.2 3.8 C14.2 3.8 15 4.4 15 5.4 L15 8 Z" fill="#3D2A85"></path>'},
    {"id": "shoes", "name": "Shoes", "icon_svg": '<path d="M6 5.6 C8.4 5 11 5.2 12.6 6 C13.4 8.4 14.4 10.4 15.4 12 C16 13 15 14 12.6 14.2 C9.4 14.6 6.6 14.4 5.4 13.8 C4.6 13.4 4.4 11.6 4.8 9.6 C5.2 7.8 5.4 6.6 6 5.6 Z" fill="#7EC8A4"></path><path d="M5.6 5.2 C8 4.6 11 4.8 12.8 5.6 L13.2 8 C11 7.2 8 7 5.8 7.6 Z" fill="#F2C94C"></path><path d="M4.2 12 C6.6 11.4 13 11.8 15.6 12.4 C16.2 13.6 15.2 14.6 12.6 14.8 C9.4 15.2 6.6 15 5.4 14.4 C4.6 14 4.2 13 4.2 12 Z" fill="#3F7C5C"></path><path d="M17.6 14 C19 14 20 14.6 20 15.6 C20 16.8 19 17.4 17.6 17.4 C16.2 17.4 15.2 16.8 15.2 15.6 C15.2 14.6 16.2 14 17.6 14 Z" fill="#8E87B8"></path>'},
]
