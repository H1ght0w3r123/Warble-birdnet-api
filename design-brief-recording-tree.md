# Design Brief: Recording Tree Redesign

## Background

Every other piece of art in Warble — the mic button, the Home birdhouse badge, the Trophies and Collections nav icons, the settings gear, the Awards/My Flock/OutFlitters-era wordmarks, The Hoot-tique sign, the Dress Up avatar ring — has been redrawn in a consistent hand-painted, chunky wood-toy style. The recording-screen tree is the one major element still in the *old* placeholder style: a flat, low-poly geometric shape built from ~59 triangular facets. It needs to be redrawn to match everything else, without losing what the tree currently *does*.

## Target style

Derived from the assets already shipped this project — use this as the style guide for the redesign, and for any leaf sprites made alongside it:

- **Material:** painted wood — visible grain lines running along each form, occasional cracks/knots as texture detail, like the mic badge, birdhouse badge, gear, trophy, cards and shop sign.
- **Rendering:** chunky, rounded, slightly toy-like 3D forms with soft bevelled edges — a highlight along the top/lit edge of each shape and a deeper shadow tone along the underside, not flat/vector shading.
- **Palette:** warm orange-to-brown wood tones (roughly `#E8845C` → `#B85A36` → `#5A3A28` range) for trunk/bark; the canopy should introduce green in the same painted-wood/organic rendering style established by the leaf accents on the Hoot-tique sign (mid-to-deep greens, not the flat `#3F7C5C`/`#5FB88F` fills currently used).
- **Shadow:** a soft, blurred ambient drop shadow under the whole tree, consistent with how other elements sit on the page (see the avatar ring, mic button).
- **Format:** transparent-background PNG per layer (see Deliverables) — no baked-in background, no baked-in drop shadow if that's going to be applied in CSS as it is elsewhere (confirm which; recommend baking the shadow in, since that's how the existing tree does it and how most other elements on the page work).

## What the current tree does (must be preserved)

The tree sits on the live recording screen and reacts to audio in real time. There are two distinct animation levels layered on top of each other, both driven from JS, both currently implemented by transforming individual SVG polygons:

1. **Quiver (continuous, while recording).** The canopy is split into ~59 small triangular facets, each pre-assigned a frequency bin, an amplitude, and a rotation pivot point baked into the SVG (`data-bin`, `data-amp`, `data-pivot`). Every animation frame, each facet reads the current volume in *its* frequency band and rotates slightly around its own pivot — plus a gentle idle "breathing" sway so the tree is never fully still even in silence. The result reads as a shimmer that ripples unevenly across the canopy in response to whatever sound is coming in, rather than the whole tree moving as one rigid piece.
2. **Rustle (triggered the instant a bird is detected).** A stronger, directional wave starts from a point on the canopy's edge (as if something just landed there) and travels inward across the facets at a fixed speed, each facet kicking harder as the wave reaches it, decaying as it goes. At the same moment, 13 small leaf particles spawn from that landing point and fall away from the tree with gravity, drift, spin, and fade-out.

Current technical footprint, for reference:
- Rendered at 190×226px (`viewBox="0 0 160 190"`), canopy centred around SVG coordinate (80, 72).
- Trunk is currently a separate faceted shape (6-ish two-tone polygon pairs) below the canopy — this should become part of the new painted-wood trunk layer.
- Leaf particles are currently plain 4-point polygons, flat-filled from `['#F2C94C', '#5FB88F', '#7EC8A4', '#3F7C5C']` — these are the ones flagged for a matching illustrated redesign below (a separate, smaller flat-colour leaf-scatter effect elsewhere in the app, used when a card turns into a bird, is out of scope — only the recording tree's own leaves are covered here).

## The core constraint: 59 independently-rotating facets isn't an illustration brief

That per-facet wave effect works because the current canopy is built from dozens of small, flat, individually-rotatable polygons — which is a natural fit for procedural/vector art but not for a single hand-painted illustration. Asking for 59 separate painted facets that tile together seamlessly isn't realistic to produce or to keep looking good as they rotate independently.

**Recommendation:** rebuild the canopy as a small number of separate illustrated *clusters* (roughly 5-9 — e.g. upper crown, left mass, right mass, one or two lower masses, per rough size/position of today's canopy) rather than one flat piece or 59 tiny ones. Each cluster gets animated as a whole (quiver = small independent sway per cluster on its own pivot, driven by its own frequency band, same idea as today just far fewer moving parts; rustle = the same directional wave logic, just propagating across a handful of clusters instead of 59 facets). This keeps both animation beats intact at a coarser, illustration-friendly granularity. Flagging this as a recommendation rather than a locked decision — open to a different breakdown if there's a cleaner way to hit the same two behaviours.

## Deliverables

All layers at the same canvas size and in registration (so stacking them at (0,0) reproduces the full tree exactly as one piece), transparent PNG, 2x resolution for the ~190×226px display size (so roughly 380×452px canvas):

1. **Trunk + base layer** — static, doesn't animate. Painted wood trunk, root flare/base shadow.
2. **Canopy cluster layers** — one file per cluster (proposed 5-9, see above). Each needs:
   - A marked or documented **pivot point** (the coordinate it should rotate around), analogous to today's `data-pivot` — probably where that cluster visually attaches to the trunk/the cluster behind it, so rotation reads naturally rather than swinging from its own centre.
   - Enough of the cluster behind/around the pivot painted in (not just the visible leafy silhouette) so that small rotations don't reveal a gap where the layer used to be.
3. **Leaf sprite(s)** — 2-4 small individual illustrated leaves (painted-wood/organic style matching the canopy, transparent background, small enough to read as a particle at ~8-12px on screen) to replace the flat-colour polygon currently used in `spawnFallingLeaves()`. A little size/rotation variation between the 2-4 sprites is enough — the particle system already randomises position, velocity, spin and fade.

## Open questions for whoever's briefed with this

- How many canopy clusters actually look good broken apart vs. how many is a burden to paint? 5-9 is a starting guess, not a hard number.
- Should the trunk get any subtle motion at all (today it's fully static), or stay static as the anchor the canopy moves against?
- Any appetite for a distinct "just landed a bird" pose/flourish baked into the art itself, beyond what the rustle transform already does procedurally?
