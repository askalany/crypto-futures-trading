from concurrent.futures import ThreadPoolExecutor
import itertools
import time

from rich import print

from repo import get_time


def m_2(n: int):
    return pow(n,2)


def main():
    thread_it = True
    a: list[int] = list(range(1000))
    b = [] if thread_it else [m_2(i) for i in a]
    if thread_it:
        with ThreadPoolExecutor() as executor:
            b.extend([i for i in executor.map(m_2, a)])
    print(f"{b=}")


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    t_diff = t1 - t0
    print(f"{t_diff=}")
