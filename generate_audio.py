import asyncio
import json
from pathlib import Path
import edge_tts  # edge-tts library

OUTPUT_DIR = Path("audio")
OUTPUT_DIR.mkdir(exist_ok=True)

WORDS_FILE = Path("words.json")
if not WORDS_FILE.exists():
    raise FileNotFoundError(f"{WORDS_FILE} לא נמצא!")

with open(WORDS_FILE, "r", encoding="utf-8") as f:
    words_and_sentences = json.load(f)

async def generate_tts(text: str, voice: str, filename: Path):
    # edge_tts Communicate – קורא לשירות ומייצר MP3
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(filename))

new_files_count = 0

# מיפוי שפות לקולות
VOICE_MAP = {
    "en": "en-US-JennyNeural",   # אנגלית
    "he": "he-IL-AsafNeural",    # עברית (אם הקול קיים)
    "es": "es-ES-ElviraNeural",  # ספרדית לדוגמה
    # ניתן להוסיף שפות/קולות לפי הצורך
}

async def main():
    global new_files_count

    for entry in words_and_sentences:
        text = entry["text"]
        lang = entry.get("lang", "en").lower()
        voice = VOICE_MAP.get(lang, VOICE_MAP["en"])  # אם לא נמצא – ברירת מחדל לאנגלית

        safe_name = "".join(c if c.isalnum() else "_" for c in text)
        filename = OUTPUT_DIR / f"{safe_name}_{lang}.mp3"

        if filename.exists():
            print(f"Skipping existing file: {filename}")
            continue

        try:
            print(f"Generating: {text} ({lang}) → {filename}")
            await generate_tts(text, voice, filename)
            new_files_count += 1
        except Exception as e:
            print(f"Error generating audio for '{text}': {e}")

    if new_files_count == 0:
        print("No new audio files generated.")
    else:
        print(f"{new_files_count} new audio files generated!")

if __name__ == "__main__":
    asyncio.run(main())
