import re

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from tqdm import tqdm


def union_group(session, group: list[int]):
    if len(group) <= 1:
        return
    
    params = {f"id{i}": id_val for i, id_val in enumerate(group[1:])}
    params['pub_id'] = group[0]
    placeholders = ", ".join([f":id{i}" for i in range(len(group[1:]))])
    
    ## Добавление новых авторов и удаление у старых
    try:
        result = session.execute(text(f"""
                                UPDATE PublicationAuthors pa
                                LEFT JOIN PublicationAuthors pa_special ON 
                                    pa_special.publication_id = :pub_id AND 
                                    pa_special.authors_id = pa.authors_id
                                SET pa.publication_id = :pub_id
                                WHERE pa.publication_id IN ({placeholders})
                                AND pa_special.authors_id IS NULL;
                                DELETE FROM PublicationAuthors WHERE PublicationAuthors.publication_id IN ({placeholders});
                            """), 
                            params
                            )
    except OperationalError as oe:
        session.rollback()
        print(f"Error: {oe}")
        return False
    
    ## Изменение привязки рецензий
    try:
        result = session.execute(text(f"""
                                UPDATE Recension
                                SET publication_id = :pub_id
                                WHERE publication_id IN ({placeholders});
                            """), 
                            params
                            )
    except OperationalError as oe:
        session.rollback()
        print(f"Error: {oe}")
        return False

    ## Изменение привязки ISBN
    try:
        result = session.execute(text(f"""
                                UPDATE ISBN
                                SET publication_id = :pub_id
                                WHERE publication_id IN ({placeholders});
                            """), 
                            params
                            )
    except OperationalError as oe:
        session.rollback()
        print(f"Error: {oe}")
        return False

    ## Изменение привязки PublicationSite
    try:
        result = session.execute(text(f"""
                                UPDATE PublicationSite
                                SET publication_id = :pub_id
                                WHERE publication_id IN ({placeholders});
                            """), 
                            params
                            )
    except OperationalError as oe:
        session.rollback()
        print(f"Error: {oe}")
        return False


def process_books_groups(session) -> bool:
    '''
    Функция группировки книг по названию
    :param session: SQLAlchemy активная сессия базы данных
    :return: Результат работы функции
    '''
    try:
        result = session.execute(text(
        """
        WITH cte AS (
            SELECT 
                DENSE_RANK() OVER (ORDER BY metaphone) AS mphone_id,
                COUNT(*) OVER w AS cnt,
                p.*
            FROM Publication p
            WINDOW w AS (PARTITION BY p.metaphone)
        )
        SELECT GROUP_CONCAT(id) as id FROM cte
        WHERE cnt > 1 AND metaphone != ""
        GROUP BY mphone_id
        ORDER BY mphone_id;
        """
            ))
        groups = result.fetchall()
    except OperationalError as oe:
        session.rollback()
        print(f"Error: {oe}")
        return False

    groups = [list(map(int, x[0].split(','))) for x in groups]

    for t, group in tqdm(enumerate(groups)):
        union_group(session, group)
        session.commit()
    return True
