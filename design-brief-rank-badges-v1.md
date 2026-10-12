# Design Brief: birder rank badges (v1)

## What this is

Every trophy level a child wins is a leaf, and their leaves add up to a
**birder rank**: eight steps from Hatchling to Master Birder. The rank shows
as a small badge in the top bar beside the feathers, on every screen; on a
ladder of all eight that opens when it's tapped; and on the biggest
celebration in the app, when a child goes up a rank.

Each rank needs **its own badge**, so that going up feels like becoming
something new. For now the app builds them itself (`rankSeal()` in
`static/index.html`): a wooden disc with the rank's number, inside a wreath
of the painted leaf that grows a pair of leaves with every rank and turns
gold for the top two. This brief asks for eight paintings to replace them.

**Nothing in the app needs changing when they arrive.** Each one appears the
moment its file is in `static/` as `icon-rank-<key>-v1.webp` (cut from the
PNG you deliver, kept at 320 px so it's sharp at its biggest), and replaces
the built seal everywhere.

## The eight

| Rank | Leaves | File key | What it could be |
|---|---|---|---|
| Hatchling | 0 | `hatchling` | A cracked egg in a nest, a beak poking out |
| Spotter | 5 | `spotter` | A pair of chunky toy binoculars |
| Tracker | 12 | `tracker` | Bird footprints in mud, a magnifying glass |
| Scout | 25 | `scout` | A little scout's hat with a feather, or a compass |
| Ranger | 40 | `ranger` | A ranger's wide hat, or a walking stick with a map |
| Warden | 60 | `warden` | A wooden birdhouse with a lantern |
| Expert | 85 | `expert` | An open field guide, gold ribbon bookmark |
| Master Birder | 115 | `master-birder` | A golden owl, or a crown of leaves with a bird on it |

The ideas are only starting points. What matters is the **ladder**:

- **They must read as a set, in order.** Same carved wooden disc behind each
  one, same size, same light. A child should be able to put them in order
  without the names: the object gets grander and the wreath round the disc
  fuller with every step, as the built ones do now.
- **Green leaves up to Warden, gold for Expert and Master Birder.** In
  Warble gold means only two things: a rare bird, and a trophy's leaves
  turning gold at its top levels. The top two ranks are the leaves turning
  gold, so they may use gold; nothing below them should.

## Style: match what's already painted

Use the trophy emblems and the trophies' leaves as the reference
(`static/emblem-*.webp`, `static/trophy-l3-v1.webp`, `static/trophy-l7-v1.webp`,
`static/tree-leaf2-v2.webp`).

- Painted and chunky, toy-like, a soft bevel, warm light from the top centre.
- Warm colours from the app: wood orange, cream, leaf green; gold only as
  above.
- One simple object on the disc. No scenes, no backgrounds, **no numbers or
  words** - the app writes the name beside it.

## They're shown big and small

The same picture is used at about **150 px** (the celebration), **54 px**
(the ladder) and **40 px** (the top bar, beside the feather count). So:

- Bold silhouette, few details, nothing thin.
- At 40 px it must still be clear which rank it is, mostly from the size of
  the wreath and its colour. Shrink it and check.
- A rank not reached yet is shown greyed out; it should still read as a
  badge in grey.

## File delivery specification

The same rules as every Warble brief:

1. **One badge per file**, named `icon-rank-<key>_1024x1024.png` (for
   example `icon-rank-master-birder_1024x1024.png`). Any sheet with several
   together is a separate file named `PREVIEW-ONLY`.
2. **The file's pixel size IS the canvas:** exactly 1024 × 1024, square.
3. **Real transparency.** A true alpha channel, not a painted checkerboard.
   Test it on solid red: no squares, no white fringe.
4. **The badge fills the canvas**, about 90%, centred, the wreath included.
5. **Nothing on the art that isn't art.** No text, no numbers, no guides.
6. **PNG, sRGB.** The app converts them itself.
