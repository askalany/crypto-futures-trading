from math import ceil, fmod, remainder
from rich import print

bids = [
    ['33766.00', '8.793'],
    ['33760.10', '298.602'],
    ['33756.70', '0.414'],
    ['33746.90', '0.022'],
    ['33734.60', '0.001'],
    ['33710.50', '0.889'],
    ['33705.40', '0.355'],
    ['33700.10', '319.465'],
    ['33700.00', '52.696'],
    ['33681.10', '0.001'],
]
asks = [
    ['33850.00', '31.420'],
    ['33850.80', '0.015'],
    ['33854.40', '322.703'],
    ['33859.30', '0.991'],
    ['33868.10', '195.937'],
    ['33880.30', '0.002'],
    ['33895.20', '195.780'],
    ['33897.20', '0.005'],
    ['33900.00', '0.018'],
    ['33901.80', '0.001'],
]


def round_to_hundreds(price) -> float:
    p = float(price)
    rem = remainder(p, 100)
    return p + 100.0 - rem if rem > 0.0 else p + abs(rem)


def compress_book(book: list[list[str]]):
    result: dict[float, float] = {}
    for b in book:
        p = round_to_hundreds(b[0])
        result[p] = round(result[p] + float(b[1]) if p in result else float(b[1]), 4)
    return result


def main():
    a = compress_book(asks)
    print(f"{a=}")


if __name__ == '__main__':
    main()
