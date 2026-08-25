import os
import tempfile
import threading
import json
import datetime
from pathlib import Path

import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydub import AudioSegment

app = FastAPI(title="Warble BirdNET Inference API")

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
def root():
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
async def identify(file: UploadFile = File(...)):
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
                "message": "Analyzer is still loading — check the '/' endpoint, then try again shortly.",
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
        recording = Recording(analyzer, tmp_wav_path, min_conf=0.1)
        recording.analyze()
        detections = recording.detections
    finally:
        os.unlink(tmp_in_path)
        os.unlink(tmp_wav_path)

    detections.sort(key=lambda d: d["confidence"], reverse=True)

    return {"detections": detections[:10]}


# ============================================================
# Everything below here is the new all-in-one session endpoint.
# It does BirdNET + NBN Atlas tiering + duplicate checking +
# Wikipedia photos + feather maths + saving to Bubble, all in
# one call — replacing several separate Bubble workflow steps.
# ============================================================

BUBBLE_APP_URL = os.environ.get("BUBBLE_APP_URL", "")  # e.g. https://your-app.bubbleapps.io/version-test
BUBBLE_API_TOKEN = os.environ.get("BUBBLE_API_TOKEN", "")

# IMPORTANT: check these against your own app's Data API documentation
# (Settings -> API in Bubble, once the Data API is switched on). Field
# names sometimes need adjusting to match exactly what your app expects —
# don't assume these are right without checking.
BUBBLE_SIGHTING_TYPE = "sightings"
FIELD_COMMON_NAME = "Common Name"
FIELD_SCIENTIFIC_NAME = "Scientific Name"
FIELD_CONFIDENCE = "Confidence"
FIELD_TIER = "Tier"
FIELD_IMAGE = "Image"


def bubble_headers():
    return {
        "Authorization": f"Bearer {BUBBLE_API_TOKEN}",
        "Content-Type": "application/json",
    }


def check_existing_sighting(common_name: str) -> bool:
    """Ask Bubble: has this species already been saved as a Sighting?"""
    if not BUBBLE_APP_URL or not BUBBLE_API_TOKEN:
        print("Warning: Bubble credentials not set — treating everything as new.")
        return False
    url = f"{BUBBLE_APP_URL}/api/1.1/obj/{BUBBLE_SIGHTING_TYPE}"
    constraints = [{"key": FIELD_COMMON_NAME, "constraint_type": "equals", "value": common_name}]
    try:
        response = requests.get(
            url,
            headers=bubble_headers(),
            params={"constraints": json.dumps(constraints)},
            timeout=10,
        )
        response.raise_for_status()
        results = response.json().get("response", {}).get("results", [])
        return len(results) > 0
    except Exception as e:
        print(f"Warning: could not check Bubble for existing sighting of {common_name}: {e}")
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


def get_wikipedia_photo(scientific_name: str):
    """Fetch a photo URL for this species from Wikipedia. Returns None if not found."""
    title = scientific_name.replace(" ", "_")
    try:
        response = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}",
            headers={"User-Agent": "Warble bird app (dev testing)"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get("thumbnail", {}).get("source")
    except Exception as e:
        print(f"Warning: Wikipedia photo lookup failed for {scientific_name}: {e}")
        return None


def calculate_feathers(tier: str, is_duplicate: bool) -> float:
    values = {
        ("Common", False): 1, ("Visitor", False): 3, ("Rare", False): 7,
        ("Common", True): 0.2, ("Visitor", True): 0.6, ("Rare", True): 1.5,
    }
    return values.get((tier, is_duplicate), 0)


def save_sighting_to_bubble(common_name, scientific_name, confidence, tier, photo_url):
    """Create a new Sighting record directly in Bubble's database."""
    if not BUBBLE_APP_URL or not BUBBLE_API_TOKEN:
        print("Warning: Bubble credentials not set — skipping save.")
        return
    url = f"{BUBBLE_APP_URL}/api/1.1/obj/{BUBBLE_SIGHTING_TYPE}"
    payload = {
        FIELD_COMMON_NAME: common_name,
        FIELD_SCIENTIFIC_NAME: scientific_name,
        FIELD_CONFIDENCE: confidence,
        FIELD_TIER: tier,
        FIELD_IMAGE: photo_url,
    }
    try:
        response = requests.post(url, headers=bubble_headers(), json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        error_detail = ""
        try:
            error_detail = response.text
        except Exception:
            pass
        print(f"Warning: failed to save sighting '{common_name}' to Bubble: {e} | Bubble said: {error_detail}")


@app.post("/analyze-session")
async def analyze_session(
    file: UploadFile = File(...),
    lat: float = 51.5074,
    lng: float = -0.1278,
):
    """
    The all-in-one endpoint. Identifies every bird in a recording, checks
    each one's rarity tier and duplicate status, calculates feathers,
    fetches a photo, saves it to Bubble, and returns the full enriched
    list — ready to display directly in a Repeating Group.
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
        recording = Recording(analyzer, tmp_wav_path, min_conf=0.1)
        recording.analyze()
        detections = recording.detections
    finally:
        os.unlink(tmp_in_path)
        os.unlink(tmp_wav_path)

    detections.sort(key=lambda d: d["confidence"], reverse=True)

    now = datetime.datetime.utcnow()
    results = []

    for detection in detections:
        common_name = detection["common_name"]
        scientific_name = detection["scientific_name"]
        confidence = detection["confidence"]

        is_duplicate = check_existing_sighting(common_name)
        tier, record_count = get_nbn_tier(scientific_name, lat, lng)
        feathers = calculate_feathers(tier, is_duplicate)
        photo_url = get_wikipedia_photo(scientific_name)

        save_sighting_to_bubble(common_name, scientific_name, confidence, tier, photo_url)

        results.append({
            "common_name": common_name,
            "scientific_name": scientific_name,
            "confidence": confidence,
            "tier": tier,
            "nbn_record_count": record_count,
            "is_duplicate": is_duplicate,
            "feathers": feathers,
            "photo_url": photo_url,
            # Extra context, unused today — kept ready for trophy logic later:
            "detected_at": now.isoformat(),
            "hour_of_day": now.hour,
            "lat": lat,
            "lng": lng,
        })

    return {"detections": results}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
