import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant that summarizes meeting transcripts."},
            {"role": "user", "content": f"Please summarize this meeting: {text}"}
        ]
    )
    return response.choices[0].message["content"]