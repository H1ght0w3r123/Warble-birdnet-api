# Warble

A bird-identification app for children aged 5–8. A child goes outside, taps
record, and BirdNET identifies the birdsong. Finds become collectable cards,
feathers to spend on dressing up their avatar, and trophies.

Built by Phil, who is not a professional developer — explain reasoning, flag
trade-offs, and don't assume familiarity with build tooling or frameworks.

## Stack

- **Backend:** Python / FastAPI on Railway, PostgreSQL on the same project
- **Frontend:** ONE file — `static/index.html` — ~3,400 lines of inline HTML,
  CSS, JS and SVG. No framework, no build step, no npm. Deliberate: it keeps
  deployment trivial. Don't restructure it without asking.
- **Deploy:** push to `main` on GitHub → Railway builds. Phil sometimes has to
  redeploy manually, so always say so after pushing.

## The data model, in order of importance

- `curated_species.py` — the UK 100, as **10 themed packs of 10**. Each pack is
  8 common + 2 rare. This is the single source of truth for which birds Warble
  knows about, which pack they're in, and how rare they are.
- `birds.py` — everything known about each of the 100: size, weight, speed,
  population, song, brains, habitat, diet. Drives the stat tiles and the Top
  Trumps ratings. 59 of the 100 also have researched extras (wingspan,
  conservation status, kid-friendly comparisons). Also holds seasonality.
- `trophies.py` — 21 trophies, each with **three levels**. Adding challenge
  means extending a `levels` list, not inventing a new trophy.
- `accessories.py` — 40 Dress Up items on a five-band price ladder.
- `challenges.py` — 10 weekly challenges, 5 picked per week, seeded by ISO week.

## Rules that are easy to break

**Rarity is a fixed property of the species**, not a per-location calculation.
It exists *only* inside collector packs. Don't reintroduce rarity badges on My
Birds or the bird cards — that framing was deliberately removed.

**Species names must match BirdNET's output exactly** ("Eurasian Blue Tit", not
"Blue Tit"). A mismatch fails silently: the bird is simply never found. There
was a real bug of exactly this kind.

**Numbers are deliberately small** so an eight-year-old can hold them in their
head. New bird 3 feathers, rare 15, Dress Up 5–75. Don't inflate them.

**Detection is live-only.** Identification happens during recording via short
clips to `/identify`. Stopping just posts JSON for enrichment — no audio is
uploaded. There is no second server-side pass; two passes were tried and
removed for being unreliable.

## Verify by running, not by reading

This project has produced several bugs that reading the code would not have
caught — a `NOT NULL` constraint rejecting untiered birds, a deleted variable
declaration, a stale field name. Prefer exercising the real code path:

```bash
pip install fastapi sqlalchemy astral requests pydub python-multipart --break-system-packages
DATABASE_URL="sqlite:////tmp/test.db" python3 -c "..."   # stub birdnetlib, create_all, skip init_db
```

`init_db()` uses Postgres-only `ADD COLUMN IF NOT EXISTS`, so skip it under
SQLite and call `Base.metadata.create_all` instead.

After editing `static/index.html`, always check `<script>`/`</script>` and
`<svg>`/`</svg>` are balanced, and that any new top-level `const` doesn't
collide with an existing one — a duplicate is a SyntaxError that kills every
screen, not just the new feature.

## Environment variables (Railway)

`DATABASE_URL`, `XENO_CANTO_API_KEY`, `PORT`,
`RAILPACK_DEPLOY_APT_PACKAGES=ffmpeg`

## Outstanding

- 41 of the 100 birds still have no researched facts
- The 40 Dress Up accessories are placeholder-quality art
- No logo yet (brief written)
- Empty states are plain text, no illustration
