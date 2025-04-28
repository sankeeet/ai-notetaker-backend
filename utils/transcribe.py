import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_audio(audio_file_path):
    try:
        headers_auth = {"authorization": ASSEMBLYAI_API_KEY}
        upload_url = "https://api.assemblyai.com/v2/upload"

        with open(audio_file_path, "rb") as f:
            response = requests.post(upload_url, headers=headers_auth, files={"file": f})
        
        response.raise_for_status()
        audio_url = response.json()["upload_url"]

        endpoint = "https://api.assemblyai.com/v2/transcript"
        json_data = {"audio_url": audio_url}
        headers = {
            "authorization": ASSEMBLYAI_API_KEY,
            "content-type": "application/json"
        }

        transcript_response = requests.post(endpoint, json=json_data, headers=headers)
        transcript_response.raise_for_status()
        transcript_id = transcript_response.json()["id"]

        while True:
            polling_response = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
            polling_response.raise_for_status()
            status = polling_response.json()["status"]

            if status == "completed":
                return polling_response.json()["text"]
            elif status == "failed":
                raise Exception(f"Transcription failed: {polling_response.json()}")
    
    except Exception as e:
        print(f"Error in transcribe_audio: {e}")
        raise
