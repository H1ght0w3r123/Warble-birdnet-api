# Design Brief: four new avatar birds (v1)

## What this is

A child's avatar is a bird they dress up in the Hoot-tique. Three are free
from the start (Cardinal, Parrot, Penguin). The rest are UK birds the child
has to **find** - hear the real bird, or one of its family, out on a warble -
and then buy for 30 feathers. Five exist already: the Robin,
Duckling, Woodpecker, Owl and Kingfisher.

This brief asked for four more, each a bird a child in the UK can find.
**The Blue Tit is delivered and in the app** - deliver the other three the
way it came, natural-colour layers included (see "Natural colour" below):

| Avatar | File folder | Found by hearing | Character |
|---|---|---|---|
| Blue Tit (delivered) | `bluetit` | any tit: Blue, Great, Coal, Marsh or Willow Tit | Tiny, round, cheeky; blue cap, white cheeks, dark eye-stripe |
| Blackbird | `blackbird` | a Blackbird or a thrush: Song Thrush, Mistle Thrush, Redwing, Ring Ouzel | Sleek, glossy, a bright orange beak and eye-ring |
| Magpie | `magpie` | a crow: Magpie, Jay, Jackdaw, Carrion Crow, Rook, Raven | Clever and showy; long tail, a blue-green sheen on the black |
| Seagull | `seagull` | any gull: Herring, Black-headed, Common or Great Black-backed | Big, cheerful, a yellow beak; the seaside one |

**Nothing else in the app needs designing.** The finding, the price, the
Hoot-tique and the Done screen are all built; each bird appears the moment
its files are in.

## Match the five already painted

Use `static/avatar/classic/` (the Robin), `static/avatar/kingfisher/` and
`static/avatar/owl/` as the reference - same size, pose and light:

- Chunky, toy-like, painted, soft bevels, warm light from the top centre.
- Standing, facing the viewer at a slight three-quarter, feet on the ground
  line the others stand on, the same height on screen as the Robin
  (its files are in `static/avatar/classic/`).
- Cute first, accurate second: a child should know the real bird from it,
  but it's a character, not a field guide.

## The layers (the important part)

Deliver each bird exactly as the Kingfisher was delivered: separate layers so
the app can recolour it, flap its wings and dress it up. Every layer is on the
same **1000 x 1000** canvas, already in its final position - stack them and
they make the bird, nothing to nudge.

**`layers/`** - numbered back to front:

| File | What's on it | Painted in |
|---|---|---|
| `00_tail_fixed.png` | a tail that shows behind the body (if it has one) | its own colours |
| `01_foot_left_fixed.png`, `02_foot_right_fixed.png` | each leg and foot | its own colours |
| `03_body_fixed.png` | the body: chest, belly, flanks | its own colours |
| `04_wing_left_dynamic.png`, `05_wing_right_dynamic.png` | each wing in its resting position (they flap, so separately) | **neutral grey** |
| `06_head_colourable.png` | the head's feathered dome: crown, cheeks, nape | **neutral grey** |
| `07_face_fixed_overlay.png` | eyes, beak and the bird's own markings - nothing else | its own colours |

**`masks/`** - one per grey layer, same canvas:

| File | What it marks |
|---|---|
| `head_wash_mask.png`, `wing_left_wash_mask.png`, `wing_right_wash_mask.png` | white where the child's chosen colour shows on that layer, transparent where it doesn't; a soft edge is fine |

Why grey: the child picks the bird's colour from 18 swatches, and the app
tints the grey layers through their masks. **Neutral grey** means equal red,
green and blue at every pixel, carrying all the shading and highlights - a
warm or cool cast comes out wrong on half the swatches. The bird's own
markings (the Blue Tit's white cheeks, the Magpie's black and white, the
Blackbird's orange beak) belong on the fixed layers, so they stay whatever
colour the child picks.

- **The face layer is only eyes, beak and markings.** Held up on its own you
  should see straight through where the head was. A coloured head on the
  face layer would never change colour.
- **Overlap, don't butt-join.** Where a fixed part meets grey plumage, carry
  the plumage 2-3 px underneath it, or a hairline shows when the colour
  changes.
- **Roughly half to two-thirds of the bird should take the colour.** Less
  and the swatches barely change it; much more and it has no face left in
  near-black.

### Natural colour

Every bird starts in its own plumage: "Natural" is the first feather swatch,
and picking another colour only opens at the third birder rank. So each
bird also needs its colourable layers painted in the real bird's colours,
in a `natural-colour/` folder, same canvas and position as the grey ones:

| File | Replaces, for Natural |
|---|---|
| `natural_head.png` | the grey head |
| `natural_wing_left.png`, `natural_wing_right.png` | the grey wings |

The Blue Tit's set is the model. The eight birds already in the app will
get theirs too; until then the app tints their grey layers with the nearest
real colour.

## Size and placement

Match the Kingfisher, measured on its 1000 x 1000 canvas:

| | Kingfisher |
|---|---|
| Top of the head | y 110 (an owl's ear tufts can rise to about y 50) |
| Head and body, side to side | x 210 to 790 |
| Wings | y 480 to 770, hanging from the shoulders |
| Bottom of the feet (the ground) | y 920 - every bird stands on this line |

Hats sit on the head and glasses on the eyes; each bird's fit is set once its
files are in, so keep the top of the head clear (no tall crest - the Blue
Tit's cap is fine) and the eyes level, a little above halfway down the head.

## File delivery specification

1. **One folder per bird** - `bluetit/`, `blackbird/`, `magpie/`, `seagull/` -
   each holding its `layers/` and `masks/` folders, named exactly as above. A
   picture of the whole bird assembled is welcome too, named `PREVIEW-ONLY`.
2. **The file's pixel size IS the canvas:** exactly 1000 x 1000, every layer
   and every mask, 8-bit RGBA.
3. **Real transparency.** A true alpha channel, not a painted checkerboard.
   Test on solid red: no squares, no white fringe.
4. **Lined up.** Every layer of a bird in its exact place on the canvas.
5. **Nothing on the art that isn't art.** No text, no guides, no baked
   shadow.
6. **PNG, sRGB.** The app makes its own smaller copies
   (`tools/export_bird_layers.py` shrinks them to 800 x 800 for the phone).
