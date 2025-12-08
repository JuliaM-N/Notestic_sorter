CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    cat TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
);

-- przykładowe wpisy
INSERT INTO notes (text, cat, done) VALUES ('Kup mleko', 'zakupy', 0);
INSERT INTO notes (text, cat, done) VALUES ('Zrobić projekt', 'zadania', 0);
INSERT INTO notes (text, cat, done) VALUES ('Wizyta u lekarza', 'lekarz', 0);
