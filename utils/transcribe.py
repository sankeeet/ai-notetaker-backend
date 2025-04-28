import requests
import time
import os

assemblyai_api_key = os.getenv("90d54d8fadd44fb9b21e7f7383f0ed0f")

def transcribe_audio(path):
    headers = {'authorization': assemblyai_api_key}
    
    # Upload file to AssemblyAI
    with open(path, 'rb') as f:
        response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, files={'file': f})
    upload_url = response.json()['upload_url']

    # Request transcription
    transcript_request = {'audio_url': upload_url}
    transcript_response = requests.post('https://api.assemblyai.com/v2/transcript', json=transcript_request, headers=headers)
    transcript_id = transcript_response.json()['id']

    # Polling for completion
    while True:
        poll_response = requests.get(f'https://api.assemblyai.com/v2/transcript/{transcript_id}', headers=headers)
        if poll_response.json()['status'] == 'completed':
            return poll_response.json()['text']
        elif poll_response.json()['status'] == 'failed':
            raise Exception('Transcription failed')
        time.sleep(3)
