#!/usr/bin/env python3
"""How fast does a brand-new child earn feathers, against what the shop costs?

Plays pretend children through their first half-year of Warble using the
app's REAL reward code - analyze_session, the Guess the Song result and the
Hoot-tique purchase - each against its own empty database, with the clock
frozen and walked forward one warble at a time. Nothing about the rewards is
re-implemented here, so when a reward or a price changes, re-run this and
the numbers follow. Only the outside services (Wikipedia, xeno-canto, the
weather) are stubbed. It's a local tool, not part of the app:

    pip install freezegun --break-system-packages   (plus the app's own libraries)
    python3 tools/economy_sim.py                    the table, 12 children of each kind
    python3 tools/economy_sim.py --start 2026-10-12 starting in autumn instead of spring

Three kinds of child, by how often they go out:

    casual   2 warbles a week   (Wednesday after school, Saturday morning)
    typical  4 a week           (two after school, both weekend mornings)
    keen     6 a week           (one before school, three after, both weekends)

Weekday warbles are in the garden, weekend ones at a park 2.5 km away. Each
warble hears 0-5 birds: the garden packs often, the rest mostly at weekends,
rare birds seldom, summer and winter visitors only in season. Guess the Song
gets a go or two a week once it's open. The child buys the cheapest thing
they can afford as soon as they can - the impatient shopper, so "owned"
counts are the most a child could have.

The model is a guess about children, not a measurement of them. What it is
good for is comparing: before and after a price change, one reward against
another, spring against autumn. The challenges table at the end shows how
often each weekly challenge got done, which is how "before 9am" and "3
different places" were found to be out of reach for a typical child. The
challenge rules in force depend on the dates simulated (from_week and
until_week), so --start a week at or after the newest change.
"""
import argparse
import asyncio
import collections
import datetime
import json
import os
import random
import statistics
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# When each kind of child warbles: (weekday 0=Mon, hour), and where.
SCHEDULES = {
    "casual":  [(2, 16), (5, 10)],
    "typical": [(0, 16), (2, 16), (5, 10), (6, 11)],
    "keen":    [(0, 7), (1, 16), (2, 16), (3, 16), (5, 9), (6, 10)],
}
GAME_GOES_PER_WEEK = {"casual": 1, "typical": 2, "keen": 3}
HOME, PARK = (51.4545, -2.5879), (51.4721, -2.6050)
GARDEN_PACKS = {"garden_regulars", "tits_and_climbers", "seed_eaters"}
OUTSIDE_THE_100 = ["Rose-ringed Parakeet", "Rock Pigeon", "Egyptian Goose"]


def one_child(kind: str, weeks: int, seed: int, start: datetime.datetime) -> dict:
    """Runs in its own process: the app reads DATABASE_URL once, at import."""
    db = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
    os.environ["DATABASE_URL"] = "sqlite:///" + db
    sys.path.insert(0, REPO)
    os.chdir(REPO)

    from freezegun import freeze_time
    import database
    from sqlalchemy.schema import ColumnDefault
    # init_db's ALTERs are Postgres-only; a fresh SQLite file just needs the tables.
    database.init_db = lambda *a, **k: database.Base.metadata.create_all(database.engine)
    import main
    # Column defaults captured the real utcnow when imported - aim them at the
    # frozen clock so every row carries the pretend date.
    for table in database.Base.metadata.tables.values():
        for col in table.columns:
            if col.default is not None and getattr(col.default, "is_callable", False):
                col.default = ColumnDefault(lambda: datetime.datetime.utcnow())
    database.Base.metadata.create_all(database.engine)

    rng = random.Random(seed)
    main.get_wikipedia_info = lambda s: (None, None)
    main.get_bird_call_url = lambda s: None
    main.get_cached_call_url = lambda n: "/song.mp3"   # every bird can be asked about
    main.is_raining = lambda lat, lng: rng.random() < 0.12

    from curated_species import PACKS, SPECIES_RARITY
    from birds import season_state
    from accessories import ACCESSORIES
    pack_of = {n: k for k, p in PACKS.items() for n in p["common"] + p["rare"]}

    def birds_heard(month, weekend):
        weights = {}
        for name, pack in pack_of.items():
            if season_state(name, month)["state"] == "away":
                continue
            w = 1.0 if pack in GARDEN_PACKS else (0.45 if weekend else 0.12)
            weights[name] = w * (0.07 if SPECIES_RARITY[name] == "Rare" else 1)
        how_many = rng.choices(range(6), [0.10, 0.18, 0.24, 0.22, 0.16, 0.10])[0]
        names, heard = list(weights), set()
        while len(heard) < how_many:
            heard.add(rng.choices(names, [weights[n] for n in names])[0])
        if heard and rng.random() < 0.12:
            heard.add(rng.choice(OUTSIDE_THE_100))
        return [{"common_name": n, "scientific_name": n, "confidence": 0.9} for n in heard]

    async def shop(bought):
        owned = database.get_owned_accessory_ids()
        while True:
            have = database.get_total_feathers()
            can = sorted((a["cost"], k) for k, a in ACCESSORIES.items()
                         if k not in owned and a["cost"] <= have)
            if not can or (await main.purchase_accessory_endpoint(can[0][1]))["status"] != "ok":
                return
            owned.add(can[0][1])
            bought.append(can[0][0])

    async def play():
        source = collections.Counter()
        lifetime, by_week, owned_by_week, bought = [], [], [], []
        challenges = []   # per week: {challenge id: done}
        earned = 0
        schedule = SCHEDULES[kind]
        for week in range(weeks):
            week_earned = 0
            for i, (weekday, hour) in enumerate(schedule):
                when = start + datetime.timedelta(days=7 * week + weekday, hours=hour,
                                                  minutes=rng.randint(0, 50))
                spot = PARK if weekday >= 5 else HOME
                with freeze_time(when):
                    before = database.get_total_feathers()
                    result = await main.analyze_session(
                        lat=spot[0] + rng.uniform(-3e-4, 3e-4), lng=spot[1] + rng.uniform(-3e-4, 3e-4),
                        live_detections=json.dumps(birds_heard(when.month, weekday >= 5)),
                        duration_s=rng.randint(60, 240))
                    for d in result["detections"]:
                        source["birds heard again" if d["is_duplicate"] else "new birds"] += d["feathers"]
                    for b in result["bonuses"]:
                        label = b["label"]
                        source["weekly challenges" if "challenges" in label else
                               "trophy levels" if " level " in label else "packs"] += b["feathers"]
                    # Guess the Song, spread over the week's last warbles
                    if i >= len(schedule) - GAME_GOES_PER_WEEK[kind]:
                        levels = [l for l in main.song_game()["levels"] if l["unlocked"]]
                        if levels:
                            level = next((l for l in levels if l["stars"] < 3), levels[-1])
                            g0 = database.get_total_feathers()
                            out = await main.song_game_result(
                                level=level["level"],
                                correct=rng.choices([4, 5, 6, 7, 8], [0.1, 0.2, 0.3, 0.25, 0.15])[0])
                            source["weekly challenges"] += out["week_bonus"]
                            source["Guess the Song"] += database.get_total_feathers() - g0 - out["week_bonus"]
                    got = database.get_total_feathers() - before
                    earned += got
                    week_earned += got
                    lifetime.append(earned)
                    await shop(bought)
                    if i == len(schedule) - 1:   # how the week's five ended up
                        challenges.append({c["id"]: done for c, done, _ in main.evaluate_week_challenges()})
            by_week.append(week_earned)
            owned_by_week.append(len(bought))
        return dict(kind=kind, per_week=len(schedule), lifetime=lifetime, by_week=by_week,
                    owned_by_week=owned_by_week, source=dict(source), challenges=challenges, shop_size=len(ACCESSORIES),
                    birds=database.count_curated_species_found(main.ALL_CURATED_SPECIES),
                    leaves=main.total_leaves())

    try:
        return asyncio.run(play())
    finally:
        os.remove(db)


def week_reaching(child, amount):
    """The week a child who saved everything from the start could buy `amount`."""
    i = next((i for i, v in enumerate(child["lifetime"]) if v >= amount), None)
    return None if i is None else i // child["per_week"] + 1


def report(children):
    med = statistics.median
    print("Saving from zero (median, and the slowest child in brackets):\n")
    print(f"{'':9}{'1st warble':>11}{'end wk 1':>10}{'a 20 in':>10}{'a 75 in':>10}"
          f"{'wk 1-4':>9}{'wk 9+':>8}{'owned':>8}")
    for kind in SCHEDULES:
        group = [c for c in children if c["kind"] == kind]
        if not group:
            continue
        first = [c["lifetime"][0] for c in group]
        wk1 = [c["lifetime"][c["per_week"] - 1] for c in group]
        w20 = [week_reaching(c, 20) or 99 for c in group]
        w75 = [week_reaching(c, 75) or 99 for c in group]
        early = [sum(c["by_week"][:4]) / 4 for c in group]
        late = [statistics.mean(c["by_week"][8:]) for c in group if len(c["by_week"]) > 8]
        owned = [c["owned_by_week"][-1] for c in group]
        shop = group[0]["shop_size"]
        print(f"{kind:9}{f'{med(first):g} ({min(first)})':>11}{f'{med(wk1):g} ({min(wk1)})':>10}"
              f"{f'wk {med(w20):g} ({max(w20)})':>10}{f'wk {med(w75):g} ({max(w75)})':>10}"
              f"{f'{med(early):.0f}/wk':>9}{f'{med(late):.0f}/wk' if late else '-':>8}"
              f"{f'{med(owned):g}/{shop}':>8}")
    print("\nWhere the feathers came from (all children of that kind, % of what they earned):\n")
    for kind in SCHEDULES:
        total = collections.Counter()
        for c in children:
            if c["kind"] == kind:
                total.update(c["source"])
        whole = sum(total.values()) or 1
        print(f"  {kind:8} " + ", ".join(f"{k} {100 * v / whole:.0f}%" for k, v in total.most_common()))


def report_challenges(children):
    print("\nWeekly challenges (weeks with all five done; then each challenge: done / offered):\n")
    for kind in SCHEDULES:
        weeks = [w for c in children if c["kind"] == kind for w in c["challenges"]]
        if not weeks:
            continue
        offered, done = collections.Counter(), collections.Counter()
        for w in weeks:
            offered.update(w.keys())
            done.update(k for k, v in w.items() if v)
        all5 = sum(1 for w in weeks if all(w.values()))
        print(f"  {kind:8} all five {100 * all5 / len(weeks):.0f}% of weeks")
        print("           " + ", ".join(f"{k} {100 * done[k] / offered[k]:.0f}%"
                                         for k in sorted(offered, key=lambda k: done[k] / offered[k])))


def main_cli():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--weeks", type=int, default=26)
    ap.add_argument("--children", type=int, default=12, help="of each kind")
    ap.add_argument("--start", default="2026-03-02", help="a Monday, YYYY-MM-DD")
    ap.add_argument("--one", nargs=2, metavar=("KIND", "SEED"), help=argparse.SUPPRESS)
    args = ap.parse_args()
    start = datetime.datetime.strptime(args.start, "%Y-%m-%d")
    if args.one:
        # The child's own process: everything the app prints goes to stderr,
        # the result is the one line on stdout.
        real_stdout, sys.stdout = sys.stdout, sys.stderr
        child = one_child(args.one[0], args.weeks, int(args.one[1]), start)
        print(json.dumps(child), file=real_stdout)
        return
    jobs = [subprocess.Popen([sys.executable, __file__, "--one", kind, str(seed),
                              "--weeks", str(args.weeks), "--start", args.start],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            for kind in SCHEDULES for seed in range(1, args.children + 1)]
    children = []
    for job in jobs:
        out, _ = job.communicate()
        if job.returncode != 0 or not out.strip():
            sys.exit("A child's run failed - try it alone with --one KIND SEED to see why.")
        children.append(json.loads(out.strip().splitlines()[-1]))
    print(f"{args.children} children of each kind, {args.weeks} weeks from {args.start}.\n")
    report(children)
    report_challenges(children)


if __name__ == "__main__":
    main_cli()
