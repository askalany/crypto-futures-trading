import json
from base.models.FileInput import FileInput


def get_inputs_from_file(
    file_name: str = "my_trading.json",
) -> FileInput:
    with open(file=file_name, mode="r", encoding="utf-8-sig") as f:
        read = f.read()
        data = json.loads(read)
        return FileInput(**data)
