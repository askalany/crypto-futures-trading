import datetime
import time

from rich import print


def get_timestamp():
    return int(time.time() * 1000)


def get_date_and_time() -> str:
    return f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
