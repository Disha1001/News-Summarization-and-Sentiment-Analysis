from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from utils import main
import os

app = FastAPI()

@app.get("/analyze")
def analyze_news(company: str):
    """Fetch and analyze news for a given company."""
    try:
        results = main(company)
        if "error" in results:
            raise HTTPException(status_code=404, detail=results["error"])
        
        return JSONResponse(content=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/audio/{company}")
def get_hindi_audio(company: str):
    """Fetch Hindi audio analysis."""
    audio_path = f"{company}_report_hindi.mp3"
    
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found. Generate analysis first.")

    return FileResponse(audio_path, media_type="audio/mpeg", filename=f"{company}_report_hindi.mp3")
