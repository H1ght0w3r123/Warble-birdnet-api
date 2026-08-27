"""
Real database for Warble, replacing what Bubble's Data API used to do.
Uses Postgres, via Railway's DATABASE_URL. Two tables: sightings (every
bird ever found) and player_stats (a single running feather total, for
now — no accounts yet, so there's just one shared total).
"""
import os
import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
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


class RecordingSession(Base):
    """One row per recording — regardless of whether any bird was heard.
    Used for trophy checks (Fledgling, Nomad) that care about sessions
    themselves, not just successful bird finds."""
    __tablename__ = "recording_sessions"

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class EarnedTrophy(Base):
    __tablename__ = "earned_trophies"

    id = Column(Integer, primary_key=True)
    trophy_key = Column(String, unique=True, nullable=False)
    earned_at = Column(DateTime, default=datetime.datetime.utcnow)


class Location(Base):
    """A named place — created the first time a session happens somewhere
    new. lat/lng are stored already rounded to LOCATION_PRECISION."""
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Profile(Base):
    """Single-row, same pattern as PlayerStats — no accounts system
    yet, so there's just one shared profile."""
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    name = Column(String, default="Explorer")
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


def has_existing_sighting(common_name: str) -> bool:
    if SessionLocal is None:
        return False
    with SessionLocal() as session:
        return session.query(Sighting).filter_by(common_name=common_name).first() is not None


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


def record_session(lat: float, lng: float):
    """Log that a recording happened, regardless of what (if anything)
    was heard. Returns the total number of sessions ever, including
    this one — useful for the Fledgling check without a second query."""
    if SessionLocal is None:
        return 0
    with SessionLocal() as session:
        session.add(RecordingSession(lat=lat, lng=lng))
        session.commit()
        return session.query(RecordingSession).count()


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
    if SessionLocal is None:
        return set()
    with SessionLocal() as session:
        return {t.trophy_key for t in session.query(EarnedTrophy).all()}


def award_trophy(trophy_key: str) -> bool:
    """Awards a trophy if it hasn't been earned already. Returns True
    if this call newly awarded it, False if it was already earned (or
    the database isn't configured)."""
    if SessionLocal is None:
        return False
    with SessionLocal() as session:
        existing = session.query(EarnedTrophy).filter_by(trophy_key=trophy_key).first()
        if existing is not None:
            return False
        session.add(EarnedTrophy(trophy_key=trophy_key))
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
        "name": "Explorer", "avatar_body": "#C4BFDF", "avatar_face": "#E8845C", "avatar_beak": "#8E87B8",
        "equipped": {"hats": None, "neck": None, "gear": None, "held": None, "glasses": None, "shoes": None},
    }
    if SessionLocal is None:
        return default
    with SessionLocal() as session:
        p = session.query(Profile).first()
        if p is None:
            p = Profile(name="Explorer", avatar_body="#C4BFDF", avatar_face="#E8845C", avatar_beak="#8E87B8")
            session.add(p)
            session.commit()
        return {
            "name": p.name,
            "avatar_body": p.avatar_body or "#C4BFDF",
            "avatar_face": p.avatar_face or "#E8845C",
            "avatar_beak": p.avatar_beak or "#8E87B8",
            "equipped": {
                "hats": p.equipped_hats,
                "neck": p.equipped_neck,
                "gear": p.equipped_gear,
                "held": p.equipped_held,
                "glasses": p.equipped_glasses,
                "shoes": p.equipped_shoes,
            },
        }


def update_profile(name: str = None, avatar_body: str = None, avatar_face: str = None, avatar_beak: str = None):
    if SessionLocal is None:
        return
    with SessionLocal() as session:
        p = session.query(Profile).first()
        if p is None:
            p = Profile()
            session.add(p)
        if name is not None:
            p.name = name
        if avatar_body is not None:
            p.avatar_body = avatar_body
        if avatar_face is not None:
            p.avatar_face = avatar_face
        if avatar_beak is not None:
            p.avatar_beak = avatar_beak
        session.commit()


def get_owned_accessory_ids() -> set:
    if SessionLocal is None:
        return set()
    with SessionLocal() as session:
        return {a.accessory_id for a in session.query(OwnedAccessory).all()}


def purchase_accessory(accessory_id: str, cost: float, category: str) -> bool:
    """Attempts to buy an accessory - deducts feathers if affordable
    and not already owned, then wears it immediately in its category's
    slot (replacing whatever was there). Returns True only if the
    purchase actually went through."""
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
        p = session.query(Profile).first()
        if p is None:
            p = Profile()
            session.add(p)
        if category in ("hats", "neck", "gear", "glasses", "shoes"):
            setattr(p, f"equipped_{category}", accessory_id)
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
