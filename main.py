import os
import ass
import requests
from dotenv import load_dotenv

# Load the DeepL API key from the .env file
load_dotenv()
deepl_api_key = os.getenv("DEEPL_API_KEY")

# Load ASS file
with open("yourfile.ass", "r", encoding='utf_8_sig') as f:
    doc = ass.parse(f)

# Parse all events from ass file
for event in doc.events:
    if isinstance(event, ass.document.Dialogue):
        # Translate the text using Deepl API
        response = requests.post(
            # Feel free to change the api if you use the premium version
            "https://api-free.deepl.com/v2/translate",
            data={
                "auth_key": deepl_api_key,
                "text": event.text,
                "target_lang": "FR",
                "source_lang": "EN"
            }
        )
        response.raise_for_status()
        translation = response.json()["translations"][0]["text"]

        # Replace original text with translated one
        event.text = translation

# Write the translated ASS document to a new file
with open("translated.ass", "w", encoding='utf-8-sig') as f:
    doc.dump_file(f)
