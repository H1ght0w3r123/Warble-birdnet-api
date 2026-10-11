import os
import tempfile
import threading
import json
import datetime
from pathlib import Path

import requests
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse, Response
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
        check_species_names(analyzer.labels)
    except Exception as e:
        analyzer_error = str(e)
        print(f"Failed to load BirdNET analyzer: {e}")


# Warble's names for its birds that BirdNET doesn't use - each one is a
# bird that can never be found. Should always be empty; /status shows it.
unknown_species_names = []


def check_species_names(labels):
    """BirdNET labels are "Scientific name_Common name". Every name the
    app matches detections against has to be one of them, exactly."""
    global unknown_species_names
    from curated_species import ALL_CURATED_SPECIES
    known = {l.split("_", 1)[1] for l in labels if "_" in l}
    unknown_species_names = sorted(ALL_CURATED_SPECIES - known)
    if unknown_species_names:
        print("WARNING: BirdNET never says these names, so these birds can never "
              f"be found: {', '.join(unknown_species_names)}")


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
        "unknown_species_names": unknown_species_names,
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
        if not is_locally_plausible(d["scientific_name"], lat, lng):
            continue
        # Rarity is a fixed property of the species now, straight from the
        # curated list - no NBN lookup, no per-location variation. A Hawfinch
        # is rare wherever you hear it.
        # is_new mirrors the exact check used when a session is actually
        # saved (has_existing_sighting with no tier arg) - nothing is written
        # to the database from this endpoint, so this stays accurate for
        # every chunk of the same recording: a species only stops being "new"
        # once an earlier chunk of a DIFFERENT, already-saved session found it.
        filtered_detections.append({
            **d,
            "tier": rarity_of(d["common_name"]),
            "is_new": not has_existing_sighting(d["common_name"]),
            "pack_color": pack_color_for_species(d["common_name"]),
        })

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
    init_db, has_existing_sighting, save_sighting, get_trophy_levels,
    count_pre_sunrise_sessions, count_rainy_sessions, best_pre_sunrise_session,
    count_species_found_far_apart, count_species_first_heard_since, get_bird_sessions,
    get_share_count, increment_share_count, count_all_sessions,
    reset_dress_up, reset_feathers, reset_sightings, reset_everything,
    delete_species, export_everything,
    add_feathers, get_all_sightings, get_total_feathers,
    record_session, count_distinct_locations,
    get_earned_trophy_keys, award_trophy,
    get_location_name, save_location_name, get_nearby_places,
    get_cached_call_url, get_profile, update_profile,
    get_all_locations, rename_location, delete_location, get_detection_stats,
    set_session_bird_count, count_successful_sessions_this_week,
    count_empty_sessions, award_bonus_once, get_week_stats, count_completed_weeks,
    record_song_game_play,
    count_owned_accessories, distinct_seasons_warbled, max_consecutive_warble_days,
    has_species_found_far_apart, count_species_found_in,
    max_sessions_at_one_location, count_rare_sightings, count_distinct_species,
    has_session_today,
    get_owned_accessory_ids, purchase_accessory, set_equipped_item,
    count_curated_species_found, get_found_curated_species, save_call_url,
    get_bird_photo_data, get_song_game_stars, record_song_game_result,
    set_total_feathers, get_seen_marks, set_seen_mark, reset_tutorials, get_heard_species,
    add_bird_photo, get_bird_photos, delete_bird_photo,
)
from birds import (bird_data, STAT_LABELS, HABITAT_ICONS,
                   season_state, is_seasonal, SEASONAL_ORDER)
from trophies import (TROPHY_DEFINITIONS, is_before_sunrise, is_after_dark, requirement_text,
                      birder_rank)
from jokes import get_joke_of_the_day
from accessories import ACCESSORIES, CATEGORIES
from curated_species import (
    ALL_CURATED_SPECIES, PACKS, SPECIES_RARITY, TIERS,
    rarity_of, pack_for_species, pack_color_for_species,
)
from unfound_hints import UNFOUND_HINTS
from challenges import get_week_challenges, current_week_key, ALL_COMPLETE_BONUS, CHALLENGES_BY_ID
from migration_data import get_migration_info

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


def pack_species(key: str) -> set:
    p = PACKS[key]
    return set(p["common"] + p["rare"])


def count_birds_after_dark() -> int:
    """Night Owl: every bird heard in a warble after dusk or before dawn,
    worked out from where and when each warble was - so warbles from
    before this measure existed count too."""
    return sum(birds for lat, lng, when, birds in get_bird_sessions()
               if lat is not None and lng is not None and is_after_dark(lat, lng, when))


def measure_all_trophies():
    """Current value of every trophy's measure, in one place.

    Replaces the old pile of separate if-statements: each trophy is now a
    number compared against its own thresholds, which is what lets levels work
    without inventing a new check per level.
    """
    return {
        "fledgling":     count_all_sessions(),
        "early_bird":    count_pre_sunrise_sessions(),
        "nomad":         count_distinct_locations(),
        "rooster":       max_sessions_at_one_location(),
        "golden_eagle":  count_rare_sightings(),
        "dawn_chorus":   best_pre_sunrise_session(),
        "forager":       count_distinct_species(),
        "night_owl":     count_birds_after_dark(),
        "century":       count_curated_species_found(ALL_CURATED_SPECIES),
        "globetrotter":  sum(1 for p in pack_progress() if p["complete"]),
        "empty_nester":  count_empty_sessions(),
        "preener":       count_owned_accessories(),
        "evergreen":     distinct_seasons_warbled(),
        "tailwind":      max_consecutive_warble_days(),
        "migrator":      count_species_found_far_apart(5.0),
        # Repointed from the old habitat groups to the packs that replaced them
        "skylark":       count_species_found_in(pack_species("ground_feeders")),
        "high_flyer":    count_species_found_in(pack_species("hunters")),
        "still_water":   count_species_found_in(pack_species("water_birds")),
        "brooder":       count_rainy_sessions(),
        "wingman":       get_share_count(),
        "high_five":     count_completed_weeks(),
    }


# Trophies whose measure can only go so far - every bird on the list, every
# pack, every bird in a pack, every item in the shop. None may ask for more
# than exists, or its top level could never be won; Preener must ask for
# less than the whole shop. Checked when the server starts, so a pack or a
# shop change that breaks one fails loudly instead of quietly.
TROPHY_CEILINGS = {
    "century": len(ALL_CURATED_SPECIES),
    "globetrotter": len(PACKS),
    "skylark": len(pack_species("ground_feeders")),
    "high_flyer": len(pack_species("hunters")),
    "still_water": len(pack_species("water_birds")),
    "preener": len(ACCESSORIES) - 1,
}
for _key, _most in TROPHY_CEILINGS.items():
    assert TROPHY_DEFINITIONS[_key]["levels"][-1] <= _most, \
        f"{_key} asks for {TROPHY_DEFINITIONS[_key]['levels'][-1]}, only {_most} possible"


def check_all_trophies():
    """Awards every trophy level now qualified for. Returns the newly earned
    ones, each tagged with which level it was.

    Levels are checked from the top down and every unearned level below the
    one reached is awarded too - so a big jump can't leave gaps, and an
    existing player who already passed level 1 still collects it."""
    measures = measure_all_trophies()
    newly = []
    for key, value in measures.items():
        thresholds = TROPHY_DEFINITIONS[key]["levels"]
        for i, threshold in enumerate(thresholds):
            if value >= threshold and award_trophy(key, i + 1):
                newly.append({
                    "key": key,
                    "level": i + 1,
                    "level_count": len(thresholds),
                    "name": TROPHY_DEFINITIONS[key]["name"],
                    "emoji": TROPHY_DEFINITIONS[key]["emoji"],
                    "citation": TROPHY_DEFINITIONS[key]["citations"][i],
                    "description": TROPHY_DEFINITIONS[key]["description"],
                })
    return newly


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


def is_locally_plausible(scientific_name: str, lat: float, lng: float) -> bool:
    """Whether NBN Atlas has records of this species within 5km - close to
    'could this realistically be heard from here'. A wider radius lets in
    real UK species (a farmland specialist like Yellowhammer, say) that
    would never actually turn up at this recording spot."""
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


# Reward tuning - the whole ladder, so it can be read in one place:
#   1  a bird heard again (once per bird per day), or one outside the 100
#   3  a new bird (a rare one heard again: 3, once a day)
#   5  a trophy level, or a new star in Guess the Song
#  15  a new rare bird
#  25  a pack completed, or all five weekly challenges
# No per-session bonus. Turning up used to pay 10 feathers regardless of
# what was heard, which made the birds themselves feel incidental. The
# weekly challenges are the reason to come back instead.
PACK_BONUS = 25
# Every trophy level won pays this, on top of the trophy itself. Levels won
# before it was introduced were never back-paid.
TROPHY_LEVEL_FEATHERS = 5
# Guess the Song: each star won on a level for the first time - so a level
# is worth up to 15, and getting better pays, not just being perfect. Stars
# held before this was introduced were never back-paid.
SONG_GAME_STAR_FEATHERS = 5


def total_leaves() -> int:
    """Every trophy level held - the leaves on all the cups together."""
    return sum(lvl for key, lvl in get_trophy_levels().items() if key in TROPHY_DEFINITIONS)


def rank_up_between(before: int, after: int):
    """The new rank if `after` leaves crosses into one `before` didn't have."""
    a, b = birder_rank(before), birder_rank(after)
    return b if b["index"] > a["index"] else None


def award_trophy_levels():
    """Checks every trophy and pays TROPHY_LEVEL_FEATHERS for each level just
    won. For anything other than a recording, which folds the same pay into
    its own total and bonus list. Returns (newly_won, feathers, rank_up)."""
    before = total_leaves()
    newly = check_all_trophies()
    for t in newly:
        t["feathers"] = TROPHY_LEVEL_FEATHERS
    feathers = TROPHY_LEVEL_FEATHERS * len(newly)
    if feathers:
        add_feathers(feathers)
    return newly, feathers, rank_up_between(before, before + len(newly))


# --- Avatar birds ------------------------------------------------------------
# Four birds to start, four to find. The four that live in the UK unlock the
# first time the child hears the real thing, so each one is a souvenir of a
# find. The bird a family was already using when this arrived stays theirs
# ("avatar:kept", recorded once), whether or not they've heard it.
AVATAR_STARTERS = {"classic", "default", "cardinal", "parrot", "penguin"}
AVATAR_UNLOCKS = {
    "duckling":   {"hint": "Hear a duck, goose or swan to unlock",
                   "species": {"Mallard", "Canada Goose", "Graylag Goose", "Mute Swan", "Common Eider"}},
    "woodpecker": {"hint": "Hear a woodpecker to unlock",
                   "species": {"Great Spotted Woodpecker", "Eurasian Green Woodpecker",
                               "Lesser Spotted Woodpecker"}},
    "owl":        {"hint": "Hear an owl to unlock",
                   "species": {"Tawny Owl", "Barn Owl", "Little Owl", "Long-eared Owl"}},
    "kingfisher": {"hint": "Hear a Kingfisher to unlock", "species": {"Common Kingfisher"}},
}
for _rule in AVATAR_UNLOCKS.values():
    assert _rule["species"] <= ALL_CURATED_SPECIES, _rule["species"] - ALL_CURATED_SPECIES


def avatar_states(heard: set = None) -> dict:
    """Each lockable bird: unlocked or not, what unlocks it, and (once heard)
    which bird did. Starters aren't listed - they're always open."""
    heard = get_heard_species() if heard is None else heard
    kept = get_seen_marks().get("avatar:kept")
    if kept is None:
        kept = get_profile().get("avatar_species") or ""
        set_seen_mark("avatar:kept", kept)
    out = {}
    for sp, rule in AVATAR_UNLOCKS.items():
        by = sorted(rule["species"] & heard)
        out[sp] = {"unlocked": bool(by) or sp == kept, "hint": rule["hint"],
                   "heard": by[0] if by else None}
    return out


# --- Feather colours ---------------------------------------------------------
# Nine everyday colours are free; the nine bolder ones cost feathers - so
# there is always something left to spend on, alongside the shop. Bought
# colours are kept with the Dress Up items as "colour:#HEX" (they don't count
# towards Preener). The colour a family was already using stays theirs
# ("colour:kept").
FREE_COLOURS = {"#9CAF88", "#FFFFFF", "#000000", "#8B5A2B", "#F91E27",
                "#F96A1C", "#F2C94C", "#0197B8", "#E87EA1"}
SPECIAL_COLOURS = {"#6DAA44", "#B5D334", "#2E8B57", "#3CC8C0", "#2F5FD0",
                   "#1F2A6B", "#B9A6E0", "#7B3FB5", "#D0309A"}
SPECIAL_COLOUR_COST = 10


def colour_states(owned: set = None) -> dict:
    owned = get_owned_accessory_ids() if owned is None else owned
    kept = get_seen_marks().get("colour:kept")
    if kept is None:
        kept = (get_profile().get("avatar_body") or "").upper()
        set_seen_mark("colour:kept", kept)
    return {hx: {"cost": SPECIAL_COLOUR_COST, "owned": f"colour:{hx}" in owned or hx == kept}
            for hx in SPECIAL_COLOURS}


def colour_is_open(hx: str) -> bool:
    hx = (hx or "").upper()
    return hx not in SPECIAL_COLOURS or colour_states()[hx]["owned"]


def avatar_is_open(species: str, states: dict = None) -> bool:
    if species in AVATAR_STARTERS or species not in AVATAR_UNLOCKS:
        return True
    return (states or avatar_states())[species]["unlocked"]


def calculate_feathers(tier: str, is_duplicate: bool) -> float:
    """Small numbers on purpose - an eight-year-old can hold "15 feathers for
    a rare bird" in their head in a way they can't hold 50. A bird heard
    again only pays the first time that day - see analyze_session.

    Only Warble's 100 carry a tier. A bird outside the collection pays a
    token amount: still worth hearing, but it isn't going in a pack."""
    if tier is None:
        return 1
    values = {
        ("Common", False): 3, ("Rare", False): 15,
        ("Common", True): 1, ("Rare", True): 3,
    }
    return values.get((tier, is_duplicate), 1)


@app.post("/analyze-session")
async def analyze_session(
    lat: float = Form(51.5074),
    lng: float = Form(-0.1278),
    live_detections: str = Form("[]"),
    duration_s: int = Form(None),
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

    # Conditions are recorded on the session itself so the level counters can
    # be derived later, rather than only being known at this moment.
    # Which of the week's challenges were already done, so the ones this
    # recording finishes can each have their moment.
    challenges_before = challenges_done_now()
    before_sunrise = is_before_sunrise(lat, lng, now)
    raining = is_raining(lat, lng)
    _, session_id = record_session(lat, lng, before_sunrise=before_sunrise, was_raining=raining,
                                   duration_s=duration_s)

    existing_location_name = get_location_name(lat, lng)
    needs_location_name = existing_location_name is None
    # A spot we don't know yet may still be part of a place the child has
    # already named - the far side of the same field. Offer those, nearest
    # first, so they can add this spot to one instead of inventing a new name.
    nearby_places = get_nearby_places(lat, lng) if needs_location_name else []

    avatars_before = avatar_states()   # to spot a bird that becomes an avatar
    for detection in detections:
        common_name = detection["common_name"]
        scientific_name = detection["scientific_name"]
        confidence = detection["confidence"]

        # No plausibility check here any more - /identify already ran
        # is_locally_plausible on everything during recording, so a second
        # pass would only reject birds the user already watched a badge
        # appear for, recreating exactly the disappearing-detection problem
        # this restructure removes.
        # Rarity is fixed per species from the curated list. Birds outside
        # the 100 can still be detected and saved, they just carry no rarity.
        tier = rarity_of(common_name)
        is_collector = tier is not None

        # One card per species now - rarity no longer varies by place, so
        # there's nothing to re-collect.
        is_duplicate = has_existing_sighting(common_name)
        # A bird pays once a day at most: new, or the first time it's heard
        # again that day. Otherwise a garden with five regulars pays five
        # feathers every time record is tapped, however often that is.
        first_today = award_bonus_once(f"heard:{now.date().isoformat()}:{common_name}")
        feathers = calculate_feathers(tier, is_duplicate) if (first_today or not is_duplicate) else 0
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
            "is_collector": is_collector,
            "pack": pack_for_species(common_name),
            "pack_name": PACKS[pack_for_species(common_name)]["name"] if pack_for_species(common_name) else None,
            "season": season_state(common_name, now.month) if is_seasonal(common_name) else None,
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

    # Bird count has to be stored before trophies are measured - several of
    # them count sessions that found something.
    set_session_bird_count(session_id, len(results))
    # Birds that became avatars with this recording
    avatars_after = avatar_states()
    new_avatars = [sp for sp, st in avatars_after.items()
                   if st["unlocked"] and not avatars_before[sp]["unlocked"]]

    session_feathers = sum(r["feathers"] for r in results)
    bonuses = []
    packs_completed = []

    # The weekly challenges: each one this recording finished, and the
    # week's prize if that was the last of the five.
    challenges_done, week_bonus = award_week_challenges(challenges_before)
    if week_bonus:
        session_feathers += week_bonus
        bonuses.append({"label": "All 5 challenges done!", "feathers": week_bonus})

    if results:
        # Completing a pack is a real milestone worth paying for
        for key, pack in PACKS.items():
            if count_species_found_in(pack_species(key)) >= 10:
                if award_bonus_once(f"pack:{key}"):
                    session_feathers += PACK_BONUS
                    bonuses.append({"label": f"{pack['name']} complete!", "feathers": PACK_BONUS})
                    packs_completed.append({"key": key, "name": pack["name"], "art": pack["art"],
                                            "feathers": PACK_BONUS})

    # Trophies last, after the week and the packs have paid out - High Five
    # and Globetrotter count those. Outside the "found something" check: a
    # quiet session can win a trophy level too (Empty Nester).
    leaves_before = total_leaves()
    newly_earned_trophies = check_all_trophies()
    rank_up = rank_up_between(leaves_before, leaves_before + len(newly_earned_trophies))
    for t in newly_earned_trophies:
        t["feathers"] = TROPHY_LEVEL_FEATHERS
        session_feathers += TROPHY_LEVEL_FEATHERS
        bonuses.append({"label": f"{t['name']} level {t['level']}", "feathers": TROPHY_LEVEL_FEATHERS})

    new_total = add_feathers(session_feathers)

    return {
        "detections": results,
        "total_feathers_this_session": session_feathers,
        "bonuses": bonuses,
        # The same payouts, itemised for the celebrations on the Done screen
        "packs_completed": packs_completed,
        "challenges_done": challenges_done,
        "week_bonus": week_bonus,
        "total_feathers": new_total,
        "newly_earned_trophies": newly_earned_trophies,
        "rank_up": rank_up,
        "new_avatars": [{"id": sp, "heard": avatars_after[sp]["heard"]} for sp in new_avatars],
        "needs_location_name": needs_location_name,
        "nearby_places": nearby_places,
        "location_name": existing_location_name,
        "lat": lat,
        "lng": lng,
    }


@app.post("/name-location")
async def name_location(lat: float = Form(...), lng: float = Form(...), name: str = Form(...)):
    """Puts the spot (lat, lng) rounds to into the place called `name`:
    an existing place of that name (ignoring case) gains this spot, or a new
    place is started."""
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
def award_wingman(common_name: str = Form("")):
    """Awarded when a bird is shared from the app. Called by the share button
    rather than inferred, since there's no reliable way to detect that a share
    actually completed. Each bird counts once a day, so tapping share (or
    the copy-to-clipboard fallback) over and over doesn't win Wingman."""
    today = datetime.datetime.utcnow().date().isoformat()
    if award_bonus_once(f"share:{today}:{common_name or '?'}"):
        increment_share_count()
    newly, feathers, rank_up = award_trophy_levels()
    return {"newly_earned_trophies": newly, "feathers": feathers,
            "total_feathers": get_total_feathers(), "rank_up": rank_up}


def week_challenges():
    """This week's five for this child: picked once, then kept for the rest
    of the week in a seen mark, so they never change part-way through."""
    week = current_week_key()
    key = f"challenges:{week}"
    stored = get_seen_marks().get(key)
    if stored:
        picked = [CHALLENGES_BY_ID[i] for i in stored.split(",") if i in CHALLENGES_BY_ID]
        if len(picked) == 5:
            return picked
    # Playable, not just open: a level with no songs for any of the child's
    # birds can't be played, and a star in it can't be won.
    birds = get_found_curated_species(ALL_CURATED_SPECIES)
    can_play = (any(b["call_url"] for b in birds)
                and any(l["unlocked"] for l in song_game_levels(len(birds))))
    picked = get_week_challenges(can_play_game=can_play, finding_new_birds=still_finding_new_birds())
    set_seen_mark(key, ",".join(c["id"] for c in picked))
    return picked


# "Hear a new bird" is offered while new birds are still turning up most
# weeks: early on (fewer than this many species heard), or at least
# NEW_BIRD_RECENT_MIN new ones in the last four weeks.
NEW_BIRD_EARLY_SPECIES = 30
NEW_BIRD_RECENT_DAYS = 28
# Three, not one: measured with tools/economy_sim.py, a child still finding
# the odd straggler every few weeks failed it most weeks it was offered.
NEW_BIRD_RECENT_MIN = 3


def still_finding_new_birds() -> bool:
    if count_distinct_species() < NEW_BIRD_EARLY_SPECIES:
        return True
    since = datetime.datetime.utcnow() - datetime.timedelta(days=NEW_BIRD_RECENT_DAYS)
    return count_species_first_heard_since(since) >= NEW_BIRD_RECENT_MIN


def challenges_done_now() -> set:
    """The ids of this week's challenges that are already done."""
    return {c["id"] for c, done, _ in evaluate_week_challenges() if done}


def award_week_challenges(done_before: set):
    """After anything that can finish a challenge (a recording, a game):
    the challenges it finished, as {id, text, done, of}, and the week's
    prize - ALL_COMPLETE_BONUS, banked here - if the last of the five fell.
    A challenge on its own pays nothing; it gets its moment all the same."""
    week = evaluate_week_challenges()
    done_count = sum(1 for _, done, _ in week if done)
    newly = [{"id": c["id"], "text": c["text"], "done": done_count, "of": len(week)}
             for c, done, _ in week if done and c["id"] not in done_before]
    paid = 0
    if week and done_count == len(week):
        if award_bonus_once(f"challenge:{current_week_key()}:ALL"):
            paid = ALL_COMPLETE_BONUS
    return newly, paid


def evaluate_week_challenges():
    """This week's five challenges with their live progress. Returns a list of
    (challenge, is_complete, progress) so callers can award or display."""
    stats = get_week_stats()
    out = []
    for ch in week_challenges():
        progress = ch["progress"](stats)
        out.append((ch, progress >= ch["target"], progress))
    return out


@app.get("/weekly-challenges")
def weekly_challenges():
    """This week's challenges and progress. all_bonus is the week's only
    reward - feathers for finishing all of them."""
    items = []
    for ch, done, progress in evaluate_week_challenges():
        items.append({
            "id": ch["id"], "text": ch["text"], "target": ch["target"],
            "progress": min(progress, ch["target"]), "complete": done,
        })
    return {
        "challenges": items,
        "completed": sum(1 for i in items if i["complete"]),
        "all_bonus": ALL_COMPLETE_BONUS,
    }


@app.post("/species/{common_name}/delete")
async def delete_species_endpoint(common_name: str):
    """Removes one species from the collection - for misidentifications."""
    removed = delete_species(common_name)
    print(f"Deleted species '{common_name}' ({removed} sighting(s))")
    return {"status": "ok", "removed": removed}


@app.post("/species/{common_name}/photos")
async def add_bird_photo_endpoint(common_name: str, photo: str = Form(...)):
    """Attaches a self-taken photo to a species. The client has already
    shrunk/re-encoded it (same pattern as the avatar photo upload)."""
    photo_id = add_bird_photo(common_name, photo)
    return {"status": "ok", "id": photo_id}


@app.get("/species/{common_name}/photos")
def get_bird_photos_endpoint(common_name: str):
    return {"photos": get_bird_photos(common_name)}


@app.post("/bird-photos/{photo_id}/delete")
async def delete_bird_photo_endpoint(photo_id: int):
    removed = delete_bird_photo(photo_id)
    return {"status": "ok", "removed": removed}


@app.get("/export")
def export_data():
    """Full snapshot of everything, so a reset isn't irreversible."""
    return export_everything()


@app.post("/reset/{scope}")
async def reset_data(scope: str):
    """Destructive resets, kept behind explicit named scopes so a mis-typed
    call can't wipe more than intended."""
    actions = {
        "dressup": reset_dress_up,
        "tutorials": reset_tutorials,
        "feathers": reset_feathers,
        "sightings": reset_sightings,
        "everything": reset_everything,
    }
    if scope not in actions:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Unknown reset scope."})
    actions[scope]()
    print(f"RESET performed: {scope}")
    return {"status": "ok", "scope": scope}


EMPTY_PACK_MESSAGE = "Hear any of these birds to start this pack!"


def pack_progress():
    """Per-pack progress: which of the 10 birds are found, split into the 8
    common and 2 rare, and whether the pack is complete."""
    photos = {}
    # get_all_sightings() comes back newest first, so the last row seen for a
    # species is its oldest one - the find that counts as "first found".
    history = {}
    for s in get_all_sightings():
        name = s["common_name"]
        photos.setdefault(name, s.get("image_url"))
        entry = history.setdefault(name, {"count": 0})
        entry["count"] += 1
        entry["first_found"] = s["created_at"]
        entry["first_location"] = s.get("location_name")
    packs = []
    for key, pack in PACKS.items():
        birds = []
        for name in pack["common"] + pack["rare"]:
            got = name in photos
            st = season_state(name, datetime.datetime.utcnow().month)
            seen = history.get(name, {})
            birds.append({
                "common_name": name,
                "rarity": SPECIES_RARITY[name],
                "found": got,
                "season_state": st["state"],
                "season_label": st["label"],
                # Names of unfound birds are still sent - a pack is a known
                # checklist you work through, unlike the old habitat sets
                # where the unfound ones were kept secret.
                "photo_url": photos.get(name) if got else None,
                # Drives the hover caption under the fan. first_location is
                # None whenever the child skipped naming that spot, or the
                # recording had no coordinates at all.
                "found_count": seen.get("count", 0),
                "first_found": seen.get("first_found"),
                "first_location": seen.get("first_location"),
                # Only the unfound birds carry a hint - sending all 100 on
                # every load would be ~18KB of text nothing reads.
                "hint": None if got else UNFOUND_HINTS.get(name),
            })
        got = sum(1 for b in birds if b["found"])
        packs.append({
            "key": key, "name": pack["name"], "blurb": pack["blurb"],
            "emoji": pack["emoji"], "art": pack["art"],
            "color": pack["color"], "birds": birds,
            "cards_found": got, "cards_total": len(birds),
            "complete": got == len(birds),
            # An empty pack says how to start it, rather than leaving a
            # child looking at ten blank cards and a 0.
            "message": None if got else EMPTY_PACK_MESSAGE,
        })
    return packs


@app.get("/whats-here")
def whats_here():
    """Seasonal birds and where they are in their year. Drives the Home tile
    and the 'back in April' labels, so a child knows an empty slot in a pack
    is the calendar's doing rather than theirs."""
    month = datetime.datetime.utcnow().month
    found = {s["common_name"] for s in get_all_sightings()}
    birds = []
    for name in SEASONAL_ORDER:
        st = season_state(name, month)
        birds.append({
            "common_name": name, "found": name in found,
            "state": st["state"], "label": st["label"],
            "pack": pack_for_species(name),
        })
    here = [b for b in birds if b["state"] in ("here", "leaving")]
    return {
        "birds": birds,
        "here_count": len(here),
        "leaving_count": sum(1 for b in birds if b["state"] == "leaving"),
        "to_find": sum(1 for b in here if not b["found"]),
    }


@app.get("/migration/{common_name}")
def migration_info(common_name: str):
    """Where a seasonal species spends the other half of its year, for the
    Migrator card - reachable from the What's Here list or a button on the
    bird's own detail card. Returns null for anything non-migratory rather
    than a 404, since the frontend already knows via bird.is_migratory
    whether to expect data here."""
    return {"migration": get_migration_info(common_name)}


@app.get("/collector-packs")
def list_collector_packs():
    """The three collector packs with progress, for the Collections screen."""
    return {"packs": pack_progress(), "tiers": TIERS}


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
    return {**get_profile(), "avatars": avatar_states(), "colours": colour_states(),
            "rank": birder_rank(total_leaves())}


@app.post("/profile")
async def update_profile_endpoint(
    first_name: str = Form(None),
    last_name: str = Form(None),
    avatar_body: str = Form(None),
    avatar_face: str = Form(None),
    avatar_beak: str = Form(None),
    avatar_species: str = Form(None),
    show_scientific_names: bool = Form(None),
    avatar_photo: str = Form(None),
    home_scene: str = Form(None),
):
    # A bird still to be found can't be chosen, whatever the page sends.
    if avatar_species and not avatar_is_open(avatar_species):
        avatar_species = None
    if avatar_body and not colour_is_open(avatar_body):
        avatar_body = None
    update_profile(
        first_name=first_name, last_name=last_name,
        avatar_body=avatar_body, avatar_face=avatar_face, avatar_beak=avatar_beak,
        avatar_species=avatar_species,
        show_scientific_names=show_scientific_names, avatar_photo=avatar_photo,
        home_scene=home_scene,
    )
    return {"status": "ok"}


@app.get("/trophies")
def list_trophies():
    """Every trophy with the level reached, its next target, and progress
    towards it. Unearned trophies still return their first requirement - the
    Trophies page shows what everything needs."""
    levels = get_trophy_levels()
    measures = measure_all_trophies()
    out = []
    for key, t in TROPHY_DEFINITIONS.items():
        level = levels.get(key, 0)
        value = measures.get(key, 0)
        maxed = level >= len(t["levels"])
        next_i = min(level, len(t["levels"]) - 1)
        out.append({
            "key": key,
            "name": t["name"],
            "emoji": t["emoji"],
            "description": t["description"],
            "earned": level > 0,
            "level": level,
            "level_count": len(t["levels"]),
            "maxed": maxed,
            "progress": value,
            "next_target": None if maxed else t["levels"][next_i],
            "requirement": requirement_text(key, next_i),
            "citation": t["citations"][level - 1] if level > 0 else None,
        })
    leaves = sum(t["level"] for t in out)
    return {"trophies": out, "rank": birder_rank(leaves)}


@app.get("/sightings")
def list_sightings():
    """Every bird ever found, newest first — for a Collection screen.
    Each one carries its full bird record - stat tiles, Top Trumps ratings and,
    where the species has been researched, conservation status too."""
    sightings = get_all_sightings()
    for s in sightings:
        s["bird"] = bird_data(s["common_name"])
    return {"sightings": sightings, "stat_labels": STAT_LABELS}


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


# Guess the Song: hear a song, pick the bird from 2-6 of your own finds.
# (level, choices per round, distinct curated species needed to unlock it)
# A level also needs at least one star on the level before it.
SONG_GAME_LEVELS = [(1, 2, 10), (2, 3, 15), (3, 4, 20), (4, 5, 25), (5, 6, 30)]
SONG_GAME_ROUNDS = 8


def song_game_stars_for(correct: int) -> int:
    """8 of 8 is three stars, 7 is two, 6 is one, anything less none."""
    return max(0, 3 - (SONG_GAME_ROUNDS - correct))


def birds_to_go(n: int) -> str:
    return f"Hear {n} more bird{'' if n == 1 else 's'}"


def song_game_level_message(level: int, to_go: int, needs_star: bool):
    """What a locked level is waiting for, in words; None once it's open."""
    star = f"Win a star on Level {level - 1}"
    if needs_star and to_go:
        return f"{star} and {birds_to_go(to_go).lower()}"
    if needs_star:
        return f"{star} first"
    if to_go:
        return birds_to_go(to_go)
    return None


def song_game_levels(found: int) -> list:
    """Each level with whether it's open, and if not, what's missing: more
    birds heard (to_go), a star on the level before (needs_star), or both -
    and the same again as a short message."""
    stars = get_song_game_stars()
    out = []
    for n, c, need in SONG_GAME_LEVELS:
        needs_star = n > 1 and stars.get(n - 1, 0) < 1
        to_go = max(0, need - found)
        out.append({"level": n, "choices": c, "unlock_at": need,
                    "to_go": to_go, "needs_star": needs_star,
                    "unlocked": not to_go and not needs_star,
                    "stars": stars.get(n, 0),
                    "message": song_game_level_message(n, to_go, needs_star)})
    return out


def song_game_message(found: int, playable: int):
    """The game as a whole: why it can't be played yet, or None if it can."""
    first = SONG_GAME_LEVELS[0][2]
    if found < first:
        return f"{birds_to_go(first - found)} to unlock Guess the Song!"
    if not playable:
        return "Warble couldn't find songs for your birds yet. Try again later!"
    return None

# Birds xeno-canto had nothing for when asked during this run of the server,
# so a bird with no recording costs one lookup per deploy rather than one
# every time the game opens.
_no_recording = set()


@app.get("/song-game")
def song_game():
    """Everything the song game needs in one go: which levels are open, and
    every one of Warble's 100 the child has heard, with a picture and a song.

    The pool is always every bird heard so far, at every level - the levels
    differ only in how many choices are shown. A bird with no recording can
    still be a wrong answer (its picture is all that needs) but the game
    never asks about it."""
    birds = get_found_curated_species(ALL_CURATED_SPECIES)
    missing = [b for b in birds
               if not b["call_url"] and b["common_name"] not in _no_recording]
    if missing and XENO_CANTO_API_KEY:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=6) as pool:
            urls = list(pool.map(lambda b: get_bird_call_url(b["scientific_name"]), missing))
        for b, url in zip(missing, urls):
            if url:
                b["call_url"] = url
                save_call_url(b["common_name"], url)
            else:
                _no_recording.add(b["common_name"])
    found = len(birds)
    playable = sum(1 for b in birds if b["call_url"])
    return {
        "found": found,
        "rounds": SONG_GAME_ROUNDS,
        "message": song_game_message(found, playable),
        "levels": song_game_levels(found),
        "birds": [{"common_name": b["common_name"],
                   "image_url": (f"/bird-photos/{b['own_photo_id']}" if b["own_photo_id"]
                                 else b["image_url"]),
                   "own_photo": bool(b["own_photo_id"]),
                   "call_url": b["call_url"]} for b in birds],
    }


@app.post("/song-game/result")
async def song_game_result(level: int = Form(...), correct: int = Form(...)):
    """A finished level. Stars are worked out here rather than trusted from
    the app, and only a level that is actually open can earn them. Returns
    the stars for this go, the best so far, and the levels as they now
    stand - so the end screen can say a new level has opened."""
    found = count_curated_species_found(ALL_CURATED_SPECIES)
    levels = song_game_levels(found)
    this = next((l for l in levels if l["level"] == level), None)
    if this is None or not this["unlocked"]:
        return JSONResponse({"error": "level not open"}, status_code=400)
    challenges_before = challenges_done_now()
    correct = max(0, min(SONG_GAME_ROUNDS, correct))
    stars = song_game_stars_for(correct)
    before = get_song_game_stars().get(level, 0)
    best = record_song_game_result(level, correct, stars)
    record_song_game_play(level, correct, stars)
    # Only stars this level has never had before pay - replaying a level
    # you've already got two stars on pays nothing until you get the third.
    new_stars = max(0, best - before)
    feathers = SONG_GAME_STAR_FEATHERS * new_stars
    # A star can be the week's last challenge - its prize is paid here and
    # now, not at the next recording. Before the trophies: High Five counts it.
    challenges_done, week_bonus = award_week_challenges(challenges_before)
    if feathers + week_bonus:
        add_feathers(feathers + week_bonus)
    trophies, trophy_feathers, rank_up = award_trophy_levels()
    return {"stars": stars, "best_stars": best, "levels": song_game_levels(found),
            "new_stars": new_stars, "feathers": feathers,
            "challenges_done": challenges_done, "week_bonus": week_bonus,
            "newly_earned_trophies": trophies, "trophy_feathers": trophy_feathers,
            "rank_up": rank_up, "total_feathers": get_total_feathers()}


@app.get("/bird-photos/{photo_id}")
def bird_photo_image(photo_id: int):
    """A self-taken photo as an ordinary image, so it can sit in an <img>
    without sending every photo's data inside one big JSON reply."""
    import base64
    data = get_bird_photo_data(photo_id)
    if not data or "," not in data:
        return JSONResponse({"error": "not found"}, status_code=404)
    head, b64 = data.split(",", 1)
    media = head[5:].split(";")[0] if head.startswith("data:") else "image/jpeg"
    return Response(base64.b64decode(b64), media_type=media or "image/jpeg",
                    headers={"Cache-Control": "public, max-age=86400"})


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


# Any recording today opens it, bird or not - so this asks for a listen,
# not a find.
JOKE_LOCKED_MESSAGE = "Tap the mic and listen for birds to unlock today's joke!"


@app.get("/joke-of-the-day")
def joke_of_the_day():
    """Today's joke, only revealed once at least one session has
    happened today - otherwise unlocked stays false, setup/punchline
    are both null, and message says how to unlock it."""
    unlocked = has_session_today()
    joke = get_joke_of_the_day() if unlocked else {"setup": None, "punchline": None}
    return {
        "unlocked": unlocked,
        "message": None if unlocked else JOKE_LOCKED_MESSAGE,
        "setup": joke["setup"],
        "punchline": joke["punchline"],
    }


# --- What's new, and what's been explained ---------------------------------
# Each area the nav bar can light up, as the set of things in it right now.
# Visiting the area stores that set ("seen:<area>"); anything in the set
# since then is new, and lights the area up. Sets rather than counts, so a
# bird removed as a misidentification and another one found still reads as
# new, and a reset can't leave a stale high count that hides new finds.
def whats_new_items() -> dict:
    sightings = get_all_sightings()
    heard = {s["common_name"] for s in sightings}
    found_curated = len(heard & ALL_CURATED_SPECIES)
    feathers = get_total_feathers()
    owned = get_owned_accessory_ids()
    week = current_week_key()
    return {
        # Tabs
        "collection": heard,
        "habitats": heard & ALL_CURATED_SPECIES,
        "trophies": {f"{k}:{lv}" for k, top in get_trophy_levels().items()
                     for lv in range(1, top + 1)},
        # Something new to wear, or a new bird to be
        "dressup": {aid for aid, a in ACCESSORIES.items()
                    if aid not in owned and a["cost"] <= feathers}
                   | {f"avatar:{sp}" for sp, st in avatar_states(heard).items() if st["unlocked"]}
                   | {f"colour:{hx}" for hx, st in colour_states(owned).items()
                      if not st["owned"] and st["cost"] <= feathers},
        # Things on Home (Home itself never lights up)
        # A new week's set counts as new, as does each challenge finished
        "challenges": {f"{week}:{ch['id']}" for ch, done, _ in evaluate_week_challenges() if done}
                      | {f"{week}:set"},
        "joke": {datetime.datetime.utcnow().date().isoformat()} if has_session_today() else set(),
        "game": {str(l["level"]) for l in song_game_levels(found_curated) if l["unlocked"]},
    }


WHATS_NEW_SEP = "\n"
TUTORIAL_KEYS = {"welcome", "mic_intro", "home", "listening", "results", "collection", "bird", "habitats",
                 "trophies", "dressup", "challenges", "game", "game_round"}


@app.get("/whats-new")
def whats_new():
    """Which areas have something the child hasn't looked at yet, and which
    tutorial bubbles have already been closed."""
    marks = get_seen_marks()
    new = {}
    for area, items in whats_new_items().items():
        seen = set(filter(None, marks.get(f"seen:{area}", "").split(WHATS_NEW_SEP)))
        new[area] = bool(items - seen)
    return {
        "new": new,
        "tutorials": sorted(k[4:] for k in marks if k.startswith("tut:")),
    }


@app.post("/seen/{area}")
def mark_area_seen(area: str):
    """The child has looked at this area: whatever is in it now is no
    longer new."""
    items = whats_new_items()
    if area not in items:
        return JSONResponse({"error": "unknown area"}, status_code=404)
    set_seen_mark(f"seen:{area}", WHATS_NEW_SEP.join(sorted(items[area])))
    return {"status": "ok"}


@app.post("/tutorial-seen/{name}")
def mark_tutorial_seen(name: str):
    """A tutorial bubble has been closed with "Got it!" - never show it
    again (until a reset)."""
    if name not in TUTORIAL_KEYS:
        return JSONResponse({"error": "unknown tutorial"}, status_code=404)
    set_seen_mark(f"tut:{name}", "1")
    return {"status": "ok"}


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
    # Buying can win a trophy (Preener), and it should arrive now, not at
    # the next recording.
    trophies, trophy_feathers, rank_up = award_trophy_levels() if success else ([], 0, None)
    return {"status": "ok" if success else "failed", "new_total": get_total_feathers(),
            "newly_earned_trophies": trophies, "trophy_feathers": trophy_feathers,
            "rank_up": rank_up}


@app.post("/colours/{hex_code}/purchase")
async def purchase_colour(hex_code: str):
    """Buys one of the special feather colours and puts it on the bird."""
    hx = "#" + hex_code.strip("#").upper()
    if hx not in SPECIAL_COLOURS:
        return JSONResponse(status_code=404, content={"status": "error", "message": "Not a colour you buy."})
    success = purchase_accessory(f"colour:{hx}", SPECIAL_COLOUR_COST, "colour")
    if success:
        update_profile(avatar_body=hx)
    trophies, trophy_feathers, rank_up = award_trophy_levels() if success else ([], 0, None)
    return {"status": "ok" if success else "failed", "new_total": get_total_feathers(),
            "newly_earned_trophies": trophies, "trophy_feathers": trophy_feathers,
            "rank_up": rank_up}


@app.post("/accessories/equip")
async def equip_accessory_endpoint(category: str = Form(...), accessory_id: str = Form(None)):
    """accessory_id can be omitted/blank to clear that category's slot."""
    set_equipped_item(category, accessory_id if accessory_id else None)
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
