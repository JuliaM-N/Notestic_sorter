import json
import os

CATEGORIES_FILE = "categories.json" #add categories
NOTES_FILE = "notes.json"

def load_categories():
    if os.path.exists(CATEGORIES_FILE):
        try:
            with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception as e:
            print("Błąd w categories.json:", e)

    # fallback 
    return {
        "zadania": ["zrobić", "task", "zadanie"],
        "egzamin": ["egzamin", "kolokwium", "test", "egsam"],
        "lekarz": ["lekarz", "wizyta", "recepta", "appointment"],
        "zakupy": ["kupić", "zakupy", "lista", "buy"],
        "inne": []
    }

def detect_category(text, categories):
    text_lower = text.lower()
    for category, keywords in categories.items():
        if any(k in text_lower for k in keywords):
            return category
    return "inne"

def load_notes():
    notes = []
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                notes = json.load(f)
        except Exception as e:
            print("Błąd w notes.json:", e)

    for n in notes:
        if "cat" not in n or not n["cat"]:
            n["cat"] = "inne"
        if "done" not in n:
            n["done"] = False
    return notes

def save_notes(notes):
    try:
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(notes, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Błąd przy zapisie notes.json:", e)
