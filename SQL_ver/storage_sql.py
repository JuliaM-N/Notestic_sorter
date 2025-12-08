import sqlite3
import os
from storage_json import load_categories, detect_category  # możesz zostawić JSON dla kategorii

DB_FILE = "notes.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                cat TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()

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
