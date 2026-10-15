"""Turn a delivered dance video of an avatar bird into the two looping,
see-through files the "You've unlocked ..." celebration plays (AVATAR_DANCES
in static/index.html): static/avatar/<bird>/dance-v<N>.webm and .webp.

Two because no one format does it everywhere, smoothly and small:
- a WebM (VP9 with transparency), all 24 frames a second, about 0.7 MB -
  what Chrome, Android, Firefox and Edge play;
- an animated WebP, all 24 frames, about 2 MB - for iPhones and Safari,
  which can't show a see-through WebM (Apple's own see-through video, HEVC
  with alpha, can only be made on a Mac).
Every frame is kept: halving to 12 a second to save size was tried first,
and the dance looked jerky.

    pip install imageio-ffmpeg numpy pillow opencv-python   (ffmpeg comes with the first)
    python3 tools/dance_from_video.py <video.mp4> <bird> [version]

A dance arrives as an MP4 (Firefly makes them), and MP4 can't hold
transparency, so the bird comes on a flat background that's cut away here.
Which one is worked out from the frame's edges:

GREEN (or MAGENTA, for a bird with green in it) - what to ask for. A pixel
is background as far as the key colour outweighs the others (for green,
G minus the larger of R and B): fully see-through past KEY_HI, fully bird
under KEY_LO, soft in between. The green the edge pixels carry from the
background is then taken out of them ("despill"), or the bird wears a
green halo. Firefly's green is a slightly uneven (75, 183, 39), not
#00FF00 - why it's a range, not a colour.

BLACK - the blackbird's first dance came this way: a black bird on black.
It still cuts out because the black round the bird is pure (0-2, never
above ~14 even in compression noise) while the bird's darkest edge never
gets that low, so:
- a pixel is background if it's at most BLACK bright AND joined to the
  frame's edge through other such pixels (so the dark between the feathers,
  enclosed by the bird, stays bird);
- of what's left, only the biggest piece is the bird (drops specks of noise);
- the one-pixel ring round it eases in over the last levels of black, for
  a soft edge instead of a jagged one.
Higher thresholds than 6 were tried and eat into the dark gap between wing
and body.

Either way, only the biggest piece left is kept (drops specks), and the
loop is checked: the jump from the last frame back to the first is
compared with a typical frame-to-frame step, and reported. Ask for the
same picture as the first and last frame, and it comes back close to one.

The video frames the bird so tightly that wide wing flaps run off its left
and right edges; their cut-off tips are faded out over EDGE_FADE of the width so
they don't end in a straight line. The picture is cropped to the band of
rows the bird ever uses (worked out over every frame).
"""
import glob
import os
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image

BLACK = 6           # black background: at most this bright (0-255)
KEY_LO, KEY_HI = 28, 70   # green/magenta: how far the key colour outweighs the rest
BORDER = 4          # px round the frame's edge that are never bird
EDGE_FADE = 0.05    # of the width: how far in from each side the cut-off wingtips fade
WORK_WIDTH = 540    # frames are shrunk to this as soon as they're cut (a
                    # 1080x1920 video at full size is 1.6 GB held in memory)
FPS = 24            # the delivered videos' own rate; every frame is kept
WEBM_WIDTH = 432    # px wide, a bit over twice the size it's shown at
WEBM_CRF = 36       # VP9 quality (lower is better and bigger)
WEBP_WIDTH = 372    # an animated WebP compresses frames far worse than video:
WEBP_QUALITY = 60   # this keeps it near 2 MB
AVATAR = os.path.join(os.path.dirname(__file__), '..', 'static', 'avatar')


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return 'ffmpeg'


def background(path):
    """'black', 'green' or 'magenta', from the median colour of the frame's edge."""
    im = np.asarray(Image.open(path).convert('RGB')).astype(int)
    edge = np.concatenate([im[0], im[-1], im[:, 0], im[:, -1]])
    r, g, b = np.median(edge, axis=0)
    if max(r, g, b) < 30:
        return 'black'
    if g > r + 40 and g > b + 40:
        return 'green'
    if r > g + 40 and b > g + 40:
        return 'magenta'
    sys.exit(f'Background colour {(r, g, b)} is not black, green or magenta - not sure how to cut it.')


def shrink(frame):
    h, w = frame.shape[:2]
    if w <= WORK_WIDTH:
        return frame
    # Shrink with the colour weighted by its alpha, so see-through pixels
    # (whatever colour they had) don't darken the edges
    a = frame[..., 3:4].astype(np.float32) / 255
    rgb = cv2.resize(frame[..., :3].astype(np.float32) * a, (WORK_WIDTH, round(h * WORK_WIDTH / w)), interpolation=cv2.INTER_AREA)
    al = cv2.resize(a[..., 0], (WORK_WIDTH, round(h * WORK_WIDTH / w)), interpolation=cv2.INTER_AREA)
    rgb = rgb / np.maximum(al[..., None], 1e-6)
    return np.dstack([np.clip(rgb, 0, 255), al * 255]).round().astype(np.uint8)


def biggest(mask):
    _, lab, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    return lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])


def cut(path, bg_kind):
    im = np.asarray(Image.open(path).convert('RGB'))
    if bg_kind == 'black':
        return cut_black(im)
    f = im.astype(np.float64)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    if bg_kind == 'green':
        key, others = g, np.maximum(r, b)
    else:
        key, others = np.minimum(r, b), g
    alpha = np.clip((KEY_HI - (key - others)) / (KEY_HI - KEY_LO), 0, 1)
    # Firefly's videos have a thin dark line round the very edge of the
    # frame: not bird, but it would join on wherever a wing touches it.
    alpha[:BORDER], alpha[-BORDER:], alpha[:, :BORDER], alpha[:, -BORDER:] = 0, 0, 0, 0
    alpha *= biggest(alpha > 0.5)
    # Despill: no edge pixel keeps more of the key colour than the others have
    if bg_kind == 'green':
        f[..., 1] = np.minimum(g, others)
    else:
        excess = np.maximum(np.minimum(r, b) - g, 0)
        f[..., 0] = r - excess
        f[..., 2] = b - excess
    a = cv2.GaussianBlur((alpha * 255).astype(np.uint8), (3, 3), 0)
    return np.dstack([f.round().astype(np.uint8), a])


def cut_black(im):
    lum = im.max(-1).astype(int)
    bg = (lum <= BLACK).astype(np.uint8)
    _, lab = cv2.connectedComponents(bg, connectivity=4)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    outside = np.isin(lab, edge) & (bg == 1)
    bird = biggest(~outside)
    alpha = bird.astype(np.float64)
    ring = (cv2.dilate(bird.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) & ~bird
    alpha[ring] = np.clip((lum[ring] - 1) / 6, 0, 1)
    a = cv2.GaussianBlur((alpha * 255).astype(np.uint8), (3, 3), 0)
    a[bird] = 255
    return np.dstack([im, a])


def main(video, bird, version='1'):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([ffmpeg(), '-v', 'error', '-i', video, os.path.join(tmp, 'f%04d.png')], check=True)
        paths = sorted(glob.glob(os.path.join(tmp, 'f*.png')))
        kind = background(paths[0])
        frames = [shrink(cut(p, kind)) for p in paths]
    steps = [np.abs(frames[i + 1][..., :3].astype(np.int16) - frames[i][..., :3]).mean() for i in range(len(frames) - 1)]
    seam = np.abs(frames[0][..., :3].astype(np.int16) - frames[-1][..., :3]).mean()
    print(f'{kind} background; loop: last-to-first jump {seam / np.median(steps):.1f}x a typical step'
          + (' - it will show; ask for the same first and last frame' if seam > 2.5 * np.median(steps) else ''))
    h, w = frames[0].shape[:2]
    rows = np.nonzero(np.any(np.stack([f[..., 3] > 8 for f in frames]).any(0), axis=1))[0]
    y0, y1 = max(0, rows[0] - 10), min(h, rows[-1] + 11)
    x = np.arange(w)
    fade = np.clip(np.minimum(x, w - 1 - x) / (EDGE_FADE * w), 0, 1)
    big = []
    for f in frames:
        f = f[y0:y1].astype(np.float32)
        f[..., 3] *= fade[None, :]
        big.append(Image.fromarray(f.round().astype(np.uint8), 'RGBA'))
    base = os.path.join(AVATAR, bird, f'dance-v{version}')

    # The WebM, through ffmpeg from a folder of see-through PNGs
    size = (WEBM_WIDTH, round(WEBM_WIDTH * (y1 - y0) / w))
    with tempfile.TemporaryDirectory() as tmp:
        for i, im in enumerate(big):
            im.resize(size, Image.LANCZOS).save(os.path.join(tmp, f'f{i:04d}.png'))
        subprocess.run([ffmpeg(), '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, 'f%04d.png'),
                        '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-auto-alt-ref', '0',
                        '-crf', str(WEBM_CRF), '-b:v', '0', '-row-mt', '1', base + '.webm'], check=True)
    print(f'{base}.webm: {len(big)} frames, {size[0]}x{size[1]}, {os.path.getsize(base + ".webm") // 1024} KB')

    # The WebP, for Safari
    size = (WEBP_WIDTH, round(WEBP_WIDTH * (y1 - y0) / w))
    ims = [im.resize(size, Image.LANCZOS) for im in big]
    ms = [round((i + 1) * 1000 / FPS) - round(i * 1000 / FPS) for i in range(len(ims))]   # 41/42/42...
    ims[0].save(base + '.webp', save_all=True, append_images=ims[1:], duration=ms, loop=0,
                quality=WEBP_QUALITY, alpha_quality=80, method=4)
    print(f'{base}.webp: {len(ims)} frames, {size[0]}x{size[1]}, {os.path.getsize(base + ".webp") // 1024} KB')


if __name__ == '__main__':
    main(*sys.argv[1:])
