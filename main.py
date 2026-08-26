import os
import tempfile
import threading
import json
import datetime
from pathlib import Path

import requests
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydub import AudioSegment

app = FastAPI(title="Warble BirdNET Inference API")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Loads in the background so the server can start answering requests
# (including Railway's health check) right away.
analyzer = None
analyzer_error = None


def load_analyzer():
    global analyzer, analyzer_error
    try:
        print("Loading BirdNET analyzer in background...")
        from birdnetlib.analyzer import Analyzer
        analyzer = Analyzer()
        print("BirdNET analyzer loaded. Ready for requests.")
    except Exception as e:
        analyzer_error = str(e)
        print(f"Failed to load BirdNET analyzer: {e}")


threading.Thread(target=load_analyzer, daemon=True).start()


@app.get("/")
def serve_app():
    """The actual app — a real page now, not just a status check."""
    return FileResponse("static/index.html")


@app.get("/status")
def status():
    """The old root endpoint, moved here — still useful for checking
    whether the model's finished loading, same as before."""
    if analyzer is not None:
        status = "ready"
    elif analyzer_error is not None:
        status = "error"
    else:
        status = "loading"

    return {
        "status": status,
        "message": "Warble BirdNET inference API",
        "error": analyzer_error,
    }


@app.post("/identify")
async def identify(file: UploadFile = File(...), lat: float = 51.5074, lng: float = -0.1278):
    """
    Send a WAV (or MP3) audio file as multipart form-data under the field
    name 'file'. Returns the species BirdNET detected, ranked by
    confidence, highest first.
    """
    if analyzer is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "loading",
                "message": "Analyzer is still loading — check the '/status' endpoint, then try again shortly.",
            },
        )

    suffix = Path(file.filename).suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
        contents = await file.read()
        tmp_in.write(contents)
        tmp_in_path = tmp_in.name

    # Convert whatever format arrived (aac, m4a, mp3, wav, ...) into a
    # clean WAV file using ffmpeg. This is deliberately explicit rather
    # than relying on librosa's own format-fallback behaviour, which
    # varies between versions and caused exactly this kind of failure.
    tmp_wav_path = tmp_in_path + "_converted.wav"
    try:
        audio = AudioSegment.from_file(tmp_in_path)
        audio.export(tmp_wav_path, format="wav")
    except Exception as e:
        os.unlink(tmp_in_path)
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": f"Could not read this audio file: {e}"},
        )

    try:
        from birdnetlib import Recording
        recording = Recording(
            analyzer,
            tmp_wav_path,
            lat=lat,
            lon=lng,
            date=datetime.date.today(),
            min_conf=0.5,
        )
        recording.analyze()
        detections = recording.detections
    finally:
        os.unlink(tmp_in_path)
        os.unlink(tmp_wav_path)

    detections.sort(key=lambda d: d["confidence"], reverse=True)

    return {"detections": detections[:10]}


# ============================================================
# Everything below here is the all-in-one session endpoint.
# It does BirdNET + NBN Atlas tiering + duplicate checking +
# Wikipedia photos + feather maths + saving — all in one call.
# ============================================================

from database import (
    init_db, has_existing_sighting, save_sighting,
    add_feathers, get_all_sightings, get_total_feathers,
    record_session, count_distinct_locations,
    get_earned_trophy_keys, award_trophy,
    get_location_name, save_location_name,
    get_cached_call_url, get_profile, update_profile,
    get_all_locations, rename_location,
    max_sessions_at_one_location, count_rare_sightings, count_distinct_species,
    has_session_today,
)
from bird_facts import get_bird_facts
from trophies import TROPHY_DEFINITIONS, is_before_sunrise, NOCTURNAL_SPECIES
from jokes import get_joke_of_the_day

init_db()

XENO_CANTO_API_KEY = os.environ.get("XENO_CANTO_API_KEY", "")


def get_bird_call_url(scientific_name: str):
    """Fetches a real recording of this species' song from xeno-canto,
    the purpose-built bird sound archive. Filtered for high quality
    (q:A) and genuine song (not alarm calls etc). Returns None if no
    key is set, or nothing suitable is found."""
    if not XENO_CANTO_API_KEY:
        return None
    try:
        response = requests.get(
            "https://xeno-canto.org/api/3/recordings",
            params={"query": f'sp:"{scientific_name}" q:A type:song', "key": XENO_CANTO_API_KEY},
            timeout=10,
        )
        response.raise_for_status()
        recordings = response.json().get("recordings", [])
        if recordings:
            return recordings[0].get("file")
    except Exception as e:
        print(f"Warning: xeno-canto lookup failed for {scientific_name}: {e}")
    return None


def check_session_trophies(lat: float, lng: float, moment_utc: datetime.datetime):
    """
    Checks trophies that only depend on the session happening at all -
    not on what (if anything) gets detected. Called before the
    detection loop. Returns (newly_earned_keys, is_before_sunrise) -
    the sunrise flag is handed back so check_detection_trophies
    doesn't need to recompute it.
    """
    total_sessions = record_session(lat, lng)
    newly_earned = []

    if total_sessions == 1:
        if award_trophy("fledgling"):
            newly_earned.append("fledgling")

    before_sunrise = is_before_sunrise(lat, lng, moment_utc)
    if before_sunrise:
        if award_trophy("early_bird"):
            newly_earned.append("early_bird")

    if count_distinct_locations() >= 10:
        if award_trophy("nomad"):
            newly_earned.append("nomad")

    if max_sessions_at_one_location() >= 5:
        if award_trophy("rooster"):
            newly_earned.append("rooster")

    return newly_earned, before_sunrise


def check_detection_trophies(results: list, before_sunrise: bool, moment_utc: datetime.datetime):
    """
    Checks trophies that depend on what was actually detected this
    session - called after the detection loop, once results (and
    their tiers) are known.
    """
    newly_earned = []

    if count_rare_sightings() >= 5:
        if award_trophy("golden_eagle"):
            newly_earned.append("golden_eagle")

    if count_distinct_species() >= 20:
        if award_trophy("forager"):
            newly_earned.append("forager")

    species_this_session = {r["common_name"] for r in results}

    if before_sunrise and len(species_this_session) >= 5:
        if award_trophy("dawn_chorus"):
            newly_earned.append("dawn_chorus")

    # NOTE: this hour check is in UTC, same as Early Bird's sunrise
    # comparison. Unlike sunrise (which is itself computed in UTC, so
    # the comparison is self-consistent), "9pm" is a fixed civil-clock
    # threshold - during British Summer Time this will be roughly an
    # hour off from true UK local time. A reasonable simplification for
    # now, not a silent bug - worth a proper timezone fix later if it
    # matters in practice.
    if moment_utc.hour >= 21 and any(name in NOCTURNAL_SPECIES for name in species_this_session):
        if award_trophy("night_owl"):
            newly_earned.append("night_owl")

    return newly_earned


def get_nbn_tier(scientific_name: str, lat: float, lng: float):
    """Query NBN Atlas for how many records exist nearby. Returns (tier, record_count)."""
    try:
        response = requests.get(
            "https://records-ws.nbnatlas.org/occurrences/search",
            params={"q": scientific_name, "lat": lat, "lon": lng, "radius": 25},
            timeout=10,
        )
        response.raise_for_status()
        total = response.json().get("totalRecords", 0)
    except Exception as e:
        print(f"Warning: NBN Atlas lookup failed for {scientific_name}: {e}")
        total = 0  # if we genuinely can't tell, default to Rare rather than falsely calling it Common

    if total >= 100000:
        tier = "Common"
    elif total >= 1000:
        tier = "Visitor"
    else:
        tier = "Rare"
    return tier, total


def get_wikipedia_info(scientific_name: str):
    """Fetch a photo URL and a short description for this species from
    Wikipedia, in one call. Returns (photo_url, description) — either
    can be None if Wikipedia doesn't have it."""
    title = scientific_name.replace(" ", "_")
    try:
        response = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}",
            headers={"User-Agent": "Warble bird app (dev testing)"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("thumbnail", {}).get("source"), data.get("extract")
    except Exception as e:
        print(f"Warning: Wikipedia lookup failed for {scientific_name}: {e}")
        return None, None


def calculate_feathers(tier: str, is_duplicate: bool) -> float:
    values = {
        ("Common", False): 5, ("Visitor", False): 25, ("Rare", False): 50,
        ("Common", True): 1, ("Visitor", True): 2, ("Rare", True): 10,
    }
    return values.get((tier, is_duplicate), 0)


@app.post("/analyze-session")
async def analyze_session(
    file: UploadFile = File(...),
    lat: float = 51.5074,
    lng: float = -0.1278,
):
    """
    The all-in-one endpoint. Identifies every bird in a recording, checks
    each one's rarity tier and duplicate status, calculates feathers,
    fetches a photo, saves it to the database, and returns the full
    enriched list — ready to display directly on the page.
    """
    if analyzer is None:
        return JSONResponse(
            status_code=503,
            content={"status": "loading", "message": "Analyzer is still loading, try again shortly."},
        )

    suffix = Path(file.filename).suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
        contents = await file.read()
        tmp_in.write(contents)
        tmp_in_path = tmp_in.name

    tmp_wav_path = tmp_in_path + "_converted.wav"
    try:
        audio = AudioSegment.from_file(tmp_in_path)
        audio.export(tmp_wav_path, format="wav")
    except Exception as e:
        os.unlink(tmp_in_path)
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": f"Could not read this audio file: {e}"},
        )

    try:
        from birdnetlib import Recording
        recording = Recording(
            analyzer,
            tmp_wav_path,
            lat=lat,
            lon=lng,
            date=datetime.date.today(),
            min_conf=0.5,
        )
        recording.analyze()
        detections = recording.detections
    finally:
        os.unlink(tmp_in_path)
        os.unlink(tmp_wav_path)

    detections.sort(key=lambda d: d["confidence"], reverse=True)

    # If the same species was heard more than once in this one recording,
    # only keep its strongest detection — one card per bird per listen,
    # not one per moment it happened to call.
    seen_species = set()
    unique_detections = []
    for d in detections:
        if d["common_name"] not in seen_species:
            seen_species.add(d["common_name"])
            unique_detections.append(d)
    detections = unique_detections

    now = datetime.datetime.now(datetime.timezone.utc)
    results = []

    session_trophy_keys, before_sunrise = check_session_trophies(lat, lng, now)
    existing_location_name = get_location_name(lat, lng)
    needs_location_name = existing_location_name is None

    for detection in detections:
        common_name = detection["common_name"]
        scientific_name = detection["scientific_name"]
        confidence = detection["confidence"]

        is_duplicate = has_existing_sighting(common_name)
        tier, record_count = get_nbn_tier(scientific_name, lat, lng)
        feathers = calculate_feathers(tier, is_duplicate)
        photo_url, description = get_wikipedia_info(scientific_name)

        call_url = get_cached_call_url(common_name)
        if call_url is None:
            call_url = get_bird_call_url(scientific_name)

        save_sighting(common_name, scientific_name, confidence, tier, photo_url, description, lat, lng, call_url)

        results.append({
            "common_name": common_name,
            "scientific_name": scientific_name,
            "confidence": confidence,
            "tier": tier,
            "nbn_record_count": record_count,
            "is_duplicate": is_duplicate,
            "feathers": feathers,
            "call_url": call_url,
            "photo_url": photo_url,
            "description": description,
            # Extra context, unused today — kept ready for trophy logic later:
            "detected_at": now.isoformat(),
            "hour_of_day": now.hour,
            "lat": lat,
            "lng": lng,
        })

    detection_trophy_keys = check_detection_trophies(results, before_sunrise, now)
    all_earned_keys = session_trophy_keys + detection_trophy_keys
    newly_earned_trophies = [{"key": k, **TROPHY_DEFINITIONS[k]} for k in all_earned_keys]

    session_feathers = sum(r["feathers"] for r in results)
    new_total = add_feathers(session_feathers)

    return {
        "detections": results,
        "total_feathers_this_session": session_feathers,
        "total_feathers": new_total,
        "newly_earned_trophies": newly_earned_trophies,
        "needs_location_name": needs_location_name,
        "location_name": existing_location_name,
        "lat": lat,
        "lng": lng,
    }


@app.post("/name-location")
async def name_location(lat: float = Form(...), lng: float = Form(...), name: str = Form(...)):
    """Saves a free-text name for wherever (lat, lng) rounds to."""
    save_location_name(lat, lng, name)
    return {"status": "ok"}


@app.get("/locations")
def list_locations():
    """Every named location, for viewing/editing on the Profile page."""
    return {"locations": get_all_locations()}


@app.post("/locations/{location_id}/rename")
async def rename_location_endpoint(location_id: int, name: str = Form(...)):
    rename_location(location_id, name)
    return {"status": "ok"}


@app.get("/profile")
def profile():
    return get_profile()


@app.post("/profile")
async def update_profile_endpoint(name: str = Form(None), avatar_id: str = Form(None)):
    update_profile(name=name, avatar_id=avatar_id)
    return {"status": "ok"}


@app.get("/trophies")
def list_trophies():
    """All 3 built trophies, each marked earned or not."""
    earned = get_earned_trophy_keys()
    return {
        "trophies": [
            {"key": key, "earned": key in earned, **info}
            for key, info in TROPHY_DEFINITIONS.items()
        ]
    }


@app.get("/sightings")
def list_sightings():
    """Every bird ever found, newest first — for a Collection screen.
    Each one includes curated facts (size, wingspan, habitat) when
    we've researched that species — None if we haven't yet."""
    sightings = get_all_sightings()
    for s in sightings:
        s["facts"] = get_bird_facts(s["common_name"])
    return {"sightings": sightings}


@app.get("/feathers")
def feathers_total():
    """The current running feather total."""
    return {"total_feathers": get_total_feathers()}


@app.get("/joke-of-the-day")
def joke_of_the_day():
    """Today's joke, only revealed once at least one session has
    happened today - otherwise unlocked stays false and joke is null."""
    unlocked = has_session_today()
    return {
        "unlocked": unlocked,
        "joke": get_joke_of_the_day() if unlocked else None,
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
