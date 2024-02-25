import json
import os.path
from typing import Optional

from base.models.FileInput import FileInput
from model import DB


def get_inputs_from_file(file_name: str = "my_trading.json") -> Optional[FileInput]:
    try:
        with open(file_name, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            return FileInput(**data) if data else None
    except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
        print(f"Error reading or decoding the file {file_name}: {e}")
        return None


def get_db_from_file() -> Optional[DB]:
    try:
        file_name: str = "db.json"

        with open(file_name, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            return DB(**data) if data else None
    except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
        print(f"Error reading or decoding the file {file_name}: {e}")
        return None


def write_to_db_file(balance: float, file_name: str = "db.json"):
    dictionary = {"balance": balance}
    json_object = json.dumps(dictionary, indent=4)
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
