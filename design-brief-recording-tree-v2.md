# Design Brief: Recording Tree Redesign (v2)

## Why this brief exists

We already went through one full round of this. The short version of what happened, because it directly shapes what's different below:

1. First delivery baked pivot markers (dots + text) directly into the artwork - unusable, had to be redone.
2. Second delivery was flattened onto a fake checkerboard (plain RGB, not real transparency), and two of the six canopy clusters genuinely overlapped in the source file with no clean seam between them - couldn't be cleanly separated no matter how carefully we tried to cut them apart.
3. Third delivery was an infographic-style sheet (multiple items composited into one image, card borders, captions, a "full assembled tree" panel with coordinate labels). It looked complete and well-labelled, but the individual layer thumbnails turned out to each be independently centred/framed for a nice preview rather than positioned at their true offset - so the scale was consistent across pieces but the position wasn't, and there was no way to reconstruct correct placement from it. We spent a long time trying to reverse-engineer a coordinate transform from card boundaries and marker dots before concluding it just wasn't recoverable.
4. Fourth delivery (a trunk image, alone, at a size whose aspect ratio matched the target canvas exactly) worked, because there was only one thing in the file and its own proportions gave away the scale unambiguously.
5. Fifth delivery (six canopy clusters, one per named PNG, each file's pixel dimensions exactly equal to the target canvas, pivot coordinates encoded straight into the filename) worked perfectly - composited correctly on the first attempt, zero fitting or guessing required. This is the format everything below is modelled on.

So: the delivery format is now solved. What's specified below is exactly the format from point 5, applied to every remaining piece (trunk included, which wasn't quite in this format last time - see Deliverables).

## Target style

Unchanged from the original brief - derived from everything else already shipped in Warble this project (mic badge, birdhouse badge, gear, trophy, cards, shop sign, avatar ring): painted wood/organic material with visible grain or leaf-vein detail, chunky rounded toy-like forms with a soft bevelled highlight/shadow, warm orange-to-brown for wood and mid-to-deep green for foliage, transparent background, no flat vector shading.

**New note based on comparing the last (correctly-registered) assembly against the reference tree:** each canopy cluster currently reads as a very similar-shaped rounded clump repeated six times, and each one appears to have its own independent light source, so the assembled tree looks slightly "pasted together" rather than lit as one cohesive object. The single reference illustration doesn't have this problem because it's one piece of art. Two things would help the next attempt read as more unified:
- Vary the silhouette of each of the six clusters more (different lobe shapes/sizes, not the same rounded pom-pom six times).
- Light every cluster from the same direction (matching the reference: light from upper-left, roughly) so shadows land consistently across the assembled canopy instead of each piece looking independently lit.

## What the current tree's animation does (must be preserved)

Unchanged from the original brief:

1. **Quiver (continuous, while recording).** Each canopy piece rotates slightly around its own pivot, reacting to its own assigned frequency band from the mic input, plus a small idle sway so it's never fully still.
2. **Rustle (triggered on bird detection).** A stronger directional wave starts from one cluster (as if something landed there) and travels across the others in sequence, plus a scatter of small leaf particles falls away from that point with gravity, drift, spin and fade-out.

## File delivery specification - read this section before generating anything

This is the part that caused most of the rework, so it's spelled out explicitly and unambiguously. Every file delivered must meet **all** of the following:

1. **One element per file.** Never deliver a sheet, grid, infographic, or multi-panel image with more than one layer in it. Each canopy cluster, and the trunk, is its own separate file. If several pieces are shown together for review purposes, that's a separate, clearly-labelled "preview only" image and is not one of the actual delivered assets.
2. **The file's own pixel dimensions ARE the canvas.** If the target canvas is 380 x 452, the PNG itself must be exactly 380 x 452 pixels - not a larger image that happens to be the right aspect ratio, not a thumbnail, not "close enough." Exact pixel match, checked before sending.
3. **Content sits at its true final position within that canvas, not centred.** This is the mistake that broke the third delivery. A cluster that belongs in the lower-right of the assembled tree should have a large empty transparent margin on its upper-left within its own 380x452 file - it should look "cropped weirdly" in isolation. That's correct. If every individual file looks like a nicely-centred, well-composed thumbnail on its own, something has gone wrong, because that means position information has been thrown away in favour of a pretty preview.
4. **Genuine alpha transparency, not a checkerboard.** Open the file and check the alpha channel directly (or: does it composite correctly over a solid colour with no grey squares showing?). A flattened preview with a checkerboard pattern drawn into the RGB channels is not the same thing as real transparency and cannot be recovered from afterward.
5. **No pivot markers, crosshairs, dots, labels, or captions baked into the image.** The pivot coordinate is metadata, delivered separately (see #6) - never drawn onto the art itself.
6. **Pivot/anchor coordinate encoded in the filename**, in the same style that worked: `C1_top_190_96_380x452.png` (element id, short name, x, y, canvas size). If a piece has no natural single pivot, say so rather than guessing.
7. **No two pieces should overlap in a way that can't be cleanly separated if they ever need to be** - this only matters if a sheet format is used at all, which per #1 it shouldn't be, but worth stating: every file must stand alone.

Before sending a batch, composite them yourself (stack all files at (0,0) at their native size, in the intended layer order) and eyeball the result. If it doesn't look like the tree, don't send it - that check takes a minute and would have caught delivery #3 immediately, before any time got spent on our end trying to make sense of it.

## Deliverables

All at 380 x 452 canvas, all meeting every point in the File Delivery Specification above:

1. **Trunk + base** - static, one file. (Last time this came as a much larger image at a matching aspect ratio, which worked but only because the ratio happened to be exact - this time, deliver it natively at 380x452 like the clusters were, so there's no resize-and-hope step at all.)
2. **Six canopy clusters** - C1 (top), C2 (upper-left), C3 (upper-right), C4 (lower-left), C5 (lower-center), C6 (lower-right). One file each, named and positioned per the spec above. Reuse the exact same pivot coordinates that already worked: C1 (190,96), C2 (122,152), C3 (258,152), C4 (108,228), C5 (190,232), C6 (274,236) - unless the redesign (addressing the "looks pasted together" note above) changes the clusters enough that new pivots make more sense, in which case new coordinates are fine as long as they're delivered the same explicit way.
3. **Leaf sprites** - 4 individual small leaf files (~128x128 each is fine, they're particles, not canvas-registered), transparent background, no card/frame around them, matching the redesigned painted style.

## Open questions for whoever's briefed with this

- Is six clusters still the right number, or would five or seven read better once shape variety is added? Not a fixed requirement, just flagging it's not sacred.
- Should the trunk also get a shape pass (it composited fine, but hasn't been evaluated against the "consistent lighting direction" note above)?
