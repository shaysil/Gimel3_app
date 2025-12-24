import os
from pathlib import Path
from gtts import gTTS  # אם רוצים TTS חינמי מבוסס Google

# תיקיית הפלט של הקבצים
OUTPUT_DIR = Path("audio")
OUTPUT_DIR.mkdir(exist_ok=True)

# רשימת מילים ומשפטים לדוגמה
words_and_sentences = [
    {"text": "Pan", "lang": "en"},
    {"text": "Tan", "lang": "en"},
    {"text": "אני אוהב ללמוד", "lang": "he"},
    {"text": "בוא נשחק כדור", "lang": "he"},
    # הוסף כאן את כל המילים והמשפטים שאתה צריך
]

for entry in words_and_sentences:
    text = entry["text"]
    lang = entry["lang"]
    
    # יצירת שם קובץ מתאים
    filename = OUTPUT_DIR / f"{text.replace(' ', '_')}_{lang}.mp3"
    
    # יצירת קובץ אודיו
    tts = gTTS(text=text, lang=lang)
    tts.save(str(filename))
    print(f"Saved: {filename}")

print("All audio files generated!")
