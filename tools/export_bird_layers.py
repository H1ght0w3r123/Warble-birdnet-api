"""Export a delivered bird's layers to static/avatar/<id>/.

The app's colour wash is a luminance filter: it desaturates the art and then
runs the result through a ramp to the child's swatch. So the only thing that
survives from a washable layer is how BRIGHT it is - and two washable layers at
different brightness come out as two different shades of the same colour.

Layers delivered in neutral grey are passed through untouched. A washable layer
delivered in colour is converted to luminance and rescaled to match the mean
and spread of this bird's grey layers, so the whole bird washes as one piece.
That is a straight linear map, so the artist's modelling survives it.
"""
from PIL import Image
import numpy as np, os, sys

W = np.array([.2126, .7152, .0722])
CHROMA_LIMIT = 40        # above this a washable layer counts as "painted in colour"

def load(p): return np.array(Image.open(p).convert('RGBA')).astype(np.float64)

def washable(art, mask):
    return (mask[:, :, 3] > 128) & (art[:, :, 3] > 200)

def stats(art, sel):
    lum = (art[sel][:, :3] * W).sum(1)
    return lum.mean(), lum.std(), (art[sel][:, :3].max(1) - art[sel][:, :3].min(1)).mean()

def neutralise(art, mask, target_mean, target_sd):
    """Flatten a colour-painted washable region to grey at the reference tone."""
    sel = washable(art, mask)
    lum = (art[:, :, :3] * W).sum(2)
    m, sd, _ = stats(art, sel)
    scaled = np.clip((lum - m) * (target_sd / max(sd, 1e-6)) + target_mean, 6, 249)
    out = art.copy()
    for c in range(3):
        out[:, :, c] = np.where(sel, scaled, art[:, :, c])
    return out

def downscale(arr, size):
    """Premultiplied, so transparent pixels never bleed their colour into the rim."""
    a = arr[:, :, 3:4] / 255.0
    pm = np.concatenate([arr[:, :, :3] * a, arr[:, :, 3:4]], axis=2)
    sm = np.array(Image.fromarray(pm.astype(np.uint8), 'RGBA')
                  .resize((size, size), Image.LANCZOS)).astype(np.float64)
    sa = np.clip(sm[:, :, 3:4], 0, 255)
    rgb = np.where(sa > 0, sm[:, :, :3] / np.maximum(sa / 255.0, 1e-6), 0)
    return np.concatenate([np.clip(rgb, 0, 255), sa], axis=2).astype(np.uint8)

def export(bird_id, src_dir, jobs, size=800):
    """jobs: list of (art file, mask file or None, output name)"""
    art = {o: load(os.path.join(src_dir, a)) for a, m, o in jobs}
    msk = {o: (load(os.path.join(src_dir, m)) if m else None) for a, m, o in jobs}

    # the reference tone is whatever this bird's already-grey washable layers use
    greys = []
    for a, m, o in jobs:
        if msk[o] is None: continue
        mean, sd, ch = stats(art[o], washable(art[o], msk[o]))
        if ch <= CHROMA_LIMIT: greys.append((mean, sd))
    ref_mean = float(np.mean([g[0] for g in greys])) if greys else 150.0
    ref_sd   = float(np.mean([g[1] for g in greys])) if greys else 32.0
    print(f'{bird_id}: reference tone from {len(greys)} grey layer(s) - mean {ref_mean:.1f}, sd {ref_sd:.1f}')

    out_dir = f'static/avatar/{bird_id}/'
    os.makedirs(out_dir, exist_ok=True)
    total = 0
    for a, m, o in jobs:
        arr = art[o]
        if msk[o] is not None:
            mean, sd, ch = stats(arr, washable(arr, msk[o]))
            if ch > CHROMA_LIMIT:
                arr = neutralise(arr, msk[o], ref_mean, ref_sd)
                after = stats(arr, washable(arr, msk[o]))
                print(f'  {o:<16} painted in colour (chroma {ch:.0f}, luminance {mean:.0f})'
                      f' -> neutralised to {after[0]:.0f}')
            else:
                print(f'  {o:<16} already neutral (chroma {ch:.0f}, luminance {mean:.0f}) - untouched')
        small = downscale(arr, size)
        if o.startswith('wash-'):
            small[:, :, :3] = 255          # masks are read by luminance
        p = out_dir + o
        Image.fromarray(small, 'RGBA').save(p, quality=92 if not o.startswith('wash-') else 85, method=6)
        total += os.path.getsize(p) / 1024
    print(f'  {total:.0f} KB total')
