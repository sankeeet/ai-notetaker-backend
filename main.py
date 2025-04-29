import tempfile
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

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    # Use tempfile to create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())  # Write the uploaded file to the temp file
        temp_file_path = temp_file.name  # Get the path to the temporary file

    try:
        transcript = transcribe_audio(temp_file_path)
        summary = summarize_text(transcript)
        resources = get_learning_materials(summary)
    finally:
        os.remove(temp_file_path)  # Clean up the temporary file

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

@app.get("/")
async def read_root():
    return {"message": "AI Notetaker API is live!"}

