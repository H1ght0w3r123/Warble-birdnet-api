#!/usr/bin/env python3
"""Cut the Home background scenes out of a delivered contact sheet.

    pip install pillow numpy --break-system-packages
    python3 tools/build_scenes.py ~/Downloads/scenes.png --version 3

The sheet is a grid: one row per place, one column per time of day, in the
order below. Cells are separated by thin white gutters, which is what this
finds them by - they are NOT evenly spaced, so slicing the sheet into equal
quarters lands a few pixels into the neighbouring picture.

ALWAYS BUMP --version when the art changes. The filename is this project's
cache-buster; a changed image behind an unchanged name gets served stale.
Afterwards, point sceneUrl() in static/index.html at the new version.

About the upscale: the delivered sheet has been about 1000px wide, which is
roughly 240px per cell, against the 1170 a 3x phone wants. Resizing cannot
invent detail, but a LANCZOS upscale with a little unsharp does beat handing
the browser a tiny image and letting its own scaler stretch it - checked side
by side at phone size, and the difference is visible on grass and foliage. If
a future sheet arrives already large, TARGET_W just becomes a no-op downscale
guard rather than an upscale.
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

PLACES = ["garden", "river", "coast", "meadow"]   # rows, top to bottom
TIMES = ["dawn", "day", "dusk", "night"]          # columns, left to right
TARGET_W = 800
UNSHARP = dict(radius=2.2, percent=85, threshold=2)


def gutters(flags):
    """Start/end of each run of near-white rows or columns."""
    out, start = [], None
    for i, v in enumerate(flags):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(flags) - 1))
    return [r for r in out if r[1] - r[0] >= 1]


def slices(flags, wanted):
    """The `wanted` content bands between the widest gutters."""
    gaps = sorted(gutters(flags), key=lambda g: g[0] - g[1])[:wanted - 1]
    cuts = sorted(gaps)
    bands, edge = [], 0
    for a, b in cuts:
        bands.append((edge, a - 1))
        edge = b + 1
    bands.append((edge, len(flags) - 1))
    return [(s + 1, e - 1) for s, e in bands]   # a pixel in from each gutter


def trim(cell):
    """Shave any gutter left on a cell's own edges.

    The sheet's gutters are found across the whole sheet, so a detected gutter
    is only where EVERY row is white. The cells are pasted with small offsets,
    so an individual picture can still start a pixel or two later and carry a
    white stripe down one side. Trimming each cell against its own edges
    catches that; it stops as soon as an edge is picture rather than paper,
    so a genuine white cloud at the top of a frame is never eaten.
    """
    px = np.array(cell)
    top, bottom, left, right = 0, cell.height, 0, cell.width
    def paper(line):
        # flat and near-white: a cloud is bright but varies
        return (line.min(1) > 235).mean() > 0.6 and line.std(0).mean() < 6
    while top < bottom - 2 and paper(px[top]):
        top += 1
    while bottom > top + 2 and paper(px[bottom - 1]):
        bottom -= 1
    while left < right - 2 and paper(px[:, left]):
        left += 1
    while right > left + 2 and paper(px[:, right - 1]):
        right -= 1
    return cell.crop((left, top, right, bottom))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sheet", help="the delivered contact sheet")
    ap.add_argument("--version", type=int, required=True,
                    help="filename version, e.g. 3 for scene-river-dusk-v3.webp")
    ap.add_argument("--out", default=None, help="defaults to the repo's static/")
    args = ap.parse_args()
    out = args.out or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")

    sheet = Image.open(args.sheet).convert("RGB")
    px = np.array(sheet)
    white = px.min(2) > 230
    rows = slices(white.mean(1) > 0.9, len(PLACES))
    cols = slices(white.mean(0) > 0.9, len(TIMES))
    if len(rows) != len(PLACES) or len(cols) != len(TIMES):
        sys.exit("expected a %dx%d grid, found %d rows and %d columns"
                 % (len(PLACES), len(TIMES), len(rows), len(cols)))

    total = 0.0
    for r, place in enumerate(PLACES):
        y0, y1 = rows[r]
        for c, time in enumerate(TIMES):
            x0, x1 = cols[c]
            cell = trim(sheet.crop((x0, y0, x1 + 1, y1 + 1)))
            h = round(cell.height * TARGET_W / cell.width)
            cell = cell.resize((TARGET_W, h), Image.LANCZOS)
            if TARGET_W > cell.width:
                cell = cell.filter(ImageFilter.UnsharpMask(**UNSHARP))
            dest = os.path.join(out, "scene-%s-%s-v%d.webp" % (place, time, args.version))
            cell.save(dest, "WEBP", quality=86, method=6)
            kb = os.path.getsize(dest) / 1024
            total += kb
            print("%-34s %dx%-5d %5.1fKB" % (os.path.basename(dest), TARGET_W, h, kb))
    print("\n%d files, %.0f KB. Now point sceneUrl() at -v%d."
          % (len(PLACES) * len(TIMES), total, args.version))


if __name__ == "__main__":
    main()
