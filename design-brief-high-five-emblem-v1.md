# Design Brief: High Five trophy emblem (v1)

> **Delivered** - the open hand with three rays. In the app as
> `static/emblem-high_five-v1.webp` (haze cleared, made fully opaque,
> trimmed to the art, 235 x 256).

## What this is

Warble has a new trophy, **High Five**. A child wins it by finishing all
five weekly challenges in one week, and it levels up at 1, 3, 6, 10, 15, 25
and 40 such weeks. Like every trophy, it's a wooden cup with a carved emblem
set into the oval plaque on its front. The other twenty trophies each have
their own emblem; High Five is borrowing the Weekly Challenges target icon
until it has one.

**One piece of art is needed: the emblem.** Nothing else. The cup, its
leaves, the plaque, the greying-out of locked trophies and all the words
are already done by the app.

Reference sheet: `design-ref-trophy-emblems.png` (in the repo, next to this
brief). It shows the twenty existing emblems side by side, and the emblem on
a cup at real phone size, earned and locked.

## The idea

**A carved wooden open hand, palm forward, fingers spread, mid high-five,
with three short rays above it** for the "slap", like the rays on Century
and Early Bird. Five fingers for five challenges; children know the gesture
at a glance.

*Alternative, if it reads just as clearly at the size test below:* a bird's
wing raised like a hand, its five longest feathers spread like fingers.
It's more Warble, but it risks looking like Preener (one feather) or High
Flyer (spread wings), so only use it if it's unmistakable at 40 pixels.
Otherwise go with the hand.

## Style — match the twenty that exist

- **Carved, polished wood.** Warm orange-to-brown, visible grain, a soft
  bevel and a darker carved edge, exactly like `emblem-fledgling-v1.webp`
  or `emblem-century-v1.webp`.
- **Light from the top centre**, as on every emblem and cup.
- **Wood only**, with at most a small touch of the mid-green leaf colour
  some emblems use (Forager, Empty Nester, Still Water). No other colours:
  no skin tones, no gold, no stars in yellow.
- **Chunky and simple.** One bold silhouette, few details, nothing thin.

## It has to read tiny, and in grey

The emblem is shown far smaller than it's drawn:

- On a phone, the front cup is about 160 px wide and **the emblem sits in a
  space about 43 × 33 px** (the plaque is a wide oval, roughly 5:4).
- **Locked trophies are shown greyed and dimmed** (see the reference sheet),
  so the shape alone has to say "high five", without its colour.

So:

- A **wide or square silhouette** fills the plaque best. Tall, thin shapes
  end up tiny.
- Fingers clearly separated, with real gaps between them: at 40 px, five
  fingers that touch read as a mitten.
- No fine lines, no small text-like marks, no outline that disappears when greyed.

## Do NOT include

- The plaque, oval or cup. The app lays the emblem into the cup's own plaque.
- Any text, number or letter (no "5", no "High Five").
- A background, shadow on the ground, or glow.
- A star badge, ribbon or frame around it.

## File delivery specification

The same rules as every Warble brief:

1. **One file:** `emblem_high-five_1024x1024.png`. Any preview with other
   emblems or on a cup is a separate file named `PREVIEW-ONLY`.
2. **The file's pixel size IS the canvas:** exactly 1024 × 1024.
3. **Real transparency.** A true alpha channel, not a painted checkerboard.
   Test it on solid red: no squares, no white fringe.
4. **The emblem fills the canvas** edge to edge, about 90%, centred. The
   app trims and scales it to sit with the other twenty.
5. **Nothing on the art that isn't art.** No guides or measurements.
6. **PNG, sRGB.**

## Before sending

1. Put it on the reference sheet next to the twenty and check it looks like
   part of the same set: same wood, same light, same chunkiness.
2. **Shrink it to 40 px wide and turn it grey.** If it still reads as a
   hand doing a high five, it's done. If it reads as a leaf, a paw, a
   mitten or a splash, simplify and try again.
