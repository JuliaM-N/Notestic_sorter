import sqlite3
import os

DB_FILE = "notes.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # Tabela kategorii (można też załadować z categories.sql)
        c.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                name TEXT PRIMARY KEY,
                keywords TEXT
            )
        """)
        # Tabela notatek
        c.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                cat TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()

def load_categories():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, keywords FROM categories")
    rows = c.fetchall()
    conn.close()
    # Zamieniamy na słownik {kategoria: [lista_słów_kluczowych]}
    categories = {name: keywords.split(",") if keywords else [] for name, keywords in rows}
    return categories

def detect_category(text, categories):
    text_lower = text.lower()
    for category, keywords in categories.items():
        if any(k in text_lower for k in keywords):
            return category
    return "inne"

def load_notes():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, text, cat, done FROM notes")
    rows = c.fetchall()
    conn.close()
    notes = []
    for row in rows:
        notes.append({"id": row[0], "text": row[1], "cat": row[2], "done": bool(row[3])})
    return notes

def save_note(note):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if "id" in note and note["id"]:
        c.execute("UPDATE notes SET text=?, cat=?, done=? WHERE id=?",
                  (note["text"], note["cat"], int(note["done"]), note["id"]))
    else:
        c.execute("INSERT INTO notes (text, cat, done) VALUES (?, ?, ?)",
                  (note["text"], note["cat"], int(note["done"])))
        note["id"] = c.lastrowid
    conn.commit()
    conn.close()

def delete_note(note_id):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
