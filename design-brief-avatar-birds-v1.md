# Design Brief: four new avatar birds (v1)

## What this is

A child's avatar is a bird they dress up in the Hoot-tique. Three are free
from the start (Cardinal, Parrot, Penguin). The rest are UK birds the child
has to **find** - hear the real bird, or one of its family, out on a warble -
and then buy for 30 feathers. Five exist already: Classic (the robin),
Duckling, Woodpecker, Owl and Kingfisher.

This brief asks for four more, each a bird a child in the UK can find:

| Avatar | File folder | Found by hearing | Character |
|---|---|---|---|
| Blue Tit | `bluetit` | any tit: Blue, Great, Coal, Marsh or Willow Tit | Tiny, round, cheeky; blue cap, white cheeks, dark eye-stripe |
| Blackbird | `blackbird` | a Blackbird or a thrush: Song Thrush, Mistle Thrush, Redwing, Ring Ouzel | Sleek, glossy, a bright orange beak and eye-ring |
| Magpie | `magpie` | a crow: Magpie, Jay, Jackdaw, Carrion Crow, Rook, Raven | Clever and showy; long tail, a blue-green sheen on the black |
| Seagull | `seagull` | any gull: Herring, Black-headed, Common or Great Black-backed | Big, cheerful, a yellow beak; the seaside one |

**Nothing else in the app needs designing.** The finding, the price, the
Hoot-tique and the Done screen are all built; each bird appears the moment
its files are in.

## Match the five already painted

Use `static/avatar/classic/`, `static/avatar/kingfisher/` and
`static/avatar/owl/` as the reference - same size, pose and light:

- Chunky, toy-like, painted, soft bevels, warm light from the top centre.
- Standing, facing the viewer at a slight three-quarter, feet on the ground
  line the others stand on, the same height on screen as Classic.
- Cute first, accurate second: a child should know the real bird from it,
  but it's a character, not a field guide.

## The layers (the important part)

Each bird is drawn as separate layers so it can be recoloured, dance and
wear hats and glasses. Deliver every layer as its own PNG, all on the same
**800 x 800** canvas, lined up exactly (stack them and they make the bird):

| Layer | What's on it |
|---|---|
| `body` | the body and tail, without the head or wings (a long tail can be its own `tail` layer, as the Kingfisher's is) |
| `head` | the head |
| `face` | eyes and beak only |
| `wing-l`, `wing-r` | each wing, separately (they flap) |
| `foot-l`, `foot-r` | each foot |
| `wash-head`, `wash-wing-l`, `wash-wing-r` | a grey version of the parts the child's chosen colour tints - the head's cap/crown and the wings. Light grey where the colour shows bright, dark grey where it's in shadow; transparent everywhere else |

The child picks the bird's colour from 18 swatches, and the `wash` layers
are what takes it. So: the bird's own markings (the Blue Tit's white cheeks,
the Magpie's black and white, the Blackbird's beak) stay painted in; the
areas that carry the child's colour are painted in **greys** on the wash
layers. Look at the Kingfisher's wash layers for how much to give over.

Hats sit on the head and glasses on the eyes, so keep the top of the head
clear (no tall crest - the Blue Tit's cap is fine) and the eyes where the
other birds' eyes are.

## File delivery specification

1. **One layer per file**, named `<folder>-<layer>_800x800.png`
   (for example `bluetit-wing-l_800x800.png`). A picture of the whole bird
   assembled is welcome too, named `PREVIEW-ONLY`.
2. **The file's pixel size IS the canvas:** exactly 800 x 800, every layer.
3. **Real transparency.** A true alpha channel, not a painted checkerboard.
   Test on solid red: no squares, no white fringe.
4. **Lined up.** Every layer of a bird in its exact place on the canvas.
5. **Nothing on the art that isn't art.** No text, no guides.
6. **PNG, sRGB.** The app converts them itself.
