"""
Dress Up catalog. Each accessory is a small SVG snippet positioned to
overlay the existing 100x100 avatar illustration (see avatarSvg() in
the frontend) - same viewBox, same coordinate space.

Organised into 3 categories - hats, scarves, binoculars. Feather
accessories live inside "hats" rather than being their own category.
"""

ACCESSORIES = {
    "top_hat": {
        "name": "Top Hat",
        "emoji": "🎩",
        "cost": 30,
        "category": "hats",
        "svg": '<rect x="34" y="8" width="14" height="14" rx="1" fill="#2B2B2B"/><rect x="28" y="20" width="26" height="4" rx="2" fill="#2B2B2B"/>',
    },
    "crown": {
        "name": "Golden Crown",
        "emoji": "👑",
        "cost": 80,
        "category": "hats",
        "svg": '<path d="M30 20 L34 8 L40 16 L46 6 L52 16 L58 8 L62 20 Z" fill="#F2C94C" stroke="#B8901F" stroke-width="1"/>',
    },
    "flower_crown": {
        "name": "Flower Crown",
        "emoji": "🌸",
        "cost": 40,
        "category": "hats",
        "svg": '<circle cx="28" cy="24" r="4" fill="#E87EA1"/><circle cx="24" cy="30" r="4" fill="#F2C94C"/><circle cx="30" cy="34" r="4" fill="#E87EA1"/><circle cx="34" cy="20" r="4" fill="#F2C94C"/>',
    },
    "feather": {
        "name": "Tucked Feather",
        "emoji": "🪶",
        "cost": 15,
        "category": "hats",
        "svg": '<path d="M40 6 Q46 14 40 24 Q34 14 40 6 Z" fill="#E8845C" stroke="#B85A36" stroke-width="1"/>',
    },
    "baseball_cap": {
        "name": "Baseball Cap",
        "emoji": "🧢",
        "cost": 10,
        "category": "hats",
        "svg": '<path d="M28 22 Q40 8 54 20 L54 24 L28 24 Z" fill="#3B82C4"/><ellipse cx="30" cy="24" rx="10" ry="3" fill="#2C6396"/>',
    },
    "sun_hat": {
        "name": "Sun Hat",
        "emoji": "👒",
        "cost": 20,
        "category": "hats",
        "svg": '<ellipse cx="41" cy="20" rx="22" ry="6" fill="#F0D9A8"/><ellipse cx="41" cy="14" rx="10" ry="8" fill="#F0D9A8"/>',
    },
    "party_hat": {
        "name": "Party Hat",
        "emoji": "🥳",
        "cost": 12,
        "category": "hats",
        "svg": '<path d="M41 4 L52 24 L30 24 Z" fill="#E84393"/><circle cx="41" cy="4" r="3" fill="#F2C94C"/>',
    },
    "wizard_hat": {
        "name": "Wizard Hat",
        "emoji": "🧙",
        "cost": 50,
        "category": "hats",
        "svg": '<path d="M41 2 L50 24 L32 24 Z" fill="#5B3E9E"/><ellipse cx="41" cy="24" rx="16" ry="3" fill="#5B3E9E"/><circle cx="41" cy="12" r="2" fill="#F2C94C"/>',
    },
    "pirate_hat": {
        "name": "Pirate Hat",
        "emoji": "🏴",
        "cost": 45,
        "category": "hats",
        "svg": '<path d="M24 20 Q41 4 58 20 Q41 14 24 20 Z" fill="#2B2B2B"/><circle cx="41" cy="14" r="2" fill="#fff"/>',
    },
    "pith_helmet": {
        "name": "Explorer Helmet",
        "emoji": "🪖",
        "cost": 35,
        "category": "hats",
        "svg": '<ellipse cx="41" cy="16" rx="16" ry="10" fill="#D8C9A3"/><ellipse cx="41" cy="24" rx="20" ry="4" fill="#C4B48D"/>',
    },
    "antlers": {
        "name": "Reindeer Antlers",
        "emoji": "🦌",
        "cost": 25,
        "category": "hats",
        "svg": '<path d="M30 20 L26 8 M26 8 L22 6 M26 8 L30 4" stroke="#8B5A2B" stroke-width="2" fill="none"/><path d="M52 20 L56 8 M56 8 L60 6 M56 8 L52 4" stroke="#8B5A2B" stroke-width="2" fill="none"/>',
    },
    "scarf": {
        "name": "Cosy Scarf",
        "emoji": "🧣",
        "cost": 20,
        "category": "scarves",
        "svg": '<path d="M26 54 Q40 64 58 52 L54 66 Q40 72 30 64 Z" fill="#C0392B"/>',
    },
    "bow": {
        "name": "Fancy Bow",
        "emoji": "🎀",
        "cost": 15,
        "category": "scarves",
        "svg": '<path d="M30 58 L38 54 L38 62 Z" fill="#E84393"/><path d="M46 58 L38 54 L38 62 Z" fill="#E84393"/><circle cx="38" cy="58" r="3" fill="#C2185B"/>',
    },
    "bow_tie": {
        "name": "Bow Tie",
        "emoji": "🎗️",
        "cost": 20,
        "category": "scarves",
        "svg": '<path d="M32 58 L38 55 L38 61 Z" fill="#2C3444"/><path d="M44 58 L38 55 L38 61 Z" fill="#2C3444"/><rect x="36" y="56" width="4" height="4" fill="#1A1128"/>',
    },
    "necklace": {
        "name": "Beaded Necklace",
        "emoji": "📿",
        "cost": 25,
        "category": "scarves",
        "svg": '<circle cx="30" cy="58" r="2.5" fill="#E8845C"/><circle cx="35" cy="61" r="2.5" fill="#F2C94C"/><circle cx="41" cy="62" r="2.5" fill="#7EC8A4"/><circle cx="47" cy="61" r="2.5" fill="#F2C94C"/><circle cx="52" cy="58" r="2.5" fill="#E8845C"/>',
    },
    "medal": {
        "name": "Golden Medal",
        "emoji": "🏅",
        "cost": 35,
        "category": "scarves",
        "svg": '<path d="M36 50 L41 60 L46 50" stroke="#C0392B" stroke-width="3" fill="none"/><circle cx="41" cy="64" r="7" fill="#F2C94C" stroke="#B8901F" stroke-width="1"/>',
    },
    "pearls": {
        "name": "Pearl Necklace",
        "emoji": "🤍",
        "cost": 40,
        "category": "scarves",
        "svg": '<circle cx="30" cy="58" r="3" fill="#F5F0E8"/><circle cx="37" cy="62" r="3" fill="#F5F0E8"/><circle cx="45" cy="62" r="3" fill="#F5F0E8"/><circle cx="52" cy="58" r="3" fill="#F5F0E8"/>',
    },
    "striped_scarf": {
        "name": "Striped Scarf",
        "emoji": "🧣",
        "cost": 18,
        "category": "scarves",
        "svg": '<path d="M26 54 Q40 64 58 52 L54 66 Q40 72 30 64 Z" fill="#3B82C4"/><path d="M30 58 L34 68 M40 60 L42 70 M50 58 L48 66" stroke="#fff" stroke-width="2"/>',
    },
    "star_necklace": {
        "name": "Star Necklace",
        "emoji": "⭐",
        "cost": 22,
        "category": "scarves",
        "svg": '<path d="M32 55 Q40 62 48 55" stroke="#F2C94C" stroke-width="1.5" fill="none"/><path d="M40 60 L42 65 L47 65 L43 68 L45 73 L40 70 L35 73 L37 68 L33 65 L38 65 Z" fill="#F2C94C"/>',
    },
    "binoculars": {
        "name": "Binoculars",
        "emoji": "🔭",
        "cost": 25,
        "category": "binoculars",
        "svg": '<circle cx="33" cy="34" r="7" fill="none" stroke="#2B2B2B" stroke-width="3"/><circle cx="49" cy="34" r="7" fill="none" stroke="#2B2B2B" stroke-width="3"/><rect x="38" y="31" width="6" height="6" fill="#2B2B2B"/>',
    },
    "camera": {
        "name": "Camera",
        "emoji": "📷",
        "cost": 30,
        "category": "binoculars",
        "svg": '<rect x="30" y="48" width="22" height="16" rx="2" fill="#2B2B2B"/><circle cx="41" cy="56" r="6" fill="#5B93C4"/><rect x="36" y="44" width="8" height="5" fill="#2B2B2B"/>',
    },
    "compass": {
        "name": "Compass",
        "emoji": "🧭",
        "cost": 20,
        "category": "binoculars",
        "svg": '<circle cx="41" cy="56" r="10" fill="#F5EDD6" stroke="#8B5A2B" stroke-width="2"/><path d="M41 48 L44 56 L41 64 L38 56 Z" fill="#C0392B"/>',
    },
    "magnifying_glass": {
        "name": "Magnifying Glass",
        "emoji": "🔍",
        "cost": 15,
        "category": "binoculars",
        "svg": '<circle cx="36" cy="40" r="9" fill="none" stroke="#8B5A2B" stroke-width="3"/><line x1="42" y1="46" x2="50" y2="54" stroke="#8B5A2B" stroke-width="3"/>',
    },
    "backpack": {
        "name": "Explorer Backpack",
        "emoji": "🎒",
        "cost": 35,
        "category": "binoculars",
        "svg": '<rect x="28" y="46" width="26" height="24" rx="6" fill="#5F7C5C"/><rect x="34" y="42" width="14" height="8" rx="3" fill="#3F7C5C"/>',
    },
    "notebook": {
        "name": "Field Notebook",
        "emoji": "📓",
        "cost": 18,
        "category": "binoculars",
        "svg": '<rect x="30" y="48" width="18" height="22" rx="1" fill="#F5EDD6" stroke="#8B5A2B" stroke-width="1.5"/><line x1="34" y1="54" x2="44" y2="54" stroke="#8B5A2B" stroke-width="1"/><line x1="34" y1="58" x2="44" y2="58" stroke="#8B5A2B" stroke-width="1"/>',
    },
}

CATEGORIES = [
    {"id": "hats", "name": "Hats", "icon": "🎩"},
    {"id": "scarves", "name": "Scarves", "icon": "🧣"},
    {"id": "binoculars", "name": "Binoculars", "icon": "🔭"},
]

