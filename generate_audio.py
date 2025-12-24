import json
from pathlib import Path
import pyttsx3
from pydub import AudioSegment

# תיקייה ליצירת קבצי קול
OUTPUT_DIR = Path("audio")
OUTPUT_DIR.mkdir(exist_ok=True)

# קובץ עם מילים/משפטים
WORDS_FILE = Path("words.json")
if not WORDS_FILE.exists():
    raise FileNotFoundError(f"{WORDS_FILE} לא נמצא!")

with open(WORDS_FILE, "r", encoding="utf-8") as f:
    words_and_sentences = json.load(f)

# אתחול pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# מציאת קול עברי (אם קיים)
hebrew_voice = None
for v in voices:
    if "he" in v.id.lower() or "heb" in v.name.lower():
        hebrew_voice = v.id
        break

new_files_count = 0

for entry in words_and_sentences:
    text = entry["text"]
    lang = entry.get("lang", "en").lower()
    
    # שם קובץ תקין
    safe_name = "".join(c if c.isalnum() else "_" for c in text)
    wav_file = OUTPUT_DIR / f"{safe_name}_{lang}.wav"
    mp3_file = OUTPUT_DIR / f"{safe_name}_{lang}.mp3"

    if mp3_file.exists():
        print(f"Skipping existing file: {mp3_file}")
        continue

    try:
        if lang == "he" and hebrew_voice:
            engine.setProperty('voice', hebrew_voice)
        else:
            engine.setProperty('voice', voices[0].id)  # ברירת מחדל

        # שמירה כ‑WAV
        engine.save_to_file(text, str(wav_file))
        engine.runAndWait()

        # המרה ל‑MP3
        sound = AudioSegment.from_wav(str(wav_file))
        sound.export(str(mp3_file), format="mp3")

        # מחיקת קובץ WAV ביניים
        wav_file.unlink()

        new_files_count += 1
        print(f"Saved new file: {mp3_file}")

    except Exception as e:
        print(f"Error generating audio for '{text}': {e}")

if new_files_count == 0:
    print("No new audio files generated.")
else:
    print(f"{new_files_count} new audio files generated!")
