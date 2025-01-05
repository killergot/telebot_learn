import sqlite3 as sq

def database_init():
    db = sq.connect('Data/new.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS "photo_monkey" (
                    "id"	INTEGER,
                    "url"	TEXT NOT NULL,
                    PRIMARY KEY("id")
);
            """)
    db.commit()
    cur.close()
    return db

