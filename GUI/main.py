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

def load_notes():
    notes = []
    if os.path.exists("notes.json"):
        try:
            with open("notes.json", "r", encoding="utf-8") as f:
                notes = json.load(f)
        except Exception as e:
            print("Błąd w notes.json:", e)

    # Uzupełniamy brakujące kategorie
    for n in notes:
        if "cat" not in n or not n["cat"]:
            n["cat"] = detect_category(n["text"])  # przypisanie kategorii
        if "done" not in n:
            n["done"] = False
    return notes

def save_notes(notes):
    try:
        with open("notes.json", "w", encoding="utf-8") as f:
            json.dump(notes, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Błąd przy zapisie notes.json:", e)


class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notestick Sorter")

        # Dane
        self.categories = load_categories()
        self.notes = load_notes()
        self.current_category = None

        # Layout: lewy panel = kategorie, prawy panel = notatki
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Listbox kategorii
        tk.Label(self.left_frame, text="Kategorie").pack()
        self.cat_listbox = tk.Listbox(self.left_frame)
        self.cat_listbox.pack()
        for cat in self.categories.keys():
            self.cat_listbox.insert(tk.END, cat)
        self.cat_listbox.bind("<<ListboxSelect>>", self.on_category_select)

        # Notatki
        self.notes_frame = tk.Frame(self.right_frame)
        self.notes_frame.pack(fill="both", expand=True)

        # Pole dodawania notatek
        self.entry = tk.Entry(self.right_frame, width=50)
        self.entry.pack(pady=5)
        tk.Button(self.right_frame, text="Dodaj notatkę", command=self.add_note).pack()

        # Renderowanie notatek (puste na start)
        self.render_notes()

    # -----------------------
    def on_category_select(self, event):
        selection = self.cat_listbox.curselection()
        if selection:
            self.current_category = self.cat_listbox.get(selection[0])
        else:
            self.current_category = None
        self.render_notes()

    def add_note(self):
        text = self.entry.get()
        if not text.strip():
            return
        
        category = detect_category(text)  # automatyczne przypisanie kategorii
        self.notes.append({"text": text, "cat": category, "done": False})
        save_notes(self.notes)
        self.entry.delete(0, tk.END)
        self.render_notes()

        var = tk.BooleanVar()

        row = tk.Frame(self.notes_frame)
        chk = tk.Checkbutton(row, variable=var)
        lbl = tk.Label(row, text=f"[{category}] {text}")

        chk.pack(side="left")
        lbl.pack(side="left", padx=5)
        row.pack(anchor="w")

        self.notes.append({"text": text, "cat": category, "done": var})
        
    def render_notes(self):
        # Czyścimy frame notatek
        for widget in self.notes_frame.winfo_children():
            widget.destroy()

        # Filtrujemy po kategorii
        if self.current_category:
            filtered_notes = [n for n in self.notes if n["cat"] == self.current_category]
        else:
            filtered_notes = self.notes

        # Wyświetlamy notatki
        for i, note in enumerate(filtered_notes):
            var = tk.BooleanVar(value=note["done"])

            def toggle_done(n=note, v=var):
                n["done"] = v.get()
                save_notes(self.notes)

            row = tk.Frame(self.notes_frame)
            chk = tk.Checkbutton(row, variable=var, command=toggle_done)
            lbl = tk.Label(row, text=note["text"])
            chk.pack(side="left")
            lbl.pack(side="left", padx=5)
            row.pack(anchor="w", pady=2)


root = tk.Tk()
app = NoteApp(root)
root.mainloop()
