"""Cut a bird's natural-colour layers out of one finished picture of it.

Every avatar bird is drawn from layers (static/avatar/<bird>/), and the ones
a child can recolour - head, wings, sometimes the body - are painted in grey
and tinted in the page. "Natural" draws the bird in its own colours instead,
from natural-<layer>.webp files beside the grey ones (`nat:` in PROTO_BIRDS
in static/index.html).

A bird delivered with natural layers (the Blue Tit) needs nothing from here.
This is for a bird delivered as ONE finished picture in its own colours, on
the same canvas as its layers (the original eight came that way):

    python3 tools/cut_natural_layers.py <folder of <bird>.png> [bird ...]

Why it isn't just "the picture, through each layer's outline": the picture
only shows what's on top. Where the head covers the top of a wing, the
picture there is head - cut that out for the wing and, the moment the wing
flaps, a scrap of head colour flaps with it. So each layer takes the
picture only where that layer is the one on top. Everywhere else (under the
head, under a wing, under the face) it keeps its own grey painting, coloured
the way that layer is coloured where it does show: each shade of grey takes
the typical colour the picture gives that shade (a lookup from the grey's
brightness, per layer). The feathers keep their shading.

Two things that looked wrong before this was settled, both found by flapping:
- Colouring a hidden part from the NEAREST place it shows copied the shadow
  a wing casts on the body, so the cardinal's sides went dark and patchy as
  its wings lifted. The lookup uses the whole layer, and the picture fades
  into it over SEAM pixels next to anything that covers the layer.
- A layer's soft outer edge has to come from the picture too (it's the
  layer's own colour there - nothing is underneath); coloured any other way
  it showed as a light, speckly fringe round the head.
- One lookup for a whole layer mixed up its own colours: the penguin's body
  is black plumage (washed) round a white belly (not), and a pale grey under
  a wing came out white. Washed and unwashed parts of a layer (its wash
  mask) each get their own lookup.

STACKS has to match the drawing order of the bird's layers in PROTO_BIRDS
(under, torso, wings, then over); COLOURABLE lists the layers that get a
natural copy (the ones with a wash).
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

AVATAR = os.path.join(os.path.dirname(__file__), '..', 'static', 'avatar')

STACKS = {
    'classic':    ['foot-l', 'foot-r', 'body', 'wing-l', 'wing-r', 'head'],
    'cardinal':   ['foot-l', 'foot-r', 'body', 'wing-l', 'wing-r', 'head'],
    'parrot':     ['foot-l', 'foot-r', 'body', 'wing-l', 'wing-r', 'head', 'face'],
    'kingfisher': ['tail', 'foot-l', 'foot-r', 'body', 'wing-l', 'wing-r', 'head', 'face'],
    'owl':        ['foot-l', 'foot-r', 'body', 'head', 'face', 'wing-l', 'wing-r'],
    'duckling':   ['tail', 'foot-l', 'foot-r', 'body', 'head', 'face', 'wing-l', 'wing-r'],
    'penguin':    ['foot-l', 'foot-r', 'body', 'wing-l', 'wing-r', 'head', 'face'],
    'woodpecker': ['tail', 'foot-l', 'foot-r', 'body', 'wing-l', 'wing-r', 'head', 'face'],
}
COLOURABLE = {
    'cardinal': ['body', 'wing-l', 'wing-r', 'head'],
    'penguin':  ['body', 'wing-l', 'wing-r', 'head'],
}
DEFAULT_COLOURABLE = ['wing-l', 'wing-r', 'head']

# How much of a pixel the layers above may cover before the picture there
# stops counting as this layer's own colour.
SHOWS = 0.92
# How far (in pixels) the picture fades into the lookup next to a cover.
SEAM = 8.0
BINS = 64


def load(path, size):
    im = Image.open(path).convert('RGBA')
    if im.size != size:
        im = im.resize(size, Image.LANCZOS)
    return np.asarray(im).astype(np.float64)


def cut(bird, src_dir):
    d = os.path.join(AVATAR, bird)
    layers = {n: load(os.path.join(d, n + '.webp'), (800, 800)) for n in STACKS[bird]}
    pic = load(os.path.join(src_dir, bird + '.png'), (800, 800))
    order = STACKS[bird]
    for name in COLOURABLE.get(bird, DEFAULT_COLOURABLE):
        lay = layers[name]
        a = lay[..., 3] / 255
        above = np.ones(a.shape)
        for other in order[order.index(name) + 1:]:
            above *= 1 - layers[other][..., 3] / 255
        shows = (a > 0.01) & (above > SHOWS) & (pic[..., 3] >= 8)
        grey = lay[..., :3]
        lum = grey.mean(-1)
        # The lookup: each brightness of grey -> the median colour the picture
        # gives it, from the solid, uncovered middle of the layer.
        far = distance_transform_edt(above > SHOWS)
        solid = shows & (a > 0.9) & (far > SEAM)
        if not solid.any():
            solid = shows
        bins = np.minimum((lum / 256 * BINS).astype(int), BINS - 1)
        # A little wider than the mask itself: its soft edge, and the odd
        # pale streak in the plumage just outside it, belong to the plumage.
        washed = distance_transform_edt(load(os.path.join(d, f'wash-{name}.webp'), (800, 800))[..., 3] <= 127) <= 14
        out = np.zeros(grey.shape)
        for part in (washed, ~washed):
            pool = solid & part
            if pool.sum() < 200:
                pool = solid
            table = np.full((BINS, 3), np.nan)
            for k in range(BINS):
                m = pool & (bins == k)
                if m.sum() >= 12:
                    table[k] = np.median(pic[..., :3][m], axis=0)
            known = ~np.isnan(table[:, 0])
            for c in range(3):   # brightnesses never seen: from their neighbours
                table[:, c] = np.interp(np.arange(BINS), np.flatnonzero(known), table[known, c])
            out[part] = table[bins[part]]
        # The picture where the layer shows, fading into the lookup next to
        # whatever covers it (the edge of a cover is shadowed in the picture).
        w = np.where(shows, np.clip(far / SEAM, 0, 1), 0)
        w[shows & (above > 0.999) & (far > SEAM * 4)] = 1
        edge = shows & (a < 0.9)
        w[edge & (far > SEAM)] = 1
        out = w[..., None] * pic[..., :3] + (1 - w[..., None]) * out
        rgba = np.dstack([out, lay[..., 3]]).round().astype(np.uint8)
        dest = os.path.join(d, f'natural-{name}.webp')
        Image.fromarray(rgba, 'RGBA').save(dest, 'WEBP', quality=92, method=6)
        print(f'{bird}: natural-{name}.webp ({(w > 0.99).sum() / max(1, (a > 0.01).sum()):.0%} straight from the picture)')


if __name__ == '__main__':
    src = sys.argv[1]
    for b in sys.argv[2:] or STACKS:
        cut(b, src)
