import re

from sqlalchemy import text, bindparam
from sqlalchemy.exc import OperationalError
from tqdm import tqdm


def union_group(session, group: list[int]):
    if len(group) <= 1:
        return
    
    def exceq_query(query):
        query = text(query).bindparams(
            bindparam('pub_id', value=group[0]),
            bindparam('ids', value=group[1:], expanding=True)
        )
        try:
            session.execute(query)
        except OperationalError as oe:
            session.rollback()
            print(f"Error: {oe}")
            return False

    ## Добавление новых авторов и удаление у старых
    exceq_query(
        """
            UPDATE PublicationAuthors pa
            LEFT JOIN PublicationAuthors pa_special ON 
                pa_special.publication_id = :pub_id AND 
                pa_special.authors_id = pa.authors_id
            SET pa.publication_id = :pub_id
            WHERE pa.publication_id IN :ids
                AND pa_special.authors_id IS NULL;
        """
    )
    exceq_query(
        """
            DELETE FROM PublicationAuthors WHERE PublicationAuthors.publication_id IN :ids;
        """
    )
    
    ## Изменение привязки Recension
    exceq_query(
        """
            UPDATE Recension
            SET publication_id = :pub_id
            WHERE publication_id IN :ids;
        """
    )

    ## Изменение привязки ISBN
    exceq_query(
        """
            UPDATE ISBN
            SET publication_id = :pub_id
            WHERE publication_id IN :ids;
        """
    )

    ## Изменение привязки PublicationSite
    exceq_query(
        """
            UPDATE PublicationSite
            SET publication_id = :pub_id
            WHERE publication_id IN :ids;
        """
    )


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
