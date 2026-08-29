"""
Real database for Warble, replacing what Bubble's Data API used to do.
Uses Postgres, via Railway's DATABASE_URL. Two tables: sightings (every
bird ever found) and player_stats (a single running feather total, for
now — no accounts yet, so there's just one shared total).
"""
import os
import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "")

# Railway sometimes provides the URL in a format SQLAlchemy is picky
# about (postgres:// vs postgresql://) — normalise it just in case.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = sessionmaker(bind=engine) if engine else None
Base = declarative_base()


LOCATION_PRECISION = 3  # ~110m — same precision Nomad's distinct-location count already uses


class Sighting(Base):
    __tablename__ = "sightings"

    id = Column(Integer, primary_key=True)
    common_name = Column(String, nullable=False)
    scientific_name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    tier = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    call_url = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class PlayerStats(Base):
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True)
    total_feathers = Column(Float, default=0)
    share_count = Column(Integer, default=0)


class RecordingSession(Base):
    """One row per recording — regardless of whether any bird was heard.
    Used for trophy checks (Fledgling, Nomad) that care about sessions
    themselves, not just successful bird finds."""
    __tablename__ = "recording_sessions"

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    bird_count = Column(Integer, default=0)   # filled in after detection
    before_sunrise = Column(Boolean, default=False)
    was_raining = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class EarnedTrophy(Base):
    __tablename__ = "earned_trophies"

    id = Column(Integer, primary_key=True)
    trophy_key = Column(String, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    earned_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint("trophy_key", "level", name="uq_trophy_level"),)


class Location(Base):
    """A named place — created the first time a session happens somewhere
    new. lat/lng are stored already rounded to LOCATION_PRECISION."""
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AwardedBonus(Base):
    """One row per one-off feather bonus already paid, keyed by something
    unique to the occasion - "week:2026-W35", "habitat:Woodland". Keeps
    bonuses idempotent without needing a column per bonus type."""
    __tablename__ = "awarded_bonuses"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    awarded_at = Column(DateTime, default=datetime.datetime.utcnow)


class Profile(Base):
    """Single-row, same pattern as PlayerStats — no accounts system
    yet, so there's just one shared profile."""
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    name = Column(String, default="Explorer")   # legacy single-field name, kept for migration
    first_name = Column(String, default="Explorer")
    last_name = Column(String, nullable=True)
    show_scientific_names = Column(Boolean, default=True)
    avatar_photo = Column(Text, nullable=True)   # data URL, replaces the bird avatar when set
    avatar_body = Column(String, default="#C4BFDF")
    avatar_face = Column(String, default="#E8845C")
    avatar_beak = Column(String, default="#8E87B8")
    equipped_hats = Column(String, nullable=True)
    equipped_neck = Column(String, nullable=True)
    equipped_gear = Column(String, nullable=True)
    equipped_held = Column(String, nullable=True)
    equipped_glasses = Column(String, nullable=True)
    equipped_shoes = Column(String, nullable=True)


class OwnedAccessory(Base):
    __tablename__ = "owned_accessories"

    id = Column(Integer, primary_key=True)
    accessory_id = Column(String, unique=True, nullable=False)
    purchased_at = Column(DateTime, default=datetime.datetime.utcnow)


def init_db():
    """Create tables if they don't exist yet, and seed one PlayerStats row."""
    if engine is None:
        print("Warning: DATABASE_URL not set — database features disabled.")
        return
    Base.metadata.create_all(engine)

    # create_all only creates missing TABLES, not missing COLUMNS on
    # tables that already exist. Since 'sightings' already has real data
    # in it, new fields need to be added explicitly like this — safe to
    # run every startup, since "IF NOT EXISTS" makes it a no-op once done.
    from sqlalchemy import text
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE sightings ADD COLUMN IF NOT EXISTS description VARCHAR"))
        conn.execute(text("ALTER TABLE sightings ADD COLUMN IF NOT EXISTS lat FLOAT"))
        conn.execute(text("ALTER TABLE sightings ADD COLUMN IF NOT EXISTS lng FLOAT"))
        conn.execute(text("ALTER TABLE sightings ADD COLUMN IF NOT EXISTS call_url VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS equipped_accessory VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS avatar_body VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS avatar_breast VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS avatar_face VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS avatar_beak VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS first_name VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS last_name VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS show_scientific_names BOOLEAN DEFAULT TRUE"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS avatar_photo TEXT"))
        conn.execute(text("ALTER TABLE recording_sessions ADD COLUMN IF NOT EXISTS bird_count INTEGER DEFAULT 0"))
        conn.execute(text("ALTER TABLE recording_sessions ADD COLUMN IF NOT EXISTS before_sunrise BOOLEAN DEFAULT FALSE"))
        conn.execute(text("ALTER TABLE recording_sessions ADD COLUMN IF NOT EXISTS was_raining BOOLEAN DEFAULT FALSE"))
        conn.execute(text("ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS share_count INTEGER DEFAULT 0"))
        # trophy_key was unique when trophies were one-shot; levels need one row per level
        conn.execute(text("ALTER TABLE earned_trophies ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1"))
        try:
            conn.execute(text("ALTER TABLE earned_trophies DROP CONSTRAINT IF EXISTS earned_trophies_trophy_key_key"))
        except Exception as e:
            print(f"Note: could not drop old trophy_key constraint: {e}")
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS equipped_hats VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS equipped_neck VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS equipped_gear VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS equipped_held VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS equipped_glasses VARCHAR"))
        conn.execute(text("ALTER TABLE profile ADD COLUMN IF NOT EXISTS equipped_shoes VARCHAR"))

    with SessionLocal() as session:
        existing = session.query(PlayerStats).first()
        if existing is None:
            session.add(PlayerStats(total_feathers=0))
            session.commit()
        existing_profile = session.query(Profile).first()
        if existing_profile is None:
            session.add(Profile(name="Explorer", avatar_body="#C4BFDF", avatar_face="#E8845C", avatar_beak="#8E87B8"))
            session.commit()
        else:
            # One-time migration: "Breast" was renamed to "Face" - avatar_breast
            # isn't a mapped column any more, so read its old value with raw
            # SQL and carry it forward into avatar_face if that's still empty,
            # so nobody's existing colour choice is silently lost.
            if existing_profile.avatar_face is None:
                with engine.begin() as conn:
                    row = conn.execute(text("SELECT avatar_breast FROM profile LIMIT 1")).fetchone()
                old_breast = row[0] if row else None
                if old_breast:
                    existing_profile.avatar_face = old_breast
                    session.commit()

            # One-time migration: an item equipped under the old
            # single-slot system would otherwise be silently lost now
            # that equipping is per-category. equipped_accessory isn't
            # a mapped column any more, so read it with raw SQL. Only
            # applies if the matching category slot is still empty, so
            # this is safe to leave in place / re-run on every startup.
            with engine.begin() as conn:
                row = conn.execute(text("SELECT equipped_accessory FROM profile LIMIT 1")).fetchone()
            old_equipped = row[0] if row else None
            if old_equipped:
                from accessories import ACCESSORIES
                item = ACCESSORIES.get(old_equipped)
                if item:
                    slot_column = f"equipped_{item['category']}"
                    if getattr(existing_profile, slot_column, None) is None:
                        setattr(existing_profile, slot_column, old_equipped)
                        session.commit()


def has_existing_sighting(common_name: str, tier: str = None) -> bool:
    """Whether this bird is already in the collection.

    For collector species a tier is passed in, and the same bird at a tier you
    haven't got yet counts as NEW - that's what makes all three collectable.
    For everything else tier is None and any previous sighting counts."""
    if SessionLocal is None:
        return False
    with SessionLocal() as session:
        q = session.query(Sighting).filter_by(common_name=common_name)
        if tier is not None:
            q = q.filter_by(tier=tier)
        return q.first() is not None


def count_full_collector_sets(collector_species: set) -> int:
    """How many collector species are held at all three tiers - the Globetrotter
    trophy. Counts distinct tiers per species and looks for a full three."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        rows = session.query(Sighting.common_name, Sighting.tier).distinct().all()
    by_species = {}
    for name, tier in rows:
        if name in collector_species and tier:
            by_species.setdefault(name, set()).add(tier)
    return sum(1 for tiers in by_species.values() if len(tiers) >= 3)


def get_tiers_found_for(common_name: str):
    """Which tiers of a species are already collected."""
    if SessionLocal is None:
        return []
    with SessionLocal() as session:
        rows = session.query(Sighting.tier).filter_by(common_name=common_name).distinct().all()
        return [r[0] for r in rows if r[0]]


def save_sighting(common_name, scientific_name, confidence, tier, image_url, description=None, lat=None, lng=None, call_url=None):
    if SessionLocal is None:
        print("Warning: no database configured — skipping save.")
        return
    with SessionLocal() as session:
        session.add(Sighting(
            common_name=common_name,
            scientific_name=scientific_name,
            confidence=confidence,
            tier=tier,
            image_url=image_url,
            description=description,
            lat=lat,
            lng=lng,
            call_url=call_url,
        ))
        session.commit()


def get_cached_call_url(common_name: str):
    """Returns a call recording URL already fetched for this species on
    an earlier sighting, if any — avoids re-querying xeno-canto for a
    species that's already been looked up once."""
    if SessionLocal is None:
        return None
    with SessionLocal() as session:
        existing = session.query(Sighting).filter(
            Sighting.common_name == common_name,
            Sighting.call_url.isnot(None),
        ).first()
        return existing.call_url if existing else None


def add_feathers(amount: float) -> float:
    """Add to the running feather total, and return the new total."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        stats = session.query(PlayerStats).first()
        stats.total_feathers += amount
        session.commit()
        return stats.total_feathers


def set_total_feathers(amount: float) -> float:
    """Sets the running feather total directly (not additive) - a dev
    convenience for testing, not part of normal gameplay flow."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        stats = session.query(PlayerStats).first()
        if stats is None:
            stats = PlayerStats(total_feathers=amount)
            session.add(stats)
        else:
            stats.total_feathers = amount
        session.commit()
        return stats.total_feathers


def get_all_sightings():
    if SessionLocal is None:
        return []
    with SessionLocal() as session:
        rows = session.query(Sighting).order_by(Sighting.created_at.desc()).all()
        # One lookup of every named location, rather than a query per
        # sighting — cheap either way at this scale, but no reason not to.
        locations_by_coords = {
            (loc.lat, loc.lng): loc.name for loc in session.query(Location).all()
        }
        result = []
        for r in rows:
            location_name = None
            if r.lat is not None and r.lng is not None:
                key = (round(r.lat, LOCATION_PRECISION), round(r.lng, LOCATION_PRECISION))
                location_name = locations_by_coords.get(key)
            result.append({
                "common_name": r.common_name,
                "scientific_name": r.scientific_name,
                "confidence": r.confidence,
                "tier": r.tier,
                "image_url": r.image_url,
                "description": r.description,
                "call_url": r.call_url,
                "location_name": location_name,
                "created_at": r.created_at.isoformat(),
            })
        return result


def get_total_feathers() -> float:
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        stats = session.query(PlayerStats).first()
        return stats.total_feathers if stats else 0


def record_session(lat: float, lng: float, before_sunrise: bool = False, was_raining: bool = False):
    """Log that a recording happened, regardless of what (if anything) was
    heard. Returns (total_sessions_ever, this_session_id) — the count feeds
    the Fledgling check without a second query, and the id lets the caller
    fill in bird_count once detection has finished."""
    if SessionLocal is None:
        return 0, None
    with SessionLocal() as session:
        row = RecordingSession(lat=lat, lng=lng, before_sunrise=before_sunrise, was_raining=was_raining)
        session.add(row)
        session.commit()
        return session.query(RecordingSession).count(), row.id


def set_session_bird_count(session_id, count: int):
    """Records how many birds a session found, once detection is done."""
    if SessionLocal is None or session_id is None:
        return
    with SessionLocal() as session:
        row = session.query(RecordingSession).filter_by(id=session_id).first()
        if row:
            row.bird_count = count
            session.commit()


def count_successful_sessions_today() -> int:
    """Sessions today that actually found a bird - caps the per-session bonus
    so it can't be farmed by tapping record repeatedly."""
    if SessionLocal is None:
        return 0
    start = datetime.datetime.combine(datetime.datetime.utcnow().date(), datetime.time.min)
    with SessionLocal() as session:
        return session.query(RecordingSession).filter(
            RecordingSession.created_at >= start,
            RecordingSession.bird_count > 0,
        ).count()


def count_successful_sessions_this_week() -> int:
    """Successful sessions since Monday - drives the weekly target."""
    if SessionLocal is None:
        return 0
    today = datetime.datetime.utcnow().date()
    monday = today - datetime.timedelta(days=today.weekday())
    start = datetime.datetime.combine(monday, datetime.time.min)
    with SessionLocal() as session:
        return session.query(RecordingSession).filter(
            RecordingSession.created_at >= start,
            RecordingSession.bird_count > 0,
        ).count()


def _week_start():
    today = datetime.datetime.utcnow().date()
    monday = today - datetime.timedelta(days=today.weekday())
    return datetime.datetime.combine(monday, datetime.time.min)


def get_week_stats():
    """Everything the weekly challenges need, gathered in one pass rather than
    one query per challenge. Week runs Monday to Sunday, UTC."""
    blank = {
        "sessions": 0, "days": 0, "locations": 0, "species": set(),
        "best_session_birds": 0, "tiers": set(), "earliest_hour": None,
    }
    if SessionLocal is None:
        return blank

    start = _week_start()
    with SessionLocal() as session:
        rows = session.query(
            RecordingSession.lat, RecordingSession.lng,
            RecordingSession.bird_count, RecordingSession.created_at,
        ).filter(RecordingSession.created_at >= start,
                 RecordingSession.bird_count > 0).all()
        sightings = session.query(
            Sighting.common_name, Sighting.tier,
        ).filter(Sighting.created_at >= start).all()

    if not rows and not sightings:
        return blank

    return {
        "sessions": len(rows),
        "days": len({r.created_at.date() for r in rows if r.created_at}),
        "locations": len({(round(r.lat, LOCATION_PRECISION), round(r.lng, LOCATION_PRECISION))
                          for r in rows if r.lat is not None}),
        "species": {s.common_name for s in sightings},
        "best_session_birds": max((r.bird_count or 0 for r in rows), default=0),
        "tiers": {s.tier for s in sightings},
        "earliest_hour": min((r.created_at.hour for r in rows if r.created_at), default=None),
    }


def count_all_sessions() -> int:
    """Every session ever - Fledgling's measure."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        return session.query(RecordingSession).count()


def count_pre_sunrise_sessions() -> int:
    """Sessions started before sunrise - Early Bird's measure."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        return session.query(RecordingSession).filter(
            RecordingSession.before_sunrise == True,  # noqa: E712
            RecordingSession.bird_count > 0).count()


def count_rainy_sessions() -> int:
    """Sessions warbled in the rain - Brooder's measure."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        return session.query(RecordingSession).filter(
            RecordingSession.was_raining == True).count()  # noqa: E712


def best_pre_sunrise_session() -> int:
    """Most birds heard in a single pre-sunrise session - Dawn Chorus."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        rows = session.query(RecordingSession.bird_count).filter(
            RecordingSession.before_sunrise == True).all()  # noqa: E712
    return max((r[0] or 0 for r in rows), default=0)


def count_sightings_of(species: set) -> int:
    """How many sightings belong to a given set of species - Night Owl counts
    nocturnal birds this way."""
    if SessionLocal is None or not species:
        return 0
    with SessionLocal() as session:
        return session.query(Sighting).filter(Sighting.common_name.in_(species)).count()


def count_species_found_far_apart(min_km: float = 5.0) -> int:
    """How many species have been found in two places at least min_km apart -
    Migrator's measure. Was a yes/no check; levels need a count."""
    if SessionLocal is None:
        return 0
    import math
    with SessionLocal() as session:
        rows = session.query(Sighting.common_name, Sighting.lat, Sighting.lng).all()

    by_species = {}
    for name, lat, lng in rows:
        if lat is None or lng is None:
            continue
        by_species.setdefault(name, set()).add((round(lat, 3), round(lng, 3)))

    def km_between(a, b):
        R = 6371.0
        p1, p2 = math.radians(a[0]), math.radians(b[0])
        dp, dl = p2 - p1, math.radians(b[1] - a[1])
        h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
        return 2 * R * math.asin(math.sqrt(h))

    total = 0
    for points in by_species.values():
        pts = list(points)
        if any(km_between(pts[i], pts[j]) >= min_km
               for i in range(len(pts)) for j in range(i + 1, len(pts))):
            total += 1
    return total


def get_share_count() -> int:
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        stats = session.query(PlayerStats).first()
        return (stats.share_count or 0) if stats else 0


def increment_share_count() -> int:
    """Wingman counts shares, so they have to be recorded rather than inferred."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        stats = session.query(PlayerStats).first()
        if stats is None:
            stats = PlayerStats(total_feathers=0, share_count=0)
            session.add(stats)
        stats.share_count = (stats.share_count or 0) + 1
        session.commit()
        return stats.share_count


def count_empty_sessions() -> int:
    """Sessions that found nothing - used for the Empty Nester trophy."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        return session.query(RecordingSession).filter(RecordingSession.bird_count == 0).count()


def award_bonus_once(key: str) -> bool:
    """Claims a one-off bonus. True only the first time for a given key, so
    callers can pay out without checking first."""
    if SessionLocal is None:
        return False
    with SessionLocal() as session:
        if session.query(AwardedBonus).filter_by(key=key).first():
            return False
        session.add(AwardedBonus(key=key))
        session.commit()
        return True


def has_session_today() -> bool:
    """Whether at least one recording has happened today (UTC, matching
    how session timestamps are stored) — used to unlock the joke of
    the day only after the first warble."""
    if SessionLocal is None:
        return False
    today_start = datetime.datetime.combine(datetime.datetime.utcnow().date(), datetime.time.min)
    with SessionLocal() as session:
        return session.query(RecordingSession).filter(
            RecordingSession.created_at >= today_start
        ).count() > 0


def count_distinct_locations(precision: int = 3) -> int:
    """Counts genuinely different places sessions have happened, by
    rounding coordinates to `precision` decimal places (3 dp is
    roughly 110m) so the same spot doesn't count twice just from GPS
    jitter."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        rows = session.query(RecordingSession.lat, RecordingSession.lng).all()
        rounded = {(round(lat, precision), round(lng, precision)) for lat, lng in rows}
        return len(rounded)


def max_sessions_at_one_location(precision: int = 3) -> int:
    """The highest number of sessions that have happened at any single
    place — used for the Rooster trophy (5+ visits to the same spot)."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        rows = session.query(RecordingSession.lat, RecordingSession.lng).all()
        counts = {}
        for lat, lng in rows:
            key = (round(lat, precision), round(lng, precision))
            counts[key] = counts.get(key, 0) + 1
        return max(counts.values()) if counts else 0


def count_rare_sightings() -> int:
    """How many Rare-tier discoveries in total — used for Golden Eagle."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        return session.query(Sighting).filter_by(tier="Rare").count()


def count_distinct_species() -> int:
    """How many different species found in total — used for Forager."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        return session.query(Sighting.common_name).distinct().count()


def count_curated_species_found(curated_set: set) -> int:
    """How many species from the curated 100-species list have been
    found so far — used for the Century trophy and the Collection's
    completion tracker. Detection itself is never restricted to this
    list; this only counts the overlap."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        found = {row[0] for row in session.query(Sighting.common_name).distinct().all()}
        return len(found & curated_set)


def get_earned_trophy_keys() -> set:
    """Keys of every trophy earned at any level."""
    if SessionLocal is None:
        return set()
    with SessionLocal() as session:
        return {t.trophy_key for t in session.query(EarnedTrophy).all()}


def get_trophy_levels() -> dict:
    """Highest level reached for each trophy, e.g. {"night_owl": 2}."""
    if SessionLocal is None:
        return {}
    out = {}
    with SessionLocal() as session:
        for t in session.query(EarnedTrophy).all():
            lvl = t.level or 1
            if lvl > out.get(t.trophy_key, 0):
                out[t.trophy_key] = lvl
    return out


def award_trophy(trophy_key: str, level: int = 1) -> bool:
    """Awards one level of a trophy. Returns True only the first time that
    specific level is earned, so a level can't pay out twice."""
    if SessionLocal is None:
        return False
    with SessionLocal() as session:
        existing = session.query(EarnedTrophy).filter_by(
            trophy_key=trophy_key, level=level).first()
        if existing is not None:
            return False
        session.add(EarnedTrophy(trophy_key=trophy_key, level=level))
        session.commit()
        return True


def get_location_name(lat: float, lng: float):
    """Returns the name for this location if one's been saved, else None."""
    if SessionLocal is None:
        return None
    rlat, rlng = round(lat, LOCATION_PRECISION), round(lng, LOCATION_PRECISION)
    with SessionLocal() as session:
        loc = session.query(Location).filter_by(lat=rlat, lng=rlng).first()
        return loc.name if loc else None


def save_location_name(lat: float, lng: float, name: str):
    """Names a location, creating it if new or renaming it if it
    already existed (in case someone wants to correct a typo later)."""
    if SessionLocal is None:
        return
    rlat, rlng = round(lat, LOCATION_PRECISION), round(lng, LOCATION_PRECISION)
    with SessionLocal() as session:
        existing = session.query(Location).filter_by(lat=rlat, lng=rlng).first()
        if existing:
            existing.name = name
        else:
            session.add(Location(lat=rlat, lng=rlng, name=name))
        session.commit()


def get_profile():
    default = {
        "first_name": "Explorer", "last_name": None,
        "avatar_body": "#C4BFDF", "avatar_face": "#E8845C", "avatar_beak": "#8E87B8",
        "avatar_photo": None, "show_scientific_names": True,
        "equipped": {"hats": None, "neck": None, "gear": None, "held": None, "glasses": None, "shoes": None},
    }
    if SessionLocal is None:
        return default
    with SessionLocal() as session:
        p = session.query(Profile).first()
        if p is None:
            p = Profile(first_name="Explorer", avatar_body="#C4BFDF", avatar_face="#E8845C", avatar_beak="#8E87B8")
            session.add(p)
            session.commit()
        # One-time migration: the name used to be a single field. Carry it into
        # first_name so nobody's existing name is lost by the split.
        if not p.first_name and p.name:
            p.first_name = p.name
            session.commit()
        return {
            "first_name": p.first_name or "Explorer",
            "last_name": p.last_name,
            "avatar_body": p.avatar_body or "#C4BFDF",
            "avatar_face": p.avatar_face or "#E8845C",
            "avatar_beak": p.avatar_beak or "#8E87B8",
            "avatar_photo": p.avatar_photo,
            "show_scientific_names": True if p.show_scientific_names is None else p.show_scientific_names,
            "equipped": {
                "hats": p.equipped_hats,
                "neck": p.equipped_neck,
                "gear": p.equipped_gear,
                "held": p.equipped_held,
                "glasses": p.equipped_glasses,
                "shoes": p.equipped_shoes,
            },
        }


def update_profile(first_name: str = None, last_name: str = None,
                   avatar_body: str = None, avatar_face: str = None, avatar_beak: str = None,
                   show_scientific_names: bool = None, avatar_photo: str = None):
    """avatar_photo accepts the string "none" to clear a photo, since an empty
    form field is indistinguishable from "not provided"."""
    if SessionLocal is None:
        return
    with SessionLocal() as session:
        p = session.query(Profile).first()
        if p is None:
            p = Profile()
            session.add(p)
        if first_name is not None:
            p.first_name = first_name
        if last_name is not None:
            p.last_name = last_name
        if avatar_body is not None:
            p.avatar_body = avatar_body
        if avatar_face is not None:
            p.avatar_face = avatar_face
        if avatar_beak is not None:
            p.avatar_beak = avatar_beak
        if show_scientific_names is not None:
            p.show_scientific_names = show_scientific_names
        if avatar_photo is not None:
            p.avatar_photo = None if avatar_photo == "none" else avatar_photo
        session.commit()


def count_owned_accessories() -> int:
    """How many Dress Up items have been bought - used for Preener."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        return session.query(OwnedAccessory).count()


def distinct_seasons_warbled() -> int:
    """How many of the four seasons have had at least one session - Evergreen.
    Meteorological seasons (Dec-Feb winter, etc), from UTC timestamps."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        rows = session.query(RecordingSession.created_at).all()
    seasons = set()
    for (created,) in rows:
        if created:
            seasons.add((created.month % 12) // 3)   # 0 winter, 1 spring, 2 summer, 3 autumn
    return len(seasons)


def max_consecutive_warble_days() -> int:
    """Longest run of consecutive calendar days with at least one session -
    used for Tailwind."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        rows = session.query(RecordingSession.created_at).all()
    days = sorted({c.date() for (c,) in rows if c})
    if not days:
        return 0
    best = run = 1
    for prev, cur in zip(days, days[1:]):
        run = run + 1 if (cur - prev).days == 1 else 1
        best = max(best, run)
    return best


def has_species_found_far_apart(min_km: float = 5.0) -> bool:
    """True if any single species has been found in two places at least
    min_km apart - used for Migrator. Uses the haversine formula rather than
    flat coordinate differences, since a degree of longitude is much shorter
    than a degree of latitude at UK latitudes."""
    if SessionLocal is None:
        return False
    import math
    with SessionLocal() as session:
        rows = session.query(Sighting.common_name, Sighting.lat, Sighting.lng).all()

    by_species = {}
    for name, lat, lng in rows:
        if lat is None or lng is None:
            continue
        by_species.setdefault(name, set()).add((round(lat, 3), round(lng, 3)))

    def km_between(a, b):
        R = 6371.0
        p1, p2 = math.radians(a[0]), math.radians(b[0])
        dp = p2 - p1
        dl = math.radians(b[1] - a[1])
        h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
        return 2 * R * math.asin(math.sqrt(h))

    for points in by_species.values():
        pts = list(points)
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                if km_between(pts[i], pts[j]) >= min_km:
                    return True
    return False


def count_species_found_in(habitat_species: set) -> int:
    """How many species from a given habitat group have been found."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        found = {r[0] for r in session.query(Sighting.common_name).distinct().all()}
    return len(found & habitat_species)


def delete_species(common_name: str) -> int:
    """Removes every sighting of one species - for clearing out a
    misidentification. Returns how many rows went.

    Deliberately does NOT refund or deduct feathers: they were genuinely
    earned at the time, and clawing them back for a bad detection that wasn't
    the user's fault would feel like a punishment."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        n = session.query(Sighting).filter_by(common_name=common_name).delete()
        session.commit()
        return n


def export_everything():
    """A full snapshot of the user's data, so a reset can be undone by hand if
    something was cleared that shouldn't have been."""
    if SessionLocal is None:
        return {}
    with SessionLocal() as session:
        return {
            "exported_at": datetime.datetime.utcnow().isoformat(),
            "sightings": [
                {"common_name": s.common_name, "scientific_name": s.scientific_name,
                 "confidence": s.confidence, "tier": s.tier, "lat": s.lat, "lng": s.lng,
                 "created_at": s.created_at.isoformat() if s.created_at else None}
                for s in session.query(Sighting).all()
            ],
            "sessions": [
                {"lat": r.lat, "lng": r.lng, "bird_count": r.bird_count,
                 "created_at": r.created_at.isoformat() if r.created_at else None}
                for r in session.query(RecordingSession).all()
            ],
            "trophies": [t.trophy_key for t in session.query(EarnedTrophy).all()],
            "locations": [{"name": l.name, "lat": l.lat, "lng": l.lng}
                          for l in session.query(Location).all()],
            "accessories": [a.accessory_id for a in session.query(OwnedAccessory).all()],
            "bonuses": [b.key for b in session.query(AwardedBonus).all()],
            "feathers": (session.query(PlayerStats).first().total_feathers
                         if session.query(PlayerStats).first() else 0),
        }


# --- Resets -----------------------------------------------------------------
# Deliberately explicit about which tables each scope clears, rather than one
# vague "wipe everything" - so it's obvious what survives each one.

def reset_dress_up():
    """Sold-back wardrobe: forget owned items and unequip everything. Avatar
    colours are kept - they're the bird's identity, not a purchase."""
    if SessionLocal is None:
        return
    with SessionLocal() as session:
        session.query(OwnedAccessory).delete()
        p = session.query(Profile).first()
        if p:
            for slot in ("hats", "neck", "gear", "held", "glasses", "shoes"):
                setattr(p, f"equipped_{slot}", None)
        session.commit()


def reset_feathers():
    """Feather balance back to zero. Owned items are kept - this is the
    balance, not the wardrobe."""
    if SessionLocal is None:
        return
    with SessionLocal() as session:
        stats = session.query(PlayerStats).first()
        if stats:
            stats.total_feathers = 0
        session.commit()


def reset_sightings():
    """Every bird, session, trophy and one-off bonus. Trophies and bonuses go
    too because they're earned FROM sightings and sessions - leaving them
    would mean holding a trophy for birds that no longer exist, and would
    silently block those bonuses from ever paying out again."""
    if SessionLocal is None:
        return
    with SessionLocal() as session:
        session.query(Sighting).delete()
        session.query(RecordingSession).delete()
        session.query(EarnedTrophy).delete()
        session.query(AwardedBonus).delete()
        session.query(Location).delete()
        session.commit()


def reset_everything():
    """Back to a first-open state, profile included."""
    if SessionLocal is None:
        return
    reset_sightings()
    reset_dress_up()
    with SessionLocal() as session:
        session.query(PlayerStats).delete()
        session.query(Profile).delete()
        session.commit()
    init_db()   # recreate the single-row PlayerStats and Profile defaults


def get_detection_stats():
    """Headline stats for the Profile page. Returns None for any stat there
    isn't enough data to answer honestly, rather than inventing a default."""
    if SessionLocal is None:
        return {"total_detections": 0, "top_bird": None, "top_location": None, "top_time": None}

    with SessionLocal() as session:
        sightings = session.query(Sighting.common_name, Sighting.lat, Sighting.lng,
                                 Sighting.created_at).all()
        total = len(sightings)
        if total == 0:
            return {"total_detections": 0, "top_bird": None, "top_location": None, "top_time": None}

        bird_counts = {}
        for s in sightings:
            bird_counts[s.common_name] = bird_counts.get(s.common_name, 0) + 1
        top_name, top_count = max(bird_counts.items(), key=lambda kv: kv[1])

        # Only count locations the user has actually named - an unnamed spot
        # has nothing meaningful to display.
        named = {(l.lat, l.lng): l.name for l in session.query(Location).all()}
        loc_counts = {}
        for s in sightings:
            if s.lat is None or s.lng is None:
                continue
            key = (round(s.lat, LOCATION_PRECISION), round(s.lng, LOCATION_PRECISION))
            if key in named:
                loc_counts[named[key]] = loc_counts.get(named[key], 0) + 1
        top_location = None
        if loc_counts:
            name, count = max(loc_counts.items(), key=lambda kv: kv[1])
            top_location = {"name": name, "count": count}

        # NOTE: timestamps are stored in UTC, so these buckets are UTC hours.
        # During British Summer Time they'll sit about an hour off local time -
        # the same known simplification as the Night Owl trophy.
        def bucket(hour):
            if 5 <= hour < 8:
                return "Dawn"
            if 8 <= hour < 12:
                return "Morning"
            if 12 <= hour < 17:
                return "Afternoon"
            return "Evening"

        time_counts = {}
        for s in sightings:
            if s.created_at:
                b = bucket(s.created_at.hour)
                time_counts[b] = time_counts.get(b, 0) + 1
        top_time = None
        if time_counts:
            name, count = max(time_counts.items(), key=lambda kv: kv[1])
            top_time = {"name": name, "count": count}

        return {
            "total_detections": total,
            "top_bird": {"name": top_name, "count": top_count},
            "top_location": top_location,
            "top_time": top_time,
        }


def delete_location(location_id: int):
    """Removes a saved location name. The recording sessions that happened
    there are untouched - this only forgets the label, so the spot simply
    becomes unnamed again and can be renamed on a future visit."""
    if SessionLocal is None:
        return
    with SessionLocal() as session:
        loc = session.query(Location).filter_by(id=location_id).first()
        if loc:
            session.delete(loc)
            session.commit()


def get_owned_accessory_ids() -> set:
    if SessionLocal is None:
        return set()
    with SessionLocal() as session:
        return {a.accessory_id for a in session.query(OwnedAccessory).all()}


def purchase_accessory(accessory_id: str, cost: float, category: str = None) -> bool:
    """Buys an accessory: deducts feathers if affordable and not already
    owned. Returns True only if the purchase went through.

    Deliberately does NOT equip it. Buying and wearing are separate choices -
    auto-equipping would silently replace whatever the bird already had on."""
    if SessionLocal is None:
        return False
    with SessionLocal() as session:
        already_owned = session.query(OwnedAccessory).filter_by(accessory_id=accessory_id).first()
        if already_owned:
            return False
        stats = session.query(PlayerStats).first()
        if stats is None or stats.total_feathers < cost:
            return False
        stats.total_feathers -= cost
        session.add(OwnedAccessory(accessory_id=accessory_id))
        session.commit()
        return True


def set_equipped_item(category: str, accessory_id):
    """Sets (or clears, if accessory_id is None) the worn item for one
    of the 6 slots: hats, glasses, neck, gear, held, shoes."""
    if SessionLocal is None:
        return
    if category not in ("hats", "neck", "gear", "held", "glasses", "shoes"):
        return
    with SessionLocal() as session:
        p = session.query(Profile).first()
        if p is None:
            p = Profile()
            session.add(p)
        setattr(p, f"equipped_{category}", accessory_id)
        session.commit()


def get_all_locations():
    if SessionLocal is None:
        return []
    with SessionLocal() as session:
        rows = session.query(Location).order_by(Location.created_at.desc()).all()
        return [{"id": l.id, "name": l.name, "lat": l.lat, "lng": l.lng} for l in rows]


def rename_location(location_id: int, new_name: str):
    if SessionLocal is None:
        return
    with SessionLocal() as session:
        loc = session.query(Location).filter_by(id=location_id).first()
        if loc:
            loc.name = new_name
            session.commit()
