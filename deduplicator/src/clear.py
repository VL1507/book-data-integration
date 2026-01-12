import re

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from tqdm import tqdm


def process_word(word):
    '''
    Очищает слово от "мусора"

    :param word: Слово, которое необходимо преобразовать
    :return: Очищенная версия слова
    '''
    bad_words = ['Манга', 'Новелла', 'Манхва', 'Подарочное издание', 'Официальный мерч', 'Тату', 'Роман', 'Артбук', 'Сборник', 'Повесть', '"', '«', '»', "'"]
    bad_words.extend([x.lower() for x in bad_words])
    word = re.sub(r'\(#([1-9])\)', lambda m: f'№{m.group(1)}', word)
    word = re.sub(r'\((?!Не\))(?!не\))[^)]*\)', '', word)
    word = re.sub(r'#[^ ]*', '', word)
    word = re.sub(r'\+[^$]*', '', word)
    for b in bad_words:
        word = word.replace(b, '')
    while '..' in word or '  ' in word:
        word = re.sub(r'\s+', ' ', word)
        word = re.sub(r'(.)+', '.', word)
    word = word.strip(' .,|:;')
    return word


def process_books_name(session) -> bool:
    '''
    Функция преобразования названия книг в их очищенную версию
    :param session: SQLAlchemy активная сессия базы данных
    :return: Результат работы функции
    '''
    try:
        result = session.execute(text("SELECT id, name FROM Publication"))
        rows = result.fetchall()
    except OperationalError as oe:
        session.rollback()
        print(f"Error: {oe}")
        return False

    batch_size = int(len(rows) ** 0.5)

    for t, row in tqdm(enumerate(rows)):
        pub_id, name = row
        try:
            session.execute(text("""
                                UPDATE Publication 
                                SET name = :name 
                                WHERE id = :pub_id
                            """), {
                'name': process_word(name),
                'pub_id': pub_id
            })
        except OperationalError as oe:
            continue
        if t % batch_size == 0:
            session.commit()
    session.commit()
    return True
