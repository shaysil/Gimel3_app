import asyncio
import json
from pathlib import Path
import edge_tts

OUTPUT_DIR = Path("audio")
OUTPUT_DIR.mkdir(exist_ok=True)

WORDS_FILE = Path("words.json")
if not WORDS_FILE.exists():
    raise FileNotFoundError(f"{WORDS_FILE} לא נמצא!")

with open(WORDS_FILE, "r", encoding="utf-8") as f:
    words_and_sentences = json.load(f)

new_files_count = 0

# דוגמה לרשימת קולות לפי שפה (ניתן למלא לפי הפלט של `python -m edge_tts --list-voices`)
VOICE_LIST = {
    "he": ["he-IL-AsafNeural", "he-IL-HilaNeural"],  # fallback עברית
    "en": ["en-US-JennyNeural", "en-US-GuyNeural"],
    "es": ["es-ES-ElviraNeural", "es-ES-AlvaroNeural"],
    # הוסף שפות/קולות נוספים לפי הצורך
}

async def generate_tts_with_fallback(text: str, lang: str, filename: Path):
    voices = VOICE_LIST.get(lang, VOICE_LIST["en"])  # אם השפה לא קיימת, נשתמש באנגלית
    last_error = None

    for voice in voices:
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(filename))
            return True  # הצלחה
        except Exception as e:
            print(f"Voice '{voice}' failed: {e}")
            last_error = e

    # אם כל הקולות נכשלו
    print(f"Failed to generate audio for '{text}' ({lang}) after trying all voices.")
    if last_error:
        print(f"Last error: {last_error}")
    return False

async def main():
    global new_files_count

    for entry in words_and_sentences:
        text = entry["text"]
        lang = entry.get("lang", "en").lower()

        safe_name = "".join(c if c.isalnum() else "_" for c in text)
        filename = OUTPUT_DIR / f"{safe_name}_{lang}.mp3"

        if filename.exists():
            print(f"Skipping existing file: {filename}")
            continue

        print(f"Generating: {text} ({lang}) → {filename}")
        success = await generate_tts_with_fallback(text, lang, filename)
        if success:
            new_files_count += 1

    if new_files_count == 0:
        print("No new audio files generated.")
    else:
        print(f"{new_files_count} new audio files generated!")

if __name__ == "__main__":
    asyncio.run(main())
