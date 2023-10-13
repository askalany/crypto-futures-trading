import datetime
import time

from rich import print


def get_timestamp():
    return int(time.time() * 1000)


def get_date_and_time():
    return f"date and time = {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"


def print_date_and_time() -> None:
    print(get_date_and_time())
