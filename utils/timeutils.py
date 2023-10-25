import datetime


def get_date_and_time() -> str:
    return f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
