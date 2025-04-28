from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from utils.transcribe import transcribe_audio
from utils.summarize import summarize_text
from utils.resources import get_learning_materials
from utils.pdf_gen import create_pdf
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = transcribe_audio(path)
    summary = summarize_text(transcript)
    resources = get_learning_materials(summary)

    os.remove(path)
    return {
        "transcript": transcript,
        "summary": summary,
        "resources": resources
    }

@app.post("/generate-pdf/")
async def generate_pdf(summary: str, transcript: str):
    filename = "meeting_notes.pdf"
    create_pdf(summary, transcript, filename)
    return FileResponse(path=filename, filename=filename, media_type='application/pdf')