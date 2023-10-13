from itertools import islice
from typing import Any


def batched(iterable, n):
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def batched_lists(iterable, n) -> list[list[Any]]:
    b = batched(iterable=iterable, n=n)
    return [list(i) for i in b]
