from strategy.riski import get_margin_ratio


def main():
    mr = get_margin_ratio() * 100
    print(f"{mr=}")


if __name__ == "__main__":
    main()
