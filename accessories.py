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
        "tile_viewbox": "14.04 -29.78 68.66 68.66",
        "svg": '<g transform="rotate(-4 50 26)"><image xlink:href="/static/accessories/hat_cozy_beanie.webp" href="/static/accessories/hat_cozy_beanie.webp" x="22.27" y="-17.76" width="55.20" height="44.76"/></g>',
    },
    "cosy_scarf": {
        "name": "Cosy Scarf",
        "emoji": "🧣",
        "cost": 10,
        "category": "neck",
        "tile_viewbox": "23.43 37.63 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_cosy_scarf.webp" href="/static/accessories/neck_cosy_scarf.webp" x="27.6" y="54.5" width="46.3" height="20.9"/>',
    },
    "fancy_bow": {
        "name": "Fancy Bow",
        "emoji": "🎀",
        "cost": 5,
        "category": "neck",
        "tile_viewbox": "23.43 39.88 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_fancy_bow.webp" href="/static/accessories/neck_fancy_bow.webp" x="27.6" y="54.5" width="46.3" height="25.39"/>',
    },
    "bow_tie": {
        "name": "Bow Tie",
        "emoji": "🎗️",
        "cost": 5,
        "category": "neck",
        "tile_viewbox": "23.43 36.33 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_bow_tie.webp" href="/static/accessories/neck_bow_tie.webp" x="27.6" y="54.5" width="46.3" height="18.29"/>',
    },
    "beaded_necklace": {
        "name": "Beaded Necklace",
        "emoji": "📿",
        "cost": 10,
        "category": "neck",
        "tile_viewbox": "23.43 37.71 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_beaded_necklace.webp" href="/static/accessories/neck_beaded_necklace.webp" x="27.6" y="54.5" width="46.3" height="21.06"/>',
    },
    "golden_medal": {
        "name": "Golden Medal",
        "emoji": "🏅",
        "cost": 75,
        "category": "neck",
        "tile_viewbox": "18.02 49.51 65.47 65.47",
        "svg": '<image xlink:href="/static/accessories/neck_golden_medal.webp" href="/static/accessories/neck_golden_medal.webp" x="27.6" y="54.5" width="46.3" height="55.48"/>',
    },
    "pearl_necklace": {
        "name": "Pearl Necklace",
        "emoji": "🤍",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "23.43 39.81 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_pearl_necklace.webp" href="/static/accessories/neck_pearl_necklace.webp" x="27.6" y="54.5" width="46.3" height="25.25"/>',
    },
    "striped_scarf": {
        "name": "Striped Scarf",
        "emoji": "🧣",
        "cost": 10,
        "category": "neck",
        "tile_viewbox": "23.43 38.94 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_striped_scarf.webp" href="/static/accessories/neck_striped_scarf.webp" x="27.6" y="54.5" width="46.3" height="23.51"/>',
    },
    "star_necklace": {
        "name": "Star Necklace",
        "emoji": "⭐",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "23.43 49.94 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_star_necklace.webp" href="/static/accessories/neck_star_necklace.webp" x="27.6" y="54.5" width="46.3" height="45.51"/>',
    },
    "flower_lei": {
        "name": "Flower Lei",
        "emoji": "🌺",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "23.43 38.71 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_flower_lei.webp" href="/static/accessories/neck_flower_lei.webp" x="27.6" y="54.5" width="46.3" height="23.06"/>',
    },
    "hip_hop_chain": {
        "name": "Hip-Hop Chain",
        "emoji": "💰",
        "cost": 50,
        "category": "neck",
        "tile_viewbox": "22.61 50.21 56.27 56.27",
        "svg": '<image xlink:href="/static/accessories/neck_hip_hop_chain.webp" href="/static/accessories/neck_hip_hop_chain.webp" x="27.6" y="54.5" width="46.3" height="47.69"/>',
    },
    "spiked_collar": {
        "name": "Spiked Collar",
        "emoji": "⛓️",
        "cost": 30,
        "category": "neck",
        "tile_viewbox": "23.43 36.04 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_spiked_collar.webp" href="/static/accessories/neck_spiked_collar.webp" x="27.6" y="54.5" width="46.3" height="17.71"/>',
    },
    "glow_necklace": {
        "name": "Glow Necklace",
        "emoji": "✨",
        "cost": 15,
        "category": "neck",
        "tile_viewbox": "23.43 38.57 54.63 54.63",
        "svg": '<image xlink:href="/static/accessories/neck_glow_necklace.webp" href="/static/accessories/neck_glow_necklace.webp" x="27.6" y="54.5" width="46.3" height="22.77"/>',
    },
    "round_specs": {
        "name": "Round Wire Specs",
        "emoji": "👓",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "12.64 -0.62 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_round_wire_specs.webp" href="/static/accessories/glasses_round_wire_specs.webp" x="18.34" y="24.62" width="63.28" height="24.2"/>',
    },
    "explorer_goggles": {
        "name": "Explorer Goggles",
        "emoji": "🥽",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "12.64 -0.62 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_explorer_goggles.webp" href="/static/accessories/glasses_explorer_goggles.webp" x="18.34" y="23.89" width="63.28" height="22.65"/>',
    },
    "sunglasses": {
        "name": "Aviator Sunglasses",
        "emoji": "🕶️",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "12.64 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_aviator_sunglasses.webp" href="/static/accessories/glasses_aviator_sunglasses.webp" x="18.34" y="25.12" width="63.28" height="23.2"/>',
    },
    "star_glasses": {
        "name": "Star Glasses",
        "emoji": "⭐",
        "cost": 75,
        "category": "glasses",
        "tile_viewbox": "12.64 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_star_glasses.webp" href="/static/accessories/glasses_star_glasses.webp" x="18.34" y="22.96" width="63.28" height="24.52"/>',
    },
    "black_browline": {
        "name": "Browline Glasses",
        "emoji": "🤓",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "12.64 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_black_browline.webp" href="/static/accessories/glasses_black_browline.webp" x="18.34" y="25.21" width="63.28" height="20.02"/>',
    },
    "cat_eye": {
        "name": "Cat-Eye Glasses",
        "emoji": "😼",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "12.64 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_cat_eye.webp" href="/static/accessories/glasses_cat_eye.webp" x="18.34" y="24.79" width="63.28" height="20.85"/>',
    },
    "heart_glasses": {
        "name": "Heart Glasses",
        "emoji": "💗",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "12.64 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_heart_glasses.webp" href="/static/accessories/glasses_heart_glasses.webp" x="18.34" y="24.05" width="63.28" height="22.34"/>',
    },
    "movie_3d": {
        "name": "3D Movie Glasses",
        "emoji": "🎬",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "12.64 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_movie_3d.webp" href="/static/accessories/glasses_movie_3d.webp" x="18.34" y="24.99" width="63.28" height="20.45"/>',
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
        "tile_viewbox": "12.64 -2.12 74.67 74.67",
        "svg": '<image xlink:href="/static/accessories/glasses_rainbow_holo.webp" href="/static/accessories/glasses_rainbow_holo.webp" x="18.34" y="24.82" width="63.28" height="20.8"/>',
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
        "tile_viewbox": "68.06 54.51 26.08 26.08",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_ice_cream.webp" href="/static/accessories/held_ice_cream.webp" x="70.75" y="53.88" width="14.87" height="26"/></g>',
    },
    "walkie_talkie": {
        "name": "Walkie Talkie",
        "emoji": "📻",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "65.72 53.97 27.97 27.97",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_walkie_talkie.webp" href="/static/accessories/held_walkie_talkie.webp" x="68.7" y="53.88" width="15.4" height="26"/></g>',
    },
    "microphone": {
        "name": "Microphone",
        "emoji": "🎤",
        "cost": 75,
        "category": "held",
        "tile_viewbox": "68.30 54.40 27.49 27.49",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_microphone.webp" href="/static/accessories/held_microphone.webp" x="71.37" y="54.4" width="16.75" height="26"/></g>',
    },
    "lollipop": {
        "name": "Lollipop",
        "emoji": "🍭",
        "cost": 5,
        "category": "held",
        "tile_viewbox": "66 52.55 26.90 26.90",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_lollipop.webp" href="/static/accessories/held_lollipop.webp" x="67.87" y="53.36" width="18.54" height="26"/></g>',
    },
    "drumsticks": {
        "name": "Drumsticks",
        "emoji": "🥁",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "64.65 56.10 27.49 27.49",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_drumsticks.webp" href="/static/accessories/held_drumsticks.webp" x="69.7" y="57.0" width="13.39" height="26"/></g>',
    },
    "magnifying_glass": {
        "name": "Magnifying Glass",
        "emoji": "🔍",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "68.47 53.82 27.26 27.26",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_magnifying_glass.webp" href="/static/accessories/held_magnifying_glass.webp" x="70.4" y="53.88" width="18.75" height="26"/></g>',
    },
    "water_bottle": {
        "name": "Water Bottle",
        "emoji": "🍶",
        "cost": 5,
        "category": "held",
        "tile_viewbox": "64.56 52.26 29.38 29.38",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_water_bottle.webp" href="/static/accessories/held_water_bottle.webp" x="68.8" y="53.62" width="15.21" height="26"/></g>',
    },
    "stick": {
        "name": "Stick",
        "emoji": "🌿",
        "cost": 5,
        "category": "held",
        "tile_viewbox": "71.12 54.92 28.56 28.56",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_stick.webp" href="/static/accessories/held_stick.webp" x="73.4" y="55.18" width="19.98" height="26"/></g>',
    },
    "magic_baton": {
        "name": "Magic Baton",
        "emoji": "🪄",
        "cost": 30,
        "category": "held",
        "tile_viewbox": "72.32 55.72 27.26 27.26",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_magic_baton.webp" href="/static/accessories/held_magic_baton.webp" x="74.2" y="54.4" width="18.31" height="26"/></g>',
    },
    "star_wand": {
        "name": "Star Wand",
        "emoji": "⭐",
        "cost": 30,
        "category": "held",
        "tile_viewbox": "73.20 55.70 26.20 26.20",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_star_wand.webp" href="/static/accessories/held_star_wand.webp" x="73.74" y="53.88" width="19.0" height="26"/></g>',
    },
    "baby_rattle": {
        "name": "Rattle",
        "emoji": "🍼",
        "cost": 15,
        "category": "held",
        "tile_viewbox": "70.94 56.39 27.73 27.73",
        "svg": '<g transform="rotate(14 76.4 79.1)"><image xlink:href="/static/accessories/held_baby_rattle.webp" href="/static/accessories/held_baby_rattle.webp" x="72.87" y="55.7" width="19.59" height="26"/></g>',
    },
    "binoculars": {
        "name": "Binoculars",
        "emoji": "🔭",
        "cost": 75,
        "category": "neck",
        "tile_viewbox": "21.85 50.09 57.81 57.81",
        "svg": '<image xlink:href="/static/accessories/neck_binoculars.webp" href="/static/accessories/neck_binoculars.webp" x="27.6" y="54.5" width="46.3" height="48.99"/>',
    },
}

# Each category carries its own 24x24 icon inline. Previously icons lived in a
# separate parallel list matched by index - fragile, and easy to silently
# mismatch when reordering or adding a category, which this change does both of.
CATEGORIES = [
    {"id": "hats", "name": "Hats", "icon_svg": '<path d="M8.6 4.4 L15.4 4.4 L16.4 13.6 L7.6 13.6 Z" fill="#2D1B69"></path><path d="M7.6 10.6 L16.4 10.6 L16.4 13.6 L7.6 13.6 Z" fill="#E8845C"></path><path d="M3.6 14.4 C7 13 17 13 20.4 14.4 C20.4 16.4 17 17.6 12 17.6 C7 17.6 3.6 16.4 3.6 14.4 Z" fill="#2D1B69"></path>'},
    {"id": "glasses", "name": "Glasses", "icon_svg": '<circle cx="7.4" cy="12.4" r="4.6" fill="#1A1128"></circle><circle cx="16.6" cy="12.4" r="4.6" fill="#1A1128"></circle><circle cx="7.4" cy="12.4" r="2.9" fill="#F5EDD6"></circle><circle cx="16.6" cy="12.4" r="2.9" fill="#F5EDD6"></circle><path d="M10.6 10.6 C11.4 10.1 12.6 10.1 13.4 10.6 L13.4 12 C12.6 11.5 11.4 11.5 10.6 12 Z" fill="#1A1128"></path><path d="M2.8 11 C2 11.2 1.4 11.8 1 12.4 L2 13.4 C2.4 12.9 2.8 12.6 3.4 12.5 Z" fill="#1A1128"></path><path d="M21.2 11 C22 11.2 22.6 11.8 23 12.4 L22 13.4 C21.6 12.9 21.2 12.6 20.6 12.5 Z" fill="#1A1128"></path>'},
    {"id": "neck", "name": "Neck", "icon_svg": '<path d="M3.6 7 C6 8 9 9.8 10.8 12 C9 14.2 6 16 3.6 17 C4.4 13.6 4.4 10.4 3.6 7 Z" fill="#E87EA1"></path><path d="M20.4 7 C18 8 15 9.8 13.2 12 C15 14.2 18 16 20.4 17 C19.6 13.6 19.6 10.4 20.4 7 Z" fill="#E87EA1"></path><path d="M10.2 9.4 C11.4 9 12.6 9 13.8 9.4 C14.2 10.8 14.2 13.2 13.8 14.6 C12.6 15 11.4 15 10.2 14.6 C9.8 13.2 9.8 10.8 10.2 9.4 Z" fill="#B85A36"></path>'},
    {"id": "held", "name": "Held", "icon_svg": '<path d="M5 13 C5 10 7 8 10 8 L14 8 C17 8 19 10 19 13 L19 15 C19 17.6 17 19 14 19 L10 19 C7 19 5 17.6 5 15 Z" fill="#8E87B8"></path><circle cx="12" cy="13.4" r="3.2" fill="#F5EDD6"></circle><path d="M9 8 L9 5.4 C9 4.4 9.8 3.8 10.8 3.8 L13.2 3.8 C14.2 3.8 15 4.4 15 5.4 L15 8 Z" fill="#3D2A85"></path>'},
    {"id": "shoes", "name": "Shoes", "icon_svg": '<path d="M6 5.6 C8.4 5 11 5.2 12.6 6 C13.4 8.4 14.4 10.4 15.4 12 C16 13 15 14 12.6 14.2 C9.4 14.6 6.6 14.4 5.4 13.8 C4.6 13.4 4.4 11.6 4.8 9.6 C5.2 7.8 5.4 6.6 6 5.6 Z" fill="#7EC8A4"></path><path d="M5.6 5.2 C8 4.6 11 4.8 12.8 5.6 L13.2 8 C11 7.2 8 7 5.8 7.6 Z" fill="#F2C94C"></path><path d="M4.2 12 C6.6 11.4 13 11.8 15.6 12.4 C16.2 13.6 15.2 14.6 12.6 14.8 C9.4 15.2 6.6 15 5.4 14.4 C4.6 14 4.2 13 4.2 12 Z" fill="#3F7C5C"></path><path d="M17.6 14 C19 14 20 14.6 20 15.6 C20 16.8 19 17.4 17.6 17.4 C16.2 17.4 15.2 16.8 15.2 15.6 C15.2 14.6 16.2 14 17.6 14 Z" fill="#8E87B8"></path>'},
]
