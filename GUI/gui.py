import tkinter as tk
from storage import load_notes, save_notes, load_categories, detect_category

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notestick Sorter")

        # Dane
        self.categories = load_categories()
        self.notes = load_notes()
        self.current_category = None

        # Layout
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(self.left_frame, text="Kategorie").pack()
        self.cat_listbox = tk.Listbox(self.left_frame)
        self.cat_listbox.pack()
        for cat in self.categories.keys():
            self.cat_listbox.insert(tk.END, cat)
        self.cat_listbox.bind("<<ListboxSelect>>", self.on_category_select)

        self.notes_frame = tk.Frame(self.right_frame)
        self.notes_frame.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.right_frame, width=50)
        self.entry.pack(pady=5)
        tk.Button(self.right_frame, text="Dodaj notatkę", command=self.add_note).pack()

        self.render_notes()

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

        category = detect_category(text, self.categories)
        self.notes.append({"text": text, "cat": category, "done": False})
        save_notes(self.notes)
        self.entry.delete(0, tk.END)
        self.render_notes()

    def render_notes(self):
        for widget in self.notes_frame.winfo_children():
            widget.destroy()

        if self.current_category:
            filtered = [n for n in self.notes if n["cat"] == self.current_category]
        else:
            filtered = self.notes

        for note in filtered:
            var = tk.BooleanVar(value=note["done"])

            def toggle_done(n=note, v=var):
                n["done"] = v.get()
                save_notes(self.notes)

            def delete_note(n=note):
                self.notes.remove(n)
                save_notes(self.notes)
                self.render_notes()

            row = tk.Frame(self.notes_frame)
            chk = tk.Checkbutton(row, variable=var, command=toggle_done)
            lbl = tk.Label(row, text=note["text"])
            btn_del = tk.Button(row, text="Usuń", command=delete_note)

            chk.pack(side="left")
            lbl.pack(side="left", padx=5)
            btn_del.pack(side="left", padx=5)
            row.pack(anchor="w", pady=2)
import tkinter as tk
from storage import load_notes, save_notes, load_categories, detect_category

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notestick Sorter")

        # Dane
        self.categories = load_categories()
        self.notes = load_notes()
        self.current_category = None

        # Layout
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(self.left_frame, text="Kategorie").pack()
        self.cat_listbox = tk.Listbox(self.left_frame)
        self.cat_listbox.pack()
        for cat in self.categories.keys():
            self.cat_listbox.insert(tk.END, cat)
        self.cat_listbox.bind("<<ListboxSelect>>", self.on_category_select)

        self.notes_frame = tk.Frame(self.right_frame)
        self.notes_frame.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.right_frame, width=50)
        self.entry.pack(pady=5)
        tk.Button(self.right_frame, text="Dodaj notatkę", command=self.add_note).pack()

        self.render_notes()

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

        category = detect_category(text, self.categories)
        self.notes.append({"text": text, "cat": category, "done": False})
        save_notes(self.notes)
        self.entry.delete(0, tk.END)
        self.render_notes()

    def render_notes(self):
        for widget in self.notes_frame.winfo_children():
            widget.destroy()

        if self.current_category:
            filtered = [n for n in self.notes if n["cat"] == self.current_category]
        else:
            filtered = self.notes

        for note in filtered:
            var = tk.BooleanVar(value=note["done"])

            def toggle_done(n=note, v=var):
                n["done"] = v.get()
                save_notes(self.notes)

            def delete_note(n=note):
                self.notes.remove(n)
                save_notes(self.notes)
                self.render_notes()

            row = tk.Frame(self.notes_frame)
            chk = tk.Checkbutton(row, variable=var, command=toggle_done)
            lbl = tk.Label(row, text=note["text"])
            btn_del = tk.Button(row, text="Usuń", command=delete_note)

            chk.pack(side="left")
            lbl.pack(side="left", padx=5)
            btn_del.pack(side="left", padx=5)
            row.pack(anchor="w", pady=2)
