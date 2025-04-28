from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI that summarizes meeting transcripts in 50 words or less."},
            {"role": "user", "content": f"Summarize this meeting: {text}"}
        ]
    )
    return response.choices[0].message.content
