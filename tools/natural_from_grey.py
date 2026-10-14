"""Make a bird's natural-colour layers from its own grey ones, for a bird
whose real colour is one plain colour all over its colourable parts.

Natural (the bird in its own plumage) draws each colourable layer from a
natural-<layer>.webp beside the grey one (`nat:` in PROTO_BIRDS in
static/index.html). Painted natural layers are best (the Blue Tit came with
them), and a finished picture of the bird can be cut into them
(tools/cut_natural_layers.py). But the Blackbird is simply black: its grey
layers already carry every feather's shading, and only need taking down to
glossy black. That's what this does - inside each layer's wash mask only, so
the parts the mask leaves alone (none, on the Blackbird) keep their paint.

Why not just tint it black with the page's own wash: the wash maps the grey's
brightness through mid-grey to the swatch colour and on up to white, so the
light-grey feather highlights come out pale grey and the bird reads as slate,
not black. Here the brightness is squeezed into the dark end instead
(BLACK below), keeping the highlights as a sheen.

    python3 tools/natural_from_grey.py blackbird
"""
import os
import sys

import numpy as np
from PIL import Image

AVATAR = os.path.join(os.path.dirname(__file__), '..', 'static', 'avatar')

# bird: (colourable layers, (darkest, lightest, curve), sheen per channel)
BIRDS = {
    'blackbird': (['tail', 'body', 'wing-l', 'wing-r', 'head'], (14, 120, 1.8), (0.95, 0.97, 1.08)),
}


def make(bird):
    layers, (lo, hi, curve), sheen = BIRDS[bird]
    d = os.path.join(AVATAR, bird)
    for name in layers:
        lay = np.asarray(Image.open(os.path.join(d, name + '.webp')).convert('RGBA')).astype(np.float64)
        mask = np.asarray(Image.open(os.path.join(d, f'wash-{name}.webp')).convert('RGBA'))[..., 3:4] / 255
        lum = lay[..., :3] @ np.array([.2126, .7152, .0722])
        v = lo + (hi - lo) * (lum / 255) ** curve
        dark = np.clip(v[..., None] * np.array(sheen), 0, 255)
        rgb = mask * dark + (1 - mask) * lay[..., :3]
        out = np.dstack([rgb, lay[..., 3]]).round().astype(np.uint8)
        Image.fromarray(out, 'RGBA').save(os.path.join(d, f'natural-{name}.webp'), quality=92, method=6)
        print(f'{bird}: natural-{name}.webp')


if __name__ == '__main__':
    for b in sys.argv[1:] or BIRDS:
        make(b)
