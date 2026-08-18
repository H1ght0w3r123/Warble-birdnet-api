import os
import tempfile
import threading
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

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
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        from birdnetlib import Recording
        recording = Recording(analyzer, tmp_path, min_conf=0.1)
        recording.analyze()
        detections = recording.detections
    finally:
        os.unlink(tmp_path)

    detections.sort(key=lambda d: d["confidence"], reverse=True)

    return {"detections": detections[:10]}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
