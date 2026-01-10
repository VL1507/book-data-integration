from config import JSON_PATH_BOOK24
from json_to_db import load_from_json, dump_to_sql


def main():
    print("Hello from data-pipeline!")

    book_items = load_from_json(path=JSON_PATH_BOOK24)
    print(f"{len(book_items) = }")
    print(dump_to_sql(book_items=book_items))


if __name__ == "__main__":
    main()
