#!/usr/bin/env python3
"""Turn the delivered collector-pack artwork into the app's webp assets.

Run this whenever the pack art is re-exported. It is a local tool, not part
of the running app, so its libraries are deliberately NOT in requirements.txt
(adding them would slow every Railway build for something Railway never runs):

    pip install pillow numpy scipy --break-system-packages
    python3 tools/build_pack_art.py ~/Downloads/warble_collection_assets --version 2

It expects one folder of PNGs named <slug>_<kind>.png, where <slug> is a
pack's "art" value in curated_species.py and <kind> is icon, badge or name -
30 files for the ten packs. It writes
static/pack-<slug>-<kind>-v<version>.webp and leaves the old version alone.

ALWAYS BUMP --version when the art changes. The filename is this project's
cache-buster: browsers and Railway's CDN will happily serve yesterday's
picture from a filename they have already seen, which has cost us a
deploy-and-stare cycle before. After building, update the three src= lines in
static/index.html to match (search for "pack-${p.art}-").

Two things about the source art are worth knowing, because they will happen
again on the next export:

1. Every PNG arrives with its own FILENAME baked across the bottom in grey
   text. It has to come off, and it will not come off by colour: the art's
   white sticker outline is the same tone as the caption's halo, and the halo
   is connected to the art's drop shadow, so neither a brightness threshold
   nor a flood fill separates them. What does separate them is that the art
   is orange and the caption is grey, AND that a line of letters breaks a
   pixel row into several separate runs where the soft shadow under a round
   badge is one continuous run. Cutting on the run count is what stops this
   clipping the bottom off the badges - cutting on greyness alone flattened
   four of them.

2. The downscale is premultiplied. Resampling straight RGB drags the colour
   of fully transparent pixels into every edge, which is the fringing we have
   chased across the card frame and the leaf marks before now.

If a future export arrives with real alpha and no caption, this script still
works - the caption pass simply finds nothing to cut.
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from curated_species import PACKS  # noqa: E402

KINDS = ("icon", "badge", "name", "emblem")

# Export heights, roughly 3x the largest size each is ever drawn at, so they
# stay crisp on a 3x phone screen without carrying pixels nobody will see.
TARGET_H = {"icon": 120, "badge": 120, "name": 84}

# The emblem is the flat one-colour mark that sits in the card frame's two
# corner discs, recoloured per pack via CSS mask + background-color. It is
# squared off and padded so every pack drops into the same round disc at the
# same size whatever its own proportions.
#
# Emblems are delivered on flat white rather than with an alpha channel, on
# purpose: generators ignore a transparency request more often than they
# honour it, and one flat colour on flat white keys out in a single step with
# nothing to guess at. PAPER is that background, INK the lightest tone that
# still counts as solid mark - one mark came back in two greens, so the
# mapping has to make both fully opaque and leave only the real anti-aliased
# edge in between.
EMBLEM_BOX = 120
PAPER = 254.0
INK = 120.0

ORANGE = 0.30   # saturation at or above this is artwork, never caption text
CARVED = 110    # luminance below this is the icon's recessed fill, not its raised ridge
GREY = 0.20     # saturation below this is caption text, or the art's own outline
VISIBLE = 16    # alpha above this counts as a pixel that is there at all
SPECK = 40      # islands smaller than this are anti-aliasing left behind


def row_runs(row):
    """How many separate horizontal runs of visible pixel this row breaks into."""
    edges = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
    return int((edges == 1).sum())


def strip_caption(im):
    """Return the alpha mask of the artwork with the baked filename removed."""
    rgb, alpha = im[:, :, :3], im[:, :, 3]
    hi, lo = rgb.max(2), rgb.min(2)
    sat = np.where(hi > 0, (hi - lo) / np.maximum(hi, 1), 0)

    visible = alpha > VISIBLE
    art = visible & (sat > ORANGE)
    grey = visible & (sat < GREY)

    height = visible.shape[0]
    per_row = visible.sum(1)
    grey_per_row = grey.sum(1)
    caption_rows = [
        y for y in range(int(height * 0.5), height)
        if per_row[y] and grey_per_row[y] / per_row[y] > 0.75 and row_runs(visible[y]) >= 3
    ]
    # -3 takes the caption's own white halo along with the letters
    cut = max(0, min(caption_rows) - 3) if caption_rows else height

    keep = visible.copy()
    keep[cut:] &= ~grey[cut:]
    keep = ndimage.binary_propagation(art, mask=keep)   # drop whatever that orphaned

    labels, count = ndimage.label(keep)
    if count > 1:
        sizes = ndimage.sum(np.ones_like(labels), labels, range(1, count + 1))
        keep &= np.isin(labels, [i + 1 for i, s in enumerate(sizes) if s >= SPECK])
    return keep, cut < height


def emblem_alpha(im):
    """Flat mark on flat white -> a white-on-transparent mask."""
    lum = im[:, :, :3].mean(2).astype(np.float64)
    if im.shape[2] == 4:                      # honour real alpha if it is there
        lum = np.where(im[:, :, 3] > 16, lum, PAPER)
    a = np.clip((PAPER - lum) / (PAPER - INK), 0.0, 1.0)

    solid = a > 0.5
    if not solid.any():
        raise ValueError("no mark found - is this file blank?")
    labels, count = ndimage.label(solid)
    if count > 1:
        sizes = ndimage.sum(np.ones_like(labels), labels, range(1, count + 1))
        near = ndimage.binary_dilation(
            np.isin(labels, [i + 1 for i, sz in enumerate(sizes) if sz >= SPECK]),
            np.ones((5, 5)))
        a = np.where(near, a, 0.0)            # drop stray dust, keep soft edges
    return a


def downscale(rgba, height):
    """Premultiplied-alpha resize - see note 2 in the module docstring."""
    a = rgba[:, :, 3:4].astype(np.float64) / 255.0
    premul = np.concatenate([rgba[:, :, :3].astype(np.float64) * a, a * 255.0], axis=2)
    width = max(1, round(rgba.shape[1] * height / rgba.shape[0]))
    small = np.array(
        Image.fromarray(premul.astype(np.uint8)).resize((width, height), Image.LANCZOS)
    ).astype(np.float64)
    sa = small[:, :, 3:4] / 255.0
    rgb = np.where(sa > 0, small[:, :, :3] / np.maximum(sa, 1e-6), 0)
    return np.concatenate([np.clip(rgb, 0, 255), small[:, :, 3:4]], axis=2).astype(np.uint8)


def write_emblem(im, out, slug, version):
    """White-on-transparent mask for the card frame's corner discs.

    Squared off and centred here rather than in CSS, because the ten marks are
    not the same shape - a tall dive and a wide duck-on-waves both have to
    drop into the same round disc without either being stretched.
    """
    a = emblem_alpha(im)
    ys, xs = np.where(a > 0.02)
    cropped = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

    side = max(cropped.shape)
    square = np.zeros((side, side), np.float64)
    y = (side - cropped.shape[0]) // 2
    x = (side - cropped.shape[1]) // 2
    square[y:y + cropped.shape[0], x:x + cropped.shape[1]] = cropped

    rgba = np.zeros((side, side, 4), np.uint8)
    rgba[:, :, :3] = 255
    rgba[:, :, 3] = np.round(square * 255).astype(np.uint8)
    rgba = downscale(rgba, EMBLEM_BOX)

    dest = os.path.join(out, "pack-%s-emblem-v%d.webp" % (slug, version))
    Image.fromarray(rgba).save(dest, "WEBP", quality=90, method=6, lossless=True)
    kb = os.path.getsize(dest) / 1024
    print("%-36s %3dx%-3d %5.1fKB" % (os.path.basename(dest), rgba.shape[1], rgba.shape[0], kb))
    return kb


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="folder of <slug>_<kind>.png files")
    ap.add_argument("--version", type=int, required=True,
                    help="filename version, e.g. 2 for pack-locals-icon-v2.webp")
    ap.add_argument("--out", default=None, help="defaults to the repo's static/")
    ap.add_argument("--only", nargs="+", choices=KINDS, default=list(KINDS),
                    help="build just these kinds, so re-delivering one of them "
                         "does not renumber the others")
    args = ap.parse_args()

    out = args.out or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")

    # Same guard as unfound_hints.py: a slug that does not match a pack fails
    # loudly here rather than silently shipping a broken image link.
    wanted = {(p["art"], kind) for p in PACKS.values() for kind in args.only}
    missing = sorted("%s_%s.png" % (s, k) for s, k in wanted
                     if not os.path.exists(os.path.join(args.source, "%s_%s.png" % (s, k))))
    if missing:
        sys.exit("%s is missing %d file(s):\n  %s" % (args.source, len(missing), "\n  ".join(missing)))

    total = 0.0
    for slug, kind in sorted(wanted):
        src = os.path.join(args.source, "%s_%s.png" % (slug, kind))
        im = np.array(Image.open(src).convert("RGBA")).astype(np.int16)

        if kind == "emblem":
            total += write_emblem(im, out, slug, args.version)
            continue

        keep, had_caption = strip_caption(im)
        art = im.copy()
        art[:, :, 3] = np.where(keep, im[:, :, 3], 0)
        ys, xs = np.where(keep)
        art = art[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.uint8)
        art = downscale(art, TARGET_H[kind])

        dest = os.path.join(out, "pack-%s-%s-v%d.webp" % (slug, kind, args.version))
        Image.fromarray(art).save(dest, "WEBP", quality=88, method=6)
        kb = os.path.getsize(dest) / 1024
        total += kb


        print("%-36s %3dx%-3d %5.1fKB%s" % (os.path.basename(dest), art.shape[1],
                                            art.shape[0], kb,
                                            "" if had_caption else "  (no caption found)"))
    print("\n%d files, %.0f KB. Now point static/index.html at -v%d."
          % (len(wanted), total, args.version))


if __name__ == "__main__":
    main()
