from fastapi import FastAPI, Query
from soniox.speech_service import SpeechClient, TranscriptionConfig
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SONIOX_API_KEY")

app = FastAPI(title="Chinese → English Speech Translator")

@app.get("/translate")
def translate(audio_url: str = Query(...)):
    # Download audio
    resp = requests.get(audio_url, stream=True)
    resp.raise_for_status()
    audio_bytes = resp.content

    # Transcribe + Translate
    with SpeechClient(api_key=API_KEY) as client:
        config = TranscriptionConfig(
            language="zh",
            translate_to=["en"]
        )
        response = client.transcribe(audio_bytes, config)

        results = []
        for r in response.results:
            results.append({
                "chinese": r.text,
                "english": r.translations.get("en", "")
            })

    return {"results": results}
