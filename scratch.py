import time

from rich import print

from repo import get_time

if __name__ == "__main__":
    server_time = get_time()
    system_time = round(time.time() * 1000)
    time_difference = server_time - system_time
    deviation = float((float(time_difference) / float(system_time)) * 100.0)
    print(f"{server_time=}, {system_time=}, {time_difference=}. {deviation=}")
    print()
