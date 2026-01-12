import re

from fonetika.metaphone import RussianMetaphone
from sqlalchemy import text, inspect
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
    return RussianMetaphone(reduce_word=False, reduce_phonemes=True, reduce_vowels=True).transform(word)

def column_exists(session, table_name, column_name):
    """Проверяет, существует ли колонка в таблице"""
    inspector = inspect(session.bind)
    columns = inspector.get_columns(table_name)
    return any(col['name'] == column_name for col in columns)

def process_books_name(session) -> bool:
    '''
    Функция преобразования названия книг в их метафоны с использованием библиотеки fonetika
    :param session: SQLAlchemy активная сессия базы данных
    :return: Результат работы функции
    '''
    try:
        if not column_exists(session, 'Publication', "metaphone"):
            session.execute(text("""
                        ALTER TABLE Publication 
                        ADD COLUMN metaphone VARCHAR(255) DEFAULT NULL
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

    batch_size = int(len(rows)**0.5)

    for t, row in tqdm(enumerate(rows)):
        pub_id, name = row
        try:
            session.execute(text("""
                                UPDATE Publication 
                                SET metaphone = :metaphone 
                                WHERE id = :pub_id
                            """), {
                'metaphone': process_phonetic(name),
                'pub_id': pub_id
            })
        except OperationalError as oe:
            continue
        if t % batch_size == 0:
            session.commit()
    session.commit()
    return True
