from config import JSON_PATH_BOOK24, JSON_PATH_CHITAI_GOROD, JSON_PATH_LABIRINT
from json_to_db import load_from_json, dump_to_sql

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-7s | %(filename)s:%(lineno)d | %(name)-20s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    print("Hello from data-pipeline!")

    book_items = load_from_json(path=JSON_PATH_LABIRINT)
    print(f"{len(book_items) = }")
    print(dump_to_sql(book_items=book_items))


if __name__ == "__main__":
    main()
