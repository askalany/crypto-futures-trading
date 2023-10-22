from typing import Union


def f_money(amount, color: Union[None, str] = None) -> str:
    formatted_amount = "{:,.2f}".format(amount)
    if color:
        return f"[{color}]{formatted_amount}"
    if amount > 0:
        return f"[green]{formatted_amount}[/green]"
    elif amount < 0:
        return f"[red]{formatted_amount}[/red]"
    else:
        return formatted_amount


def f_pct(percentage: float) -> str:
    formatted_percentage = f"{percentage:.2f}%"
    if percentage > 0.0:
        return f"[green]{formatted_percentage}[/green]"
    elif percentage < 0.0:
        return f"[red]{formatted_percentage}[/red]"
    else:
        return formatted_percentage
