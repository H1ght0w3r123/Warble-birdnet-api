import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from birdnet.models import ModelV2M4

app = FastAPI(title="Warble BirdNET Inference API")

# The model loads once, when the server starts up — not on every request.
# This is the slow bit (can take a minute or two on first boot), so don't
# worry if the very first request after a deploy feels sluggish.
print("Loading BirdNET model... this can take a minute on first startup.")
model = ModelV2M4()
print("BirdNET model loaded. Ready for requests.")


@app.get("/")
def root():
    """
    Visit this in a browser to confirm the service is alive at all.
    If this doesn't load, the problem is deployment/networking.
    If this loads but /identify doesn't, the problem is narrower.
    """
    return {"status": "ok", "message": "Warble BirdNET inference API is running."}


@app.post("/identify")
async def identify(file: UploadFile = File(...)):
    """
    Send a WAV (or FLAC/OGG) audio file as multipart form-data under the
    field name 'file'. Returns the species BirdNET detected, ranked by
    confidence, highest first.
    """
    suffix = Path(file.filename).suffix or ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = Path(tmp.name)

    try:
        predictions = model.predict_species_within_audio_file(tmp_path)
    finally:
        os.unlink(tmp_path)

    # predictions is keyed by (start_seconds, end_seconds) time chunks,
    # each holding an ordered dict of {"ScientificName_CommonName": confidence}
    results = []
    for (start, end), species_scores in predictions.items():
        for label, confidence in species_scores.items():
            if "_" in label:
                scientific_name, common_name = label.split("_", 1)
            else:
                scientific_name, common_name = label, label
            results.append({
                "start_time": start,
                "end_time": end,
                "scientific_name": scientific_name,
                "common_name": common_name,
                "confidence": round(float(confidence), 4),
            })

    results.sort(key=lambda r: r["confidence"], reverse=True)

    return {"detections": results[:10]}


# This block only matters if the app is ever started with `python main.py`
# directly. Railway will normally use the Procfile instead — but having
# this here too means the app still does the right thing either way.
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
