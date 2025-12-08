CREATE TABLE IF NOT EXISTS categories (
    name TEXT PRIMARY KEY,
    keywords TEXT
);

-- przykładowe wpisy
INSERT OR IGNORE INTO categories VALUES ('zadania', 'zrobić,task,zadanie');
INSERT OR IGNORE INTO categories VALUES ('egzamin', 'egzamin,kolokwium,test');
INSERT OR IGNORE INTO categories VALUES ('lekarz', 'lekarz,wizyta,recepta');
INSERT OR IGNORE INTO categories VALUES ('zakupy', 'kupić,zakupy,lista');
INSERT OR IGNORE INTO categories VALUES ('inne', '');

