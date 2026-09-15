"""
Dress Up catalog - 47 items across 6 categories, real design art
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
        "tile_viewbox": "26 -3 48 34",
        "svg": '<g transform="rotate(-8 50 26)"><image xlink:href="/static/accessories/hat_top_hat.webp" href="/static/accessories/hat_top_hat.webp" x="28.21" y="-1" width="43.57" height="28"/></g>',
    },
    "golden_crown": {
        "name": "Golden Crown",
        "emoji": "👑",
        "cost": 75,
        "category": "hats",
        "tile_viewbox": "25 -3 50 34",
        "svg": '<g transform="rotate(6 50 26)"><image xlink:href="/static/accessories/hat_golden_crown.webp" href="/static/accessories/hat_golden_crown.webp" x="26.87" y="-1" width="46.26" height="28"/></g>',
    },
    "flower_crown": {
        "name": "Flower Crown",
        "emoji": "🌸",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "15 -3 70 34",
        "svg": '<g transform="rotate(-5 50 26)"><image xlink:href="/static/accessories/hat_flower_crown.webp" href="/static/accessories/hat_flower_crown.webp" x="17.41" y="-1" width="65.17" height="28"/></g>',
    },
    "deerstalker_hat": {
        "name": "Deerstalker Hat",
        "emoji": "🔍",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "25 -3 50 34",
        "svg": '<g transform="rotate(-6 50 26)"><image xlink:href="/static/accessories/hat_deerstalker_hat.webp" href="/static/accessories/hat_deerstalker_hat.webp" x="27.68" y="-1" width="44.64" height="28"/></g>',
    },
    "baseball_cap": {
        "name": "Baseball Cap",
        "emoji": "🧢",
        "cost": 10,
        "category": "hats",
        "tile_viewbox": "27 -3 46 34",
        "svg": '<g transform="rotate(-9 50 26)"><image xlink:href="/static/accessories/hat_baseball_cap.webp" href="/static/accessories/hat_baseball_cap.webp" x="29.79" y="-1" width="40.42" height="28"/></g>',
    },
    "sun_hat": {
        "name": "Sun Hat",
        "emoji": "👒",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "18 -3 64 34",
        "svg": '<g transform="rotate(5 50 26)"><image xlink:href="/static/accessories/hat_sun_hat.webp" href="/static/accessories/hat_sun_hat.webp" x="20.5" y="-1" width="59" height="28"/></g>',
    },
    "party_hat": {
        "name": "Party Hat",
        "emoji": "🥳",
        "cost": 10,
        "category": "hats",
        "tile_viewbox": "36 -3 28 34",
        "svg": '<g transform="rotate(9 50 26)"><image xlink:href="/static/accessories/hat_party_hat.webp" href="/static/accessories/hat_party_hat.webp" x="38.25" y="-1" width="23.5" height="28"/></g>',
    },
    "wizard_hat": {
        "name": "Wizard Hat",
        "emoji": "🧙",
        "cost": 75,
        "category": "hats",
        "tile_viewbox": "27 -3 46 34",
        "svg": '<g transform="rotate(-7 50 26)"><image xlink:href="/static/accessories/hat_wizard_hat.webp" href="/static/accessories/hat_wizard_hat.webp" x="29.64" y="-1" width="40.73" height="28"/></g>',
    },
    "pirate_hat": {
        "name": "Pirate Hat",
        "emoji": "🏴",
        "cost": 40,
        "category": "hats",
        "tile_viewbox": "24 -3 52 34",
        "svg": '<g transform="rotate(8 50 26)"><image xlink:href="/static/accessories/hat_pirate_hat.webp" href="/static/accessories/hat_pirate_hat.webp" x="26.61" y="-1" width="46.78" height="28"/></g>',
    },
    "explorer_helmet": {
        "name": "Explorer Helmet",
        "emoji": "🪖",
        "cost": 40,
        "category": "hats",
        "tile_viewbox": "26 -3 48 34",
        "svg": '<g transform="rotate(-6 50 26)"><image xlink:href="/static/accessories/hat_explorer_helmet.webp" href="/static/accessories/hat_explorer_helmet.webp" x="27.96" y="-1" width="44.07" height="28"/></g>',
    },
    "ski_hat": {
        "name": "Ski Hat",
        "emoji": "🎿",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "34 -3 32 34",
        "svg": '<g transform="rotate(7 50 26)"><image xlink:href="/static/accessories/hat_ski_hat.webp" href="/static/accessories/hat_ski_hat.webp" x="35.83" y="-1" width="28.35" height="28"/></g>',
    },
    "cozy_beanie": {
        "name": "Cozy Beanie",
        "emoji": "🧶",
        "cost": 10,
        "category": "hats",
        "tile_viewbox": "34 -3 32 34",
        "svg": '<g transform="rotate(-4 50 26)"><image xlink:href="/static/accessories/hat_cozy_beanie.webp" href="/static/accessories/hat_cozy_beanie.webp" x="35.77" y="-1" width="28.47" height="28"/></g>',
    },
    "cosy_scarf": {
        "name": "Cosy Scarf",
        "emoji": "🧣",
        "cost": 10,
        "category": "neck",
        "tile_viewbox": "28 63 50 38",
        "svg": '<path d="M29.5 66 C35.5 72.6 43 75.6 50 75.6 C57 75.6 64.5 72.6 70.5 66 C71.4 73 64.5 82.6 50 82.6 C35.5 82.6 28.6 73 29.5 66 Z" fill="#E87EA1"></path><path d="M61.6 71.6 C65 70 68.2 67.8 70.5 65.6 C71.4 69.6 70.8 74 68.6 78.4 C66 80.4 63.2 81.6 60.6 82.4 C61.2 78.6 61.4 75 61.6 71.6 Z" fill="#E87EA1"></path><path d="M33 70.6 C35.4 73.2 38.2 75.2 41 76.4 L40 80.8 C36.8 79.4 33.8 77 31.4 74 Z" fill="#1A1128" opacity="0.12"></path><path d="M43.4 77 C45.8 77.6 48 77.8 50 77.8 L50 82.2 C47.4 82.2 44.8 81.8 42.4 81.2 Z" fill="#1A1128" opacity="0.12"></path><path d="M52 77.8 C54.2 77.6 56.4 77.2 58.4 76.6 L59.4 81 C57 81.7 54.6 82.2 52 82.2 Z" fill="#1A1128" opacity="0.12"></path><path d="M60.6 76 C63.4 74.6 66 72.6 68 70.2 L69.4 74 C67.4 76.8 64.6 79 61.6 80.4 Z" fill="#1A1128" opacity="0.12"></path><path d="M31.4 76.6 C36.6 81 43 83 50 83 C57 83 63.4 81 68.6 76.6 C66.6 80.6 60 84.6 50 84.6 C40 84.6 33.4 80.6 31.4 76.6 Z" fill="#B85A36"></path><path d="M59.6 79.6 C63.6 78.4 67.4 77 70.6 75.4 C72.6 80.6 74 86.4 74.6 91.6 C71 93 67.4 94 63.8 94.6 C62.6 89.4 61.4 84.4 59.6 79.6 Z" fill="#E87EA1"></path><path d="M67 92.8 C69.6 92.2 72.2 91.4 74.6 91.6 C74 86.4 72.6 80.6 70.6 75.4 C69.4 76 68.2 76.6 67 77.2 C68.6 82.2 69.4 87.4 67 92.8 Z" fill="#1A1128" opacity="0.14"></path><path d="M63.8 94.6 L66 94.2 L66.6 98.4 L64.6 98.6 Z" fill="#B85A36"></path><path d="M67.6 93.8 L69.8 93.2 L70.8 97.4 L68.8 97.8 Z" fill="#B85A36"></path><path d="M71.4 92.6 L73.6 92 L75 96 L73 96.6 Z" fill="#B85A36"></path>',
    },
    "fancy_bow": {
        "name": "Fancy Bow",
        "emoji": "🎀",
        "cost": 5,
        "category": "neck",
        "tile_viewbox": "28 65 44 26",
        "svg": '<path d="M46 73.6 C42 68.4 34.6 67.4 31.6 70.6 C28.6 73.8 31.6 79.4 37.6 79.6 C41 79.7 44.4 77.6 46 74.6 Z" fill="#E87EA1"></path><path d="M54 73.6 C58 68.4 65.4 67.4 68.4 70.6 C71.4 73.8 68.4 79.4 62.4 79.6 C59 79.7 55.6 77.6 54 74.6 Z" fill="#E87EA1"></path><path d="M46 74.6 C43.6 76.4 40.4 78 37 78.6 C40.6 76.6 43.4 74.6 45.4 72.6 Z" fill="#1A1128" opacity="0.2"></path><path d="M54 74.6 C56.4 76.4 59.6 78 63 78.6 C59.4 76.6 56.6 74.6 54.6 72.6 Z" fill="#1A1128" opacity="0.2"></path><path d="M47.4 76.6 C46.2 80.6 44 84.6 41 87.6 C43.6 87 46 85.6 48 83.6 Z" fill="#E87EA1"></path><path d="M52.6 76.6 C53.8 80.6 56 84.6 59 87.6 C56.4 87 54 85.6 52 83.6 Z" fill="#E87EA1"></path><path d="M44.6 71.4 C46 70.8 47.4 70.6 48.6 70.6 L48.6 77.4 C47.4 77.4 46 77.2 44.6 76.6 Z" fill="#E87EA1"></path><path d="M55.4 71.4 C54 70.8 52.6 70.6 51.4 70.6 L51.4 77.4 C52.6 77.4 54 77.2 55.4 76.6 Z" fill="#E87EA1"></path><path d="M46.4 70.6 C48.8 69.6 51.2 69.6 53.6 70.6 C54.6 72.4 54.6 75.4 53.6 77.4 C51.2 78.4 48.8 78.4 46.4 77.4 C45.4 75.4 45.4 72.4 46.4 70.6 Z" fill="#E87EA1"></path><path d="M52 70 C54 71.4 54.8 74 54.4 77.6 C53.6 78.2 52.6 78.4 51.4 78.4 C52.6 75.6 52.8 72.6 52 70 Z" fill="#1A1128" opacity="0.2"></path>',
    },
    "bow_tie": {
        "name": "Bow Tie",
        "emoji": "🎗️",
        "cost": 5,
        "category": "neck",
        "tile_viewbox": "32 64 36 20",
        "svg": '<path d="M35 66.6 C39.4 68 44.4 70.4 47.6 73.4 C44.4 76.4 39.4 78.8 35 80.2 C36.2 76 36.2 70.8 35 66.6 Z" fill="#2D1B69"></path><path d="M65 66.6 C60.6 68 55.6 70.4 52.4 73.4 C55.6 76.4 60.6 78.8 65 80.2 C63.8 76 63.8 70.8 65 66.6 Z" fill="#2D1B69"></path><path d="M35 73.4 C38.6 75 43.4 77.2 47.6 73.4 C44.4 76.4 39.4 78.8 35 80.2 C35.6 78 35.8 75.6 35 73.4 Z" fill="#1A1128" opacity="0.25"></path><path d="M65 73.4 C61.4 75 56.6 77.2 52.4 73.4 C55.6 76.4 60.6 78.8 65 80.2 C64.4 78 64.2 75.6 65 73.4 Z" fill="#1A1128" opacity="0.25"></path><path d="M46.6 69.6 C48.8 68.8 51.2 68.8 53.4 69.6 C54.2 71.8 54.2 75 53.4 77.2 C51.2 78 48.8 78 46.6 77.2 C45.8 75 45.8 71.8 46.6 69.6 Z" fill="#3D2A85"></path><path d="M50 68.9 L50 77.9 L48.6 77.7 L48.6 69 Z" fill="#1A1128" opacity="0.2"></path>',
    },
    "beaded_necklace": {
        "name": "Beaded Necklace",
        "emoji": "📿",
        "cost": 10,
        "category": "neck",
        "tile_viewbox": "30 63 40 21",
        "svg": '<path d="M32.6 66 C35.4 72.8 42.2 78.4 50 80.2 C57.8 78.4 64.6 72.8 67.4 66 C67.4 71.8 62.8 77.8 56.8 81 C52 83.4 48 83.4 43.2 81 C37.2 77.8 32.6 71.8 32.6 66 Z" fill="#8E87B8"></path><circle cx="34" cy="68" r="2.4" fill="#7EC8A4"></circle><circle cx="37.4" cy="72" r="2.6" fill="#F2C94C"></circle><circle cx="41" cy="75.2" r="2.8" fill="#E87EA1"></circle><circle cx="45.2" cy="77.6" r="3" fill="#7EC8A4"></circle><circle cx="50" cy="78.8" r="3.2" fill="#F2C94C"></circle><circle cx="54.8" cy="77.6" r="3" fill="#E87EA1"></circle><circle cx="59" cy="75.2" r="2.8" fill="#7EC8A4"></circle><circle cx="62.6" cy="72" r="2.6" fill="#F2C94C"></circle><circle cx="66" cy="68" r="2.4" fill="#E87EA1"></circle><circle cx="36.6" cy="71.2" r="0.85" fill="#F5EDD6" opacity="0.7"></circle><circle cx="44.2" cy="76.6" r="0.95" fill="#F5EDD6" opacity="0.7"></circle><circle cx="49" cy="77.9" r="1" fill="#F5EDD6" opacity="0.7"></circle><circle cx="61.8" cy="71.2" r="0.85" fill="#F5EDD6" opacity="0.7"></circle>',
    },
    "golden_medal": {
        "name": "Golden Medal",
        "emoji": "🏅",
        "cost": 75,
        "category": "neck",
        "tile_viewbox": "34 62 32 32",
        "svg": '<path d="M38.6 64.6 C41 64.6 43.4 64.6 45 65.4 C47.4 69.4 49.6 73.4 51.4 77.4 C49.8 78.6 48 79.4 46.4 79.6 C43.6 74.6 41 69.6 38.6 64.6 Z" fill="#E8845C"></path><path d="M61.4 64.6 C59 64.6 56.6 64.6 55 65.4 C52.6 69.4 50.4 73.4 48.6 77.4 C50.2 78.6 52 79.4 53.6 79.6 C56.4 74.6 59 69.6 61.4 64.6 Z" fill="#E8845C"></path><path d="M46.4 79.6 C48 79 50 78.6 52 78.6 C53.4 78.6 52.6 76.6 51.4 77.4 C49.8 78.4 48 79.2 46.4 79.6 Z" fill="#B85A36"></path><path d="M47.4 78.4 C48.4 77.4 51.6 77.4 52.6 78.4 C53.2 79.4 52.6 80.6 51.4 80.6 L48.6 80.6 C47.4 80.6 46.8 79.4 47.4 78.4 Z" fill="#B8901F"></path><circle cx="50" cy="84" r="7.4" fill="#B8901F"></circle><circle cx="50" cy="84" r="6" fill="#F2C94C"></circle><path d="M50 79.6 L51.6 82.6 L55 83.2 L52.6 85.6 L53.2 89 L50 87.4 L46.8 89 L47.4 85.6 L45 83.2 L48.4 82.6 Z" fill="#B8901F"></path><path d="M45.6 81.4 C46.8 79.8 48.6 78.8 50.6 78.6 C48.2 79.6 46.6 81 45.6 82.8 Z" fill="#F5EDD6" opacity="0.5"></path>',
    },
    "pearl_necklace": {
        "name": "Pearl Necklace",
        "emoji": "🤍",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "30 62 40 26",
        "svg": '<path d="M32.6 65.6 C35.4 72.4 42.2 78 50 79.8 C57.8 78 64.6 72.4 67.4 65.6 C67.4 71.4 62.8 77.4 56.8 80.6 C52 83 48 83 43.2 80.6 C37.2 77.4 32.6 71.4 32.6 65.6 Z" fill="#8E87B8"></path><circle cx="34" cy="67.4" r="2.2" fill="#F5EDD6"></circle><circle cx="37.2" cy="71.2" r="2.4" fill="#F5EDD6"></circle><circle cx="40.8" cy="74.4" r="2.5" fill="#F5EDD6"></circle><circle cx="44.8" cy="76.8" r="2.6" fill="#F5EDD6"></circle><circle cx="55.2" cy="76.8" r="2.6" fill="#F5EDD6"></circle><circle cx="59.2" cy="74.4" r="2.5" fill="#F5EDD6"></circle><circle cx="62.8" cy="71.2" r="2.4" fill="#F5EDD6"></circle><circle cx="66" cy="67.4" r="2.2" fill="#F5EDD6"></circle><path d="M47.8 77.4 C48.6 76.4 51.4 76.4 52.2 77.4 C52.8 78.2 52.2 79.4 51.2 79.4 L48.8 79.4 C47.8 79.4 47.2 78.2 47.8 77.4 Z" fill="#8E87B8"></path><circle cx="50" cy="82.6" r="3.6" fill="#F5EDD6"></circle><path d="M46.6 83.6 C47.4 85.8 49.6 86.8 52 86.2 C50.6 86.8 47.8 86.4 46.6 83.6 Z" fill="#8E87B8" opacity="0.5"></path><circle cx="48.6" cy="81.2" r="1.2" fill="#FFFFFF"></circle><circle cx="36.4" cy="70.4" r="0.75" fill="#FFFFFF" opacity="0.8"></circle><circle cx="44" cy="76.1" r="0.8" fill="#FFFFFF" opacity="0.8"></circle><circle cx="62" cy="70.4" r="0.75" fill="#FFFFFF" opacity="0.8"></circle>',
    },
    "striped_scarf": {
        "name": "Striped Scarf",
        "emoji": "🧣",
        "cost": 10,
        "category": "neck",
        "tile_viewbox": "28 63 50 38",
        "svg": '<path d="M29.5 66 C35.5 72.6 43 75.6 50 75.6 C57 75.6 64.5 72.6 70.5 66 C71.4 73 64.5 82.6 50 82.6 C35.5 82.6 28.6 73 29.5 66 Z" fill="#7EC8A4"></path><path d="M61.6 71.6 C65 70 68.2 67.8 70.5 65.6 C71.4 69.6 70.8 74 68.6 78.4 C66 80.4 63.2 81.6 60.6 82.4 C61.2 78.6 61.4 75 61.6 71.6 Z" fill="#7EC8A4"></path><path d="M30.4 71 C36 76 43 78.8 50 78.8 C57 78.8 64 76 69.6 71 C69.4 72.6 69 74 68.4 75.4 C63 79.4 56.6 81.4 50 81.4 C43.4 81.4 37 79.4 31.6 75.4 C31 74 30.6 72.6 30.4 71 Z" fill="#F5EDD6"></path><path d="M33.4 67.6 C39 71.4 44.6 73.2 50 73.2 C55.4 73.2 61 71.4 66.6 67.6 C66.4 68.8 66 69.9 65.4 71 C60.4 74 55.2 75.4 50 75.4 C44.8 75.4 39.6 74 34.6 71 C34 69.9 33.6 68.8 33.4 67.6 Z" fill="#F5EDD6" opacity="0.55"></path><path d="M31.4 77 C36.6 81.4 43 83.4 50 83.4 C57 83.4 63.4 81.4 68.6 77 C66.6 81 60 84.6 50 84.6 C40 84.6 33.4 81 31.4 77 Z" fill="#3F7C5C"></path><path d="M59.6 79.6 C63.6 78.4 67.4 77 70.6 75.4 C72.6 80.6 74 86.4 74.6 91.6 C71 93 67.4 94 63.8 94.6 C62.6 89.4 61.4 84.4 59.6 79.6 Z" fill="#7EC8A4"></path><path d="M61.6 84.6 L71.6 81.4 L72.6 85.4 L62.8 88.6 Z" fill="#F5EDD6"></path><path d="M63.4 90 L73.8 87 L74.4 90.6 L64.2 93.6 Z" fill="#F5EDD6" opacity="0.8"></path><path d="M63.8 94.6 L66 94.2 L66.6 98.4 L64.6 98.6 Z" fill="#3F7C5C"></path><path d="M67.6 93.8 L69.8 93.2 L70.8 97.4 L68.8 97.8 Z" fill="#3F7C5C"></path><path d="M71.4 92.6 L73.6 92 L75 96 L73 96.6 Z" fill="#3F7C5C"></path>',
    },
    "star_necklace": {
        "name": "Star Necklace",
        "emoji": "⭐",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "32 62 36 34",
        "svg": '<path d="M34.6 65.2 C37.4 71.4 43 76.4 50 78.4 C57 76.4 62.6 71.4 65.4 65.2 C65.6 70.6 61.6 76.2 55.6 79.4 C52 81.2 48 81.2 44.4 79.4 C38.4 76.2 34.4 70.6 34.6 65.2 Z" fill="#8E87B8"></path><path d="M47.8 76.8 C48.6 75.8 51.4 75.8 52.2 76.8 C52.8 77.6 52.2 78.8 51.2 78.8 L48.8 78.8 C47.8 78.8 47.2 77.6 47.8 76.8 Z" fill="#B8901F"></path><path d="M50 73.6 L52.8 80.2 L59.6 82.8 L52.8 85.4 L50 92 L47.2 85.4 L40.4 82.8 L47.2 80.2 Z" fill="#F2C94C"></path><path d="M50 73.6 L52.8 80.2 L59.6 82.8 L50 82.8 Z" fill="#FFFFFF" opacity="0.22"></path><path d="M50 92 L47.2 85.4 L40.4 82.8 L50 82.8 Z" fill="#B8901F" opacity="0.5"></path><circle cx="50" cy="82.8" r="1.6" fill="#B8901F"></circle>',
    },
    "explorer_backpack": {
        "name": "Explorer Backpack",
        "emoji": "🎒",
        "cost": 40,
        "category": "gear",
        "tile_viewbox": "13 54 74 38",
        "svg": '<path d="M15.4 61 C15.4 58.6 17 57 19.6 57 L26 57 C27.4 57 28 58 28 59.4 L28 73 C28 75 26.6 76 24.4 76 L19.6 76 C17 76 15.4 74.4 15.4 72 Z" fill="#7EC8A4"></path><path d="M24 57.4 C26.6 58 28 59 28 60.6 L28 73 C28 75 26.6 76 24.4 76 C25.4 74 25.6 71.6 25.4 68.6 C25 64.6 24.6 61 24 57.4 Z" fill="#3F7C5C"></path><path d="M84.6 61 C84.6 58.6 83 57 80.4 57 L74 57 C72.6 57 72 58 72 59.4 L72 73 C72 75 73.4 76 75.6 76 L80.4 76 C83 76 84.6 74.4 84.6 72 Z" fill="#7EC8A4"></path><path d="M76 57.4 C73.4 58 72 59 72 60.6 L72 73 C72 75 73.4 76 75.6 76 C74.6 74 74.4 71.6 74.6 68.6 C75 64.6 75.4 61 76 57.4 Z" fill="#3F7C5C"></path><path d="M37.6 61 C39.6 60.4 42.4 60.4 44.4 61 C45.4 69.6 46 78.6 46 87.6 C44 88.2 41.4 88.2 39.4 87.6 C39.4 78.6 38.6 69.6 37.6 61 Z" fill="#3F7C5C"></path><path d="M62.4 61 C60.4 60.4 57.6 60.4 55.6 61 C54.6 69.6 54 78.6 54 87.6 C56 88.2 58.6 88.2 60.6 87.6 C60.6 78.6 61.4 69.6 62.4 61 Z" fill="#3F7C5C"></path><path d="M43 60.6 C44 60.7 44.4 60.8 44.4 61 C45.4 69.6 46 78.6 46 87.6 C45.4 87.8 44.8 88 44.2 88 C44.2 78.6 43.6 69.4 43 60.6 Z" fill="#7EC8A4" opacity="0.5"></path><path d="M57 60.6 C56 60.7 55.6 60.8 55.6 61 C54.6 69.6 54 78.6 54 87.6 C54.6 87.8 55.2 88 55.8 88 C55.8 78.6 56.4 69.4 57 60.6 Z" fill="#7EC8A4" opacity="0.5"></path><path d="M39 71.6 L46 71.6 L46 76.4 L39 76.4 Z" fill="#F2C94C"></path><path d="M54 71.6 L61 71.6 L61 76.4 L54 76.4 Z" fill="#F2C94C"></path><path d="M41 73 L44 73 L44 75 L41 75 Z" fill="#B8901F"></path><path d="M56 73 L59 73 L59 75 L56 75 Z" fill="#B8901F"></path>',
    },
    "round_specs": {
        "name": "Round Wire Specs",
        "emoji": "👓",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "20 36 60 26",
        "svg": '<image xlink:href="/static/accessories/glasses_round_wire_specs.webp" href="/static/accessories/glasses_round_wire_specs.webp" x="22" y="39.29" width="56" height="21.42"/>',
    },
    "explorer_goggles": {
        "name": "Explorer Goggles",
        "emoji": "🥽",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "20 38 60 22",
        "svg": '<image xlink:href="/static/accessories/glasses_explorer_goggles.webp" href="/static/accessories/glasses_explorer_goggles.webp" x="22" y="39.98" width="56" height="20.04"/>',
    },
    "sunglasses": {
        "name": "Aviator Sunglasses",
        "emoji": "🕶️",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "20 37 60 24",
        "svg": '<image xlink:href="/static/accessories/glasses_aviator_sunglasses.webp" href="/static/accessories/glasses_aviator_sunglasses.webp" x="22" y="39.73" width="56" height="20.53"/>',
    },
    "star_glasses": {
        "name": "Star Glasses",
        "emoji": "⭐",
        "cost": 75,
        "category": "glasses",
        "tile_viewbox": "20 36 60 26",
        "svg": '<image xlink:href="/static/accessories/glasses_star_glasses.webp" href="/static/accessories/glasses_star_glasses.webp" x="22" y="39.15" width="56" height="21.7"/>',
    },
    "black_browline": {
        "name": "Browline Glasses",
        "emoji": "🤓",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "20 39 60 20",
        "svg": '<image xlink:href="/static/accessories/glasses_black_browline.webp" href="/static/accessories/glasses_black_browline.webp" x="22" y="41.14" width="56" height="17.72"/>',
    },
    "cat_eye": {
        "name": "Cat-Eye Glasses",
        "emoji": "😼",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "20 38 60 22",
        "svg": '<image xlink:href="/static/accessories/glasses_cat_eye.webp" href="/static/accessories/glasses_cat_eye.webp" x="22" y="40.77" width="56" height="18.45"/>',
    },
    "heart_glasses": {
        "name": "Heart Glasses",
        "emoji": "💗",
        "cost": 20,
        "category": "glasses",
        "tile_viewbox": "20 35 60 28",
        "svg": '<image xlink:href="/static/accessories/glasses_heart_glasses.webp" href="/static/accessories/glasses_heart_glasses.webp" x="22" y="40.12" width="56" height="19.77"/>',
    },
    "movie_3d": {
        "name": "3D Movie Glasses",
        "emoji": "🎬",
        "cost": 10,
        "category": "glasses",
        "tile_viewbox": "20 39 60 20",
        "svg": '<image xlink:href="/static/accessories/glasses_movie_3d.webp" href="/static/accessories/glasses_movie_3d.webp" x="22" y="40.95" width="56" height="18.1"/>',
    },
    "monocle": {
        "name": "Monocle",
        "emoji": "🧐",
        "cost": 40,
        "category": "glasses",
        "tile_viewbox": "48 38 36 22",
        "svg": '<image xlink:href="/static/accessories/glasses_monocle.webp" href="/static/accessories/glasses_monocle.webp" x="50" y="41.13" width="32" height="17.73"/>',
    },
    "rainbow_holo": {
        "name": "Rainbow Holo Sunglasses",
        "emoji": "🌈",
        "cost": 75,
        "category": "glasses",
        "tile_viewbox": "20 38 60 22",
        "svg": '<image xlink:href="/static/accessories/glasses_rainbow_holo.webp" href="/static/accessories/glasses_rainbow_holo.webp" x="22" y="40.8" width="56" height="18.41"/>',
    },
    "wellies": {
        "name": "Wellies",
        "emoji": "👢",
        "cost": 10,
        "category": "shoes",
        "tile_viewbox": "33 84 34 17",
        "svg": '<path d="M38.4 87.4 C41.6 86.8 45 86.8 47.4 87.4 C47.8 90.6 48 93.6 48 96.2 C48 98.6 46 99.8 42.6 99.8 C38.6 99.8 36.4 98.6 36.4 96.2 C36.6 93.2 37.4 90.2 38.4 87.4 Z" fill="#7EC8A4"></path><path d="M61.6 87.4 C58.4 86.8 55 86.8 52.6 87.4 C52.2 90.6 52 93.6 52 96.2 C52 98.6 54 99.8 57.4 99.8 C61.4 99.8 63.6 98.6 63.6 96.2 C63.4 93.2 62.6 90.2 61.6 87.4 Z" fill="#7EC8A4"></path><path d="M38 86.6 C41.4 85.8 45 85.8 47.8 86.6 L48.2 89.6 C45 88.8 41.2 88.8 38 89.6 Z" fill="#F2C94C"></path><path d="M62 86.6 C58.6 85.8 55 85.8 52.2 86.6 L51.8 89.6 C55 88.8 58.8 88.8 62 89.6 Z" fill="#F2C94C"></path><path d="M44.4 87.2 C46 87.3 47 87.4 47.4 87.6 C47.8 90.8 48 93.6 48 96.2 C48 97.6 47.4 98.6 46.2 99.2 C46.8 96.6 46.6 93.6 46 90.4 C45.6 89.2 45 88.1 44.4 87.2 Z" fill="#1A1128" opacity="0.16"></path><path d="M55.6 87.2 C54 87.3 53 87.4 52.6 87.6 C52.2 90.8 52 93.6 52 96.2 C52 97.6 52.6 98.6 53.8 99.2 C53.2 96.6 53.4 93.6 54 90.4 C54.4 89.2 55 88.1 55.6 87.2 Z" fill="#1A1128" opacity="0.16"></path><path d="M36.4 96.4 C39.6 95.8 45 95.8 48 96.4 C48 98.8 46 99.9 42.4 99.9 C38.6 99.9 36.4 98.8 36.4 96.4 Z" fill="#3F7C5C"></path><path d="M63.6 96.4 C60.4 95.8 55 95.8 52 96.4 C52 98.8 54 99.9 57.6 99.9 C61.4 99.9 63.6 98.8 63.6 96.4 Z" fill="#3F7C5C"></path>',
    },
    "trainers": {
        "name": "Trainers",
        "emoji": "👟",
        "cost": 20,
        "category": "shoes",
        "tile_viewbox": "33 85 34 16",
        "svg": '<path d="M37 88.2 C40.4 87.6 44.4 87.8 46.6 88.8 C47.6 91.6 48.4 94 49.4 96 C50 97.2 49 98.4 46.6 98.6 C42 99 38 98.8 36.4 98 C35.2 97.4 35 95.4 35.4 93.2 C35.8 91.2 36.4 89.6 37 88.2 Z" fill="#F5EDD6"></path><path d="M63 88.2 C59.6 87.6 55.6 87.8 53.4 88.8 C52.4 91.6 51.6 94 50.6 96 C50 97.2 51 98.4 53.4 98.6 C58 99 62 98.8 63.6 98 C64.8 97.4 65 95.4 64.6 93.2 C64.2 91.2 63.6 89.6 63 88.2 Z" fill="#F5EDD6"></path><path d="M38.2 91.6 C41.4 92.8 44.6 94.8 47.4 97.2 L48.8 94.6 C46 92.4 42.6 90.4 39 89.2 Z" fill="#E8845C"></path><path d="M61.8 91.6 C58.6 92.8 55.4 94.8 52.6 97.2 L51.2 94.6 C54 92.4 57.4 90.4 61 89.2 Z" fill="#E8845C"></path><path d="M38.8 88.6 L45 89.8 L44.6 91.2 L38.4 90 Z" fill="#C4BFDF"></path><path d="M61.2 88.6 L55 89.8 L55.4 91.2 L61.6 90 Z" fill="#C4BFDF"></path><path d="M35.2 96.2 C38.6 95.6 45.6 96 49.2 96.8 C49.8 97.8 49 98.8 46.6 99 C42 99.4 38 99.2 36.4 98.4 C35.4 98 35.1 97.2 35.2 96.2 Z" fill="#1A1128"></path><path d="M64.8 96.2 C61.4 95.6 54.4 96 50.8 96.8 C50.2 97.8 51 98.8 53.4 99 C58 99.4 62 99.2 63.6 98.4 C64.6 98 64.9 97.2 64.8 96.2 Z" fill="#1A1128"></path>',
    },
    "hiking_boots": {
        "name": "Hiking Boots",
        "emoji": "🥾",
        "cost": 40,
        "category": "shoes",
        "tile_viewbox": "33 84 34 17",
        "svg": '<path d="M37.6 86.8 C41 86.2 44.8 86.4 47 87.4 C47.6 90.8 48.4 93.8 49.2 96.2 C49.8 97.6 48.6 98.8 46 99 C41.6 99.4 37.6 99.2 36 98.4 C34.8 97.8 34.6 95.4 35.2 92.6 C35.8 90.2 36.6 88.2 37.6 86.8 Z" fill="#B85A36"></path><path d="M62.4 86.8 C59 86.2 55.2 86.4 53 87.4 C52.4 90.8 51.6 93.8 50.8 96.2 C50.2 97.6 51.4 98.8 54 99 C58.4 99.4 62.4 99.2 64 98.4 C65.2 97.8 65.4 95.4 64.8 92.6 C64.2 90.2 63.4 88.2 62.4 86.8 Z" fill="#B85A36"></path><path d="M37.2 86.4 C40.6 85.6 44.6 85.8 47.4 86.8 L47.8 89.2 C44.6 88.2 40.6 88 37.4 88.8 Z" fill="#E9DDBE"></path><path d="M62.8 86.4 C59.4 85.6 55.4 85.8 52.6 86.8 L52.2 89.2 C55.4 88.2 59.4 88 62.6 88.8 Z" fill="#E9DDBE"></path><path d="M38.6 90.2 L45.6 91.8 L45.2 93.2 L38.2 91.6 Z" fill="#F5EDD6"></path><path d="M39 93.4 L46.4 95 L46 96.4 L38.6 94.8 Z" fill="#F5EDD6"></path><path d="M61.4 90.2 L54.4 91.8 L54.8 93.2 L61.8 91.6 Z" fill="#F5EDD6"></path><path d="M61 93.4 L53.6 95 L54 96.4 L61.4 94.8 Z" fill="#F5EDD6"></path><path d="M34.8 95.6 C38.4 95 46 95.4 49.6 96.2 C50.2 97.8 48.8 99 46 99.2 C41.6 99.6 37.6 99.4 36 98.6 C35 98.2 34.7 96.8 34.8 95.6 Z" fill="#1A1128"></path><path d="M65.2 95.6 C61.6 95 54 95.4 50.4 96.2 C49.8 97.8 51.2 99 54 99.2 C58.4 99.6 62.4 99.4 64 98.6 C65 98.2 65.3 96.8 65.2 95.6 Z" fill="#1A1128"></path><path d="M37.4 99.2 L37.4 96.6 L39.4 96.6 L39.4 99.2 Z" fill="#F5EDD6" opacity="0.28"></path><path d="M42.6 99.4 L42.6 96.8 L44.6 96.8 L44.6 99.4 Z" fill="#F5EDD6" opacity="0.28"></path><path d="M60.6 99.2 L60.6 96.6 L62.6 96.6 L62.6 99.2 Z" fill="#F5EDD6" opacity="0.28"></path><path d="M55.4 99.4 L55.4 96.8 L57.4 96.8 L57.4 99.4 Z" fill="#F5EDD6" opacity="0.28"></path>',
    },
    "roller_skates": {
        "name": "Roller Skates",
        "emoji": "🛼",
        "cost": 75,
        "category": "shoes",
        "tile_viewbox": "33 84 34 18",
        "svg": '<path d="M38 86.8 C41.4 86.2 45 86.4 47.4 87.2 C47.8 90.2 48 92.8 48 94.8 L36.4 94.8 C36.6 91.8 37.2 89 38 86.8 Z" fill="#C4BFDF"></path><path d="M62 86.8 C58.6 86.2 55 86.4 52.6 87.2 C52.2 90.2 52 92.8 52 94.8 L63.6 94.8 C63.4 91.8 62.8 89 62 86.8 Z" fill="#C4BFDF"></path><path d="M37.4 89.8 C41 89 44.8 89 48 89.8 L48 92 C44.8 91.2 41 91.2 37.2 92 Z" fill="#E87EA1"></path><path d="M62.6 89.8 C59 89 55.2 89 52 89.8 L52 92 C55.2 91.2 59 91.2 62.8 92 Z" fill="#E87EA1"></path><path d="M44.6 87 C46.2 87.1 47.2 87.2 47.4 87.4 C47.8 90.4 48 92.8 48 94.8 L46 94.8 C46 92.4 45.6 89.6 44.6 87 Z" fill="#1A1128" opacity="0.14"></path><path d="M55.4 87 C53.8 87.1 52.8 87.2 52.6 87.4 C52.2 90.4 52 92.8 52 94.8 L54 94.8 C54 92.4 54.4 89.6 55.4 87 Z" fill="#1A1128" opacity="0.14"></path><path d="M35.4 94.6 C39 94 45.6 94 49 94.6 L49 96.6 C45.6 97.2 39 97.2 35.4 96.6 Z" fill="#8E87B8"></path><path d="M64.6 94.6 C61 94 54.4 94 51 94.6 L51 96.6 C54.4 97.2 61 97.2 64.6 96.6 Z" fill="#8E87B8"></path><circle cx="38.4" cy="98.2" r="2.3" fill="#F2C94C"></circle><circle cx="46" cy="98.2" r="2.3" fill="#F2C94C"></circle><circle cx="54" cy="98.2" r="2.3" fill="#F2C94C"></circle><circle cx="61.6" cy="98.2" r="2.3" fill="#F2C94C"></circle><circle cx="38.4" cy="98.2" r="0.95" fill="#B8901F"></circle><circle cx="46" cy="98.2" r="0.95" fill="#B8901F"></circle><circle cx="54" cy="98.2" r="0.95" fill="#B8901F"></circle><circle cx="61.6" cy="98.2" r="0.95" fill="#B8901F"></circle>',
    },
    "ice_cream": {
        "name": "Ice Cream",
        "emoji": "🍦",
        "cost": 10,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><path d="M73.5 65 L86.5 65 L80 83 Z" fill="#D9A441"></path><path d="M73.5 65 L86.5 65 L80 83 Z" fill="#1A1128" opacity="0.12"></path><circle cx="76.3" cy="61.5" r="5.2" fill="#E87EA1"></circle><circle cx="83.7" cy="61.5" r="5.2" fill="#F5EDD6"></circle><circle cx="80" cy="56.5" r="5.4" fill="#7EC8A4"></circle></g>',
    },
    "walkie_talkie": {
        "name": "Walkie Talkie",
        "emoji": "📻",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><rect x="72.5" y="58" width="15" height="24" rx="2.5" fill="#2D1B69"></rect><rect x="75.5" y="61" width="9" height="6" rx="1" fill="#7EC8A4"></rect><circle cx="77.5" cy="72" r="1.7" fill="#C4BFDF"></circle><circle cx="82.5" cy="72" r="1.7" fill="#C4BFDF"></circle><circle cx="77.5" cy="77" r="1.7" fill="#C4BFDF"></circle><circle cx="82.5" cy="77" r="1.7" fill="#C4BFDF"></circle><rect x="83" y="48" width="2.6" height="11" rx="1.3" fill="#1A1128"></rect></g>',
    },
    "microphone": {
        "name": "Microphone",
        "emoji": "🎤",
        "cost": 75,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><rect x="78.4" y="65" width="3.2" height="18" rx="1.6" fill="#2B2B2B"></rect><circle cx="80" cy="60.5" r="7.2" fill="#8E87B8"></circle><circle cx="80" cy="60.5" r="4.8" fill="#C4BFDF"></circle><rect x="76" y="81" width="8" height="3.2" rx="1.6" fill="#1A1128"></rect></g>',
    },
    "lollipop": {
        "name": "Lollipop",
        "emoji": "🍭",
        "cost": 5,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><rect x="78.8" y="63" width="2.6" height="20" rx="1.3" fill="#F5EDD6"></rect><circle cx="80" cy="59.5" r="8.2" fill="#E87EA1"></circle><circle cx="80" cy="59.5" r="5.4" fill="#F5EDD6"></circle><circle cx="80" cy="59.5" r="2.7" fill="#E87EA1"></circle></g>',
    },
    "drumsticks": {
        "name": "Drumsticks",
        "emoji": "🥁",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><g transform="rotate(-11 75.5 69)"><rect x="74" y="57" width="3" height="26" rx="1.5" fill="#D9A441"></rect><circle cx="75.5" cy="56" r="2.8" fill="#B8901F"></circle></g><g transform="rotate(11 84.5 69)"><rect x="83" y="57" width="3" height="26" rx="1.5" fill="#D9A441"></rect><circle cx="84.5" cy="56" r="2.8" fill="#B8901F"></circle></g></g>',
    },
    "magnifying_glass": {
        "name": "Magnifying Glass",
        "emoji": "🔍",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><circle cx="80" cy="60" r="7.6" fill="#C4BFDF" opacity="0.55"></circle><circle cx="80" cy="60" r="7.6" fill="none" stroke="#8B5A2B" stroke-width="3"></circle><rect x="78.5" y="67" width="3" height="16" rx="1.5" fill="#8B5A2B"></rect></g>',
    },
    "water_bottle": {
        "name": "Water Bottle",
        "emoji": "🍶",
        "cost": 5,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><rect x="76" y="51" width="8" height="5.5" rx="1.5" fill="#3F7C5C"></rect><rect x="74" y="56" width="12" height="27" rx="3.5" fill="#7EC8A4"></rect><rect x="74" y="64" width="12" height="6.5" fill="#F5EDD6"></rect><rect x="76.4" y="59" width="2.5" height="20" rx="1.2" fill="#FFFFFF" opacity="0.35"></rect></g>',
    },
    "binoculars": {
        "name": "Binoculars",
        "emoji": "🔭",
        "cost": 75,
        "category": "gear",
        "tile_viewbox": "38 42 32 42",
        "svg": '<path d="M42 47 L56 65 L66 47" fill="none" stroke="#3D2A85" stroke-width="2.5" stroke-linecap="round"></path><rect x="47.5" y="63" width="17" height="12.5" rx="2.2" fill="#2D1B69"></rect><circle cx="51.5" cy="69.2" r="3.6" fill="#1A1128"></circle><circle cx="60.5" cy="69.2" r="3.6" fill="#1A1128"></circle><circle cx="51.5" cy="69.2" r="2" fill="#5B93C4"></circle><circle cx="60.5" cy="69.2" r="2" fill="#5B93C4"></circle>',
    },
    "camera": {
        "name": "Camera",
        "emoji": "📷",
        "cost": 75,
        "category": "gear",
        "tile_viewbox": "38 42 32 42",
        "svg": '<path d="M42 47 L56 65 L66 47" fill="none" stroke="#2B2B2B" stroke-width="2.5" stroke-linecap="round"></path><rect x="46.5" y="63" width="19" height="13.5" rx="2.5" fill="#2B2B2B"></rect><circle cx="56" cy="69.8" r="4.8" fill="#5B93C4"></circle><circle cx="56" cy="69.8" r="2.5" fill="#1A1128"></circle><rect x="61" y="60.2" width="4.2" height="3.2" rx="1" fill="#2B2B2B"></rect>',
    },
    "compass": {
        "name": "Compass",
        "emoji": "🧭",
        "cost": 40,
        "category": "gear",
        "tile_viewbox": "38 42 32 42",
        "svg": '<path d="M42 47 L56 65 L66 47" fill="none" stroke="#8B5A2B" stroke-width="2.5" stroke-linecap="round"></path><circle cx="56" cy="69.5" r="8.2" fill="#F5EDD6"></circle><circle cx="56" cy="69.5" r="8.2" fill="none" stroke="#8B5A2B" stroke-width="2"></circle><path d="M56 63 L58.6 69.5 L56 76 L53.4 69.5 Z" fill="#C0392B"></path>',
    },
    "field_notebook": {
        "name": "Field Notebook",
        "emoji": "📓",
        "cost": 10,
        "category": "gear",
        "tile_viewbox": "38 42 32 42",
        "svg": '<path d="M42 47 L56 65 L66 47" fill="none" stroke="#8B5A2B" stroke-width="2.5" stroke-linecap="round"></path><rect x="48" y="63" width="16" height="17.5" rx="1.5" fill="#F5EDD6"></rect><rect x="48" y="63" width="16" height="17.5" rx="1.5" fill="none" stroke="#8B5A2B" stroke-width="1.5"></rect><path d="M51 68 L61 68 M51 72 L61 72 M51 76 L61 76" stroke="#8E87B8" stroke-width="1"></path>',
    },
    "satchel": {
        "name": "Satchel",
        "emoji": "👜",
        "cost": 10,
        "category": "gear",
        "tile_viewbox": "38 42 32 42",
        "svg": '<path d="M42 47 L56 65 L66 47" fill="none" stroke="#B85A36" stroke-width="2.5" stroke-linecap="round"></path><rect x="46" y="63" width="20" height="14" rx="2.5" fill="#E8845C"></rect><path d="M46 63 L66 63 L66 69 C66 70.2 65 70.6 64 70.6 L48 70.6 C47 70.6 46 70.2 46 69 Z" fill="#B85A36"></path><rect x="53" y="67" width="6" height="4.6" rx="1.2" fill="#F2C94C"></rect>',
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
