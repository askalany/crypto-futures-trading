from enum import Enum
from typing import Optional

from pydantic import BaseModel

from data.enums import (
    STPMODE,
    PositionSide,
    PriceMatch,
    ResponseType,
    TimeInForce,
    WorkingType,
)


class NewOrderRequest(BaseModel):
    symbol: str  # ,YES
    side: Enum  # ,YES
    positionSide: Optional[PositionSide]  # ,NO
    type: Enum  # ,YES
    timeInForce: Optional[TimeInForce]  # ,NO
    quantity: Optional[float]  # ,NO
    reduceOnly: Optional[str]  # ,NO
    price: Optional[float]  # ,NO
    newClientOrderId: Optional[str]  # ,NO
    stopPrice: Optional[float]  # ,NO
    closePosition: Optional[str]  # ,NO
    activationPrice: Optional[float]  # ,NO
    callbackRate: Optional[float]  # ,NO
    workingType: Optional[WorkingType]  # ,NO
    priceProtect: Optional[str]  # ,NO
    newOrderRespType: Optional[ResponseType]  # ,NO
    priceMatch: Optional[PriceMatch]  # ,NO
    selfTradePreventionMode: Optional[STPMODE]  # ,NO
    goodTillDate: Optional[int]  # ,NO
    recvWindow: Optional[int]  # ,NO
    timestamp: int  # ,YES
