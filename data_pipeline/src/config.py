import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")


JSON_PATH_BOOK24 = Path("./results/json/book24/book24_2026-01-10T15-56-20+00-00.json")
JSON_PATH_CHITAI_GOROD = Path(
    "results\json\chitai-gorod\chitai-gorod_2026-01-10T15-58-38+00-00.json"
)
JSON_PATH_LABIRINT = Path(
    "results\json\labirint\labirint_2026-01-10T16-01-38+00-00.json"
)
print(DATABASE_URL)
