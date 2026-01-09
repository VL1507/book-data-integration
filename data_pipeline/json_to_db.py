import json
from pathlib import Path

from db_conn import Session

from config import JSON_PATH_BOOK24
from json_model import BookSitesCrawlerItem


def load_from_json(path: Path) -> list[BookSitesCrawlerItem]:
    with open(file=path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    items = []
    for row in data:
        item = BookSitesCrawlerItem(**row)
        items.append(item)

    return items


print(load_from_json(path=JSON_PATH_BOOK24))
