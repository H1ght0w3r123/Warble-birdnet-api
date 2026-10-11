# Design Brief: Hoot-tique Restocks — seasonal drops (v1)

## Why

Feathers keep coming in long after a child has bought what they want. The
Hoot-tique has 70 items costing 1,880 feathers, and once they're all owned
every reward pays feathers there is nothing left to spend on. The nine
special colours (10 feathers each) help at the margin. The real fix is that
the shop keeps getting new things.

So the Hoot-tique **restocks four times a year**, with a small themed drop
each season. Each drop is about **10 items worth roughly 200–250 feathers
in total**: about five weeks of feathers for the keen child who is first to
own most of the shop (6 warbles a week earns about 45), and about six
weeks for a child warbling four times a week (about 35). Either way a drop
is bought before the next one lands, so feathers stay worth saving without
the shop ever feeling out of reach. (Earning rates measured with
`tools/economy_sim.py`.)

## What a drop is

| | |
|---|---|
| Items per drop | 8–12 |
| Spread | every category, not one: about 3 hats, 2 glasses, 2 neck, 2 held, 1 shoes |
| Prices | the existing bands only: 5 · 10 · 20 · 40 · 75. One 75 "dream" item per drop at most |
| Total cost | about 200–250 feathers |
| When | 1 March, 1 June, 1 September, 1 December |
| Theme | the season (ideas below), so a drop feels like an event |

**Theme ideas.** Use these as starting points, not a shopping list:

- **Spring:** blossom crown, daffodil glasses, rain hat, nest-twig scarf, watering can (held), wellies with ladybirds
- **Summer:** sun visor, starfish sunglasses, flower lei, ice-lolly (held), bucket and spade (held), flip-flop sandals
- **Autumn:** acorn cap, leaf-frame glasses, knitted scarf, conker on a string (held), welly boots in conker brown
- **Winter:** bobble hat, snowflake glasses, fluffy earmuffs (hat), robin-red scarf, mug of cocoa (held), snow boots

## What the app already does — do NOT redraw these

- The **eight birds** (Classic, Cardinal, Parrot, Kingfisher, Owl, Duckling, Penguin, Woodpecker), their colours and their poses.
- **Prices and names.** The app writes all words; no text in any file.
- **Shop tiles.** The app crops each item's own picture into its tile.

## File delivery specification — the same rules as every Warble brief

1. **One item per file.** Any "all together" picture is a separate file named `PREVIEW-ONLY`.
2. **The file's pixel size IS the canvas.** It is exactly the size given below, not a bigger image of the same shape.
3. **Real transparency.** A true alpha channel, not a painted checkerboard. Test it on solid red: no squares.
4. **Nothing on the art that isn't art.** No guide lines, dots, labels or measurements.
5. **No text.**
6. **PNG, sRGB, full resolution.** The app converts them itself.

**Style:** the same as the shop today. Painted, chunky, toy-like shapes
with a soft bevel, warm light from the top centre, and colours that sit
well next to the existing 70.

## The canvases, by category

Match the files already in `static/accessories/` exactly. They are the
reference for scale and placement.

### Hats — the most work, because they are fitted per bird

- **One tile picture:** `hat_<name>_800x800.png` on an 800 × 800 canvas, drawn on the average head, like `hats/beret.webp`.
- **Eight fitted pictures,** one per bird: `hat_<name>_<bird>_800x800.png`, each on that bird's own 800 × 800 canvas. Place each hat exactly where it sits on that bird, using the existing `hats/<bird>/*.webp` as the guide for where a head is.
- **Say whether it hides the crest.** A hat that would have the bird's crest or tuft poking through needs the crest hidden. Say yes or no per hat; the app already has the crest masks.

### Glasses

- `glasses_<name>_447x165.png`, the same canvas as `glasses_aviator_sunglasses-v2.webp`.
- Lenses centred on the two eyes, the same span as the existing glasses.

### Neck

- `neck_<name>_444x202.png`, the same canvas as `neck_beaded_necklace.webp`.

### Held

- `held_<name>_324x430.png`, the same canvas as `held_baby_rattle.webp`.
- It hangs from the bird's right wing; the grip goes at the top of the canvas.

### Shoes

- A pair, as a left and right file: `shoes_<name>-l_255x210.png` and `shoes_<name>-r_255x210.png`, like `shoes_ballet_slippers-l-v2.webp`.

## Also needed: one trophy emblem

The new **High Five** trophy needs its own carved-wood emblem. It has its
own brief: `design-brief-high-five-emblem-v1.md`.

## Before sending

Put each item on all eight birds in the app's Dress Up preview (or on the
reference canvases) and check it sits right on every one. A hat that floats
above the Owl or swallows the Penguin's eyes isn't finished.
