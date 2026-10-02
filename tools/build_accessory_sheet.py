#!/usr/bin/env python3
"""Cut a sheet of Dress Up accessories into one transparent webp per item.

A local tool, not part of the running app - its libraries are deliberately not
in requirements.txt:

    pip install pillow numpy scipy --break-system-packages
    python3 tools/build_accessory_sheet.py SHEET.png --cols 3 --rows 6 \\
        --names round_specs,black_browline,... --prefix glasses --version 2

Items are read off the sheet column by column, top to bottom, and saved as
static/accessories/<prefix>_<name>-v<version>.webp. Always bump --version when
the art changes: the filename is this project's cache-buster.

Four things about these sheets are worth knowing, because they will happen
again on the next one:

1. The sheet arrives with REAL transparency, but viewers show it on a smeared
   coloured glow. That glow is the colour still stored in the near-invisible
   pixels round each item (alpha 1-15, up to ~9px out): it is not a background
   to remove, but it has to go, or each item wears a faint coloured fog. The
   alpha is remapped so 12 and below is gone and the soft edge above it stays.

2. The solid parts are not solid - frames top out at alpha 240-254 - so the
   same remap takes 240 and above to fully opaque. Otherwise the bird ghosts
   through every frame.

3. Items touch. A leaf tip or a wing joins two neighbours into one piece, and
   a loose sparkle or a monocle's chain is a piece on its own. Pieces are kept
   whole and handed to the cell their middle falls in; only a piece that
   straddles a row cut with real weight on both sides is split at the cut. The
   cuts are the emptiest row between each pair of rows.

4. The downscale is premultiplied. Resampling straight RGB drags the colour of
   transparent pixels into every edge - here that would be the glow again.

Clear lenses are drawn as frosted white at 55-70% opacity, which leaves the
bird's eyes milky behind them. --lens-clear scales down the alpha of bright,
colourless, translucent pixels (the lens) on the items named in
--lens-clear-names, and leaves everything else alone. Name them: tinted lenses
are drawn solid on purpose (they are shades), and the same test would
otherwise catch the white glare streaks painted on them.
"""
import argparse
import os

import numpy as np
from PIL import Image
from scipy import ndimage

ALPHA_FLOOR = 12      # at or below: the leftover glow, gone
ALPHA_SOLID = 240     # at or above: meant to be solid, made solid
PIECE_ALPHA = 40      # what counts as ink when finding pieces and cuts
EXPORT_W = 520        # px wide; the old glasses were ~510
PAD = 4               # px of air kept round each item before scaling


def remap_alpha(al):
    a = (al.astype(np.float64) - ALPHA_FLOOR) / (ALPHA_SOLID - ALPHA_FLOOR)
    return np.clip(a, 0, 1) * 255


def clear_lenses(rgba, keep):
    """Thin out frosted-white lens pixels so eyes show through them."""
    rgb = rgba[:, :, :3]
    al = rgba[:, :, 3]
    lum = rgb @ np.array([.2126, .7152, .0722])
    chroma = rgb.max(2) - rgb.min(2)
    lens = (al > 60) & (al < 235) & (lum > 170) & (chroma < 40)
    out = rgba.copy()
    out[:, :, 3] = np.where(lens, al * keep, al)
    return out, int(lens.sum())


def premul_resize(rgba, w):
    h = max(1, round(rgba.shape[0] * w / rgba.shape[1]))
    a = rgba[:, :, 3:4] / 255.0
    pm = np.concatenate([rgba[:, :, :3] * a, rgba[:, :, 3:4]], 2)
    sm = np.array(Image.fromarray(np.clip(pm, 0, 255).astype(np.uint8), 'RGBA')
                  .resize((w, h), Image.LANCZOS)).astype(np.float64)
    sa = sm[:, :, 3:4]
    rgb = np.where(sa > 0, sm[:, :, :3] / np.maximum(sa / 255.0, 1e-6), 0)
    return np.concatenate([np.clip(rgb, 0, 255), sa], 2).astype(np.uint8)


def split_sheet(sheet, cols, rows):
    """-> {(col, row): boolean mask of that item's pixels}"""
    al = sheet[:, :, 3]
    H, W = al.shape
    ink = al >= PIECE_ALPHA
    col_edges = [round(W * c / cols) for c in range(cols + 1)]
    cells = {}
    for c in range(cols):
        x0, x1 = col_edges[c], col_edges[c + 1]
        prof = ink[:, x0:x1].sum(1)
        cuts = []
        for r in range(1, rows):
            mid, span = H * r / rows, H / rows * 0.4
            lo, hi = int(mid - span), int(mid + span)
            cuts.append(lo + int(np.argmin(prof[lo:hi])))
        edges = [0] + cuts + [H]
        for r in range(rows):
            cells[(c, r)] = (x0, edges[r], x1, edges[r + 1])

    masks = {k: np.zeros_like(ink) for k in cells}
    lbl, n = ndimage.label(ink)
    for i in range(1, n + 1):
        piece = lbl == i
        ys, xs = np.where(piece)
        if len(xs) < 20:
            continue
        cx, cy = xs.mean(), ys.mean()
        home = next(k for k, (x0, y0, x1, y1) in cells.items() if x0 <= cx < x1 and y0 <= cy < y1)
        c = home[0]
        # does it straddle a cut with real weight both sides? then split it
        split = False
        for r in range(rows - 1):
            cut = cells[(c, r)][3]
            above = (ys < cut).sum()
            below = (ys >= cut).sum()
            if above > 500 and below > 500:
                m_above = piece.copy(); m_above[cut:, :] = False
                m_below = piece.copy(); m_below[:cut, :] = False
                masks[(c, r)] |= m_above
                masks[(c, r + 1)] |= m_below
                split = True
                break
        if not split:
            masks[home] |= piece
    # take back the soft edge round each item: everything faint within reach
    # of its own ink, so a cut never shaves an anti-aliased rim off
    for k in masks:
        near = ndimage.binary_dilation(masks[k], np.ones((7, 7)))
        x0, y0, x1, y1 = cells[k]
        box = np.zeros_like(near); box[y0:y1, x0:x1] = True
        masks[k] = near & (box | masks[k])
    return masks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sheet')
    ap.add_argument('--cols', type=int, required=True)
    ap.add_argument('--rows', type=int, required=True)
    ap.add_argument('--names', required=True, help='comma list, column by column, top to bottom')
    ap.add_argument('--prefix', required=True)
    ap.add_argument('--version', type=int, required=True)
    ap.add_argument('--lens-clear', type=float, default=None,
                    help='multiply frosted clear-lens alpha by this (e.g. 0.4)')
    ap.add_argument('--lens-clear-names', default='',
                    help='comma list of the items with clear lenses')
    ap.add_argument('--out', default='static/accessories')
    args = ap.parse_args()

    names = args.names.split(',')
    assert len(names) == args.cols * args.rows, f'{len(names)} names for {args.cols * args.rows} cells'
    sheet = np.array(Image.open(args.sheet).convert('RGBA')).astype(np.float64)
    masks = split_sheet(sheet, args.cols, args.rows)

    for idx, name in enumerate(names):
        c, r = divmod(idx, args.rows)
        m = masks[(c, r)]
        ys, xs = np.where(m)
        y0, y1 = max(ys.min() - PAD, 0), ys.max() + PAD + 1
        x0, x1 = max(xs.min() - PAD, 0), xs.max() + PAD + 1
        item = sheet[y0:y1, x0:x1].copy()
        item[:, :, 3] = np.where(m[y0:y1, x0:x1], remap_alpha(item[:, :, 3]), 0)
        note = ''
        if args.lens_clear is not None and name in args.lens_clear_names.split(','):
            item, n = clear_lenses(item, args.lens_clear)
            note = f'  {n} lens px thinned'
        small = premul_resize(item, min(EXPORT_W, item.shape[1]))
        path = os.path.join(args.out, f'{args.prefix}_{name}-v{args.version}.webp')
        Image.fromarray(small, 'RGBA').save(path, quality=90, method=6)
        print(f'{name:<20} {x1 - x0}x{y1 - y0} -> {small.shape[1]}x{small.shape[0]} '
              f'{os.path.getsize(path) // 1024}KB{note}')


if __name__ == '__main__':
    main()
