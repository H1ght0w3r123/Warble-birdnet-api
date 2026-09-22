# Design Brief: Collector Card Frames, Ten Pack Variants

## Read this first

The ask is ten cards identical to the supplied frame, differing only in the
two corner discs. **An image generator cannot do that, and the failure is not
obvious by eye.** It will return ten cards that each look right on their own
and are all slightly different: the wood grain will redraw, the corner radius
will drift a few pixels, the photo window will move, the nameplate will
change height. The app positions the bird photo and the bird's name against
that frame by measurement, so ten frames with ten geometries means the photo
sits correctly on one pack and wrong on the other nine.

So this brief has two parts.

- **Part A is the ask that works.** Generate the ten *marks* only - the flat
  shape that goes in the disc - and they get composited into the one supplied
  frame. The frame is then literally the same pixels on all ten cards, which
  is what "exact replica" actually requires.
- **Part B is the literal ask**, ten whole cards, with the full specification
  and the checks that would have to pass. It is here in case the marks route
  is not possible, not because it is the better one.

Part A is roughly a tenth of the work for the generator and is the only
version that can be guaranteed correct.

---

# Part A - the ten marks (recommended)

## What to produce

Ten images. Each is one flat silhouette: the pack's symbol, in a single solid
colour, on a transparent background.

- **Canvas:** 440 x 440px, transparent.
- **The mark:** centred, filling about 330px of that 440 (75%), scaled to fit
  whichever of its own dimensions is larger so nothing is cropped or
  stretched.
- **Fill:** one flat colour, `#666E49`. No gradient, no shading, no bevel, no
  drop shadow, no outline. The recolouring happens in the app.
- **Internal gaps:** where two parts of the symbol meet, leave a clear
  transparent gap of at least 8px at this size, so the parts read separately
  rather than merging into one blob. In the supplied card, the acorn's cap and
  its nut are two shapes with a gap between them, and the cracked shell is
  three separate shards. That separation is the whole reason the mark is
  readable.
- **Detail budget:** this mark is drawn at **13 pixels across** in the app.
  Anything thinner than about 1/15th of the mark's width disappears. Draw for
  a rubber stamp, not an illustration.

## The ten marks

Each one is the same subject as the pack's existing icon, flattened:

| # | Pack | Mark |
|---|------|------|
| 1 | Locals | A small bird perched on the roof of a birdhouse |
| 2 | Acrobats | A bird hanging upside down from a twig |
| 3 | Nutcrackers | An acorn with its shell cracking away in shards *(this is the one already drawn in the supplied card - match its treatment)* |
| 4 | Little Loudmouths | A small round bird with sound rays fanning from its beak |
| 5 | Mischiefs | A bird's face wearing a bandit's eye mask |
| 6 | Diggers | A bird's foot scratching at soil, with a few scattered seeds |
| 7 | Sky Divers | A bird in a steep dive, with speed lines |
| 8 | Waterwings | A bird floating on stylised waves |
| 9 | Mucky Puddles | A duckling in a splashing puddle |
| 10 | Wind Surfers | A bird gliding over a curling wave of wind |

## Proportion note

Marks 6 to 10 are the risk. As drawn in the existing icons they are wide, low
bands, and a wide band fitted into a circular disc ends up a couple of pixels
tall. **Draw each mark to roughly fill a square**, stacking or compacting the
composition rather than spreading it horizontally - a bird above a wave rather
than a bird beside a wave.

## File delivery

One PNG per mark, real alpha, named exactly:

```
locals.png  acrobats.png  nutcrackers.png  littleloudmouths.png  mischiefs.png
diggers.png  skydivers.png  waterwings.png  muckypuddles.png  windsurfers.png
```

**No captions, labels, filenames or watermarks anywhere in the image.** Every
previous delivery on this project has arrived with its own filename baked
across the bottom of the picture, and removing it is fiddly because it is the
same tone as the artwork's own white edging.

---

# Part B - ten whole card frames (only if Part A is not possible)

## The source

The supplied card is the master. Everything below is measured off it and is
what a variant has to reproduce, not a description of what it looks like.

| | |
|---|---|
| Canvas | 1024 x 1536px, transparent outside the card |
| Card artwork | 906 x 1394px, sitting at (59, 53) in that canvas |
| Card proportion | 0.6499 (this is load-bearing - the app's card box is built to it) |
| Card corner radius | 69px (7.62% of the card's width) |

All positions below are percentages **of the card artwork**, not of the
canvas, so they survive a resize.

| Element | Position |
|---|---|
| Photo window (the grey panel) | left 5.96%, top 4.52%, width 87.97%, height 56.10% |
| Nameplate (the cream panel) | left 4.19%, top 60.90%, width 91.60%, height 35.80% |
| Top-left disc, centre | x 9.00%, y 5.95% |
| Bottom-right disc, centre | x 91.28%, y 93.15% |
| Disc diameter | 12.14% of card width (110px at 906px) |
| Mark inside the disc | about 74% of the disc's diameter |

## Palette

| | |
|---|---|
| Wood, lit face | `#D87A38` |
| Wood, shadowed outer edge | `#743206` |
| Photo window fill | `#D8CBB7` |
| Nameplate cream | `#F8DFC0` |
| Disc plate cream | `#F7DBBA` |
| Mark | `#666E49` |

## What must be pixel-identical across all ten

Everything except the two discs' contents. Specifically: the wood grain
pattern and its lighting, the card's outline and corner radius, the cream lip
around the photo window, the window's own size and position, the nameplate's
size and position, the discs' size and position, and the discs' rim and plate.

## What changes

Only the symbol inside the two discs, which is the same symbol in both corners
of a given card. Use the ten marks listed in Part A. The bottom-right disc is
**not** rotated - in the supplied card both discs read upright.

## Acceptance checks

A returned set passes only if all of these hold. They are worth checking
before anything is built against the files, because a near-miss is invisible
until the app puts a photo in the window.

1. All ten files are 1024 x 1536 with the card occupying the same 906 x 1394
   box at the same offset.
2. Overlaying any two of the ten and differencing them shows changes **only**
   inside the two discs - nowhere else.
3. The photo window's four edges land within 2px of the master on every card.
4. The nameplate's top edge lands within 2px of the master on every card.
5. Real alpha outside the card. Not a white or checkerboard background
   flattened into the image.
6. No captions, labels, filenames or watermarks.

If check 2 fails - and with a generative model it usually will - the set is
still salvageable: the discs can be cut out of the returned cards and dropped
into the master frame, which is Part A arrived at the long way round.
