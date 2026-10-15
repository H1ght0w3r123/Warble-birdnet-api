"""Turn a delivered dance video of an avatar bird into the looping animated
WebP the "You've unlocked ..." celebration plays (AVATAR_DANCES in
static/index.html, static/avatar/<bird>/dance-v<N>.webp).

    pip install imageio-ffmpeg numpy pillow opencv-python   (ffmpeg comes with the first)
    python3 tools/dance_from_video.py <video.mp4> <bird> [version]

Why this exists: a dance arrives as an MP4 (Firefly makes them), and MP4
can't hold transparency, so "transparent background" comes out as solid
black. The blackbird's first one did - a black bird on black. It still cuts
out cleanly because the black round the bird is pure (0-2, never above ~14
even in compression noise) while the bird's darkest edge never gets that
low, so:
- a pixel is background if it's at most BLACK bright AND joined to the
  frame's edge through other such pixels (so the dark between the feathers,
  enclosed by the bird, stays bird);
- of what's left, only the biggest piece is the bird (drops specks of noise);
- the one-pixel ring round it eases in over the last levels of black, for
  a soft edge instead of a jagged one.
Higher thresholds than 6 were tried and eat into the dark gap between wing
and body. A bird on a colour (green, magenta) would cut out more easily -
ask for that, or a WebM/MOV with real transparency, if a pale bird ever
loses its edge to this.

The video frames the bird so tightly that wide wing flaps run off its left
and right edges; their cut-off tips are faded out over EDGE_FADE pixels so
they don't end in a straight line. The picture is cropped to the band of
rows the bird ever uses (worked out over every frame), and every other
frame is kept (EVERY), at the same speed.
"""
import glob
import os
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image

BLACK = 6           # background is at most this bright (0-255)
EDGE_FADE = 36      # px, in the video's own size
WIDTH = 432         # px wide, about twice the size it's shown at
QUALITY = 70
EVERY = 2           # keep every 2nd frame: 12 a second. All 24 at this size
                    # was 3 MB - too much to fetch on a phone as the card
                    # opens; 12 is 1.5 MB and still reads as a dance.
AVATAR = os.path.join(os.path.dirname(__file__), '..', 'static', 'avatar')


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return 'ffmpeg'


def cut(path):
    im = np.asarray(Image.open(path).convert('RGB'))
    lum = im.max(-1).astype(int)
    bg = (lum <= BLACK).astype(np.uint8)
    _, lab = cv2.connectedComponents(bg, connectivity=4)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    outside = np.isin(lab, edge) & (bg == 1)
    _, lab2, stats, _ = cv2.connectedComponentsWithStats((~outside).astype(np.uint8), connectivity=8)
    bird = lab2 == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    alpha = bird.astype(np.float64)
    ring = (cv2.dilate(bird.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) & ~bird
    alpha[ring] = np.clip((lum[ring] - 1) / 6, 0, 1)
    a = cv2.GaussianBlur((alpha * 255).astype(np.uint8), (3, 3), 0)
    a[bird] = 255
    return np.dstack([im, a])


def main(video, bird, version='1'):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([ffmpeg(), '-v', 'error', '-i', video, os.path.join(tmp, 'f%04d.png')], check=True)
        frames = [cut(p) for p in sorted(glob.glob(os.path.join(tmp, 'f*.png')))[::EVERY]]
    h, w = frames[0].shape[:2]
    rows = np.nonzero(np.any(np.stack([f[..., 3] > 8 for f in frames]).any(0), axis=1))[0]
    y0, y1 = max(0, rows[0] - 10), min(h, rows[-1] + 11)
    x = np.arange(w)
    fade = np.clip(np.minimum(x, w - 1 - x) / EDGE_FADE, 0, 1)
    out_h = round(WIDTH * (y1 - y0) / w)
    ims = []
    for f in frames:
        f = f[y0:y1].astype(np.float32)
        f[..., 3] *= fade[None, :]
        ims.append(Image.fromarray(f.round().astype(np.uint8), 'RGBA').resize((WIDTH, out_h), Image.LANCZOS))
    dest = os.path.join(AVATAR, bird, f'dance-v{version}.webp')
    fps = 24 / EVERY   # the delivered videos are 24 a second
    ims[0].save(dest, save_all=True, append_images=ims[1:], duration=round(1000 / fps), loop=0,
                quality=QUALITY, method=4)
    print(f'{dest}: {len(ims)} frames, {WIDTH}x{out_h}, {os.path.getsize(dest) // 1024} KB')


if __name__ == '__main__':
    main(*sys.argv[1:])
