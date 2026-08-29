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
async def identify(
    file: UploadFile = File(...),
    # Must be Form(), not bare params: the frontend sends these as form
    # fields, and FastAPI treats undecorated scalars as QUERY params - so
    # these were silently ignored and every plausibility check ran against
    # the London defaults regardless of where the user actually was.
    lat: float = Form(51.5074),
    lng: float = Form(-0.1278),
):
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
        # NOT passing lat/lon/date here deliberately - birdnetlib's own
        # geographic+seasonal species filtering was tried and appears to
        # have caused a real regression (recordings that used to detect
        # correctly stopped detecting anything, even after separately
        # confirming the confidence threshold wasn't the cause). NBN
        # Atlas tiering already does the "how plausible is this here"
        # job, more transparently (tags as Rare rather than silently
        # hiding a detection) - so it's the sole mechanism for that now.
        recording = Recording(
            analyzer,
            tmp_wav_path,
            min_conf=0.15,
        )
        recording.analyze()
        detections = recording.detections
    finally:
        os.unlink(tmp_in_path)
        os.unlink(tmp_wav_path)

    # BirdNET's model includes non-bird classes alongside real species -
    # human speech being the one most likely to fire in a garden with a child
    # narrating. These are never valid finds, so they're dropped before any
    # other filtering rather than being allowed to occupy one of the top-3
    # candidate slots below.
    before_nonbird = len(detections)
    detections = [d for d in detections if not is_non_bird(d["common_name"])]
    if len(detections) < before_nonbird:
        print(f"identify: filtered out {before_nonbird - len(detections)} non-bird detection(s)")

    detections.sort(key=lambda d: d["confidence"], reverse=True)
    print(f"identify: BirdNET returned {len(detections)} detection(s) at {lat},{lng}"
          + (": " + ", ".join(f"{d['common_name']} {d['confidence']:.2f}" for d in detections[:5]) if detections else ""))

    # Same plausibility check /analyze-session uses, applied here too so
    # a live "yes" and the final result are answering the same question
    # - only check the top few candidates to keep this endpoint fast
    # enough for repeated calls during a live preview loop.
    filtered_detections = []
    for d in detections[:3]:
        if is_locally_plausible(d["scientific_name"], lat, lng):
            tier, _ = get_nbn_tier(d["scientific_name"], lat, lng)
            filtered_detections.append({**d, "tier": tier})

    if len(filtered_detections) < len(detections[:3]):
        rejected = [d["common_name"] for d in detections[:3]
                    if d["common_name"] not in {f["common_name"] for f in filtered_detections}]
        print(f"identify: rejected as not locally plausible: {rejected}")

    return {"detections": filtered_detections}


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
    get_all_locations, rename_location, delete_location, get_detection_stats,
    set_session_bird_count, count_successful_sessions_today, count_successful_sessions_this_week,
    count_empty_sessions, award_bonus_once, get_week_stats,
    count_owned_accessories, distinct_seasons_warbled, max_consecutive_warble_days,
    has_species_found_far_apart, count_species_found_in,
    max_sessions_at_one_location, count_rare_sightings, count_distinct_species,
    has_session_today,
    get_owned_accessory_ids, purchase_accessory, set_equipped_item,
    count_curated_species_found,
    set_total_feathers,
)
from bird_facts import get_bird_facts
from trophies import TROPHY_DEFINITIONS, is_before_sunrise, NOCTURNAL_SPECIES
from jokes import get_joke_of_the_day
from accessories import ACCESSORIES, CATEGORIES
from curated_species import ALL_CURATED_SPECIES, CURATED_SPECIES
from challenges import get_week_challenges, current_week_key, ALL_COMPLETE_BONUS

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
    detection loop. Returns (newly_earned_keys, is_before_sunrise, session_id)
    - the sunrise flag is handed back so check_detection_trophies doesn't need
    to recompute it, and the session id lets the caller record how many birds
    were found once detection has finished.
    """
    total_sessions, session_id = record_session(lat, lng)
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

    if distinct_seasons_warbled() >= 4:
        if award_trophy("evergreen"):
            newly_earned.append("evergreen")

    if max_consecutive_warble_days() >= 3:
        if award_trophy("tailwind"):
            newly_earned.append("tailwind")

    if count_owned_accessories() >= 10:
        if award_trophy("preener"):
            newly_earned.append("preener")

    # Checked here rather than in the detection pass, since it's about
    # sessions that found nothing - the detection pass never runs for those.
    if count_empty_sessions() >= 20:
        if award_trophy("empty_nester"):
            newly_earned.append("empty_nester")

    # Only call the weather API while this is still unearned - no point paying
    # the latency on every session once it's already won.
    if "brooder" not in get_earned_trophy_keys() and is_raining(lat, lng):
        if award_trophy("brooder"):
            newly_earned.append("brooder")

    return newly_earned, before_sunrise, session_id


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

    if count_curated_species_found(ALL_CURATED_SPECIES) >= len(ALL_CURATED_SPECIES):
        if award_trophy("century"):
            newly_earned.append("century")

    # Habitat-group trophies, counted against the curated 100-species list
    habitat_trophies = [
        ("skylark", "Farmland & Hedgerow"),
        ("high_flyer", "Raptors & Others"),
        ("still_water", "Wetland & Water"),
    ]
    for key, habitat in habitat_trophies:
        if count_species_found_in(set(CURATED_SPECIES[habitat])) >= 5:
            if award_trophy(key):
                newly_earned.append(key)

    if has_species_found_far_apart(5.0):
        if award_trophy("migrator"):
            newly_earned.append("migrator")

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


# BirdNET's label set isn't purely birds - it also classifies human speech,
# dogs, sirens, engines and general noise. None are valid finds for Warble.
NON_BIRD_LABELS = {
    "human vocal", "human non-vocal", "human whistle", "human",
    "dog", "engine", "environmental", "fireworks", "gun",
    "noise", "power tools", "siren",
}


def is_non_bird(common_name: str) -> bool:
    """True if this label is one of BirdNET's non-bird classes. Substring
    checks on 'human' and 'noise' too, so variants of those labels across
    model versions are caught rather than slipping through on an exact-match
    miss - a human voice reported as a bird is the worst case here."""
    name = (common_name or "").strip().lower()
    if name in NON_BIRD_LABELS:
        return True
    return "human" in name or "noise" in name


def is_raining(lat: float, lng: float) -> bool:
    """Whether it's currently raining at this spot, via Open-Meteo (free, no
    API key needed). Used for the Brooder trophy. Returns False if the lookup
    fails - better to not award a trophy than to award one wrongly."""
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lng, "current": "precipitation"},
            timeout=6,
        )
        response.raise_for_status()
        mm = response.json().get("current", {}).get("precipitation", 0) or 0
        if mm > 0:
            print(f"Brooder: {mm}mm precipitation at {lat},{lng} - it's raining")
        return mm > 0
    except Exception as e:
        print(f"Warning: weather lookup failed for {lat},{lng}: {e}")
        return False


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


def is_locally_plausible(scientific_name: str, lat: float, lng: float) -> bool:
    """A tighter, more garden-relevant plausibility check than the
    25km tier calculation above. 25km is wide enough that a real UK
    species (e.g. a farmland specialist like Yellowhammer) can easily
    have genuine records somewhere in that radius even though it would
    never actually turn up at this specific recording spot. Uses a
    much smaller radius, closer to 'could this realistically be heard
    from here' than 'does this species exist somewhere in the wider
    region'. Deliberately separate from get_nbn_tier so the existing,
    already-calibrated 25km tier/feather system is untouched."""
    try:
        response = requests.get(
            "https://records-ws.nbnatlas.org/occurrences/search",
            params={"q": scientific_name, "lat": lat, "lon": lng, "radius": 5},
            timeout=10,
        )
        response.raise_for_status()
        total = response.json().get("totalRecords", 0)
    except Exception as e:
        print(f"Warning: local plausibility check failed for {scientific_name}: {e}")
        return True  # if we can't tell, fail open rather than silently hiding a real find

    return total >= 3


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


# Reward tuning. Duplicates pay meaningfully now because once a child has
# found their local birds, repeats are what going outside actually produces -
# the old 1-feather duplicate meant the app stopped paying right when the
# habit should have been forming.
SESSION_BONUS = 10        # per successful session, max 2/day
HABITAT_SET_BONUS = 100


def calculate_feathers(tier: str, is_duplicate: bool) -> float:
    values = {
        ("Common", False): 5, ("Visitor", False): 25, ("Rare", False): 50,
        ("Common", True): 3, ("Visitor", True): 8, ("Rare", True): 20,
    }
    return values.get((tier, is_duplicate), 0)


@app.post("/analyze-session")
async def analyze_session(
    lat: float = Form(51.5074),
    lng: float = Form(-0.1278),
    live_detections: str = Form("[]"),
):
    """
    Takes the species already identified live during recording, then does the
    enrichment: rarity tier, duplicate check, feathers, photo, saving, and
    trophies - returning the full list ready to display.

    No audio is uploaded or analysed here. Identification happens entirely in
    the live pass during recording (short clips sent to /identify), which is
    now the single source of truth. Earlier versions re-analysed the whole
    recording server-side as well - first as a rival result, then merged - but
    running two passes proved unreliable in practice.

    Trade-off worth knowing: the live pass scores independent ~3.5s clips, so
    a call straddling a clip boundary can be split and missed. Continuous
    analysis of the whole recording didn't have that weakness. Recording for
    longer is the practical mitigation - more clips, more chances.
    """
    print(f"analyze-session: received lat={lat}, lng={lng}")

    # Already confidence-filtered and plausibility-checked by /identify during
    # recording, so no further filtering here - just deduplicate by species.
    detections = []
    seen_names = set()
    try:
        for d in json.loads(live_detections):
            name = d.get("common_name")
            if name and name not in seen_names:
                seen_names.add(name)
                detections.append({
                    "common_name": name,
                    "scientific_name": d.get("scientific_name", ""),
                    "confidence": d.get("confidence", 0.0),
                })
    except (ValueError, TypeError) as e:
        print(f"Warning: couldn't parse live_detections: {e}")

    now = datetime.datetime.now(datetime.timezone.utc)
    results = []

    session_trophy_keys, before_sunrise, session_id = check_session_trophies(lat, lng, now)
    existing_location_name = get_location_name(lat, lng)
    needs_location_name = existing_location_name is None

    for detection in detections:
        common_name = detection["common_name"]
        scientific_name = detection["scientific_name"]
        confidence = detection["confidence"]

        # No plausibility check here any more - /identify already ran
        # is_locally_plausible on everything during recording, so a second
        # pass would only reject birds the user already watched a badge
        # appear for, recreating exactly the disappearing-detection problem
        # this restructure removes.
        tier, record_count = get_nbn_tier(scientific_name, lat, lng)

        is_duplicate = has_existing_sighting(common_name)
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
    bonuses = []

    # Record what this session found before any of the bonus checks below,
    # since they all read from it.
    set_session_bird_count(session_id, len(results))

    if results:
        # Rewards showing up, not just discovering something new - which is the
        # behaviour that keeps going once the local birds are all found. Capped
        # at 2/day so it can't be farmed by tapping record repeatedly.
        if count_successful_sessions_today() <= 2:
            session_feathers += SESSION_BONUS
            bonuses.append({"label": "Warble bonus", "feathers": SESSION_BONUS})

        # Weekly challenges. The old standalone "3 warbles a week" bonus is now
        # just one of these, so there's a single weekly mechanic rather than two
        # competing ones.
        for ch, done, _ in evaluate_week_challenges():
            if done and award_bonus_once(f"challenge:{current_week_key()}:{ch['id']}"):
                session_feathers += ch["feathers"]
                bonuses.append({"label": ch["text"], "feathers": ch["feathers"]})

        if all(done for _, done, _ in evaluate_week_challenges()):
            if award_bonus_once(f"challenge:{current_week_key()}:ALL"):
                session_feathers += ALL_COMPLETE_BONUS
                bonuses.append({"label": "All 5 challenges done!", "feathers": ALL_COMPLETE_BONUS})

        # Habitat sets - completing one is a real milestone worth paying for
        for habitat, species in CURATED_SPECIES.items():
            if count_species_found_in(set(species)) >= len(species):
                if award_bonus_once(f"habitat:{habitat}"):
                    session_feathers += HABITAT_SET_BONUS
                    bonuses.append({"label": f"{habitat} complete!", "feathers": HABITAT_SET_BONUS})

    new_total = add_feathers(session_feathers)

    return {
        "detections": results,
        "total_feathers_this_session": session_feathers,
        "bonuses": bonuses,
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


@app.get("/where-am-i")
def where_am_i(lat: float, lng: float):
    """A friendly name for where a recording is happening. Prefers a
    name the user has already given this spot; otherwise falls back to
    a town/country lookup via OpenStreetMap's Nominatim. Returns None
    if neither is available, so the caller can just omit the line."""
    saved = get_location_name(lat, lng)
    if saved:
        return {"name": saved, "source": "saved"}

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lng, "format": "json", "zoom": 12},
            headers={"User-Agent": "Warble/1.0 (bird identification app for children)"},
            timeout=6,
        )
        response.raise_for_status()
        addr = response.json().get("address", {})
        # Nominatim uses different keys depending on how built-up the area is
        town = (addr.get("town") or addr.get("city") or addr.get("village")
                or addr.get("suburb") or addr.get("hamlet") or addr.get("county"))
        country = addr.get("country")
        if town and country:
            return {"name": f"{town}, {country}", "source": "gps"}
        if town or country:
            return {"name": town or country, "source": "gps"}
    except Exception as e:
        print(f"Warning: reverse geocode failed for {lat},{lng}: {e}")

    return {"name": None, "source": None}


@app.post("/trophies/wingman")
def award_wingman():
    """Awarded when a bird is shared from the app. Called by the share button
    rather than inferred, since there's no reliable way to detect that a share
    actually completed."""
    newly = []
    if award_trophy("wingman"):
        newly.append({"key": "wingman", **TROPHY_DEFINITIONS["wingman"]})
    return {"newly_earned_trophies": newly}


def evaluate_week_challenges():
    """This week's five challenges with their live progress. Returns a list of
    (challenge, is_complete, progress) so callers can award or display."""
    stats = get_week_stats()
    out = []
    for ch in get_week_challenges():
        progress = ch["progress"](stats)
        out.append((ch, progress >= ch["target"], progress))
    return out


@app.get("/weekly-challenges")
def weekly_challenges():
    """This week's challenges and progress, for the Home lozenge."""
    items = []
    for ch, done, progress in evaluate_week_challenges():
        items.append({
            "id": ch["id"], "text": ch["text"], "target": ch["target"],
            "feathers": ch["feathers"],
            "progress": min(progress, ch["target"]), "complete": done,
        })
    return {
        "challenges": items,
        "completed": sum(1 for i in items if i["complete"]),
        "all_bonus": ALL_COMPLETE_BONUS,
    }


@app.get("/habitats")
def list_habitats():
    """The six habitat sets with progress, for the Habitats screen. Unfound
    species are returned as names so the client can render silhouettes and
    keep the collection's shape visible, without revealing what they are."""
    found = set()
    for s in get_all_sightings():
        found.add(s["common_name"])
    sets = []
    for habitat, species in CURATED_SPECIES.items():
        got = [s for s in species if s in found]
        sets.append({
            "name": habitat,
            "total": len(species),
            "found_count": len(got),
            "found": got,
            "complete": len(got) >= len(species),
        })
    return {"habitats": sets, "set_bonus": HABITAT_SET_BONUS}


@app.get("/detection-stats")
def detection_stats():
    """Headline warbling stats for the Profile page."""
    return get_detection_stats()


@app.get("/locations")
def list_locations():
    """Every named location, for viewing/editing on the Profile page."""
    return {"locations": get_all_locations()}


@app.post("/locations/{location_id}/delete")
async def delete_location_endpoint(location_id: int):
    delete_location(location_id)
    return {"status": "ok"}


@app.post("/locations/{location_id}/rename")
async def rename_location_endpoint(location_id: int, name: str = Form(...)):
    rename_location(location_id, name)
    return {"status": "ok"}


@app.get("/profile")
def profile():
    return get_profile()


@app.post("/profile")
async def update_profile_endpoint(
    first_name: str = Form(None),
    last_name: str = Form(None),
    avatar_body: str = Form(None),
    avatar_face: str = Form(None),
    avatar_beak: str = Form(None),
    show_scientific_names: bool = Form(None),
    avatar_photo: str = Form(None),
):
    update_profile(
        first_name=first_name, last_name=last_name,
        avatar_body=avatar_body, avatar_face=avatar_face, avatar_beak=avatar_beak,
        show_scientific_names=show_scientific_names, avatar_photo=avatar_photo,
    )
    return {"status": "ok"}


@app.get("/trophies")
def list_trophies():
    """Every trophy, each marked earned or not. Unearned ones are still
    returned in full - the Trophies page now shows what they require."""
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


@app.get("/curated-progress")
def curated_progress():
    """How many of the 100 curated species have been found — the
    Collection's completion tracker towards the Century trophy.
    Detection itself is never restricted to this list; this is purely
    a progress readout."""
    return {
        "found": count_curated_species_found(ALL_CURATED_SPECIES),
        "total": len(ALL_CURATED_SPECIES),
    }


@app.get("/feathers")
def feathers_total():
    """The current running feather total."""
    return {"total_feathers": get_total_feathers()}


@app.get("/dev/set-feathers/{amount}")
def dev_set_feathers(amount: float):
    """Dev convenience - set the feather total directly by visiting
    this URL. Not part of normal gameplay, no auth, just a quick
    testing tool for now."""
    new_total = set_total_feathers(amount)
    return {"status": "ok", "total_feathers": new_total}


@app.get("/joke-of-the-day")
def joke_of_the_day():
    """Today's joke, only revealed once at least one session has
    happened today - otherwise unlocked stays false and setup/punchline
    are both null."""
    unlocked = has_session_today()
    joke = get_joke_of_the_day() if unlocked else {"setup": None, "punchline": None}
    return {
        "unlocked": unlocked,
        "setup": joke["setup"],
        "punchline": joke["punchline"],
    }


@app.get("/accessories")
def list_accessories():
    """The whole Dress Up catalog, each marked owned or not, plus the
    5 categories (with their icons) in display order."""
    owned = get_owned_accessory_ids()
    return {
        "accessories": [
            {"id": aid, "owned": aid in owned, **info}
            for aid, info in ACCESSORIES.items()
        ],
        "categories": CATEGORIES,
    }


@app.post("/accessories/{accessory_id}/purchase")
async def purchase_accessory_endpoint(accessory_id: str):
    if accessory_id not in ACCESSORIES:
        return JSONResponse(status_code=404, content={"status": "error", "message": "Unknown accessory."})
    item = ACCESSORIES[accessory_id]
    success = purchase_accessory(accessory_id, item["cost"], item["category"])
    return {"status": "ok" if success else "failed", "new_total": get_total_feathers()}


@app.post("/accessories/equip")
async def equip_accessory_endpoint(category: str = Form(...), accessory_id: str = Form(None)):
    """accessory_id can be omitted/blank to clear that category's slot."""
    set_equipped_item(category, accessory_id if accessory_id else None)
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
