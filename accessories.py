"""
Dress Up catalog. Each accessory is a small SVG snippet positioned to
overlay the existing 100x100 avatar illustration (see avatarSvg() in
the frontend) - same viewBox, same coordinate space.
"""

ACCESSORIES = {
    "top_hat": {
        "name": "Top Hat",
        "emoji": "🎩",
        "cost": 30,
        "svg": '<rect x="34" y="8" width="14" height="14" rx="1" fill="#2B2B2B"/><rect x="28" y="20" width="26" height="4" rx="2" fill="#2B2B2B"/>',
    },
    "scarf": {
        "name": "Cosy Scarf",
        "emoji": "🧣",
        "cost": 20,
        "svg": '<path d="M26 54 Q40 64 58 52 L54 66 Q40 72 30 64 Z" fill="#C0392B"/>',
    },
    "glasses": {
        "name": "Cool Glasses",
        "emoji": "🕶️",
        "cost": 25,
        "svg": '<circle cx="33" cy="32" r="7" fill="none" stroke="#2B2B2B" stroke-width="2.5"/><circle cx="49" cy="28" r="7" fill="none" stroke="#2B2B2B" stroke-width="2.5"/><line x1="40" y1="30" x2="42" y2="29" stroke="#2B2B2B" stroke-width="2.5"/>',
    },
    "bow": {
        "name": "Fancy Bow",
        "emoji": "🎀",
        "cost": 15,
        "svg": '<path d="M30 58 L38 54 L38 62 Z" fill="#E84393"/><path d="M46 58 L38 54 L38 62 Z" fill="#E84393"/><circle cx="38" cy="58" r="3" fill="#C2185B"/>',
    },
    "crown": {
        "name": "Golden Crown",
        "emoji": "👑",
        "cost": 80,
        "svg": '<path d="M30 20 L34 8 L40 16 L46 6 L52 16 L58 8 L62 20 Z" fill="#F2C94C" stroke="#B8901F" stroke-width="1"/>',
    },
    "flower_crown": {
        "name": "Flower Crown",
        "emoji": "🌸",
        "cost": 40,
        "svg": '<circle cx="28" cy="24" r="4" fill="#E87EA1"/><circle cx="24" cy="30" r="4" fill="#F2C94C"/><circle cx="30" cy="34" r="4" fill="#E87EA1"/><circle cx="34" cy="20" r="4" fill="#F2C94C"/>',
    },
}
