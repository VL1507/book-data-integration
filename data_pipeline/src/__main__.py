from config import JSON_PATH_BOOK24, JSON_PATH_CHITAI_GOROD, JSON_PATH_LABIRINT, LOGGING_LEVEL
from json_to_db import load_from_json, dump_to_sql

import logging

logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s | %(levelname)-7s | %(filename)s:%(lineno)d | %(name)-20s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(name=__name__)


def main():
    print("Hello from data-pipeline!")

    for json_path in (JSON_PATH_BOOK24, JSON_PATH_CHITAI_GOROD, JSON_PATH_LABIRINT):
        book_items = load_from_json(path=json_path)
        logger.info(f"{len(book_items) = }")
        print(dump_to_sql(book_items=book_items))


if __name__ == "__main__":
    main()
