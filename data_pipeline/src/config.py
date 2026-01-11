import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


JSON_PATH_BOOK24 = Path("results\book24.json")
JSON_PATH_CHITAI_GOROD = Path("results\chitai-gorod.json")
JSON_PATH_LABIRINT = Path("results\labirint\.json")
print(DATABASE_URL)
