# Design Brief: small information icons (v1)

> **Delivered** - all 24, as one sheet. Cut into `static/icon-<name>-v1.webp`
> by `tools/build_icons.py` (background made transparent, the printed names
> left off, each 128px tall in its own shape). A redraw of any one is `-v2`.
>
> Since then the bird card's habitat tags were removed (where a bird lives is
> already in its facts), so the five habitat icons (`garden-parks`, `woodland`,
> `wetland-coast`, `farmland`, `towns`) are in `static/` but not shown anywhere.

## What this is

Warble's design language is painted art, never emoji. Almost everything is
painted already. These 24 small icons are the last places that still show a
phone emoji or a plain text symbol (an arrow, a cross, "???"), and each is
waiting for a painting.

**Nothing in the app needs changing when they arrive.** Each one appears the
moment its file is in `static/` as `icon-<name>-v1.webp` (from the PNG you
deliver). Until then the emoji or symbol stays as a stand-in. A later redraw is
`-v2`, and the newest version always wins.

## The 24 icons

| File name | Stands in for | Where it shows | Idea |
|---|---|---|---|
| `weight` | ⚖️ | Bird card fact tile: "9g WEIGHT" | A little balance scale, or a bird on a kitchen scale |
| `length` | 📏 | Bird card fact tile: "11cm LENGTH" | A wooden ruler |
| `wingspan` | ↔️ | Bird card fact tile: "19cm WINGSPAN" | Two spread wings with an arrow tip to tip |
| `habitat` | 🏞️ | Bird card fact tile: "WHERE IT LIVES" | A tree with a little nest |
| `diet` | 🍽️ | Bird card fact tile: "WHAT IT EATS" | A worm and a seed, or a bird feeder |
| `garden-parks` | 🌳 | Habitat tag on the bird card | A round leafy tree |
| `woodland` | 🌲 | Habitat tag | Two pine trees |
| `wetland-coast` | 🌊 | Habitat tag | A wave with reeds |
| `farmland` | 🌾 | Habitat tag | A wheat stalk |
| `towns` | 🏘️ | Habitat tag | Two little houses with chimneys |
| `tip-sunrise` | 🌅 | Warbling tip "Early birds sing loudest" | A sun coming up over a hill |
| `tip-quiet` | 🤫 | Tip "Stay still and quiet" | A finger to lips, or a sleeping owl |
| `tip-places` | 📍 | Tip "Try lots of different places" | A map with a dotted path |
| `tip-close` | 🎧 | Tip "Get close, but not too close" | A phone held up towards a bird on a branch |
| `tip-rain` | 🌦️ | Tip "Birds sing on rainy days too" | A cloud with rain and a peeping sun |
| `tip-calm` | 🧘 | Tip "It's okay to hear nothing" | An empty nest, calm and cosy |
| `pin` | 📍 | Before a place's name ("📍 Back Garden") | A wooden map pin |
| `lock` | 🔒 | Corner of a locked Guess the Song level | A small wooden padlock |
| `camera` | 📷 | Corner of a game tile showing the child's own photo | A chunky toy camera |
| `back` | ← | "Back" at the top of inner screens | A carved wooden arrow pointing left |
| `forward` | → | "Learn more", "More warbling tips", "Collection card" | The same arrow pointing right |
| `close` | ✕ | Removing a named place in Settings | A small carved cross |
| `pause` | ⏸ | "Stop" while a bird's call is playing | Two chunky wooden bars, to pair with the painted play button |
| `mystery` | ??? | The name sign of a trophy not yet won | A question mark carved in wood, or a closed seed pod |

## Style: match what's already painted

Use the nav icons, the mic and the trophy emblems as the reference
(`static/nav-*.webp`, `static/mic-v2.webp`, `static/emblem-*.webp`).

- **Painted and chunky.** Toy-like shapes, a soft bevel, warm light from the
  top centre.
- **Warm colours from the app.** Wood orange, cream, leaf green, and sky blue
  where water or sky needs it. **No gold**: in Warble, gold only ever means a
  rare bird.
- **One simple object each.** No scenes, no backgrounds.

## They're tiny

These show at the size of the words beside them: **about 20-35 pixels** on a
phone. Some sit on cream (fact tiles, tips, place buttons), and the habitat
icons sit on a **green** tag. So:

- Bold silhouettes, few details, nothing thin.
- Each must still read at 20 px, on cream **and** on green.
- A dark outline or edge, so it doesn't vanish on either background.

## File delivery specification

The same rules as every Warble brief:

1. **One icon per file**, named exactly as the table:
   `icon-<name>_512x512.png` (for example `icon-weight_512x512.png`). Any
   sheet with several together is a separate file named `PREVIEW-ONLY`.
2. **The file's pixel size IS the canvas:** exactly 512 × 512.
3. **Real transparency.** A true alpha channel, not a painted checkerboard.
   Test it on solid red: no squares, no white fringe.
4. **The icon fills the canvas**, about 90%, centred.
5. **Nothing on the art that isn't art.** No text, no guides.
6. **PNG, sRGB.** The app converts them itself.

## Before sending

Shrink each one to 20 px and look at it on cream (#FBEAD1) and on green
(#7EC8A4). If you can't tell what it is, simplify it.
