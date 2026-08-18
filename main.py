cat > /mnt/user-data/outputs/warble-birdnet-api/main.py << 'EOF'
import os
import tempfile
import threading
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI(title="Warble BirdNET Inference API")

# The model isn't loaded yet when the server starts — it loads in the
# background instead, so Railway's health check gets an instant answer
# and doesn't time out waiting for the (slow) model load to finish.
model = None
model_error = None


def load_model():
    global model, model_error
    try:
        print("Loading BirdNET model in background...")
        from birdnet.models import ModelV2M4
        model = ModelV2M4()
        print("BirdNET model loaded. Ready for requests.")
    except Exception as e:
        model_error = str(e)
        print(f"Failed to load BirdNET model: {e}")


threading.Thread(target=load_model, daemon=True).start()


@app.get("/")
def root():
    """
    Visit this in a browser any time to check status. It answers
    immediately, even while the model is still loading in the background.
    """
    if model is not None:
        status = "ready"
    elif model_error is not None:
        status = "error"
    else:
        status = "loading"

    return {
        "status": status,
        "message": "Warble BirdNET inference API",
        "model_error": model_error,
    }


@app.post("/identify")
async def identify(file: UploadFile = File(...)):
    """
    Send a WAV (or FLAC/OGG) audio file as multipart form-data under the
    field name 'file'. Returns the species BirdNET detected, ranked by
    confidence, highest first.
    """
    if model is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "loading",
                "message": "Model is still loading — check the '/' endpoint, then try again shortly.",
            },
        )

    suffix = Path(file.filename).suffix or ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = Path(tmp.name)

    try:
        predictions = model.predict_species_within_audio_file(tmp_path)
    finally:
        os.unlink(tmp_path)

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


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
EOF
echo "main.py updated"
