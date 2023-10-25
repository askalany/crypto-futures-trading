from data.enums import PositionSide
from pydantic import BaseModel


class ListenKeyResponse(BaseModel):
    listenKey: str


class MarkPriceResponse(BaseModel):
    symbol: str
    markPrice: float
    indexPrice: float
    estimatedSettlePrice: float
    lastFundingRate: float
    nextFundingTime: int
    interestRate: float
    time: int


class PositionInformationResponse(BaseModel):
    symbol: str
    positionAmt: float
    entryPrice: float
    breakEvenPrice: float
    markPrice: float
    unRealizedProfit: float
    liquidationPrice: float
    leverage: int
    maxNotionalValue: float
    marginType: str
    isolatedMargin: float
    isAutoAddMargin: bool
    positionSide: PositionSide
    notional: float
    isolatedWallet: str
    updateTime: int


class Asset(BaseModel):
    asset: str
    walletBalance: str
    unrealizedProfit: str
    marginBalance: str
    maintMargin: str
    initialMargin: str
    positionInitialMargin: str
    openOrderInitialMargin: str
    crossWalletBalance: str
    crossUnPnl: str
    availableBalance: str
    maxWithdrawAmount: str
    marginAvailable: bool
    updateTime: int


class Position(BaseModel):
    symbol: str
    initialMargin: str
    maintMargin: str
    unrealizedProfit: str
    positionInitialMargin: str
    openOrderInitialMargin: str
    leverage: str
    isolated: bool
    entryPrice: str
    maxNotional: str
    bidNotional: str
    askNotional: str
    positionSide: PositionSide
    positionAmt: str
    updateTime: int
