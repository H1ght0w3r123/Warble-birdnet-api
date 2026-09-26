"""Export a delivered bird's layers to static/avatar/<id>/.

The app's colour wash is a luminance filter: it desaturates a washable layer
and runs the result through a ramp to the child's swatch. So the only thing
that survives is how BRIGHT the art is, and two washable layers at different
brightness come out as two different shades of the same colour.

Layers delivered in neutral grey are passed through untouched. A washable layer
delivered in colour is converted to luminance and rescaled to match this bird's
grey layers, so the whole bird washes as one piece. The map is linear, so the
artist's modelling survives it.

Everything is judged on the VISIBLE part of each layer only - the part not
covered by a layer above it in the stack. The Parrot's head layer is the reason
this matters: it carries the yellow face underneath a separate fixed overlay,
which drags its measured chroma to 60 while the plumage a child actually sees
is a clean neutral 18. Measured on the whole layer it looks like it needs
fixing; measured on what shows, it plainly does not.
"""
from PIL import Image
import numpy as np
import os

LUMA = np.array([.2126, .7152, .0722])
CHROMA_LIMIT = 40          # above this, a visible washable region counts as painted in colour


def load(path):
    return np.array(Image.open(path).convert('RGBA')).astype(np.float64)


def measure(art, sel):
    px = art[sel][:, :3]
    lum = (px * LUMA).sum(1)
    return lum.mean(), lum.std(), (px.max(1) - px.min(1)).mean()


def neutralise(art, region, target_mean, target_sd, measured):
    """Flatten a colour-painted washable region to grey at the reference tone."""
    mean, sd, _ = measured
    lum = (art[:, :, :3] * LUMA).sum(2)
    scaled = np.clip((lum - mean) * (target_sd / max(sd, 1e-6)) + target_mean, 6, 249)
    out = art.copy()
    for c in range(3):
        out[:, :, c] = np.where(region, scaled, art[:, :, c])
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


def export(bird_id, src_dir, stack, extras=(), size=800):
    """stack:  back-to-front list of (art file, wash mask file or None, output name)
       extras: (source file, output name) pairs copied straight through - the wash
               masks themselves, which are not part of the visual stack and must
               not be counted as covering the layers beneath them."""
    art = {out: load(os.path.join(src_dir, a)) for a, m, out in stack}
    msk = {out: (load(os.path.join(src_dir, m)) if m else None) for a, m, out in stack}
    names = [out for _, _, out in stack]

    # What each layer actually shows: its own alpha minus everything above it.
    covered = {}
    above = np.zeros(art[names[0]].shape[:2], bool)
    for name in reversed(names):
        covered[name] = above.copy()
        above = above | (art[name][:, :, 3] > 200)

    def visible_wash(name):
        if msk[name] is None:
            return None
        return (msk[name][:, :, 3] > 128) & (art[name][:, :, 3] > 200) & ~covered[name]

    # The reference tone is whatever this bird's already-neutral layers use.
    greys = []
    for name in names:
        sel = visible_wash(name)
        if sel is None or sel.sum() < 500:
            continue
        mean, sd, chroma = measure(art[name], sel)
        if chroma <= CHROMA_LIMIT:
            greys.append((mean, sd))
    ref_mean = float(np.mean([g[0] for g in greys])) if greys else 150.0
    ref_sd = float(np.mean([g[1] for g in greys])) if greys else 32.0
    print(f'{bird_id}: reference tone from {len(greys)} neutral layer(s) '
          f'- luminance {ref_mean:.0f}, sd {ref_sd:.0f}')

    out_dir = f'static/avatar/{bird_id}/'
    os.makedirs(out_dir, exist_ok=True)
    total = 0
    for src, name in extras:
        small = downscale(load(os.path.join(src_dir, src)), size)
        small[:, :, :3] = 255               # masks are read by luminance
        path = out_dir + name
        Image.fromarray(small, 'RGBA').save(path, quality=85, method=6)
        total += os.path.getsize(path) / 1024
    for a, m, name in stack:
        arr = art[name]
        sel = visible_wash(name)
        if sel is not None and sel.sum() >= 500:
            stats = measure(arr, sel)
            mean, sd, chroma = stats
            if chroma > CHROMA_LIMIT:
                whole = (msk[name][:, :, 3] > 128) & (arr[:, :, 3] > 200)
                arr = neutralise(arr, whole, ref_mean, ref_sd, stats)
                after = measure(arr, sel)
                print(f'  {name:<18} painted in colour (visible chroma {chroma:.0f}, '
                      f'luminance {mean:.0f}) -> neutralised to {after[0]:.0f}')
            else:
                print(f'  {name:<18} already neutral (visible chroma {chroma:.0f}, '
                      f'luminance {mean:.0f}) - untouched')
        path = out_dir + name
        Image.fromarray(downscale(arr, size), 'RGBA').save(path, quality=92, method=6)
        total += os.path.getsize(path) / 1024
    print(f'  {total:.0f} KB total')
