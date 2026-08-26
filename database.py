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
    avatar_id = Column(String, default="robin")


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

    with SessionLocal() as session:
        existing = session.query(PlayerStats).first()
        if existing is None:
            session.add(PlayerStats(total_feathers=0))
            session.commit()
        existing_profile = session.query(Profile).first()
        if existing_profile is None:
            session.add(Profile(name="Explorer", avatar_id="robin"))
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
    if SessionLocal is None:
        return {"name": "Explorer", "avatar_id": "robin"}
    with SessionLocal() as session:
        p = session.query(Profile).first()
        if p is None:
            p = Profile(name="Explorer", avatar_id="robin")
            session.add(p)
            session.commit()
        return {"name": p.name, "avatar_id": p.avatar_id}


def update_profile(name: str = None, avatar_id: str = None):
    if SessionLocal is None:
        return
    with SessionLocal() as session:
        p = session.query(Profile).first()
        if p is None:
            p = Profile()
            session.add(p)
        if name is not None:
            p.name = name
        if avatar_id is not None:
            p.avatar_id = avatar_id
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
