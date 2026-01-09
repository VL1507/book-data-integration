import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


JSON_PATH_BOOK24 = Path("./results/json/book24/book24_2026-01-04T12-03-51+00-00.json")
JSON_PATH_CHITAI_GOROD = Path(
    "/results/json/chitai-gorod/chitai-gorod_2026-01-04T12-08-50+00-00.json"
)
JSON_PATH_LABIRINT = Path(
    "/results/json/labirint/labirint_2026-01-04T11-52-01+00-00.json"
)
print(DATABASE_URL)