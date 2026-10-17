"""Cut the Top Trumps leaf and socket out of the trophy paintings, so the bird
card's stats wear exactly the trophies' leaves (buildStatBars in
static/index.html): static/stat-leaf-v1.webp and static/stat-socket-v1.webp.

    python3 tools/cut_stat_leaves.py

The trophies' leaves aren't separate pictures - they're painted into each
cup's base (trophy-l0 has the three carved hollows empty, trophy-l3 has a
green leaf in each). So the middle hollow is cut out of both, through the
same mask: the green leaf's own shape in l3, grown by RIM pixels to take in
the carved edge round it, softened so it doesn't end in a hard line. The
empty socket is the bare hollow from l0, the leaf is the filled one from l3.
If the trophy art is repainted, run this again.
"""
import os

import cv2
import numpy as np
from PIL import Image

STATIC = os.path.join(os.path.dirname(__file__), '..', 'static')
BOX = (156, 318, 213, 377)   # around the middle hollow (leaf at x 163-205, y 327-369)
RIM = 4


def main():
    empty = np.asarray(Image.open(os.path.join(STATIC, 'trophy-l0-v1.webp')).convert('RGBA'))
    full = np.asarray(Image.open(os.path.join(STATIC, 'trophy-l3-v1.webp')).convert('RGBA'))
    x0, y0, x1, y1 = BOX
    empty, full = empty[y0:y1, x0:x1], full[y0:y1, x0:x1]
    f = full.astype(int)
    green = (f[..., 1] > f[..., 0] + 30) & (f[..., 1] > f[..., 2] + 30)
    _, lab, stats, _ = cv2.connectedComponentsWithStats(green.astype(np.uint8))
    leaf = (lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    leaf = cv2.morphologyEx(leaf, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    mask = cv2.dilate(leaf, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * RIM + 1, 2 * RIM + 1)))
    alpha = cv2.GaussianBlur(mask.astype(np.float32) * 255, (5, 5), 0)
    for name, src in (('stat-socket-v1.webp', empty), ('stat-leaf-v1.webp', full)):
        a = np.minimum(alpha, src[..., 3]).round().astype(np.uint8)
        Image.fromarray(np.dstack([src[..., :3], a]), 'RGBA').save(os.path.join(STATIC, name), quality=92, method=6)
        print(name, src.shape[1], 'x', src.shape[0])


if __name__ == '__main__':
    main()
