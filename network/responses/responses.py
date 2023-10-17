from dataclasses import dataclass


@dataclass(kw_only=True)
class CancelAllOrdersResponse:
    code: int
    msg: str
