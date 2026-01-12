import re

from fonetika.metaphone import RussianMetaphone
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from tqdm import tqdm


def process_phonetic(word):
    '''
    Возвращает звуковое представление строки без знаков препинания

    :param word: Слово, которое необходимо преобразовать
    :return: Звуковое представление слова
    '''
    word = re.sub(r'[^А-я0-9\s]', '', word)
    word = re.sub(r'\s+', ' ', word)
    word = word.strip()
    return RussianMetaphone().transform(word)


def process_books_name(session) -> bool:
    '''
    Функция преобразования названия книг в их метафоны с использованием библиотеки fonetika
    :param session: SQLAlchemy активная сессия базы данных
    :return: Результат работы функции
    '''
    try:
        session.execute(text("""
                    ALTER TABLE Publication 
                    ADD COLUMN IF NOT EXISTS metaphone VARCHAR(30) DEFAULT NULL
                """))
        session.commit()
    except OperationalError as oe:
        session.rollback()
        print(f"Error: {oe}")
        return False

    try:
        result = session.execute(text("SELECT id, name FROM Publication WHERE metaphone IS NULL"))
        rows = result.fetchall()
    except OperationalError as oe:
        session.rollback()
        print(f"Error: {oe}")
        return False

    batch_size = int(len(result)**0.5)

    for t, id, name in tqdm(enumerate(rows)):
        try:
            session.execute(text("""
                                UPDATE Publication 
                                SET metaphone = :metaphone 
                                WHERE id = :id
                            """), {
                'metaphone': process_phonetic(name),
                'city_id': id
            })
        except OperationalError as oe:
            continue
        if t % batch_size == 0:
            session.commit()
    session.commit()
    return True
