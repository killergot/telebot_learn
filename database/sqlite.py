import sqlite3 as sq

def db_start():
    global db,cur

    db = sq.connect('Data/new.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS "photo_monkey" (
                    "id"	INTEGER,
                    "url"	TEXT NOT NULL,
                    PRIMARY KEY("id")
);
            """)
    db.commit()

async def create_photo(url : str)  ->  str:
    photo = cur.execute(f"select 1 from photo_monkey where url == ('{url}');").fetchone()
    if not photo:
        cur.execute(f"INSERT INTO photo_monkey ('url') values ('{url}');")
        db.commit()
        return 'Фото обезьянки успешно добавлено'
    return 'Данное фото уже есть в базе'

async def delete_photo(url : str) -> str:
    photo = cur.execute(f"select 1 from photo_monkey where url == '{url}';").fetchone()
    if not photo:
        return 'Этого фото нет в базе'
    else:
        cur.execute(f"DELETE FROM photo_monkey WHERE url = '{url}';")
        db.commit()
        return 'Фото успешно удалено'

async def get_random_photo() -> str:
    photo : tuple = cur.execute(f"SELECT url FROM photo_monkey ORDER BY RANDOM() LIMIT 1;").fetchone()
    return photo[0]

async def get_all_photo() -> str:
    photo = cur.execute(f"select * from photo_monkey;").fetchone()
    return photo

