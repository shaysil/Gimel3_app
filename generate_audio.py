import os
import json
from pathlib import Path
from gtts import gTTS

# תיקיית הפלט
OUTPUT_DIR = Path("audio")
OUTPUT_DIR.mkdir(exist_ok=True)

# קריאת רשימת מילים/משפטים מקובץ JSON
WORDS_FILE = Path("words.json")
if not WORDS_FILE.exists():
    raise FileNotFoundError(f"{WORDS_FILE} לא נמצא!")

with open(WORDS_FILE, "r", encoding="utf-8") as f:
    words_and_sentences = json.load(f)

for entry in words_and_sentences:
    text = entry["text"]
    lang = entry.get("lang", "en")  # ברירת מחדל: אנגלית

    # יצירת שם קובץ תקין
    safe_name = "".join(c if c.isalnum() else "_" for c in text)
    filename = OUTPUT_DIR / f"{safe_name}_{lang}.mp3"

    # יצירת קובץ אודיו
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(str(filename))
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error generating audio for '{text}': {e}")

print("All audio files generated!")
