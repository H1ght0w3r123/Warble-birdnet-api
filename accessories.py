"""
Dress Up catalog - 33 items across 5 categories, real design art
(Warble art pass 02). Each accessory overlays the 100x100 avatar
illustration (see avatarSvg() in the frontend). tile_viewbox is the
cropped viewBox used to render this item inside a 96px carousel tile,
so the art fills the tile regardless of which zone it sits in.

Hats carry their tilt baked into a <g transform> wrapper (translate +
rotate around a 50,26 pivot) rather than a CSS transform, since the
app has no per-item CSS-transform pipeline for these overlays - this
is the SVG-native equivalent, same visual result.
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
    "starter": 20,     # one good session
    "everyday": 45,    # two or three sessions
    "special": 90,     # about a week
    "prestige": 170,   # a fortnight - a real goal
    "legendary": 320,  # a month or so - the things to dream about
}

ACCESSORIES = {
    "top_hat": {
        "name": "Top Hat",
        "emoji": "🎩",
        "cost": 90,
        "category": "hats",
        "tile_viewbox": "24 0 52 30",
        "svg": '<g transform="translate(0,-3) rotate(-8 50 26)"><path d="M39.5 5 C39.5 4 60.5 4 60.5 5 L62.5 21 L37.5 21 Z" fill="#1A1128"></path><path d="M41 4.6 C42.4 4.2 45 4.2 45.6 4.8 L44.4 21 L39.8 21 Z" fill="#FFFFFF" opacity="0.12"></path><path d="M37.9 15.5 L62.1 15.5 L62.5 20.6 L37.5 20.6 Z" fill="#E8845C"></path><path d="M37.7 18.6 L62.3 18.6 L62.5 20.6 L37.5 20.6 Z" fill="#1A1128" opacity="0.2"></path><path d="M48 16.2 L52.5 16.2 L52.5 20.2 L48 20.2 Z" fill="#F2C94C"></path><path d="M28 22.6 C34 20.4 66 20.4 72 22.6 C72.6 24.8 68 26.8 50 26.8 C32 26.8 27.4 24.8 28 22.6 Z" fill="#1A1128"></path><path d="M30 22.4 C36 20.9 64 20.9 70 22.4 C64 23.8 36 23.8 30 22.4 Z" fill="#FFFFFF" opacity="0.1"></path></g>',
    },
    "golden_crown": {
        "name": "Golden Crown",
        "emoji": "👑",
        "cost": 320,
        "category": "hats",
        "tile_viewbox": "24 0 52 30",
        "svg": '<g transform="translate(0,-3.5) rotate(6 50 26)"><path d="M32 20 C32 19 33 18.6 34 19 L38.5 7.5 C39 6.4 40.4 6.4 40.9 7.5 L45 18 L49 5.4 C49.4 4.2 50.6 4.2 51 5.4 L55 18 L59.1 7.5 C59.6 6.4 61 6.4 61.5 7.5 L66 19 C67 18.6 68 19 68 20 Z" fill="#F2C94C"></path><path d="M31 18.6 C40 20.4 60 20.4 69 18.6 C69.6 22 69.2 24.4 68 25.6 C58 27 42 27 32 25.6 C30.8 24.4 30.4 22 31 18.6 Z" fill="#F2C94C"></path><path d="M31.6 22.8 C41 24.6 59 24.6 68.4 22.8 C68.2 24.2 67.8 25.1 68 25.6 C58 27 42 27 32 25.6 C32.2 25.1 31.8 24.2 31.6 22.8 Z" fill="#B8901F"></path><circle cx="38.5" cy="22" r="2.1" fill="#E87EA1"></circle><circle cx="50" cy="22.6" r="2.4" fill="#7EC8A4"></circle><circle cx="61.5" cy="22" r="2.1" fill="#C4BFDF"></circle><circle cx="40" cy="7" r="1.6" fill="#F5EDD6"></circle><circle cx="50" cy="4.8" r="1.8" fill="#F5EDD6"></circle><circle cx="60" cy="7" r="1.6" fill="#F5EDD6"></circle></g>',
    },
    "flower_crown": {
        "name": "Flower Crown",
        "emoji": "🌸",
        "cost": 90,
        "category": "hats",
        "tile_viewbox": "24 8 52 24",
        "svg": '<g transform="translate(0,-2.5) rotate(-5 50 26)"><path d="M28 27 C32 18.5 40 14 50 14 C60 14 68 18.5 72 27 C68.5 21.5 60 18.4 50 18.4 C40 18.4 31.5 21.5 28 27 Z" fill="#3F7C5C"></path><path d="M30 24.6 C34 19.6 41.5 16.8 50 16.8 C58.5 16.8 66 19.6 70 24.6 C66 21 58.5 19 50 19 C41.5 19 34 21 30 24.6 Z" fill="#7EC8A4"></path><path d="M35 22 C33 19.4 33.4 16.6 35.6 15.6 C36.6 17.8 36.6 20.4 35 22 Z" fill="#7EC8A4"></path><path d="M65 22 C67 19.4 66.6 16.6 64.4 15.6 C63.4 17.8 63.4 20.4 65 22 Z" fill="#7EC8A4"></path><circle cx="38" cy="15.5" r="2.3" fill="#E87EA1"></circle><circle cx="40.3" cy="17.2" r="2.3" fill="#E87EA1"></circle><circle cx="39.4" cy="20" r="2.3" fill="#E87EA1"></circle><circle cx="36.6" cy="20" r="2.3" fill="#E87EA1"></circle><circle cx="35.7" cy="17.2" r="2.3" fill="#E87EA1"></circle><circle cx="38" cy="18" r="1.7" fill="#F2C94C"></circle><circle cx="60" cy="15.5" r="2.3" fill="#C4BFDF"></circle><circle cx="62.3" cy="17.2" r="2.3" fill="#C4BFDF"></circle><circle cx="61.4" cy="20" r="2.3" fill="#C4BFDF"></circle><circle cx="58.6" cy="20" r="2.3" fill="#C4BFDF"></circle><circle cx="57.7" cy="17.2" r="2.3" fill="#C4BFDF"></circle><circle cx="60" cy="18" r="1.7" fill="#F5EDD6"></circle><circle cx="50" cy="14.6" r="2.6" fill="#F2C94C"></circle><circle cx="50" cy="14.6" r="1.1" fill="#B8901F"></circle><circle cx="45" cy="16.6" r="1.6" fill="#E87EA1"></circle><circle cx="55" cy="16.6" r="1.6" fill="#E87EA1"></circle></g>',
    },
    "tucked_feather": {
        "name": "Tucked Feather",
        "emoji": "🪶",
        "cost": 20,
        "category": "hats",
        "tile_viewbox": "54 0 30 32",
        "svg": '<g transform="translate(0,-2) rotate(7 50 26)"><path d="M59.5 26.5 C63.5 17.5 69.5 9.5 78.5 3.5 C79 12 74.5 21 66.5 27.5 Z" fill="#7EC8A4"></path><path d="M66.5 27.5 C74.5 21 79 12 78.5 3.5 C75.5 11.5 71 19.5 66.5 27.5 Z" fill="#3F7C5C"></path><path d="M66.5 27.5 C71 19.5 75.5 11.5 78.5 3.5 C77.4 12 73.4 20 67.6 27.8 Z" fill="#F5EDD6" opacity="0.5"></path><path d="M57.5 22 C60.5 21 63.5 22.6 63 25.4 C60 26.4 57.5 25 57.5 22 Z" fill="#F2C94C"></path><path d="M58 24.4 C60.4 25.6 62 25.8 63 25.4 C60 26.4 57.8 25.2 58 24.4 Z" fill="#B8901F"></path></g>',
    },
    "baseball_cap": {
        "name": "Baseball Cap",
        "emoji": "🧢",
        "cost": 45,
        "category": "hats",
        "tile_viewbox": "26 2 58 28",
        "svg": '<g transform="translate(0,-3) rotate(-9 50 26)"><path d="M29.5 24.4 C29.5 12.6 38.6 6.6 50 6.6 C61.4 6.6 70.5 12.6 70.5 24.4 C63 25.8 37 25.8 29.5 24.4 Z" fill="#E8845C"></path><path d="M33 22 C33 13.6 39.4 8.6 46 7.4 C40.4 10.4 36.6 15.6 36 22.4 Z" fill="#FFFFFF" opacity="0.16"></path><path d="M50 6.6 C50 12 50 19 50 25.2 L47.6 25.2 C47.6 19 47.8 12 47.8 6.7 Z" fill="#1A1128" opacity="0.14"></path><path d="M49 20 C60 20.6 72 21.6 80.5 23 C83.5 23.6 83.4 27 80 27 C69 27 57 26 49 25.2 Z" fill="#B85A36"></path><path d="M49 24 C57 24.8 68 25.8 79 26 C79.8 26.6 80.6 27 80 27 C69 27 57 26 49 25.2 Z" fill="#1A1128" opacity="0.22"></path><circle cx="49" cy="7.4" r="2.2" fill="#B85A36"></circle></g>',
    },
    "sun_hat": {
        "name": "Sun Hat",
        "emoji": "👒",
        "cost": 90,
        "category": "hats",
        "tile_viewbox": "20 4 60 28",
        "svg": '<g transform="translate(0,-3) rotate(5 50 26)"><path d="M22 24.6 C26 20 36 18.6 50 18.6 C64 18.6 74 20 78 24.6 C74.5 27.8 64 29.4 50 29.4 C36 29.4 25.5 27.8 22 24.6 Z" fill="#F2C94C"></path><path d="M24 26 C29 28.6 38.5 29.4 50 29.4 C61.5 29.4 71 28.6 76 26 C71.5 27.4 62 28.2 50 28.2 C38 28.2 28.5 27.4 24 26 Z" fill="#B8901F"></path><path d="M36.5 22.4 C36.5 12.4 42.4 8.4 50 8.4 C57.6 8.4 63.5 12.4 63.5 22.4 C58 24 42 24 36.5 22.4 Z" fill="#F2C94C"></path><path d="M39.5 20.6 C39.5 13.4 43.4 10 47.4 9.2 C43.6 11.6 41.6 15.6 41.4 21 Z" fill="#FFFFFF" opacity="0.2"></path><path d="M36.6 18 C42 19.6 58 19.6 63.4 18 C63.5 20 63.5 21.4 63.5 22.4 C58 24 42 24 36.5 22.4 C36.5 21.4 36.5 20 36.6 18 Z" fill="#7EC8A4"></path><path d="M60 18.6 L66 16.6 L67 21 L61.5 22.6 Z" fill="#3F7C5C"></path></g>',
    },
    "party_hat": {
        "name": "Party Hat",
        "emoji": "🥳",
        "cost": 45,
        "category": "hats",
        "tile_viewbox": "34 0 32 30",
        "svg": '<g transform="translate(0,-3.5) rotate(9 50 26)"><path d="M50 3 C52.5 9 58 19 62.5 25.4 C58 26.6 42 26.6 37.5 25.4 C42 19 47.5 9 50 3 Z" fill="#E87EA1"></path><path d="M50 3 C52.5 9 58 19 62.5 25.4 C58.6 26.4 54 26.6 50 26.6 Z" fill="#1A1128" opacity="0.16"></path><path d="M46.6 12.4 C48.6 12.8 51.4 12.8 53.4 12.4 L54.8 16 C51.6 16.6 48.4 16.6 45.2 16 Z" fill="#F5EDD6"></path><path d="M43.4 19.4 C47 20.2 53 20.2 56.6 19.4 L58 23 C53 23.8 47 23.8 42 23 Z" fill="#F5EDD6"></path><circle cx="50" cy="3" r="3.6" fill="#F2C94C"></circle><circle cx="51.4" cy="4.2" r="1.5" fill="#B8901F" opacity="0.55"></circle></g>',
    },
    "wizard_hat": {
        "name": "Wizard Hat",
        "emoji": "🧙",
        "cost": 320,
        "category": "hats",
        "tile_viewbox": "26 0 48 32",
        "svg": '<g transform="translate(0,-3) rotate(-7 50 26)"><path d="M52 2.6 C50 8 52 14 56 19 C58.6 21.6 60.6 23 62 24 C58 25.2 42 25.2 38 24 C42 19.6 47 12 49 6.6 C49.8 4.6 50.8 3 52 2.6 Z" fill="#2D1B69"></path><path d="M52 2.6 C54 6 55 12 57.6 17 C59.4 20.2 61 22.6 62 24 C58.8 24.8 54.6 25.2 50.6 25.2 Z" fill="#1A1128" opacity="0.24"></path><path d="M52 2.6 C48.6 3.6 45.6 6 44 8.6 C46.6 7 49 5 50.6 3.4 Z" fill="#3D2A85"></path><path d="M28 24 C34 21.6 66 21.6 72 24 C72 26.8 63 28.6 50 28.6 C37 28.6 28 26.8 28 24 Z" fill="#3D2A85"></path><path d="M29.4 26 C35 27.8 42 28.6 50 28.6 C58 28.6 65 27.8 70.6 26 C65 27.2 58 27.8 50 27.8 C42 27.8 35 27.2 29.4 26 Z" fill="#1A1128" opacity="0.28"></path><path d="M38.6 20.6 C44 22 56 22 61.4 20.6 C61.8 22 62 23.2 62 24 C56 25.2 44 25.2 38 24 C38 23.2 38.2 22 38.6 20.6 Z" fill="#F2C94C"></path><path d="M54 11 L55.4 13.6 L58 15 L55.4 16.4 L54 19 L52.6 16.4 L50 15 L52.6 13.6 Z" fill="#F2C94C"></path><path d="M46 17.6 L46.8 19 L48.2 19.8 L46.8 20.6 L46 22 L45.2 20.6 L43.8 19.8 L45.2 19 Z" fill="#F2C94C" opacity="0.8"></path></g>',
    },
    "pirate_hat": {
        "name": "Pirate Hat",
        "emoji": "🏴",
        "cost": 170,
        "category": "hats",
        "tile_viewbox": "22 6 56 24",
        "svg": '<g transform="translate(0,-3) rotate(8 50 26)"><path d="M24 26.6 C24 15.6 35 9 50 9 C65 9 76 15.6 76 26.6 C70 23.2 60.6 21.6 50 21.6 C39.4 21.6 30 23.2 24 26.6 Z" fill="#1A1128"></path><path d="M25.4 24.4 C31.6 21.4 40.4 20 50 20 C59.6 20 68.4 21.4 74.6 24.4 C75.2 25.2 75.6 25.9 76 26.6 C70 23.2 60.6 21.6 50 21.6 C39.4 21.6 30 23.2 24 26.6 C24.4 25.9 24.8 25.2 25.4 24.4 Z" fill="#E9DDBE"></path><path d="M30 17.6 C34.6 13.6 41.6 11.2 49 11 C42.4 12.4 36.4 15 32.6 19 Z" fill="#FFFFFF" opacity="0.14"></path><circle cx="50" cy="16.4" r="3.6" fill="#F5EDD6"></circle><path d="M47.6 19 L52.4 19 L52 21 L48 21 Z" fill="#F5EDD6"></path><circle cx="48.6" cy="15.8" r="1.05" fill="#1A1128"></circle><circle cx="51.4" cy="15.8" r="1.05" fill="#1A1128"></circle></g>',
    },
    "explorer_helmet": {
        "name": "Explorer Helmet",
        "emoji": "🪖",
        "cost": 170,
        "category": "hats",
        "tile_viewbox": "22 6 56 25",
        "svg": '<g transform="translate(0,-3) rotate(-6 50 26)"><path d="M24 25 C30 21.4 40 20 50 20 C60 20 70 21.4 76 25 C71 27.6 61 28.8 50 28.8 C39 28.8 29 27.6 24 25 Z" fill="#F5EDD6"></path><path d="M25.6 26.2 C31 28 40 28.8 50 28.8 C60 28.8 69 28 74.4 26.2 C69 27.4 60 28 50 28 C40 28 31 27.4 25.6 26.2 Z" fill="#E9DDBE"></path><path d="M31.4 23 C31.4 13 40 8.4 50 8.4 C60 8.4 68.6 13 68.6 23 C61 24.6 39 24.6 31.4 23 Z" fill="#E9DDBE"></path><path d="M35 21 C35 13.6 40.4 10 45.6 9.2 C40.6 11.4 37.4 15.4 37 21.4 Z" fill="#FFFFFF" opacity="0.4"></path><path d="M50 8.4 L50 24.2 L48 24.2 L48 8.4 Z" fill="#1A1128" opacity="0.1"></path><path d="M31.6 19 C39 20.6 61 20.6 68.4 19 C68.6 20.6 68.6 22 68.6 23 C61 24.6 39 24.6 31.4 23 C31.4 22 31.4 20.6 31.6 19 Z" fill="#3F7C5C"></path><circle cx="49" cy="9" r="2.2" fill="#F5EDD6"></circle></g>',
    },
    "reindeer_antlers": {
        "name": "Reindeer Antlers",
        "emoji": "🦌",
        "cost": 170,
        "category": "hats",
        "tile_viewbox": "26 0 48 28",
        "svg": '<g transform="translate(0,-3.5) rotate(4 50 26)"><path d="M45 25.4 C43.4 20 40.6 16 36.8 13 C35 11.6 32.6 10.6 31 11 C29.6 11.4 29.4 9.6 30.8 8.6 C32.4 7.6 35 8.6 37.2 10.4 C36.4 8.2 35.8 5.6 36.8 4.4 C37.8 3.2 39.6 3.8 40.2 5.6 C40.8 7.4 41 9.8 41.6 11.8 C42.6 9.6 44.2 8 45.6 8.4 C47 8.8 47 11 46.4 13.4 C45.6 16.6 45.4 21 45.6 25.4 Z" fill="#E9DDBE"></path><path d="M45.6 25.4 C45.4 21 45.6 16.6 46.4 13.4 C47 11 47 8.8 45.6 8.4 C46 10.4 45.4 13 44.6 16.2 C44 19.2 43.8 22.4 44 25.4 Z" fill="#B8901F" opacity="0.35"></path><path d="M55 25.4 C56.6 20 59.4 16 63.2 13 C65 11.6 67.4 10.6 69 11 C70.4 11.4 70.6 9.6 69.2 8.6 C67.6 7.6 65 8.6 62.8 10.4 C63.6 8.2 64.2 5.6 63.2 4.4 C62.2 3.2 60.4 3.8 59.8 5.6 C59.2 7.4 59 9.8 58.4 11.8 C57.4 9.6 55.8 8 54.4 8.4 C53 8.8 53 11 53.6 13.4 C54.4 16.6 54.6 21 54.4 25.4 Z" fill="#E9DDBE"></path><path d="M54.4 25.4 C54.6 21 54.4 16.6 53.6 13.4 C53 11 53 8.8 54.4 8.4 C54 10.4 54.6 13 55.4 16.2 C56 19.2 56.2 22.4 56 25.4 Z" fill="#B8901F" opacity="0.35"></path></g>',
    },
    "cosy_scarf": {
        "name": "Cosy Scarf",
        "emoji": "🧣",
        "cost": 45,
        "category": "neck",
        "tile_viewbox": "28 63 50 38",
        "svg": '<path d="M29.5 66 C35.5 72.6 43 75.6 50 75.6 C57 75.6 64.5 72.6 70.5 66 C71.4 73 64.5 82.6 50 82.6 C35.5 82.6 28.6 73 29.5 66 Z" fill="#E87EA1"></path><path d="M61.6 71.6 C65 70 68.2 67.8 70.5 65.6 C71.4 69.6 70.8 74 68.6 78.4 C66 80.4 63.2 81.6 60.6 82.4 C61.2 78.6 61.4 75 61.6 71.6 Z" fill="#E87EA1"></path><path d="M33 70.6 C35.4 73.2 38.2 75.2 41 76.4 L40 80.8 C36.8 79.4 33.8 77 31.4 74 Z" fill="#1A1128" opacity="0.12"></path><path d="M43.4 77 C45.8 77.6 48 77.8 50 77.8 L50 82.2 C47.4 82.2 44.8 81.8 42.4 81.2 Z" fill="#1A1128" opacity="0.12"></path><path d="M52 77.8 C54.2 77.6 56.4 77.2 58.4 76.6 L59.4 81 C57 81.7 54.6 82.2 52 82.2 Z" fill="#1A1128" opacity="0.12"></path><path d="M60.6 76 C63.4 74.6 66 72.6 68 70.2 L69.4 74 C67.4 76.8 64.6 79 61.6 80.4 Z" fill="#1A1128" opacity="0.12"></path><path d="M31.4 76.6 C36.6 81 43 83 50 83 C57 83 63.4 81 68.6 76.6 C66.6 80.6 60 84.6 50 84.6 C40 84.6 33.4 80.6 31.4 76.6 Z" fill="#B85A36"></path><path d="M59.6 79.6 C63.6 78.4 67.4 77 70.6 75.4 C72.6 80.6 74 86.4 74.6 91.6 C71 93 67.4 94 63.8 94.6 C62.6 89.4 61.4 84.4 59.6 79.6 Z" fill="#E87EA1"></path><path d="M67 92.8 C69.6 92.2 72.2 91.4 74.6 91.6 C74 86.4 72.6 80.6 70.6 75.4 C69.4 76 68.2 76.6 67 77.2 C68.6 82.2 69.4 87.4 67 92.8 Z" fill="#1A1128" opacity="0.14"></path><path d="M63.8 94.6 L66 94.2 L66.6 98.4 L64.6 98.6 Z" fill="#B85A36"></path><path d="M67.6 93.8 L69.8 93.2 L70.8 97.4 L68.8 97.8 Z" fill="#B85A36"></path><path d="M71.4 92.6 L73.6 92 L75 96 L73 96.6 Z" fill="#B85A36"></path>',
    },
    "fancy_bow": {
        "name": "Fancy Bow",
        "emoji": "🎀",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "28 65 44 26",
        "svg": '<path d="M46 73.6 C42 68.4 34.6 67.4 31.6 70.6 C28.6 73.8 31.6 79.4 37.6 79.6 C41 79.7 44.4 77.6 46 74.6 Z" fill="#E87EA1"></path><path d="M54 73.6 C58 68.4 65.4 67.4 68.4 70.6 C71.4 73.8 68.4 79.4 62.4 79.6 C59 79.7 55.6 77.6 54 74.6 Z" fill="#E87EA1"></path><path d="M46 74.6 C43.6 76.4 40.4 78 37 78.6 C40.6 76.6 43.4 74.6 45.4 72.6 Z" fill="#1A1128" opacity="0.2"></path><path d="M54 74.6 C56.4 76.4 59.6 78 63 78.6 C59.4 76.6 56.6 74.6 54.6 72.6 Z" fill="#1A1128" opacity="0.2"></path><path d="M47.4 76.6 C46.2 80.6 44 84.6 41 87.6 C43.6 87 46 85.6 48 83.6 Z" fill="#E87EA1"></path><path d="M52.6 76.6 C53.8 80.6 56 84.6 59 87.6 C56.4 87 54 85.6 52 83.6 Z" fill="#E87EA1"></path><path d="M44.6 71.4 C46 70.8 47.4 70.6 48.6 70.6 L48.6 77.4 C47.4 77.4 46 77.2 44.6 76.6 Z" fill="#E87EA1"></path><path d="M55.4 71.4 C54 70.8 52.6 70.6 51.4 70.6 L51.4 77.4 C52.6 77.4 54 77.2 55.4 76.6 Z" fill="#E87EA1"></path><path d="M46.4 70.6 C48.8 69.6 51.2 69.6 53.6 70.6 C54.6 72.4 54.6 75.4 53.6 77.4 C51.2 78.4 48.8 78.4 46.4 77.4 C45.4 75.4 45.4 72.4 46.4 70.6 Z" fill="#E87EA1"></path><path d="M52 70 C54 71.4 54.8 74 54.4 77.6 C53.6 78.2 52.6 78.4 51.4 78.4 C52.6 75.6 52.8 72.6 52 70 Z" fill="#1A1128" opacity="0.2"></path>',
    },
    "bow_tie": {
        "name": "Bow Tie",
        "emoji": "🎗️",
        "cost": 20,
        "category": "neck",
        "tile_viewbox": "32 64 36 20",
        "svg": '<path d="M35 66.6 C39.4 68 44.4 70.4 47.6 73.4 C44.4 76.4 39.4 78.8 35 80.2 C36.2 76 36.2 70.8 35 66.6 Z" fill="#2D1B69"></path><path d="M65 66.6 C60.6 68 55.6 70.4 52.4 73.4 C55.6 76.4 60.6 78.8 65 80.2 C63.8 76 63.8 70.8 65 66.6 Z" fill="#2D1B69"></path><path d="M35 73.4 C38.6 75 43.4 77.2 47.6 73.4 C44.4 76.4 39.4 78.8 35 80.2 C35.6 78 35.8 75.6 35 73.4 Z" fill="#1A1128" opacity="0.25"></path><path d="M65 73.4 C61.4 75 56.6 77.2 52.4 73.4 C55.6 76.4 60.6 78.8 65 80.2 C64.4 78 64.2 75.6 65 73.4 Z" fill="#1A1128" opacity="0.25"></path><path d="M46.6 69.6 C48.8 68.8 51.2 68.8 53.4 69.6 C54.2 71.8 54.2 75 53.4 77.2 C51.2 78 48.8 78 46.6 77.2 C45.8 75 45.8 71.8 46.6 69.6 Z" fill="#3D2A85"></path><path d="M50 68.9 L50 77.9 L48.6 77.7 L48.6 69 Z" fill="#1A1128" opacity="0.2"></path>',
    },
    "beaded_necklace": {
        "name": "Beaded Necklace",
        "emoji": "📿",
        "cost": 45,
        "category": "neck",
        "tile_viewbox": "30 63 40 21",
        "svg": '<path d="M32.6 66 C35.4 72.8 42.2 78.4 50 80.2 C57.8 78.4 64.6 72.8 67.4 66 C67.4 71.8 62.8 77.8 56.8 81 C52 83.4 48 83.4 43.2 81 C37.2 77.8 32.6 71.8 32.6 66 Z" fill="#8E87B8"></path><circle cx="34" cy="68" r="2.4" fill="#7EC8A4"></circle><circle cx="37.4" cy="72" r="2.6" fill="#F2C94C"></circle><circle cx="41" cy="75.2" r="2.8" fill="#E87EA1"></circle><circle cx="45.2" cy="77.6" r="3" fill="#7EC8A4"></circle><circle cx="50" cy="78.8" r="3.2" fill="#F2C94C"></circle><circle cx="54.8" cy="77.6" r="3" fill="#E87EA1"></circle><circle cx="59" cy="75.2" r="2.8" fill="#7EC8A4"></circle><circle cx="62.6" cy="72" r="2.6" fill="#F2C94C"></circle><circle cx="66" cy="68" r="2.4" fill="#E87EA1"></circle><circle cx="36.6" cy="71.2" r="0.85" fill="#F5EDD6" opacity="0.7"></circle><circle cx="44.2" cy="76.6" r="0.95" fill="#F5EDD6" opacity="0.7"></circle><circle cx="49" cy="77.9" r="1" fill="#F5EDD6" opacity="0.7"></circle><circle cx="61.8" cy="71.2" r="0.85" fill="#F5EDD6" opacity="0.7"></circle>',
    },
    "golden_medal": {
        "name": "Golden Medal",
        "emoji": "🏅",
        "cost": 320,
        "category": "neck",
        "tile_viewbox": "34 62 32 32",
        "svg": '<path d="M38.6 64.6 C41 64.6 43.4 64.6 45 65.4 C47.4 69.4 49.6 73.4 51.4 77.4 C49.8 78.6 48 79.4 46.4 79.6 C43.6 74.6 41 69.6 38.6 64.6 Z" fill="#E8845C"></path><path d="M61.4 64.6 C59 64.6 56.6 64.6 55 65.4 C52.6 69.4 50.4 73.4 48.6 77.4 C50.2 78.6 52 79.4 53.6 79.6 C56.4 74.6 59 69.6 61.4 64.6 Z" fill="#E8845C"></path><path d="M46.4 79.6 C48 79 50 78.6 52 78.6 C53.4 78.6 52.6 76.6 51.4 77.4 C49.8 78.4 48 79.2 46.4 79.6 Z" fill="#B85A36"></path><path d="M47.4 78.4 C48.4 77.4 51.6 77.4 52.6 78.4 C53.2 79.4 52.6 80.6 51.4 80.6 L48.6 80.6 C47.4 80.6 46.8 79.4 47.4 78.4 Z" fill="#B8901F"></path><circle cx="50" cy="84" r="7.4" fill="#B8901F"></circle><circle cx="50" cy="84" r="6" fill="#F2C94C"></circle><path d="M50 79.6 L51.6 82.6 L55 83.2 L52.6 85.6 L53.2 89 L50 87.4 L46.8 89 L47.4 85.6 L45 83.2 L48.4 82.6 Z" fill="#B8901F"></path><path d="M45.6 81.4 C46.8 79.8 48.6 78.8 50.6 78.6 C48.2 79.6 46.6 81 45.6 82.8 Z" fill="#F5EDD6" opacity="0.5"></path>',
    },
    "pearl_necklace": {
        "name": "Pearl Necklace",
        "emoji": "🤍",
        "cost": 90,
        "category": "neck",
        "tile_viewbox": "30 62 40 26",
        "svg": '<path d="M32.6 65.6 C35.4 72.4 42.2 78 50 79.8 C57.8 78 64.6 72.4 67.4 65.6 C67.4 71.4 62.8 77.4 56.8 80.6 C52 83 48 83 43.2 80.6 C37.2 77.4 32.6 71.4 32.6 65.6 Z" fill="#8E87B8"></path><circle cx="34" cy="67.4" r="2.2" fill="#F5EDD6"></circle><circle cx="37.2" cy="71.2" r="2.4" fill="#F5EDD6"></circle><circle cx="40.8" cy="74.4" r="2.5" fill="#F5EDD6"></circle><circle cx="44.8" cy="76.8" r="2.6" fill="#F5EDD6"></circle><circle cx="55.2" cy="76.8" r="2.6" fill="#F5EDD6"></circle><circle cx="59.2" cy="74.4" r="2.5" fill="#F5EDD6"></circle><circle cx="62.8" cy="71.2" r="2.4" fill="#F5EDD6"></circle><circle cx="66" cy="67.4" r="2.2" fill="#F5EDD6"></circle><path d="M47.8 77.4 C48.6 76.4 51.4 76.4 52.2 77.4 C52.8 78.2 52.2 79.4 51.2 79.4 L48.8 79.4 C47.8 79.4 47.2 78.2 47.8 77.4 Z" fill="#8E87B8"></path><circle cx="50" cy="82.6" r="3.6" fill="#F5EDD6"></circle><path d="M46.6 83.6 C47.4 85.8 49.6 86.8 52 86.2 C50.6 86.8 47.8 86.4 46.6 83.6 Z" fill="#8E87B8" opacity="0.5"></path><circle cx="48.6" cy="81.2" r="1.2" fill="#FFFFFF"></circle><circle cx="36.4" cy="70.4" r="0.75" fill="#FFFFFF" opacity="0.8"></circle><circle cx="44" cy="76.1" r="0.8" fill="#FFFFFF" opacity="0.8"></circle><circle cx="62" cy="70.4" r="0.75" fill="#FFFFFF" opacity="0.8"></circle>',
    },
    "striped_scarf": {
        "name": "Striped Scarf",
        "emoji": "🧣",
        "cost": 45,
        "category": "neck",
        "tile_viewbox": "28 63 50 38",
        "svg": '<path d="M29.5 66 C35.5 72.6 43 75.6 50 75.6 C57 75.6 64.5 72.6 70.5 66 C71.4 73 64.5 82.6 50 82.6 C35.5 82.6 28.6 73 29.5 66 Z" fill="#7EC8A4"></path><path d="M61.6 71.6 C65 70 68.2 67.8 70.5 65.6 C71.4 69.6 70.8 74 68.6 78.4 C66 80.4 63.2 81.6 60.6 82.4 C61.2 78.6 61.4 75 61.6 71.6 Z" fill="#7EC8A4"></path><path d="M30.4 71 C36 76 43 78.8 50 78.8 C57 78.8 64 76 69.6 71 C69.4 72.6 69 74 68.4 75.4 C63 79.4 56.6 81.4 50 81.4 C43.4 81.4 37 79.4 31.6 75.4 C31 74 30.6 72.6 30.4 71 Z" fill="#F5EDD6"></path><path d="M33.4 67.6 C39 71.4 44.6 73.2 50 73.2 C55.4 73.2 61 71.4 66.6 67.6 C66.4 68.8 66 69.9 65.4 71 C60.4 74 55.2 75.4 50 75.4 C44.8 75.4 39.6 74 34.6 71 C34 69.9 33.6 68.8 33.4 67.6 Z" fill="#F5EDD6" opacity="0.55"></path><path d="M31.4 77 C36.6 81.4 43 83.4 50 83.4 C57 83.4 63.4 81.4 68.6 77 C66.6 81 60 84.6 50 84.6 C40 84.6 33.4 81 31.4 77 Z" fill="#3F7C5C"></path><path d="M59.6 79.6 C63.6 78.4 67.4 77 70.6 75.4 C72.6 80.6 74 86.4 74.6 91.6 C71 93 67.4 94 63.8 94.6 C62.6 89.4 61.4 84.4 59.6 79.6 Z" fill="#7EC8A4"></path><path d="M61.6 84.6 L71.6 81.4 L72.6 85.4 L62.8 88.6 Z" fill="#F5EDD6"></path><path d="M63.4 90 L73.8 87 L74.4 90.6 L64.2 93.6 Z" fill="#F5EDD6" opacity="0.8"></path><path d="M63.8 94.6 L66 94.2 L66.6 98.4 L64.6 98.6 Z" fill="#3F7C5C"></path><path d="M67.6 93.8 L69.8 93.2 L70.8 97.4 L68.8 97.8 Z" fill="#3F7C5C"></path><path d="M71.4 92.6 L73.6 92 L75 96 L73 96.6 Z" fill="#3F7C5C"></path>',
    },
    "star_necklace": {
        "name": "Star Necklace",
        "emoji": "⭐",
        "cost": 90,
        "category": "neck",
        "tile_viewbox": "32 62 36 34",
        "svg": '<path d="M34.6 65.2 C37.4 71.4 43 76.4 50 78.4 C57 76.4 62.6 71.4 65.4 65.2 C65.6 70.6 61.6 76.2 55.6 79.4 C52 81.2 48 81.2 44.4 79.4 C38.4 76.2 34.4 70.6 34.6 65.2 Z" fill="#8E87B8"></path><path d="M47.8 76.8 C48.6 75.8 51.4 75.8 52.2 76.8 C52.8 77.6 52.2 78.8 51.2 78.8 L48.8 78.8 C47.8 78.8 47.2 77.6 47.8 76.8 Z" fill="#B8901F"></path><path d="M50 73.6 L52.8 80.2 L59.6 82.8 L52.8 85.4 L50 92 L47.2 85.4 L40.4 82.8 L47.2 80.2 Z" fill="#F2C94C"></path><path d="M50 73.6 L52.8 80.2 L59.6 82.8 L50 82.8 Z" fill="#FFFFFF" opacity="0.22"></path><path d="M50 92 L47.2 85.4 L40.4 82.8 L50 82.8 Z" fill="#B8901F" opacity="0.5"></path><circle cx="50" cy="82.8" r="1.6" fill="#B8901F"></circle>',
    },
    "explorer_backpack": {
        "name": "Explorer Backpack",
        "emoji": "🎒",
        "cost": 170,
        "category": "gear",
        "tile_viewbox": "13 54 74 38",
        "svg": '<path d="M15.4 61 C15.4 58.6 17 57 19.6 57 L26 57 C27.4 57 28 58 28 59.4 L28 73 C28 75 26.6 76 24.4 76 L19.6 76 C17 76 15.4 74.4 15.4 72 Z" fill="#7EC8A4"></path><path d="M24 57.4 C26.6 58 28 59 28 60.6 L28 73 C28 75 26.6 76 24.4 76 C25.4 74 25.6 71.6 25.4 68.6 C25 64.6 24.6 61 24 57.4 Z" fill="#3F7C5C"></path><path d="M84.6 61 C84.6 58.6 83 57 80.4 57 L74 57 C72.6 57 72 58 72 59.4 L72 73 C72 75 73.4 76 75.6 76 L80.4 76 C83 76 84.6 74.4 84.6 72 Z" fill="#7EC8A4"></path><path d="M76 57.4 C73.4 58 72 59 72 60.6 L72 73 C72 75 73.4 76 75.6 76 C74.6 74 74.4 71.6 74.6 68.6 C75 64.6 75.4 61 76 57.4 Z" fill="#3F7C5C"></path><path d="M37.6 61 C39.6 60.4 42.4 60.4 44.4 61 C45.4 69.6 46 78.6 46 87.6 C44 88.2 41.4 88.2 39.4 87.6 C39.4 78.6 38.6 69.6 37.6 61 Z" fill="#3F7C5C"></path><path d="M62.4 61 C60.4 60.4 57.6 60.4 55.6 61 C54.6 69.6 54 78.6 54 87.6 C56 88.2 58.6 88.2 60.6 87.6 C60.6 78.6 61.4 69.6 62.4 61 Z" fill="#3F7C5C"></path><path d="M43 60.6 C44 60.7 44.4 60.8 44.4 61 C45.4 69.6 46 78.6 46 87.6 C45.4 87.8 44.8 88 44.2 88 C44.2 78.6 43.6 69.4 43 60.6 Z" fill="#7EC8A4" opacity="0.5"></path><path d="M57 60.6 C56 60.7 55.6 60.8 55.6 61 C54.6 69.6 54 78.6 54 87.6 C54.6 87.8 55.2 88 55.8 88 C55.8 78.6 56.4 69.4 57 60.6 Z" fill="#7EC8A4" opacity="0.5"></path><path d="M39 71.6 L46 71.6 L46 76.4 L39 76.4 Z" fill="#F2C94C"></path><path d="M54 71.6 L61 71.6 L61 76.4 L54 76.4 Z" fill="#F2C94C"></path><path d="M41 73 L44 73 L44 75 L41 75 Z" fill="#B8901F"></path><path d="M56 73 L59 73 L59 75 L56 75 Z" fill="#B8901F"></path>',
    },
    "round_specs": {
        "name": "Round Specs",
        "emoji": "👓",
        "cost": 45,
        "category": "glasses",
        "tile_viewbox": "22 40 56 20",
        "svg": '<path d="M30.4 48 C28 48.4 25.6 49.6 24 51.2 L25.4 53.2 C27 51.8 29 50.8 31 50.6 Z" fill="#1A1128"></path><path d="M69.6 48 C72 48.4 74.4 49.6 76 51.2 L74.6 53.2 C73 51.8 71 50.8 69 50.6 Z" fill="#1A1128"></path><path d="M45.6 47.4 C47.6 46.2 52.4 46.2 54.4 47.4 L54.4 49.8 C52.4 48.6 47.6 48.6 45.6 49.8 Z" fill="#1A1128"></path><circle cx="38" cy="50" r="7.8" fill="#1A1128"></circle><circle cx="62" cy="50" r="7.8" fill="#1A1128"></circle><circle cx="38" cy="50" r="6" fill="#F5EDD6" opacity="0.5"></circle><circle cx="62" cy="50" r="6" fill="#F5EDD6" opacity="0.5"></circle><path d="M34 46.6 C35.4 45 37.6 44.2 39.6 44.4 C37.2 45 35.4 46.2 34.6 47.8 Z" fill="#FFFFFF" opacity="0.75"></path><path d="M58 46.6 C59.4 45 61.6 44.2 63.6 44.4 C61.2 45 59.4 46.2 58.6 47.8 Z" fill="#FFFFFF" opacity="0.75"></path>',
    },
    "explorer_goggles": {
        "name": "Explorer Goggles",
        "emoji": "🥽",
        "cost": 170,
        "category": "glasses",
        "tile_viewbox": "20 41 60 18",
        "svg": '<path d="M22 47.6 C28 44.4 72 44.4 78 47.6 C78 50 78 52.4 78 54.8 C72 51.6 28 51.6 22 54.8 C22 52.4 22 50 22 47.6 Z" fill="#3F7C5C"></path><path d="M23 51.6 C29 48.8 71 48.8 77 51.6 C77 53 77 54 77 54.8 C71 51.6 29 51.6 23 54.8 C23 54 23 53 23 51.6 Z" fill="#1A1128" opacity="0.18"></path><path d="M28.6 46 C33.2 44 42 44 46.6 46 C47.6 49.4 47.6 52.6 46.6 56 C42 58 33.2 58 28.6 56 C27.6 52.6 27.6 49.4 28.6 46 Z" fill="#8E87B8"></path><path d="M53.4 46 C58 44 66.8 44 71.4 46 C72.4 49.4 72.4 52.6 71.4 56 C66.8 58 58 58 53.4 56 C52.4 52.6 52.4 49.4 53.4 46 Z" fill="#8E87B8"></path><path d="M30.8 47.4 C34.6 46 40.6 46 44.4 47.4 C45.2 50 45.2 52 44.4 54.6 C40.6 56 34.6 56 30.8 54.6 C30 52 30 50 30.8 47.4 Z" fill="#C4BFDF"></path><path d="M55.6 47.4 C59.4 46 65.4 46 69.2 47.4 C70 50 70 52 69.2 54.6 C65.4 56 59.4 56 55.6 54.6 C54.8 52 54.8 50 55.6 47.4 Z" fill="#C4BFDF"></path><path d="M32.6 48.6 C34.6 47.4 37.4 47 39.6 47.4 C36.8 48 34.6 49.2 33.6 51 Z" fill="#FFFFFF" opacity="0.7"></path><path d="M57.4 48.6 C59.4 47.4 62.2 47 64.4 47.4 C61.6 48 59.4 49.2 58.4 51 Z" fill="#FFFFFF" opacity="0.7"></path><path d="M45.4 46.6 L54.6 46.6 L54.6 54.4 L45.4 54.4 Z" fill="#F2C94C"></path><path d="M47.4 48.6 L52.6 48.6 L52.6 52.4 L47.4 52.4 Z" fill="#B8901F"></path>',
    },
    "sunglasses": {
        "name": "Sunglasses",
        "emoji": "🕶️",
        "cost": 90,
        "category": "glasses",
        "tile_viewbox": "24 40 52 22",
        "svg": '<path d="M26 44.6 C34 42.4 66 42.4 74 44.6 L74 47.4 C66 45.6 34 45.6 26 47.4 Z" fill="#E8845C"></path><path d="M27 46.8 C33 45.6 42 45.8 46.6 47.4 C46.6 52 44 56.4 39.6 57.8 C34.6 59.2 29.6 56.4 27.8 52 C27.2 50.4 27 48.6 27 46.8 Z" fill="#2D1B69"></path><path d="M73 46.8 C67 45.6 58 45.8 53.4 47.4 C53.4 52 56 56.4 60.4 57.8 C65.4 59.2 70.4 56.4 72.2 52 C72.8 50.4 73 48.6 73 46.8 Z" fill="#2D1B69"></path><path d="M46.6 47.4 C48.6 46.6 51.4 46.6 53.4 47.4 L53.4 49.6 C51.4 48.8 48.6 48.8 46.6 49.6 Z" fill="#E8845C"></path><path d="M31 49.4 C33 48.4 35.6 48.2 37.6 48.6 C34.8 49.4 32.6 50.8 31.6 53 Z" fill="#FFFFFF" opacity="0.35"></path><path d="M57 49.4 C59 48.4 61.6 48.2 63.6 48.6 C60.8 49.4 58.6 50.8 57.6 53 Z" fill="#FFFFFF" opacity="0.35"></path><path d="M26 44.6 C34 42.4 66 42.4 74 44.6 C66 43.8 34 43.8 26 44.6 Z" fill="#FFFFFF" opacity="0.2"></path>',
    },
    "star_glasses": {
        "name": "Star Glasses",
        "emoji": "⭐",
        "cost": 320,
        "category": "glasses",
        "tile_viewbox": "24 40 52 22",
        "svg": '<path d="M30.4 48.4 C28 48.8 25.8 49.8 24.2 51.2 L25.6 53.2 C27.2 51.8 29 50.9 31 50.7 Z" fill="#F2C94C"></path><path d="M69.6 48.4 C72 48.8 74.2 49.8 75.8 51.2 L74.4 53.2 C72.8 51.8 71 50.9 69 50.7 Z" fill="#F2C94C"></path><path d="M38 42.4 L41.2 48.4 L47.8 49.2 L43 53.6 L44.2 60.2 L38 57 L31.8 60.2 L33 53.6 L28.2 49.2 L34.8 48.4 Z" fill="#F2C94C"></path><path d="M62 42.4 L65.2 48.4 L71.8 49.2 L67 53.6 L68.2 60.2 L62 57 L55.8 60.2 L57 53.6 L52.2 49.2 L58.8 48.4 Z" fill="#F2C94C"></path><path d="M38 46.4 L39.9 49.9 L43.8 50.4 L40.9 53 L41.6 56.9 L38 55 L34.4 56.9 L35.1 53 L32.2 50.4 L36.1 49.9 Z" fill="#E87EA1" opacity="0.85"></path><path d="M62 46.4 L63.9 49.9 L67.8 50.4 L64.9 53 L65.6 56.9 L62 55 L58.4 56.9 L59.1 53 L56.2 50.4 L60.1 49.9 Z" fill="#E87EA1" opacity="0.85"></path><path d="M46 49.2 C48 48.4 52 48.4 54 49.2 L54 51.4 C52 50.6 48 50.6 46 51.4 Z" fill="#F2C94C"></path>',
    },
    "wellies": {
        "name": "Wellies",
        "emoji": "👢",
        "cost": 45,
        "category": "shoes",
        "tile_viewbox": "33 84 34 17",
        "svg": '<path d="M38.4 87.4 C41.6 86.8 45 86.8 47.4 87.4 C47.8 90.6 48 93.6 48 96.2 C48 98.6 46 99.8 42.6 99.8 C38.6 99.8 36.4 98.6 36.4 96.2 C36.6 93.2 37.4 90.2 38.4 87.4 Z" fill="#7EC8A4"></path><path d="M61.6 87.4 C58.4 86.8 55 86.8 52.6 87.4 C52.2 90.6 52 93.6 52 96.2 C52 98.6 54 99.8 57.4 99.8 C61.4 99.8 63.6 98.6 63.6 96.2 C63.4 93.2 62.6 90.2 61.6 87.4 Z" fill="#7EC8A4"></path><path d="M38 86.6 C41.4 85.8 45 85.8 47.8 86.6 L48.2 89.6 C45 88.8 41.2 88.8 38 89.6 Z" fill="#F2C94C"></path><path d="M62 86.6 C58.6 85.8 55 85.8 52.2 86.6 L51.8 89.6 C55 88.8 58.8 88.8 62 89.6 Z" fill="#F2C94C"></path><path d="M44.4 87.2 C46 87.3 47 87.4 47.4 87.6 C47.8 90.8 48 93.6 48 96.2 C48 97.6 47.4 98.6 46.2 99.2 C46.8 96.6 46.6 93.6 46 90.4 C45.6 89.2 45 88.1 44.4 87.2 Z" fill="#1A1128" opacity="0.16"></path><path d="M55.6 87.2 C54 87.3 53 87.4 52.6 87.6 C52.2 90.8 52 93.6 52 96.2 C52 97.6 52.6 98.6 53.8 99.2 C53.2 96.6 53.4 93.6 54 90.4 C54.4 89.2 55 88.1 55.6 87.2 Z" fill="#1A1128" opacity="0.16"></path><path d="M36.4 96.4 C39.6 95.8 45 95.8 48 96.4 C48 98.8 46 99.9 42.4 99.9 C38.6 99.9 36.4 98.8 36.4 96.4 Z" fill="#3F7C5C"></path><path d="M63.6 96.4 C60.4 95.8 55 95.8 52 96.4 C52 98.8 54 99.9 57.6 99.9 C61.4 99.9 63.6 98.8 63.6 96.4 Z" fill="#3F7C5C"></path>',
    },
    "trainers": {
        "name": "Trainers",
        "emoji": "👟",
        "cost": 90,
        "category": "shoes",
        "tile_viewbox": "33 85 34 16",
        "svg": '<path d="M37 88.2 C40.4 87.6 44.4 87.8 46.6 88.8 C47.6 91.6 48.4 94 49.4 96 C50 97.2 49 98.4 46.6 98.6 C42 99 38 98.8 36.4 98 C35.2 97.4 35 95.4 35.4 93.2 C35.8 91.2 36.4 89.6 37 88.2 Z" fill="#F5EDD6"></path><path d="M63 88.2 C59.6 87.6 55.6 87.8 53.4 88.8 C52.4 91.6 51.6 94 50.6 96 C50 97.2 51 98.4 53.4 98.6 C58 99 62 98.8 63.6 98 C64.8 97.4 65 95.4 64.6 93.2 C64.2 91.2 63.6 89.6 63 88.2 Z" fill="#F5EDD6"></path><path d="M38.2 91.6 C41.4 92.8 44.6 94.8 47.4 97.2 L48.8 94.6 C46 92.4 42.6 90.4 39 89.2 Z" fill="#E8845C"></path><path d="M61.8 91.6 C58.6 92.8 55.4 94.8 52.6 97.2 L51.2 94.6 C54 92.4 57.4 90.4 61 89.2 Z" fill="#E8845C"></path><path d="M38.8 88.6 L45 89.8 L44.6 91.2 L38.4 90 Z" fill="#C4BFDF"></path><path d="M61.2 88.6 L55 89.8 L55.4 91.2 L61.6 90 Z" fill="#C4BFDF"></path><path d="M35.2 96.2 C38.6 95.6 45.6 96 49.2 96.8 C49.8 97.8 49 98.8 46.6 99 C42 99.4 38 99.2 36.4 98.4 C35.4 98 35.1 97.2 35.2 96.2 Z" fill="#1A1128"></path><path d="M64.8 96.2 C61.4 95.6 54.4 96 50.8 96.8 C50.2 97.8 51 98.8 53.4 99 C58 99.4 62 99.2 63.6 98.4 C64.6 98 64.9 97.2 64.8 96.2 Z" fill="#1A1128"></path>',
    },
    "hiking_boots": {
        "name": "Hiking Boots",
        "emoji": "🥾",
        "cost": 170,
        "category": "shoes",
        "tile_viewbox": "33 84 34 17",
        "svg": '<path d="M37.6 86.8 C41 86.2 44.8 86.4 47 87.4 C47.6 90.8 48.4 93.8 49.2 96.2 C49.8 97.6 48.6 98.8 46 99 C41.6 99.4 37.6 99.2 36 98.4 C34.8 97.8 34.6 95.4 35.2 92.6 C35.8 90.2 36.6 88.2 37.6 86.8 Z" fill="#B85A36"></path><path d="M62.4 86.8 C59 86.2 55.2 86.4 53 87.4 C52.4 90.8 51.6 93.8 50.8 96.2 C50.2 97.6 51.4 98.8 54 99 C58.4 99.4 62.4 99.2 64 98.4 C65.2 97.8 65.4 95.4 64.8 92.6 C64.2 90.2 63.4 88.2 62.4 86.8 Z" fill="#B85A36"></path><path d="M37.2 86.4 C40.6 85.6 44.6 85.8 47.4 86.8 L47.8 89.2 C44.6 88.2 40.6 88 37.4 88.8 Z" fill="#E9DDBE"></path><path d="M62.8 86.4 C59.4 85.6 55.4 85.8 52.6 86.8 L52.2 89.2 C55.4 88.2 59.4 88 62.6 88.8 Z" fill="#E9DDBE"></path><path d="M38.6 90.2 L45.6 91.8 L45.2 93.2 L38.2 91.6 Z" fill="#F5EDD6"></path><path d="M39 93.4 L46.4 95 L46 96.4 L38.6 94.8 Z" fill="#F5EDD6"></path><path d="M61.4 90.2 L54.4 91.8 L54.8 93.2 L61.8 91.6 Z" fill="#F5EDD6"></path><path d="M61 93.4 L53.6 95 L54 96.4 L61.4 94.8 Z" fill="#F5EDD6"></path><path d="M34.8 95.6 C38.4 95 46 95.4 49.6 96.2 C50.2 97.8 48.8 99 46 99.2 C41.6 99.6 37.6 99.4 36 98.6 C35 98.2 34.7 96.8 34.8 95.6 Z" fill="#1A1128"></path><path d="M65.2 95.6 C61.6 95 54 95.4 50.4 96.2 C49.8 97.8 51.2 99 54 99.2 C58.4 99.6 62.4 99.4 64 98.6 C65 98.2 65.3 96.8 65.2 95.6 Z" fill="#1A1128"></path><path d="M37.4 99.2 L37.4 96.6 L39.4 96.6 L39.4 99.2 Z" fill="#F5EDD6" opacity="0.28"></path><path d="M42.6 99.4 L42.6 96.8 L44.6 96.8 L44.6 99.4 Z" fill="#F5EDD6" opacity="0.28"></path><path d="M60.6 99.2 L60.6 96.6 L62.6 96.6 L62.6 99.2 Z" fill="#F5EDD6" opacity="0.28"></path><path d="M55.4 99.4 L55.4 96.8 L57.4 96.8 L57.4 99.4 Z" fill="#F5EDD6" opacity="0.28"></path>',
    },
    "roller_skates": {
        "name": "Roller Skates",
        "emoji": "🛼",
        "cost": 320,
        "category": "shoes",
        "tile_viewbox": "33 84 34 18",
        "svg": '<path d="M38 86.8 C41.4 86.2 45 86.4 47.4 87.2 C47.8 90.2 48 92.8 48 94.8 L36.4 94.8 C36.6 91.8 37.2 89 38 86.8 Z" fill="#C4BFDF"></path><path d="M62 86.8 C58.6 86.2 55 86.4 52.6 87.2 C52.2 90.2 52 92.8 52 94.8 L63.6 94.8 C63.4 91.8 62.8 89 62 86.8 Z" fill="#C4BFDF"></path><path d="M37.4 89.8 C41 89 44.8 89 48 89.8 L48 92 C44.8 91.2 41 91.2 37.2 92 Z" fill="#E87EA1"></path><path d="M62.6 89.8 C59 89 55.2 89 52 89.8 L52 92 C55.2 91.2 59 91.2 62.8 92 Z" fill="#E87EA1"></path><path d="M44.6 87 C46.2 87.1 47.2 87.2 47.4 87.4 C47.8 90.4 48 92.8 48 94.8 L46 94.8 C46 92.4 45.6 89.6 44.6 87 Z" fill="#1A1128" opacity="0.14"></path><path d="M55.4 87 C53.8 87.1 52.8 87.2 52.6 87.4 C52.2 90.4 52 92.8 52 94.8 L54 94.8 C54 92.4 54.4 89.6 55.4 87 Z" fill="#1A1128" opacity="0.14"></path><path d="M35.4 94.6 C39 94 45.6 94 49 94.6 L49 96.6 C45.6 97.2 39 97.2 35.4 96.6 Z" fill="#8E87B8"></path><path d="M64.6 94.6 C61 94 54.4 94 51 94.6 L51 96.6 C54.4 97.2 61 97.2 64.6 96.6 Z" fill="#8E87B8"></path><circle cx="38.4" cy="98.2" r="2.3" fill="#F2C94C"></circle><circle cx="46" cy="98.2" r="2.3" fill="#F2C94C"></circle><circle cx="54" cy="98.2" r="2.3" fill="#F2C94C"></circle><circle cx="61.6" cy="98.2" r="2.3" fill="#F2C94C"></circle><circle cx="38.4" cy="98.2" r="0.95" fill="#B8901F"></circle><circle cx="46" cy="98.2" r="0.95" fill="#B8901F"></circle><circle cx="54" cy="98.2" r="0.95" fill="#B8901F"></circle><circle cx="61.6" cy="98.2" r="0.95" fill="#B8901F"></circle>',
    },
    "ice_cream": {
        "name": "Ice Cream",
        "emoji": "🍦",
        "cost": 45,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><path d="M73.5 65 L86.5 65 L80 83 Z" fill="#D9A441"></path><path d="M73.5 65 L86.5 65 L80 83 Z" fill="#1A1128" opacity="0.12"></path><circle cx="76.3" cy="61.5" r="5.2" fill="#E87EA1"></circle><circle cx="83.7" cy="61.5" r="5.2" fill="#F5EDD6"></circle><circle cx="80" cy="56.5" r="5.4" fill="#7EC8A4"></circle></g>',
    },
    "walkie_talkie": {
        "name": "Walkie Talkie",
        "emoji": "📻",
        "cost": 90,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><rect x="72.5" y="58" width="15" height="24" rx="2.5" fill="#2D1B69"></rect><rect x="75.5" y="61" width="9" height="6" rx="1" fill="#7EC8A4"></rect><circle cx="77.5" cy="72" r="1.7" fill="#C4BFDF"></circle><circle cx="82.5" cy="72" r="1.7" fill="#C4BFDF"></circle><circle cx="77.5" cy="77" r="1.7" fill="#C4BFDF"></circle><circle cx="82.5" cy="77" r="1.7" fill="#C4BFDF"></circle><rect x="83" y="48" width="2.6" height="11" rx="1.3" fill="#1A1128"></rect></g>',
    },
    "microphone": {
        "name": "Microphone",
        "emoji": "🎤",
        "cost": 320,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><rect x="78.4" y="65" width="3.2" height="18" rx="1.6" fill="#2B2B2B"></rect><circle cx="80" cy="60.5" r="7.2" fill="#8E87B8"></circle><circle cx="80" cy="60.5" r="4.8" fill="#C4BFDF"></circle><rect x="76" y="81" width="8" height="3.2" rx="1.6" fill="#1A1128"></rect></g>',
    },
    "lollipop": {
        "name": "Lollipop",
        "emoji": "🍭",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><rect x="78.8" y="63" width="2.6" height="20" rx="1.3" fill="#F5EDD6"></rect><circle cx="80" cy="59.5" r="8.2" fill="#E87EA1"></circle><circle cx="80" cy="59.5" r="5.4" fill="#F5EDD6"></circle><circle cx="80" cy="59.5" r="2.7" fill="#E87EA1"></circle></g>',
    },
    "drumsticks": {
        "name": "Drumsticks",
        "emoji": "🥁",
        "cost": 90,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><g transform="rotate(-11 75.5 69)"><rect x="74" y="57" width="3" height="26" rx="1.5" fill="#D9A441"></rect><circle cx="75.5" cy="56" r="2.8" fill="#B8901F"></circle></g><g transform="rotate(11 84.5 69)"><rect x="83" y="57" width="3" height="26" rx="1.5" fill="#D9A441"></rect><circle cx="84.5" cy="56" r="2.8" fill="#B8901F"></circle></g></g>',
    },
    "magnifying_glass": {
        "name": "Magnifying Glass",
        "emoji": "🔍",
        "cost": 90,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><circle cx="80" cy="60" r="7.6" fill="#C4BFDF" opacity="0.55"></circle><circle cx="80" cy="60" r="7.6" fill="none" stroke="#8B5A2B" stroke-width="3"></circle><rect x="78.5" y="67" width="3" height="16" rx="1.5" fill="#8B5A2B"></rect></g>',
    },
    "water_bottle": {
        "name": "Water Bottle",
        "emoji": "🍶",
        "cost": 20,
        "category": "held",
        "tile_viewbox": "64 44 32 44",
        "svg": '<g transform="rotate(14 80 66)"><rect x="76" y="51" width="8" height="5.5" rx="1.5" fill="#3F7C5C"></rect><rect x="74" y="56" width="12" height="27" rx="3.5" fill="#7EC8A4"></rect><rect x="74" y="64" width="12" height="6.5" fill="#F5EDD6"></rect><rect x="76.4" y="59" width="2.5" height="20" rx="1.2" fill="#FFFFFF" opacity="0.35"></rect></g>',
    },
    "binoculars": {
        "name": "Binoculars",
        "emoji": "🔭",
        "cost": 320,
        "category": "gear",
        "tile_viewbox": "38 42 32 42",
        "svg": '<path d="M42 47 L56 65 L66 47" fill="none" stroke="#3D2A85" stroke-width="2.5" stroke-linecap="round"></path><rect x="47.5" y="63" width="17" height="12.5" rx="2.2" fill="#2D1B69"></rect><circle cx="51.5" cy="69.2" r="3.6" fill="#1A1128"></circle><circle cx="60.5" cy="69.2" r="3.6" fill="#1A1128"></circle><circle cx="51.5" cy="69.2" r="2" fill="#5B93C4"></circle><circle cx="60.5" cy="69.2" r="2" fill="#5B93C4"></circle>',
    },
    "camera": {
        "name": "Camera",
        "emoji": "📷",
        "cost": 320,
        "category": "gear",
        "tile_viewbox": "38 42 32 42",
        "svg": '<path d="M42 47 L56 65 L66 47" fill="none" stroke="#2B2B2B" stroke-width="2.5" stroke-linecap="round"></path><rect x="46.5" y="63" width="19" height="13.5" rx="2.5" fill="#2B2B2B"></rect><circle cx="56" cy="69.8" r="4.8" fill="#5B93C4"></circle><circle cx="56" cy="69.8" r="2.5" fill="#1A1128"></circle><rect x="61" y="60.2" width="4.2" height="3.2" rx="1" fill="#2B2B2B"></rect>',
    },
    "compass": {
        "name": "Compass",
        "emoji": "🧭",
        "cost": 170,
        "category": "gear",
        "tile_viewbox": "38 42 32 42",
        "svg": '<path d="M42 47 L56 65 L66 47" fill="none" stroke="#8B5A2B" stroke-width="2.5" stroke-linecap="round"></path><circle cx="56" cy="69.5" r="8.2" fill="#F5EDD6"></circle><circle cx="56" cy="69.5" r="8.2" fill="none" stroke="#8B5A2B" stroke-width="2"></circle><path d="M56 63 L58.6 69.5 L56 76 L53.4 69.5 Z" fill="#C0392B"></path>',
    },
    "field_notebook": {
        "name": "Field Notebook",
        "emoji": "📓",
        "cost": 45,
        "category": "gear",
        "tile_viewbox": "38 42 32 42",
        "svg": '<path d="M42 47 L56 65 L66 47" fill="none" stroke="#8B5A2B" stroke-width="2.5" stroke-linecap="round"></path><rect x="48" y="63" width="16" height="17.5" rx="1.5" fill="#F5EDD6"></rect><rect x="48" y="63" width="16" height="17.5" rx="1.5" fill="none" stroke="#8B5A2B" stroke-width="1.5"></rect><path d="M51 68 L61 68 M51 72 L61 72 M51 76 L61 76" stroke="#8E87B8" stroke-width="1"></path>',
    },
    "satchel": {
        "name": "Satchel",
        "emoji": "👜",
        "cost": 45,
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
