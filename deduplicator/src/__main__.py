import os
import sys
import time
from sqlalchemy.exc import OperationalError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from metaphone import process_books_metaphone
from clear import process_books_name
from deduplicate import process_books_groups


def get_engine(db_retry_attempts=5, db_retry_delay=10):
    """Создает и возвращает движок базы данных. Включает в себя логику попыток"""
    connection_string = os.getenv('DATABASE_URL')

    for attempt in range(db_retry_attempts - 1):
        try:
            return create_engine(connection_string)
        except OperationalError:
            time.sleep(db_retry_delay)
    try:
        return create_engine(connection_string)
    except OperationalError:
        sys.exit(1)


def initialize_database():
    """Инициализация базы данных"""
    engine = get_engine()
    SessionFactory = sessionmaker(bind=engine)
    return SessionFactory()

def metaphone(session):
    if process_books_metaphone(session):
        print("Program finished successfully")
    else:
        print("Program crashed with error")
        sys.exit(1)

def clear(session):
    if process_books_name(session):
        print("Program finished successfully")
    else:
        print("Program crashed with error")
        sys.exit(1)

def deduplicate(session):
    if process_books_groups(session):
        print("Program finished successfully")
    else:
        print("Program crashed with error")
        sys.exit(1)

def main():
    session = initialize_database()
    mode = os.getenv('MODE')
    if mode == 'metaphone':
        metaphone(session)
    if mode == 'clear':
        clear(session)
    if mode == 'deduplicate':
        deduplicate(session)


if __name__ == "__main__":
    main()
