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
  Trumps ratings. All 100 also have researched extras (wingspan,
  conservation status, kid-friendly comparisons); Little Owl and Canada Goose
  have no status because they're introduced species the UK lists don't assess. All 100 have an `about`:
  one or two child-level sentences shown under the badges on the bird card.
  Also holds seasonality.
- `trophies.py` — 18 trophies, each with **seven levels** (shown as empty
  sockets, then 1-3 green leaves, then the leaves turning gold). Adding
  challenge means extending a `levels` list, not inventing a new trophy.
  Every level won pays `TROPHY_LEVEL_FEATHERS` (5); levels won before that
  was introduced were deliberately not back-paid. Every level is a leaf, and
  the leaves together give a **birder rank** (`BIRDER_RANKS`: Hatchling at 0
  - Lark, Eavesdropper, Trill Seeker, Glider, Flockstar, Elder - up to
  Warbler at 95 of the 126), shown as its badge in the top bar
  beside the feathers on every screen, and celebrated when it goes up. Each rank has its own look, `rankSeal()`: a
  wooden seal with the rank's number and a wreath of the painted leaf that
  grows a pair per rank, gold for the top two (Elder, Warbler) -
  replaced by a painting when `icon-rank-<key>` arrives
  (`design-brief-rank-badges-v1.md`). Tapping the top-bar badge opens the
  whole ladder over whatever screen is showing (`openRankLadder()`), as does
  the "My rank" card on My Profile (leaves won of all of them, a bar to the
  next rank, `paintProfileRank()`); `birder_rank()` sends
  the ladder and the "how to climb" words (`message`) with the rank. Summer Squad was removed (its first level
  needed all 13 summer visitors in one summer); High Five (weeks with all
  five challenges done) was added. Forager is capped at 100 species, Empty
  Nester only counts quiet recordings of a minute or more, and Wingman
  counts one share per bird per day. Night Owl counts every bird heard
  after dark (after dusk or before dawn, `is_after_dark()`), not just owls.
  Golden Eagle counts each rare bird at most once a day, Brooder counts rainy
  warbles that heard a bird, and Nomad counts a spot within 500m of one
  already counted as the same place (`count_distinct_locations`; Rooster
  and the challenges keep the ~110m place). Preener runs
  5 to 60 and must never mean "the whole shop", which changes with every
  restock; `TROPHY_CEILINGS` in `main.py` stops the server starting if
  Preener, Century or a pack trophy asks for more than exists. The Awards
  scene carries only the front trophy's name and level on the wooden sign
  (a carved "?" until won) and "Tap for more", on the plinth under it;
  Awards opens on the trophy that most recently gained a leaf
  (`last_leaf` from `/trophies`), or the first. Everything else is on the
  trophy's card (`renderTrophyDetail`) - a layer over Awards that just lifts
  away when closed, so nothing behind it reloads - in
  this order: picture, name and level, the level's citation, the
  description, then the next level's target with a green bar. A trophy not
  won yet opens too: greyed, a carved "?" for its name, no story, just what
  it takes to win it. Phil edits
  the trophies' words and numbers in a spreadsheet; Dawn Chorus,
  Globetrotter and Skylark were removed that way (levels won on them no
  longer count as leaves; their feathers were kept).
- `accessories.py` — 70 Dress Up items priced 5, 10, 15, 20, 30, 40, 50 or 75
  (1,880 for the lot). Four seasonal restocks a year are planned:
  `design-brief-shop-restock-v1.md`. Feather colours: every bird starts
  **Natural** - its own plumage, no colour change (`NATURAL`, stored as
  `avatar_body`; the first swatch on the wheel, an empty see-through
  ring). Changing colour unlocks at the third birder rank
  (`COLOUR_UNLOCK_RANK` = 2, Eavesdropper, the seal numbered 3): until then
  the wheel isn't shown and the server refuses any other colour; the rank-up
  moment says so (`colours_new`) and the Hoot-tique lights. A family that
  had coloured its bird before this keeps that colour. Then nine free, nine
  special at 10 each (`SPECIAL_COLOURS` in `main.py`), bought as
  `colour:#HEX` rows in the owned-items table (not counted by Preener).
  Natural draws each colourable layer from its natural copy (`nat` in
  `PROTO_BIRDS`, `natural-<layer>.webp`); every bird has them. The Blue Tit
  came with its own; the first eight came as one finished picture each,
  cut into layers by `tools/cut_natural_layers.py` (read its docstring - a
  layer's hidden parts have to be coloured, or they show when a wing
  flaps); the Blackbird, plain black, had its own grey layers taken down to
  glossy black by `tools/natural_from_grey.py`. A new bird needs them too,
  or Natural shows it grey. Hats are
  fitted per bird (see its docstring); a bird can wear another's fitted set
  (`hats:` in `PROTO_BIRDS` - the Blue Tit, Blackbird and Magpie wear the
  Kingfisher's: same head). How much of a bird takes a colour is the
  artist's call, in its masks: the Blackbird all over, the Magpie only its
  head and neck.
- `challenges.py` — 10 weekly challenges, 5 picked per week, seeded by ISO week.
  Pitched so a child warbling about four times a week (after school, a
  weekend morning, garden plus one other place) finishes all five most
  weeks: from 2026-W42 "in the morning" (before midday, UK time) replaced
  "before 9am", "4 birds in one warble" replaced 5, and "3 different
  places" is retired (`until_week`). A twice-a-week child can't, because
  "Go warbling 3 times" is always one of the five. Two are only offered
  when they can be done: "Hear a new bird" while new birds still turn up
  (under 30 species heard, or 3 new in the last four weeks - otherwise a
  child who has found everything near home could never finish a week),
  and "Win a star" when the game has songs to play.
  Feathers only for finishing all five (`ALL_COMPLETE_BONUS`, 25); a single
  challenge pays nothing. A child's five are picked once and kept for the
  week (`week_challenges()` in `main.py`, seen mark `challenges:<week>`).
  "Win a star in Guess the Song" is only offered to a child who can play
  it, and only from 2026-W42 (`from_week`), so adding it didn't reshuffle
  the week it arrived in. Adding a challenge: give it a `from_week` too;
  retiring one: `until_week`, and leave it in the pool.
- **Guess the Song** (Home → mini card) — hear a song, tap the bird. 5 levels
  of 8 rounds, 2–6 choices, unlocking at 10/15/20/25/30 of the 100 heard
  (`SONG_GAME_LEVELS` in `main.py`, served by `/song-game`) *and* at least one
  star on the level before. Stars: 6/8 = 1, 7/8 = 2, 8/8 = 3, worked out
  server-side by `/song-game/result`; the best per level is kept in
  `song_game_levels`. Every level draws from *all* birds heard so far; a bird
  with no recording can be a wrong choice but is never asked about. 15
  seconds to answer, from when the song starts. Each star won on a level for
  the first time pays `SONG_GAME_STAR_FEATHERS` (5), so a level is worth up
  to 15; no trophies from it yet.

`tools/build_pack_art.py` rebuilds the ten packs' icon/badge/wordmark webps
from a folder of delivered PNGs. Read its docstring before re-exporting pack
art — the source files arrive with their own filenames baked into the picture,
and the reason the obvious ways of removing that fail is written down there.

## Rules that are easy to break

**Rarity is a fixed property of the species**, not a per-location calculation.
It exists *only* inside collector packs. Don't reintroduce rarity badges on My
Birds or the bird cards — that framing was deliberately removed.

**Species names must match BirdNET's output exactly** ("Eurasian Blue Tit", not
"Blue Tit"). A mismatch fails silently: the bird is simply never found. There
were real bugs of exactly this kind - the worst was 14 of the 100 (Blackbird
and Starling among them, so Locals could never be finished) plus Nightjar,
written in British or IOC style. They're BirdNET's now ("Eurasian Blackbird",
"Gray Heron", "Ring-necked Pheasant"); `RENAMED_SPECIES` in
`curated_species.py` lists the old ones, and `rename_old_species()` moves any
stored rows on start-up. The source of truth is the label file inside
birdnetlib (`birdnetlib/models/analyzer/BirdNET_GLOBAL_6K_V2.4_Labels.txt`,
"Scientific_Common"): check any new name against it. When the analyzer loads,
`check_species_names()` logs any of the 100 it doesn't
know, and `/status` lists them as `unknown_species_names` - which should
always be empty.

**On screen, "Eurasian" and "European" read "Common"** ("Common Robin",
"Common Wren", "Common Blackbird"), "Gray" reads "Grey", and two take their
UK names (`BIRD_DISPLAY_NAMES`: Common Pheasant, Common Whitethroat). This is
display only, through
`birdName()` in `static/index.html` - the data, the API and every lookup keep
BirdNET's exact names. Any new place that shows a bird's name must go through
`birdName()`.

**Locked and empty states say how to unlock them**, and the words come from
the server: `message` on `/joke-of-the-day`, `/song-game` (and each of its
levels) and each pack in `/collector-packs`, null once there's nothing to
unlock. Change the wording in `main.py`, not the page.

**Every core experience gets a first-play tutorial, and every unlock lights
the nav bar.** Tutorials are steps in `TUTORIALS` in `static/index.html`,
shown with `showTutorial(name)` once the screen has rendered; the name must
also be in `TUTORIAL_KEYS` in `main.py`. "Something new here" is an area in
`whats_new_items()` in `main.py` (the set of things in it now), cleared by
`markSeen(area)` when the screen is visited. Home itself never glows - the
joke, challenges and game discs on it do. Both are remembered server-side in
`seen_marks`; Settings > Tutorials replays the bubbles.
Before any of it, a brand-new player gets the welcome (`renderWelcome`):
pick a bird, then an optional first name (no colour: every bird starts Natural). It's skipped for a
profile that already has a name or a non-default bird, and the tutorials
wait for it (`welcomeDecided`). The first mic tap shows "Warble needs to
listen" (`renderMicIntro`, tutorial key `mic_intro`) before the browser's
own prompts, unless the microphone is already allowed; a refused microphone
gets `renderMicBlocked`, written for the child with a line for the grown-up.
On the Done screen, "New spot!" comes *after* the feathers are collected;
then "Go again?" alone (the "Spend feathers" disc was removed - the
twitching leaf on the Hoot-tique tab does that job).

**Avatar birds: three to start, the rest found then bought.** Cardinal,
Parrot and Penguin are free (none of them live here). The UK birds -
the Robin (id `classic`; it was called Classic), Duckling, Woodpecker, Owl, Kingfisher, Blue Tit, Blackbird, Magpie - are *found* the
first time the child hears the real bird or one of its family
(`AVATAR_UNLOCKS` in `main.py`: a robin, stonechat or redstart; any
duck/goose/swan; any woodpecker; any owl; a Kingfisher; any tit; a blackbird or thrush; a magpie or crow) and then bought for
`AVATAR_PRICE` (30) in the Hoot-tique. A bird still to find isn't shown
anywhere (`shownSpecies()`: finding it is the surprise); a found one joins
the carousel showing just its price - a wood button with the feather and
30, no other words. The welcome offers only birds the child can already be. Bought birds are `avatar:<id>` rows with the Dress Up items (not
counted by Preener). Not trophies - an avatar is who the child is, so it
comes from the birds. When the price arrived, a family already playing kept
free whatever it had (`_keep_avatars_already_had`, run once at start-up,
`avatars:priced` mark). The server refuses a bird the child doesn't own on
`POST /profile`. One more is being painted (`AVATARS_TO_COME`,
`design-brief-avatar-birds-v1.md`: the Seagull);
when the art is in, move each into `AVATAR_UNLOCKS` and the page's
`AVATAR_SPECIES`.

**The Hoot-tique opens a batch at a time**, one per birder rank
(`SHOP_BATCHES` in `accessories.py`: 18 at Hatchling - every 5-feather item
among them, so the first warble still buys something - then 8, 8, 10, 12,
8, 4, 2; the showiest 75s last). A batch is hidden until its rank (a new
rank is a delivery); `/accessories` sends only open items (and anything
owned) - no words about what the next rank brings - purchase refuses an
item not open yet, the rank-up moment says "New accessories drop in the
Hoot-tique!", and each batch lights the nav bar. A restock adds its items to a batch.

**Numbers are deliberately small** so an eight-year-old can hold them in their
head. The whole ladder is at the top of the reward section of `main.py`:
1 a bird heard again (rare 3) - **once per bird per day** - or one outside
the 100; +1 on top for a migrator, one of the 14 that come and go
(`MIGRATOR_BONUS`, on the same once-per-bird-per-day terms); 3 a new bird; 5 a trophy level or a new game star; 15 a new rare
bird; 25 a pack completed or all five weekly challenges. Dress Up 5–75, a
found avatar bird 30.
Don't inflate them. They're balanced against the prices to one target: a
new child can buy something after their very first warble (Fledgling level
1 pays 5, the cheapest item costs 5 - keep both), and a child warbling four
times a week settles at about 35 feathers a week, the weekly 25 included
about two weeks in three: an ordinary 20 item a week or more, a 75 every
two or three weeks. With the shop opening by rank, a typical child runs
short of things to buy in their first year (about 450 feathers unspent at
the end; restocks and the new birds are what fill that). Before changing a reward or a price,
run `python3 tools/economy_sim.py` (needs `freezegun`) before and after: it
plays pretend children through the real reward code from zero and prints
the curve.

**Every reward is one kind of moment.** New bird, trophy level, birder rank,
pack complete, challenge done (and all five), Song Game star and level
unlock all go through `celebrate()` in `static/index.html` (with
`celebrateTrophy`, `celebratePack`, `celebrateChallenges`... wrapping it),
in one shape and one timing (`MOMENT`): a wood-and-cream card pops in over
where it was won with a burst of leaves, holds (kicker, name, +feathers),
then, tapped or timed out, bumps (`MOMENT.bump`), shrinks while spinning
once round where it is - the shrink and the spin as one step, written with
the same move/size/turn parts every step so Safari keeps them together
(`MOMENT.shrink`) - and flies home - Awards, Collections, Home, the game's stars or Next level
button - while its feathers fly to the counter. They queue one at a time; a
tap sends one home early. The new bird's reveal card is the same moment at
full size (same burst, folds small in place, flies to My Flock as an origami
bird); a new bird - not one heard before - bursts leaves over everything as
it's tapped. It wears the bird card's design (`renderCard`) but not its
facts: the photo with play, share and add-a-photo, the name, and two
badges - the collection it's in, migration if it migrates, and the feathers
it won - each nudging down
one line (`toggleBadgeNote`). A tap anywhere else collects it, and so is a new birder rank (`celebrate({big: true})`: the screen
dims, the new seal is large, the ladder underneath lights the step just
climbed, a double burst and three times the hold; it flies into the top-bar
badge, which changes as it lands) - big is kept for the rarest rewards:
that, and a newly found avatar bird (`celebrateAvatar`, last of a
recording's moments): "You've unlocked / Kingfisher / in the Hoot-tique!",
the bird large and dancing in its natural plumage (whatever colour the
child's own bird is) - it twirls in from small (two turns,
`AVATAR_SPIN`) and leaves burst over everything as it lands (`onShow`,
`burstLeaves(..., above)`); it waits for a tap (`tap: true`, no hold timer)
and flies into the Hoot-tique tab. **On the Done screen, everything won is
collected by a tap, and bursts leaves as it is:** the birds' own feathers
first (just the words, pulsing slowly - no box), then each of the
recording's other rewards as a moment that waits (a gentle nudge) instead
of flying off by itself (`momentsWaitForTap`, set while
`takeSessionMoments` queues them), bursts leaves over everything when
tapped, then flies home; only then "Go again" - so nothing is cut short.
No card says "tap"; one line, "Tap to collect" (`showTapHint`), sits at the
bottom of the screen the whole time there's something to collect. In
order: "Collection pack bird found!" for each new bird of the 100
(`pack_birds` from `/analyze-session`), "Collection pack complete!",
"Weekly challenge complete!" for each one and "Weekly challenges
complete!" for all five, trophy won / level up, the new rank ("New birder
rank!" pulsing), the new avatar bird. Each that has progress shows it as a
green bar with no numbers, growing as the card lands: the pack's birds
found, the five challenges, the trophy's leaves (`progress: {from, to}`).
Wherever a card lands (a tab, the rank badge) a twitching leaf stays
(`.landed`) until that place is visited - except Home's tab: the
challenges fly to Home, but Home never glows (its challenges disc does). Moments elsewhere (the game, the
Hoot-tique) still go home by themselves. The server has always banked the feathers
already; `/analyze-session` and `/song-game/result` itemise them
(`packs_completed`, `challenges_done`, `week_bonus`). Trophy pay outside a
recording goes through `award_trophy_levels()` and challenge pay through
`award_week_challenges()` in `main.py`, so a game star that finishes the
week pays its 25 at once. Add a new kind of reward as a `celebrate()` call,
never a new animation.

**The design language** (one page: https://claude.ai/artifact/5iNyeNjN5TTdT4DvZcH9Lq).
A storybook garden carved in warm wood. Follow it in every change to the page:
- *World:* a painted scene behind every screen (Garden, River, Meadow, Coast
  at dawn/day/dusk/night by the real clock), sharp on Home, softly blurred
  under a dusk veil elsewhere.
- *Material:* everything a child touches is carved orange wood round a cream
  face. Round disc = taps to do one thing; framed card = something to collect
  or look at (the reveal card too - gold frame if rare); **every text button
  is wood** (the shared rule at the end of the `<style>`: add a new button's
  class to that list, never give it a colour of its own). The wood is one
  solid colour - no grain, no light-to-dark shading, which read as banding
  on a phone - and one token, `--wood-rim`: a cream face is `background:linear-gradient(var(--disc-cream),
  var(--disc-cream)) padding-box, var(--wood-rim)` with a transparent border.
  Boxes a child types in are wood too: every one is `.location-input`
  (the My Flock search has its own wood bar), with a cream glow while typing.
  Panels are cream, never white; a box inside a cream card is `--cream-lt`.
  No see-through "glass" controls.
- *Text links* stay text, one colour: brown (`--wood-edge`) on cream, white
  on a scene. Never orange.
- *Colour has meaning:* **gold only for rare birds and the trophy leaves
  that turn gold** - on the trophies, and in the top two ranks' wreaths (`--rare`; there is no general gold token any more, and
  `--sun` is only for the sky gradients). **Green (`--sage`) for leaves,
  anything selected, anything finished and progress.** **Every glow is
  cream** (`rgba(var(--glow), a)`). **Feather amounts are feather blue**:
  `--feather` on cream, `--feather-lt` on a scene. Dusk purple is night and
  the veil, never text. Words on cream are brown: `--wood-edge` for names and
  titles, `--ink-brown` for body, `--ink-soft` for small labels; on a scene,
  white.
- *Exceptions, because they mean something outside Warble:* the UK
  conservation shields (red / amber / green list), the Guess the Song timer
  (green to orange to red), each pack's own colour on its card corners, and
  the orange "leaving soon" season dot.
- *Type:* Poppins 900 for titles, names and numbers, 700 for labels and
  buttons, 400 only for a quiet line or typed text. Italic only for
  scientific names. Painted wordmarks only for the five nav tabs; screens
  inside them use plain white Poppins.
- *Pictures:* painted, never emoji - except bird photos, which are shown as
  real photographs with no filter (the watercolour one was removed). Small icons go through `icon(name)`,
  which shows `static/icon-<name>-v<N>.webp` (newest version; `/painted-icons`
  lists them, read once at server start) and falls back to its stand-in in
  `ICON_STANDINS` only if the file is missing. All 24 in
  `design-brief-info-icons-v1.md` are painted and in; `tools/build_icons.py`
  cuts a delivered sheet into the files (read its docstring first). A new
  small icon gets a name there and a painting, not an emoji in a template - and that includes
  arrows, crosses and "???" (`icon('back')`, `'forward'`, `'close'`,
  `'pause'`, `'mystery'`). The painted play button and tick already exist
  (`PAINTED_PLAY`, `PAINTED_TICK`).
- *Words for children:* "31 birds · heard 61 times", never species or
  detections. Grown-up tools (sound check, the feather setter, and Debug >
  Animation previews) live on Settings' "For grown-ups" page
  (`renderGrownUps`), behind a wood button at the end of Settings - not a
  fold-open section: that opened below the bottom of a phone screen and
  looked like it did nothing. The previews (`renderAnimationPreview`) play the real Done screen
  over a made-up session set up in a form (birds, new, rare, already paid,
  pack, challenges, trophies, rank, avatar bird, new spot), each reward
  moment on its own, the recording tree and the bird reveal. They save
  nothing, put the page's rank and feathers back from the server
  (`debugRestore`) and cancel leftover moments (`cancelMoments`) on the way
  out. A new kind of moment gets a button there too.
- *Motion and voice:* see the reward moment below, and "Locked and empty
  states" above.

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

- The 40 Dress Up accessories are placeholder-quality art
- No logo yet (brief written)
- Empty states are plain text, no illustration
