#!/usr/bin/env python3
"""Cut the small painted icons (design-brief-info-icons-v1.md) out of one
delivered sheet and write static/icon-<name>-v1.webp for each.

The first delivery came as ONE picture, not 24 files: the icons in four rows
on a white background, each with its name printed underneath. This turns
that into the files the app wants. A local tool, not part of the app:

    pip install pillow numpy scipy --break-system-packages
    python3 tools/build_icons.py sheet.png static
    python3 tools/build_icons.py sheet.png static report   # also lists enclosed white patches

How it works, and what to check if a new sheet looks different:
- Rows are found where the picture has no ink across a whole line; a row
  taller than 100px is icons, a thin one is the printed names, which are
  skipped. NAMES below must match the sheet's order, row by row.
- Within a row, icons are split at columns with no ink (gaps under 14px
  are parts of one icon, like the worm and the seed).
- The white background becomes transparent by flooding in from the edges,
  so white inside a picture (the foam on the wave, the house walls) stays.
  Enclosed patches that are the background showing through a gap - the
  triangles in the scales, the pin's hole, the lock's loop - are cut too:
  near-white, grey rather than coloured, and at least 40px.
- Edge pixels are un-mixed from the white, so there's no white fringe on a
  coloured background. Check the output on solid red.
- Each icon keeps its own shape, 128px tall: the page sizes icons by
  height, so a wide one (wingspan) stays wide.
A redraw of one icon is -v2 (change the name in the save line); the server
always serves the newest version it finds.
"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
src, outdir = sys.argv[1], sys.argv[2]
REPORT = len(sys.argv) > 3
a = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H, W, _ = a.shape
diff = np.abs(a - 255).max(axis=2)
fg = diff > 18
rows = fg.sum(axis=1)
bands = []; on = False
for y, v in enumerate(rows):
    if v > 0 and not on: start = y; on = True
    if v == 0 and on: bands.append((start, y)); on = False
icon_bands = [b for b in bands if b[1] - b[0] > 100]
NAMES = [['weight','length','wingspan','habitat','diet'],
         ['garden-parks','woodland','wetland-coast','farmland','towns'],
         ['tip-sunrise','tip-quiet','tip-places','tip-close','tip-rain','tip-calm'],
         ['pin','lock','camera','back','forward','close','pause','mystery']]
report = []
for (y0, y1), names in zip(icon_bands, NAMES):
    cols = fg[y0:y1].sum(axis=0)
    segs = []; on = False
    for x, v in enumerate(cols):
        if v > 0 and not on: s = x; on = True
        if v == 0 and on: segs.append((s, x)); on = False
    if on: segs.append((s, W))
    # merge segments separated by small gaps (parts of one icon)
    merged = []
    for sg in segs:
        if merged and sg[0] - merged[-1][1] < 14: merged[-1] = (merged[-1][0], sg[1])
        else: merged.append(sg)
    merged = [m for m in merged if m[1] - m[0] > 20]
    report.append((names, merged))
    assert len(merged) == len(names), (names, merged)
    for name, (x0, x1) in zip(names, merged):
        pad = 6
        X0, X1, Y0, Y1 = max(0, x0 - pad), min(W, x1 + pad), max(0, y0 - pad), min(H, y1 + pad)
        crop = a[Y0:Y1, X0:X1]
        d = np.abs(crop - 255).max(axis=2)
        # background: near-white connected to the crop's edge
        near = d <= 40
        lab, n = ndi.label(near)
        edge_labels = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        bg = np.isin(lab, list(edge_labels))
        # enclosed pure-white holes (the pin's hole) - report them, cut them if big and truly white
        holes = near & ~bg
        hl, hn = ndi.label(holes)
        cut_holes = []
        for i in range(1, hn + 1):
            m = hl == i
            sat = (crop[m].max(axis=1) - crop[m].min(axis=1)).mean()
            if REPORT: print(f'   {name}: enclosed {int(m.sum())}px  mean diff {d[m].mean():.1f}  sat {sat:.1f}')
            # background showing through a gap: big enough, nearly white, and grey-white (not cream, not foam blue)
            if m.sum() >= 40 and d[m].mean() <= 14 and sat <= 6:
                bg |= m; cut_holes.append(int(m.sum()))
        alpha = np.ones(d.shape, np.float32)
        alpha[bg] = 0
        # soft edge: background pixels touching the shape take alpha from how un-white they are
        ring = bg & ndi.binary_dilation(~bg, iterations=2)
        alpha[ring] = np.clip((d[ring] - 6) / 60, 0, 1)
        rgb = crop.copy()
        aa = alpha[..., None]
        safe = np.where(aa > 0.02, aa, 1)
        rgb = np.where(aa > 0.02, (crop - 255 * (1 - aa)) / safe, crop)   # un-mix the white
        rgb = np.clip(rgb, 0, 255)
        img = np.dstack([rgb, alpha * 255]).astype(np.uint8)
        im = Image.fromarray(img, 'RGBA')
        bb = im.getbbox(); im = im.crop(bb)
        # Kept to its own shape, 128px tall (2x the largest it is shown at):
        # the page sizes icons by height, so a wide one stays wide.
        h = 128; w = max(1, round(im.width * h / im.height))
        im.resize((w, h), Image.LANCZOS).save(f'{outdir}/icon-{name}-v1.webp', 'WEBP', quality=90, method=6)
        print(f'{name:14} crop {x1-x0}x{y1-y0}  holes cut {cut_holes}')
