import json
from pathlib import Path

from db_conn import Session


from json_model import BookSitesCrawlerItem


def load_from_json(path: Path) -> list[BookSitesCrawlerItem]:
    with open(file=path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    items = []
    for row in data:
        # Создаём экземпляр датакласса, передавая значения из словаря
        # dataclass автоматически обработает типы и значения по умолчанию (None)
        item = BookSitesCrawlerItem(**row)
        items.append(item)

    return items

print(load_from_json(Path("./results/json/book24/book24_2026-01-04T12-03-51+00-00.json")))
