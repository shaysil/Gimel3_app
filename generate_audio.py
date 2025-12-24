import pyttsx3
from pathlib import Path
import json

OUTPUT_DIR = Path("audio")
OUTPUT_DIR.mkdir(exist_ok=True)

WORDS_FILE = Path("words.json")
with open(WORDS_FILE, "r", encoding="utf-8") as f:
    words_and_sentences = json.load(f)

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# מציאת קול עברי (אם קיים)
hebrew_voice = None
for v in voices:
    if "he" in v.id or "Hebrew" in v.name:
        hebrew_voice = v.id
        break

new_files_count = 0
for entry in words_and_sentences:
    text = entry["text"]
    lang = entry.get("lang", "en").lower()

    filename = OUTPUT_DIR / f"{''.join(c if c.isalnum() else '_ ' for c in text)}_{lang}.mp3"
    if filename.exists():
        continue

    try:
        if lang == "he" and hebrew_voice:
            engine.setProperty('voice', hebrew_voice)
        else:
            engine.setProperty('voice', voices[0].id)  # ברירת מחדל

        engine.save_to_file(text, str(filename))
        engine.runAndWait()
        new_files_count += 1
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error generating audio for '{text}': {e}")

print(f"{new_files_count} new audio files generated!")
