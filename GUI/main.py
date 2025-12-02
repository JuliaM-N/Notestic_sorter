import tkinter as tk
import json
import os
from tkinter import ttk


# Kategorie i słowa klucze
CATEGORIES = "categories.json"
NOTES_FILE= "notes.json"
def load_categories():
    if os.path.exists("categories.json"):
        try:
            with open("categories.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Błąd w categories.json:", e)

    # fallback — kategorie domyślne
    return {
        "zadania": ["zrobić", "task", "zadanie"],
        "egzamin": ["egzamin", "kolokwium", "test"],
        "lekarz": ["lekarz", "wizyta", "recepta"],
        "zakupy": ["kupić", "zakupy", "lista"],
        "inne": []
    }

# Wczytujemy kategorie do zmiennej
CATEGORIES = load_categories()

def detect_category(text):
    text_lower = text.lower()
    for category, keywords in CATEGORIES.items():
        if any(k in text_lower for k in keywords):
            return category
    return "inne"


class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notestick Sorter")

        self.notes = []

        # Pole wpisywania
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        # Przycisk dodawania
        tk.Button(root, text="Dodaj notatkę", command=self.add_note).pack()

        # Lista notatek
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

    def add_note(self):
        text = self.entry.get()
        if not text.strip():
            return
        
        category = detect_category(text)
        self.entry.delete(0, tk.END)

        var = tk.BooleanVar()

        row = tk.Frame(self.frame)
        chk = tk.Checkbutton(row, variable=var)
        lbl = tk.Label(row, text=f"[{category}] {text}")

        chk.pack(side="left")
        lbl.pack(side="left", padx=5)
        row.pack(anchor="w")

        self.notes.append({"text": text, "cat": category, "done": var})


root = tk.Tk()
app = NoteApp(root)
root.mainloop()
