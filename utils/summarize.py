import openai
import os

openai.api_key = os.getenv("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")

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant that summarizes meeting transcripts."},
            {"role": "user", "content": f"Please summarize this meeting: {text}"}
        ]
    )
    return response.choices[0].message["content"]
