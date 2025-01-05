async def create_photo(url : str, db)  ->  str:
    """
    Загрузка фото в БД
    :param url: Id фото в телеграмме
    :param db: Объект базы данных
    :return: Строка с результатом
    """
    cur = db.cursor()
    photo = cur.execute(f"select 1 from photo_monkey where url == ('{url}');").fetchone()
    if not photo:
        cur.execute(f"INSERT INTO photo_monkey ('url') values ('{url}');")
        db.commit()
        cur.close()
        return 'Фото обезьянки успешно добавлено'

    cur.close()
    return 'Данное фото уже есть в базе'

async def delete_photo(url : str, db) -> str:
    cur = db.cursor()
    photo = cur.execute(f"select 1 from photo_monkey where url == '{url}';").fetchone()
    if not photo:
        cur.close()
        return 'Этого фото нет в базе'
    else:
        cur.execute(f"DELETE FROM photo_monkey WHERE url = '{url}';")
        db.commit()
        cur.close()
        return 'Фото успешно удалено'

async def get_random_photo(url_last: str, db) -> str:
    cur = db.cursor()
    photo : tuple|None = cur.execute(f"SELECT url FROM photo_monkey WHERE url != '{url_last}' ORDER BY RANDOM() LIMIT 1;").fetchone()
    if not photo:
        cur.close()
        return None
    else:
        cur.close()
        return photo[0]

async def get_all_photo(db) -> str:
    cur = db.cursor()
    photo = cur.execute(f"select * from photo_monkey;").fetchone()
    cur.close()
    return photo
