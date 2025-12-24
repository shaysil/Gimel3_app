import os
import json
from pathlib import Path
from gtts import gTTS

OUTPUT_DIR = Path("main/audio")
OUTPUT_DIR.mkdir(exist_ok=True)

WORDS_FILE = Path("main/words.json")
if not WORDS_FILE.exists():
    raise FileNotFoundError(f"{WORDS_FILE} לא נמצא!")

with open(WORDS_FILE, "r", encoding="utf-8") as f:
    words_and_sentences = json.load(f)

new_files_count = 0

for entry in words_and_sentences:
    text = entry["text"]
    lang = entry.get("lang", "en")
    safe_name = "".join(c if c.isalnum() else "_" for c in text)
    filename = OUTPUT_DIR / f"{safe_name}_{lang}.mp3"

    if filename.exists():
        print(f"Skipping existing file: {filename}")
        continue  # כבר קיים, דילוג

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(str(filename))
        print(f"Saved new file: {filename}")
        new_files_count += 1
    except Exception as e:
        print(f"Error generating audio for '{text}': {e}")

if new_files_count == 0:
    print("No new audio files generated.")
else:
    print(f"{new_files_count} new audio files generated!")
