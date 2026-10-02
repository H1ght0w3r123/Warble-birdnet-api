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
        "tile_viewbox": "12.99 -0.74 74.31 74.31",
        "svg": '<image xlink:href="/static/accessories/glasses_round_wire_specs-v2.webp" href="/static/accessories/glasses_round_wire_specs-v2.webp" x="18.66" y="24.73" width="62.98" height="23.38"/>',
    },
    "black_browline": {
        "name": "Browline Glasses",
        "emoji": "🤓",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "11.48 -2.00 77.41 77.41",
        "svg": '<image xlink:href="/static/accessories/glasses_black_browline-v2.webp" href="/static/accessories/glasses_black_browline-v2.webp" x="17.38" y="25.78" width="65.6" height="21.87"/>',
    },
    "sunglasses": {
        "name": "Aviator Sunglasses",
        "emoji": "🕶️",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "11.66 -1.63 76.90 76.90",
        "svg": '<image xlink:href="/static/accessories/glasses_aviator_sunglasses-v2.webp" href="/static/accessories/glasses_aviator_sunglasses-v2.webp" x="17.53" y="24.79" width="65.17" height="24.05"/>',
    },
    "cat_eye": {
        "name": "Cat-Eye Glasses",
        "emoji": "😼",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "11.62 -2.03 77.04 77.04",
        "svg": '<image xlink:href="/static/accessories/glasses_cat_eye-v2.webp" href="/static/accessories/glasses_cat_eye-v2.webp" x="17.5" y="25.56" width="65.29" height="21.86"/>',
    },
    "heart_glasses": {
        "name": "Heart Glasses",
        "emoji": "💗",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "11.33 -0.92 77.55 77.55",
        "svg": '<image xlink:href="/static/accessories/glasses_heart_glasses-v2.webp" href="/static/accessories/glasses_heart_glasses-v2.webp" x="17.25" y="26.26" width="65.72" height="23.19"/>',
    },
    "movie_3d": {
        "name": "3D Movie Glasses",
        "emoji": "🎬",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "13.03 -0.65 74.22 74.22",
        "svg": '<image xlink:href="/static/accessories/glasses_movie_3d-v2.webp" href="/static/accessories/glasses_movie_3d-v2.webp" x="18.69" y="26.19" width="62.9" height="20.55"/>',
    },
    "star_glasses": {
        "name": "Star Glasses",
        "emoji": "⭐",
        "cost": 75,
        "category": "glasses",
        "tile_viewbox": "8.66 -8.32 84.91 84.91",
        "svg": '<image xlink:href="/static/accessories/glasses_star_glasses-v2.webp" href="/static/accessories/glasses_star_glasses-v2.webp" x="15.13" y="19.72" width="71.96" height="28.82"/>',
    },
    "explorer_goggles": {
        "name": "Explorer Goggles",
        "emoji": "🥽",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "4.70 -9.15 91.01 91.01",
        "svg": '<image xlink:href="/static/accessories/glasses_explorer_goggles-v2.webp" href="/static/accessories/glasses_explorer_goggles-v2.webp" x="11.64" y="22.18" width="77.12" height="28.35"/>',
    },
    "monocle": {
        "name": "Monocle",
        "emoji": "🧐",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "47.66 2.99 68.01 68.01",
        "svg": '<image xlink:href="/static/accessories/glasses_monocle-v2.webp" href="/static/accessories/glasses_monocle-v2.webp" x="52.85" y="23.45" width="57.64" height="27.09"/>',
    },
    "rainbow_holo": {
        "name": "Rainbow Holo Sunglasses",
        "emoji": "🌈",
        "cost": 75,
        "category": "glasses",
        "tile_viewbox": "12.51 -0.86 75.19 75.19",
        "svg": '<image xlink:href="/static/accessories/glasses_rainbow_holo-v2.webp" href="/static/accessories/glasses_rainbow_holo-v2.webp" x="18.24" y="25.77" width="63.72" height="21.93"/>',
    },
    "teal_specs": {
        "name": "Teal Specs",
        "emoji": "👓",
        "cost": 5,
        "category": "glasses",
        "tile_viewbox": "10.94 -2.54 78.50 78.50",
        "svg": '<image xlink:href="/static/accessories/glasses_teal_specs-v2.webp" href="/static/accessories/glasses_teal_specs-v2.webp" x="16.92" y="23.87" width="66.52" height="25.69"/>',
    },
    "shutter_shades": {
        "name": "Shutter Shades",
        "emoji": "😎",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "9.23 -3.89 81.61 81.61",
        "svg": '<image xlink:href="/static/accessories/glasses_shutter_shades-v2.webp" href="/static/accessories/glasses_shutter_shades-v2.webp" x="15.46" y="24.55" width="69.16" height="24.72"/>',
    },
    "pixel_shades": {
        "name": "Pixel Shades",
        "emoji": "😎",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "11.80 -2.00 76.91 76.91",
        "svg": '<image xlink:href="/static/accessories/glasses_pixel_shades-v2.webp" href="/static/accessories/glasses_pixel_shades-v2.webp" x="17.67" y="27.77" width="65.18" height="17.36"/>',
    },
    "daisy_glasses": {
        "name": "Daisy Glasses",
        "emoji": "🌼",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "9.30 -4.34 81.64 81.64",
        "svg": '<image xlink:href="/static/accessories/glasses_daisy_glasses-v2.webp" href="/static/accessories/glasses_daisy_glasses-v2.webp" x="15.52" y="21.94" width="69.19" height="29.09"/>',
    },
    "pineapple_glasses": {
        "name": "Pineapple Glasses",
        "emoji": "🍍",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "11.59 -3.78 76.82 76.82",
        "svg": '<image xlink:href="/static/accessories/glasses_pineapple_glasses-v2.webp" href="/static/accessories/glasses_pineapple_glasses-v2.webp" x="17.45" y="20.05" width="65.1" height="29.16"/>',
    },
    "flower_glasses": {
        "name": "Flower Glasses",
        "emoji": "🌸",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "4.24 -11.72 92.32 92.32",
        "svg": '<image xlink:href="/static/accessories/glasses_flower_glasses-v2.webp" href="/static/accessories/glasses_flower_glasses-v2.webp" x="11.28" y="18.68" width="78.24" height="31.52"/>',
    },
    "lightning_glasses": {
        "name": "Lightning Glasses",
        "emoji": "⚡",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "11.11 -0.69 76.71 76.71",
        "svg": '<image xlink:href="/static/accessories/glasses_lightning_glasses-v2.webp" href="/static/accessories/glasses_lightning_glasses-v2.webp" x="16.96" y="26.01" width="65.01" height="23.3"/>',
    },
    "butterfly_glasses": {
        "name": "Butterfly Glasses",
        "emoji": "🦋",
        "cost": 75,
        "category": "glasses",
        "tile_viewbox": "14.77 0.63 70.61 70.61",
        "svg": '<image xlink:href="/static/accessories/glasses_butterfly_glasses-v2.webp" href="/static/accessories/glasses_butterfly_glasses-v2.webp" x="20.15" y="23.52" width="59.84" height="24.83"/>',
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
    # icon_img is a silhouette generated from that category's first item
    # (cheapest, alphabetical tiebreak - same ordering the carousel itself
    # uses), rather than a hand-drawn icon, so the selector always shows
    # something that's actually in the category.
    {"id": "hats", "name": "Hats", "icon_img": "/static/cat-icon-hats-v1.webp"},
    {"id": "glasses", "name": "Glasses", "icon_img": "/static/cat-icon-glasses-v1.webp"},
    {"id": "neck", "name": "Neck", "icon_img": "/static/cat-icon-neck-v1.webp"},
    {"id": "held", "name": "Held", "icon_img": "/static/cat-icon-held-v1.webp"},
    {"id": "shoes", "name": "Shoes", "icon_img": "/static/cat-icon-shoes-v1.webp"},
]
