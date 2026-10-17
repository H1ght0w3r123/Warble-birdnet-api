"""Turn a delivered Collections book painting into static/collections-book-v<N>.webp,
the open book on its table the pack's cards lie in (BOOK and .pack-book in
static/index.html).

    python3 tools/build_book.py <painting.png> [version]

The painting comes on a flat white background above the book (an image
generator can't make a see-through one), so:
- the white is cut away: every near-white pixel joined to the top edge
  through other near-white ones (so the cream pages, enclosed by the
  cover, stay), with a soft one-pixel edge;
- the picture is cropped to TOP_MARGIN above the book's top, so the book
  sits as high on the screen as it can;
- BOTTOM_EXTRA rows of the bottom are added below, mirrored, for phones
  taller than the painting: they only ever show under the nav bar, which
  blurs them, and there a reflection can't be told from more table.

Every place in BOOK is measured on the result (a share of its width), so
a new painting means measuring the pages again: the crop printed here is
how far everything moved up.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageOps

WHITE = 240          # at least this in every channel: background
TOP_MARGIN = 16      # px kept above the book's top
BOTTOM_EXTRA = 300   # px of mirrored table added below
STATIC = os.path.join(os.path.dirname(__file__), '..', 'static')


def main(src, version='3'):
    im = np.asarray(Image.open(src).convert('RGB'))
    white = (im.min(-1) >= WHITE).astype(np.uint8)
    _, lab = cv2.connectedComponents(white, connectivity=4)
    top = np.unique(lab[0][white[0] == 1])
    bg = np.isin(lab, top) & (white == 1)
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    # soften the cut: the ring just outside the book eases out with its brightness
    ring = (cv2.dilate((~bg).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) & bg
    alpha[ring] = np.clip((255 - im.min(-1)[ring].astype(int)) * 255 // (256 - WHITE), 0, 255)
    rows = np.nonzero((alpha > 0).sum(1) > im.shape[1] * 0.05)[0]
    y0 = max(0, rows[0] - TOP_MARGIN)
    out = Image.fromarray(np.dstack([im, alpha])[y0:], 'RGBA')
    w, h = out.size
    full = Image.new('RGBA', (w, h + BOTTOM_EXTRA))
    full.paste(out, (0, 0))
    full.paste(ImageOps.flip(out.crop((0, h - BOTTOM_EXTRA, w, h))), (0, h))
    path = os.path.join(STATIC, f'collections-book-v{version}.webp')
    full.save(path, quality=88, method=6)
    print(f'{path}: {w} x {h + BOTTOM_EXTRA} ({h} painted), cropped {y0}px off the top, '
          f'{os.path.getsize(path) // 1024} KB')


if __name__ == '__main__':
    main(*sys.argv[1:])
