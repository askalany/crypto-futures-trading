from itertools import islice
from typing import Any
from typing import Generator


def batched(iterable, n) -> Generator[list[Any], None, None]:
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch


def batched_lists(iterable, n) -> list[list[Any]]:
    return list(batched(iterable=iterable, n=n))
