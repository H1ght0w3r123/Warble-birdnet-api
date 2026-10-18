"""Turn a delivered scrap of torn paper into static/note-paper-v<N>.webp, the
note under the Collections book (.pack-table .fan-caption in
static/index.html), which stretches to fit its words.

    python3 tools/build_note_paper.py <scrap.png> [version]

The scrap comes flat on solid magenta (#FF00FF), which no cream paper has
in it: a pixel is background as far as magenta outweighs it (the lower of
red and blue, minus green) - fully see-through past KEY_HI, fully paper
under KEY_LO, soft in between - and the pink the torn edge picks up from
the background is taken back out (despill). It's cropped to the paper and
shrunk to WIDTH.

The page draws it with border-image, the 9-slice way: the corners stay as
they are, the edges stretch (or repeat) along, the middle fills in. That's
why it was asked for with an even tear all the way round and a plain
middle - a one-off rip on an edge would show stretched. SLICE (px of the
result) is how far in from each side the corner and edge pieces run: past
the tear, into plain paper. Change it here and in the page together.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

KEY_LO, KEY_HI = 40, 120
WIDTH = 480
SLICE = 36
STATIC = os.path.join(os.path.dirname(__file__), '..', 'static')


def main(src, version='1'):
    f = np.asarray(Image.open(src).convert('RGB')).astype(np.float64)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    m = np.minimum(r, b) - g
    alpha = np.clip((KEY_HI - m) / (KEY_HI - KEY_LO), 0, 1)
    # only the biggest piece is paper (drops specks in the background)
    _, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 0.5).astype(np.uint8))
    alpha *= lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    # despill: no edge pixel keeps more red and blue than the green allows
    excess = np.maximum(np.minimum(r, b) - g - 30, 0)
    f[..., 0] -= excess
    f[..., 2] -= excess
    ys, xs = np.nonzero(alpha > 0.02)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    im = Image.fromarray(np.dstack([np.clip(f, 0, 255), alpha * 255]).round().astype(np.uint8)[y0:y1, x0:x1], 'RGBA')
    h = round(im.height * WIDTH / im.width)
    im = im.resize((WIDTH, h), Image.LANCZOS)
    path = os.path.join(STATIC, f'note-paper-v{version}.webp')
    im.save(path, quality=90, method=6)
    print(f'{path}: {WIDTH} x {h}, {os.path.getsize(path) // 1024} KB; slice {SLICE}px')


if __name__ == '__main__':
    main(*sys.argv[1:])
