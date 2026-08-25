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


class Sighting(Base):
    __tablename__ = "sightings"

    id = Column(Integer, primary_key=True)
    common_name = Column(String, nullable=False)
    scientific_name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    tier = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
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

    with SessionLocal() as session:
        existing = session.query(PlayerStats).first()
        if existing is None:
            session.add(PlayerStats(total_feathers=0))
            session.commit()


def has_existing_sighting(common_name: str) -> bool:
    if SessionLocal is None:
        return False
    with SessionLocal() as session:
        return session.query(Sighting).filter_by(common_name=common_name).first() is not None


def save_sighting(common_name, scientific_name, confidence, tier, image_url, description=None):
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
        ))
        session.commit()


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
        return [
            {
                "common_name": r.common_name,
                "scientific_name": r.scientific_name,
                "confidence": r.confidence,
                "tier": r.tier,
                "image_url": r.image_url,
                "description": r.description,
                "created_at": r.created_at.isoformat(),
            }
            for r in rows
        ]


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
