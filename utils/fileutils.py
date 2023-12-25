import json
from typing import Optional

from base.models.FileInput import FileInput


def get_inputs_from_file(file_name: str = "my_trading.json") -> Optional[FileInput]:
    try:
        with open(file_name, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            return FileInput(**data) if data else None
    except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
        print(f"Error reading or decoding the file {file_name}: {e}")
        return None
