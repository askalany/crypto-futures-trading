from functools import cache


@cache
def get_orders(min_order, multiplier, orders_num):
    orders = [min_order]
    [orders.append(round(multiplier * orders[i - 1], 3)) for i in range(1, orders_num)]
    return orders


def get_optimized_orders(total: float, orders_num: int, min_order: float)-> list[float]:
    if orders_num <= 0:
        raise ValueError("Length must be greater than 0")
    if min_order > total:
        raise ValueError(f"Total {total} must be greater than {min_order}")

    common_ratio = (total / min_order) ** (1.0 / (float(orders_num) - 1.0))
    series = [common_ratio ** float(i) for i in range(orders_num)]
    scaled_series = [max(min_order, num / sum(series) * total) for num in series]

    # Adjust the last element to make the sum exactly equal to or just less than the total
    scaled_series[-1] += total - sum(scaled_series)

    return scaled_series
