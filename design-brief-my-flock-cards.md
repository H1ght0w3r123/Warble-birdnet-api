# Design Brief: My Flock Card Frames (three variants)

## Read this first — these cards are not a fixed shape

The collector card worked as one flat picture because that card is always
66 x 101.5px. **A My Flock card is never the same shape twice.** Its width
comes from the screen it is on and its height from how many lines the bird's
name needs, and the two are unrelated. Measured in the real app:

| Variant | Width range | Height range | Shape (w÷h) varies from |
|---|---|---|---|
| Compact card (3 up) | 89 – 126px | 97 – 122px | **0.73 to 1.30** |
| Large card (2 up) | 138 – 193px | 154 – 169px | **0.82 to 1.25** |
| History row | 288 – 398px | 62px (fixed) | **4.65 to 6.42** |

A single picture stretched to fill that would be squashed nearly to half on
one phone and stretched half again on another. On a 390px phone today, a
third of the cards are the taller kind, because a third of these birds have
names that wrap — Common Ringed Plover, European Green Woodpecker.

So these three are **not pictures of cards. They are frames that get cut into
nine pieces**: the four corners hold their shape, the four edges repeat along
their length, and the middle is a flat fill. That is a standard thing the
browser does (CSS `border-image`), and it is what lets one drawing serve a
card of any size without distorting. It only works if the art is drawn for
it, which is what most of this brief is about.

---

## What this means for the drawing

Three rules, and everything else follows from them:

1. **The corners carry all the detail.** Whatever makes the frame look
   painted — the turn of the wood, a highlight, a nick in the edge — lives in
   the corners. They are never stretched.
2. **Each edge must be uniform along its length.** The top edge is stretched
   sideways; the left edge is stretched up and down. A knot in the middle of
   an edge, or grain that drifts along it, smears. Grain should run *across*
   each edge, not along it: on the top and bottom edges the grain runs up and
   down, on the left and right edges it runs side to side.
3. **The middle is one flat colour.** It stretches in both directions, so
   nothing in it can have a pattern, a gradient or a shadow. Flat parchment
   cream, `#F5EDD6`.

The middle only ever shows behind the bird's **name** — the photograph covers
the whole top of the card by itself. So there is no photo window to draw and
no dividing line between photo and name: a horizontal line cannot be held at
a fixed height when the card stretches. The photo will sit inside the frame
with its own rounded corners, handled in code.

---

## The three frames

Draw each at **4x** the nominal size below. Nominal is the 390px-phone case,
which is the commonest.

### 1. `flock-card-compact` — 452 x 436px (nominal 113 x 109)

The everyday card, three to a row. The frame edge should read at about **7px
at nominal size**, so roughly 28px in the file. Corner radius about 12px
nominal (48px in the file).

**Keep the slice inset clear:** the outer **64px** of the file on every side
(16px nominal) must contain the complete corner turn and nothing that needs
to stay in the middle of an edge.

### 2. `flock-card-large` — 692 x 676px (nominal 173 x 169)

The same card, two to a row. Same frame weight and same 64px slice inset — at
this size the frame simply reads as slightly finer against a bigger
photograph, which is right.

*If you would rather not draw this one twice: the compact frame will work
here scaled up, and the difference is small. Draw it separately only if you
want the large card to carry a little more detail in the corners.*

### 3. `flock-row` — 1432 x 248px (nominal 358 x 62)

The History row: a wide, short horizontal plaque. The time, a small square
bird photo and the bird's name sit on it left to right, all placed in code.

This one only ever stretches **sideways** — its height is fixed at 62px. So
the left and right caps hold the detail, and the top and bottom edges must be
uniform along their whole length.

- Frame edge about 7px nominal (28px in the file).
- Corner radius about 13px nominal (52px in the file).
- Slice inset: **72px left and right**, **28px top and bottom**.

---

## Style

It belongs to the same app as the collector card frame and the pack badges —
painted wood, warm, hand-made, no flat vector shading, no hard drop shadows.

**But it must not be mistaken for a collector card.** Those two things mean
different things: a collector card is a slot in a set you are trying to
complete, a My Flock card is a bird you actually found. The collector card is
heavy dark wood with a deep moulded edge. **Make these lighter and plainer —
a thinner frame, paler wood, less relief.** If the two are side by side on a
table, a child should be able to tell which is which without reading them.

Prioritise the photograph. The frame is a mount, not the subject.

## Palette

| | |
|---|---|
| Middle fill (behind the name) | `#F5EDD6` |
| Current card border, for reference | `#E9DDBE` |
| Collector-card wood, lit face | `#D87A38` |
| Collector-card wood, shadow | `#743206` |
| Name text sits on the middle in | `#1A1128` |

The frame should sit somewhere between the current pale `#E9DDBE` border and
the collector card's `#D87A38` — nearer the pale end.

## File delivery

Three PNGs, real alpha outside the rounded corners, named:

```
flock-card-compact.png    flock-card-large.png    flock-row.png
```

**No captions, labels, filenames or watermarks in the image.** Every delivery
on this project so far has arrived with its own filename baked across the
bottom of the picture.

Do **not** draw a bird photo, a name, a time or any other content into these
— they are empty frames. A grey or magenta block in the middle to show where
content goes is fine and will be removed; anything that looks like real
content is not.

## Acceptance checks

1. Cover the outer 64px (72/28 for the row) with a mask: what is left in the
   middle is one flat colour with nothing in it.
2. Take a 1px-tall slice from the middle of the top edge and repeat it across
   the width — it should be indistinguishable from the drawn edge. Same for
   the left edge, repeated vertically.
3. The corners are square-ish regions that contain the whole curve, inside
   the slice inset.
4. Real alpha outside the rounded corners, not white.
5. No text anywhere.

If check 1 or 2 fails, the frame will visibly smear on about a third of the
cards, and it will look fine in the mockup — this is the failure that only
shows up once it is in the app with real bird names.

---

# Appendix — the prompts

One style block; swap the SUBJECT line. Do the **compact card first** and
hold it against the acceptance checks before spending the other two.

```
A single empty picture frame for a children's bird-collecting app, drawn flat
and face-on, centred on a transparent background.

SUBJECT: <one line from below>

STYLE: painted wood in warm pale honey and soft amber, hand-painted
storybook quality with visible brush texture, gently rounded corners, a soft
bevel. Warm and toy-like, not glossy, not photographic, not flat vector. Much
lighter and thinner than a heavy dark picture frame.

CRITICAL CONSTRUCTION: the frame is going to be cut into nine pieces and
stretched, so:
- All the detail and character sits in the four corners.
- Each of the four edges is completely uniform along its length - no knots,
  no features, no variation, no drifting grain. The wood grain runs ACROSS
  each edge (up and down on the top and bottom edges, side to side on the
  left and right edges), never along it.
- The middle of the frame is one completely flat cream colour #F5EDD6 - no
  texture, no gradient, no inner shadow, no vignette, nothing.

Face-on, no perspective, no tilt, no cast shadow on the ground, no
decoration hanging off the frame, no leaves, no birds, no text, no letters,
no caption, no filename, no watermark, no border outside the frame.
```

**Subject lines**

| File | SUBJECT |
|---|---|
| `flock-card-compact.png` | A small almost-square picture frame, slightly wider than tall, with a thin edge about one fifteenth of its width |
| `flock-card-large.png` | A medium almost-square picture frame, slightly wider than tall, with a thin edge about one twenty-fifth of its width |
| `flock-row.png` | A long low horizontal plaque frame, about six times wider than it is tall, with a thin even edge all the way round |

Generators are poor at "uniform along its length" — expect to reject the
first couple on acceptance check 2.
