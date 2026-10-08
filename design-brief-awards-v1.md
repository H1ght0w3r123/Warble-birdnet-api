# Design Brief: Awards Page — "The Trophy Treehouse" (v1)

## What this is

The Awards tab is getting a full scene: a cosy treehouse room, lantern-lit,
with an archway looking out into a night forest. The trophies stand on a
mossy tree-stump podium, the trophy's name hangs on a wooden sign above, and
a carved plaque underneath says what the trophy is for and how close the
child is to the next level. A little bluebird perches on the trophy at the
front.

The mockup screenshot sent with this brief is the look to aim for. (Crop
off its top-right corner before sending it outside the family — the
profile circle there is a real photo.) **It is a
picture of the finished screen, not a template to trace** — the app builds
the screen out of separate pieces so that the trophies can be swiped, the
words can change, and the whole thing fits every phone. This brief lists
those pieces and exactly how each one must be delivered.

## What already exists — do NOT redraw these

| Already in the app | File(s) | Notes |
|---|---|---|
| The 21 trophies | `trophy-l0-v1` … `trophy-l7-v1` (369 × 390) | One wooden cup, drawn at each leaf level (empty sockets → green leaves → gold leaves). |
| The 21 trophy emblems | `emblem-<trophy>-v1` (e.g. the "100", the owl, the globe) | Laid into the cup's round plaque by the app. |
| "Awards" title lettering | `title-awards-v2` | The carved wooden word at the top. |
| Small "Warble" wordmark, feather count, gear, profile picture | — | The app's top bar, same on every screen. |
| Locked (grey) trophies | — | The app greys them out itself. Never deliver grey versions of anything. |

Attach `trophy-l0-v1.png` to whoever is drawing this: the bird (piece 7)
has to be drawn on top of it.

## What the app does in code (so it must NOT be painted in)

- **All words and numbers.** "55 of 147 levels earned", the trophy's name,
  the "Level 3" pill, "Forty of the hundred. Keep going!", "Hear 60 birds
  from Warble's list · 40/60", "TAP FOR MORE". Every one of these changes per
  trophy and per child. **No text anywhere in any delivered file.**
- **The trophies themselves**, sliding left and right when swiped.
- **The row of progress leaves** — the app lines up 20 copies of the leaf
  pieces (piece 6) and colours as many as the child has earned.
- **Shadows the trophies cast** onto the stump, the gentle pulse on the
  front trophy, and the fireflies drifting about.

## The layer stack

Bottom to top. Each numbered piece is a separate delivery, described below.

```
 9  Foreground leaves (bottom corners)      ← piece 8
 8  "TAP FOR MORE" button                   ← piece 5   (+ text by the app)
 7  Info plaque                             ← piece 4   (+ text and leaves by the app)
 6  Hanging name sign                       ← piece 3   (+ name and level by the app)
 5  Bluebird on the front trophy            ← piece 7
 4  Front trophy + emblem                   ← existing
 3  Side trophies                           ← existing
 2  Tree-stump podium                       ← piece 2
 1  Light rays through the archway          ← piece 1b
 0  The room                                ← piece 1a
```

Why the podium is its own layer, and *behind* the trophies: the trophies
slide across it when a child swipes, so they can't be part of the same
picture, and they have to be drawn on top of it to look as if they're
standing on it.

## File delivery specification — read this before drawing anything

These rules come from the recording-tree redesign
(`design-brief-recording-tree-v2.md`), where getting them wrong cost four
rounds of rework. Every file must meet **all** of them.

1. **One piece per file.** Never a sheet, grid, or "here are all the pieces"
   page. If you want to show everything together, that's a separate image
   clearly named `PREVIEW-ONLY`.
2. **The file's pixel size IS the canvas.** If a piece below says
   1200 × 2600, the PNG is exactly 1200 × 2600 pixels. Not a bigger image of
   the same shape. Check before sending.
3. **Pieces marked "registered" sit at their true position on their canvas,
   not centred.** Lay them over each other at (0, 0) and they must line up
   with no moving. In isolation a registered piece often looks oddly placed
   — that's correct.
4. **Real transparency.** A true alpha channel, not a grey-and-white
   checkerboard painted into the picture. Test: put the file over a solid
   red background — there should be no squares showing.
5. **Nothing drawn on the art that isn't art.** No crosshairs, guide lines,
   dots, labels, captions or measurements. Positions go in the **filename**.
6. **Anchor points in the filename**, in the format
   `name_X_Y_WxH.png` — e.g. `podium-stump_600_150_1200x540.png` means "this
   file is 1200 × 540, and the point that matters is at x 600, y 150". Where
   a piece needs a text area instead, give its box as
   `_text-LEFT-TOP-RIGHT-BOTTOM` (see pieces 3 and 4).
7. **No text.** Not even placeholder text. Blank signs, blank plaque,
   blank button.
8. **PNG, sRGB, full resolution.** The app shrinks and converts them itself.

**Before sending:** stack the pieces yourself over a phone-shaped
background, in the order above, and check it looks like the mockup. If it
doesn't, don't send it — that one-minute check would have saved weeks on
the tree.

## Style

The same as everything else in Warble: painted wood with visible grain,
chunky rounded toy-like shapes with a soft bevel, warm orange-to-brown wood,
mid-to-deep green leaves and moss, cream panels. **Light comes from the
top centre** — the glow through the archway and the lanterns — so every
piece should be lit from roughly the same place, or the assembled scene will
look pasted together (this was the main lesson of the tree).

The room is evening-dark and cosy; the pieces on top of it (sign, plaque,
podium) are lighter and warmer so they read clearly against it.

## The deliverables

Sizes are given at 3× the size they appear on a typical phone (390 points
wide), which keeps them sharp on every screen.

### 1a. The room — `bg-room_1200x2600.png` (registered, full canvas)

The treehouse interior, everything that never moves: the wooden walls and
roots framing the edges, the shelves with the owl figurine and little cups,
the hanging lanterns, the vines, the stone archway in the middle opening on
to a softly lit night forest, and the floor.

**Leave out:** the stump, the trophies, the bird, the sign, the plaque, the
foreground leaves, any fireflies, and any light rays (those are 1b).

**It will be cropped differently on different phones.** Tall, thin phones
lose a little off the sides; shorter, wider phones lose some off the top and
bottom. So:

- Keep everything that matters — the archway, the lanterns — inside the
  **safe area: x 90 to 1110, y 280 to 2320.**
- Carry the scenery all the way to every edge; nothing important within
  90 px of the sides or 280 px of the top and bottom.
- The archway's opening should be centred at about **x 600, y 1150**, so the
  trophies stand in front of it.
- Keep the areas behind the sign (around y 560–760) and the plaque (around
  y 1750–2200) fairly calm and dark — busy detail there fights with the text.

### 1b. Light rays — `bg-rays_1200x2600.png` (registered to 1a)

The soft shafts of light falling through the archway on to the podium, on
their own transparent layer on exactly the same canvas as 1a. The app makes
them breathe gently, so they must be separate from the room. Soft-edged,
pale gold, mostly transparent.

### 2. Tree-stump podium — `podium-stump_X_Y_1200x540.png`

The wide, mossy, cut tree stump with its growth rings on top, moss, little
mushrooms and a soft shadow on the floor beneath it.

- Canvas 1200 × 540, the stump filling most of the width.
- **The anchor (X, Y) is the point on the top surface where the front
  trophy's base stands** — the middle of the rings. Roughly (600, 150) in
  the mockup; tell us the real one in the filename.
- The top surface must be wide and flat enough for the front trophy (about
  330 px wide at this scale) with room behind it for the side trophies.
- Don't paint the trophies' shadows on it — the app does those, because the
  trophies move.

### 3. Hanging name sign — `sign-name_text-L-T-R-B_900x270.png`

The wooden plank hanging from two ropes with vines and leaves, **blank**.

- Canvas 900 × 270. The ropes may run off the top edge of the canvas.
- The app writes the trophy's name and a gold "Level N" pill on it. The
  longest names are **"Summer Squad"** and **"Globetrotter"** with
  "Level 7" beside them, in big bold letters — the text area must be wide
  enough for that comfortably, roughly 640 × 110.
- Put the text area's box in the filename, e.g.
  `sign-name_text-130-95-770-205_900x270.png`.
- Keep the plank's face fairly plain and dark enough that white bold letters
  stand out.

### 4. Info plaque — `plaque-info_text-L-T-R-B_1170x480.png`

The big carved panel at the bottom with vines curling round its edges,
**blank**.

- Canvas 1170 × 480.
- The app puts three things in it, top to bottom: a sentence of up to two
  lines ("Forty of the hundred. Keep going!"), the requirement and count
  ("Hear 60 birds from Warble's list · 40/60"), and the row of 20 progress
  leaves. Leave a clear face for all three, roughly 960 × 330.
- Put that box in the filename, e.g.
  `plaque-info_text-105-60-1065-390_1170x480.png`.
- The "TAP FOR MORE" button (piece 5) overlaps the bottom edge, so leave the
  middle of the bottom edge plain.
- Dark enough for cream-coloured text to read clearly.

### 5. "Tap for more" button — `btn-more_text-L-T-R-B_480x120.png`

The small wooden plank button, **blank**, with its text box in the filename.
Optional second file, `btn-more-pressed_…`, slightly darker and lower, for
when it's being pressed.

### 6. Progress leaves — `leaf-on_96x96.png`, `leaf-off_96x96.png`

Two single leaves for the progress row, each centred on its own 96 × 96
canvas, both pointing the same way:

- `leaf-on` — bright green, glossy, like the leaves in the trophy sockets.
- `leaf-off` — the same leaf shape in pale grey-brown, flat, clearly "not
  yet".

The app lines up 20 of them in a row, so they must look right repeated
side by side at about 14 points each — simple, chunky shapes, no fine
detail.

### 7. Bluebird — `bird-perch_1107x1170.png` (registered to the trophy)

The little blue-and-cream bird perched on the right-hand handle of the front
trophy, mouth open mid-song.

- **Draw it on a canvas exactly 1107 × 1170 — three times the size of
  `trophy-l0-v1.png` (369 × 390) — with the bird positioned so it sits on
  that trophy's right handle.** Lay the trophy, scaled up 3×, underneath
  while drawing, then hide it before saving. That way the app can put the
  bird on any trophy without any guessing.
- Only the bird in the file — not the trophy.
- Optional: `bird-blink_1107x1170.png`, the same bird with its eyes closed,
  so it can blink now and then.

### 8. Foreground leaves — `fg-leaves-left_WxH.png`, `fg-leaves-right_WxH.png`

The clumps of big leaves in the bottom corners that sit in front of
everything, just above the nav bar.

- Two separate files, each about 450 × 600.
- **Anchored to their outer bottom corner** (the left one to its
  bottom-left, the right one to its bottom-right), because the app pins them
  to the corners of the screen whatever its shape. So the leaves should grow
  out from that corner, and be cut off cleanly along those two edges.
- Keep them small enough not to cover the plaque's text.

## Optional — needs Phil's decision first

**Wooden nav bar.** The mockup's bottom bar is a wooden plank with vines.
That bar is on every screen, not just Awards, so changing it changes the
whole app. If wanted: `nav-plank_1290x270.png`, a long plank designed so its
middle section can stretch to any phone width (plain grain in the middle,
detail only at the two ends), with nothing that clashes with the round home
button in the centre.

## Open questions

1. **Time of day.** The rest of the app's scenes change with the real time
   (dawn, day, dusk, night). The mockup is night. One room for all times is
   simplest; the alternative is four versions of piece 1a with the forest
   outside the archway changing. Suggest starting with night only.
2. **The bird.** Should it stay on whichever trophy is at the front (and hop
   across when the child swipes), or live on one particular trophy? Assumed:
   it hops to the front one.
3. **The wooden nav bar** — Awards only, everywhere, or not at all?
