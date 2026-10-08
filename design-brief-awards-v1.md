# Design Brief: Awards Page — "The Trophy Treehouse" (v1)

## What this is

The Awards tab is getting a full scene: a cosy treehouse room, lantern-lit,
with an archway looking out into a night forest. The trophies stand on a
mossy tree-stump podium in front of the archway, and the trophy's name hangs
on a wooden sign above them.

The mockup screenshot sent with this brief is the look to aim for. (Crop
off its top-right corner before sending it outside the family — the
profile circle there is a real photo.) **It is a picture of the finished
screen, not a template to trace.** The app builds the screen in layers so
the trophies can be swiped and the words can change, and **only two pieces
of new art are needed**:

1. **The background** — the room, with the podium painted into it.
2. **The hanging sign** — blank.

The mockup also has a carved plaque at the bottom, a bird on the trophy,
leaves in the corners and a "Tap for more" button. **None of those are
wanted.** The text under the trophies sits straight on the background.

## What already exists — do NOT redraw these

| Already in the app | File(s) | Notes |
|---|---|---|
| The 21 trophies | `trophy-l0-v1` … `trophy-l7-v1` (369 × 390) | One wooden cup, drawn at each leaf level (empty sockets → green leaves → gold leaves). |
| The 21 trophy emblems | `emblem-<trophy>-v1` (e.g. the "100", the owl, the globe) | Laid into the cup's round plaque by the app. |
| "Awards" title lettering | `title-awards-v2` | The carved wooden word at the top. |
| Small "Warble" wordmark, feather count, gear, profile picture, nav bar | — | The app's own top and bottom bars, the same on every screen. |
| Locked (grey) trophies | — | The app greys them out itself. Never deliver grey versions of anything. |

## What the app does in code (so it must NOT be painted in)

- **All words and numbers** — "55 of 147 levels earned", the trophy's name,
  the "Level 3" pill, and the description and progress under the trophies.
  **No text anywhere in either file.**
- **The trophies**, which slide left and right on top of the podium when a
  child swipes — so no trophies, or their shadows, in the background.
- Any glow, sparkle or fireflies.

## The layers, bottom to top

```
 4  Trophy name + "Level N" pill   ← app, written on the sign
 3  Hanging sign                   ← NEW: piece 2
 2  Trophies + emblems             ← existing, positioned by the app
 1  Text under the trophies        ← app, straight on the background
 0  Background with the podium     ← NEW: piece 1
```

## File delivery specification — read this before drawing anything

These rules come from the recording-tree redesign
(`design-brief-recording-tree-v2.md`), where getting them wrong cost four
rounds of rework. Both files must meet **all** of them.

1. **One piece per file.** The background and the sign are two separate
   files. Any "everything together" picture is a separate image clearly
   named `PREVIEW-ONLY`.
2. **The file's pixel size IS the canvas.** If it says 1200 × 2600, the PNG
   is exactly 1200 × 2600 pixels — not a bigger image of the same shape.
3. **Real transparency for the sign.** A true alpha channel, not a
   grey-and-white checkerboard painted into the picture. Test: put it over a
   solid red background — no squares should show.
4. **Nothing drawn on the art that isn't art** — no crosshairs, guide lines,
   dots, labels or measurements. The positions the app needs go in the
   **filename** (see each piece).
5. **No text.** Not even placeholder text.
6. **PNG, sRGB, full resolution.** The app shrinks and converts them itself.

## Style

The same as everything else in Warble: painted wood with visible grain,
chunky rounded toy-like shapes with a soft bevel, warm orange-to-brown wood,
mid-to-deep green leaves and moss. **Light comes from the top centre** —
the glow through the archway and the lanterns — and falls on the podium.
The room is evening-dark and cosy; the sign is lighter and warmer so it
reads clearly against it.

## The two pieces

Sizes are 3× the size they appear on a typical phone (390 points wide),
which keeps them sharp on every screen.

### 1. Background — `bg-awards_podium-X-Y_1200x2600.png`

The whole treehouse room in one picture: the wooden walls and roots framing
the edges, shelves with the owl figurine and little cups, hanging lanterns,
vines, the stone archway in the middle opening on to a softly lit night
forest, light rays falling through it, the floor — **and the tree-stump
podium** (cut top with growth rings, moss, little mushrooms) standing in
front of the archway.

**The podium position matters most.** The app has to stand the front trophy
exactly on it, on every shape of phone. So:

- **Put the podium's anchor in the filename**: the point on the stump's top
  surface where the front trophy's base should stand (the middle of the
  rings). For example `bg-awards_podium-600-1480_1200x2600.png` means "stand
  the trophy at x 600, y 1480".
- The podium should be **centred left-to-right** (x 600), with its top
  surface about **1000 px wide** — wide enough for the front trophy (about
  330 px at this scale) with room behind it for the side trophies.
- Put the anchor somewhere around **y 1400–1550** — about halfway down.

**It will be cropped differently on different phones.** Tall, thin phones
lose a little off the sides; shorter, wider phones lose some off the top and
bottom. So:

- Keep everything that matters — the archway, the podium, the lanterns —
  inside the **safe area: x 90 to 1110, y 280 to 2320**.
- Carry the scenery all the way to every edge.
- Keep three areas fairly calm and dark, because the app writes text over
  them: **behind the sign** (around y 560–760), **just under the title**
  (around y 400–520), and **below the podium** (around y 1750–2150) where
  the trophy's description and progress go.
- No trophies, no bird, no fireflies, no text, no plaque.

### 2. Hanging name sign — `sign-name_text-L-T-R-B_900x270.png`

The wooden plank hanging from two ropes, with vines and a few leaves,
**blank**, on a transparent background.

- Canvas exactly 900 × 270. The ropes may run off the top edge.
- The app writes the trophy's name and a gold "Level N" pill on it. The
  longest names are **"Summer Squad"** and **"Globetrotter"**, with "Level 7"
  beside them, in big bold letters — so the plain area of the plank needs to
  be roughly **640 × 110**.
- **Put that text area's box in the filename** as left, top, right, bottom,
  e.g. `sign-name_text-130-95-770-205_900x270.png`.
- Keep the plank's face fairly plain and dark enough for white bold letters
  to stand out.

**Before sending:** put the sign over the background where it hangs in the
mockup, stand a trophy on the podium anchor, and check it looks like the
mockup. If it doesn't, don't send it.

## Open questions

1. **Time of day.** The rest of the app's scenes change with the real time
   (dawn, day, dusk, night). The mockup is night. One room for all times is
   simplest; the alternative is four versions of the background with the
   forest outside the archway changing. Suggest starting with night only.
2. **The wooden nav bar** in the mockup is on every screen, not just Awards,
   so it's left out of this brief. It can be a separate brief if wanted.
