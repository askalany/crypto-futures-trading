from typing import List

from pydantic import BaseModel


class CancelAllOrdersResponse(BaseModel):
    code: int
    msg: str


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
    positionSide: str
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
    positionSide: str
    positionAmt: str
    updateTime: int


class AccountInfoResponse(BaseModel):
    feeTier: int
    canTrade: bool
    canDeposit: bool
    canWithdraw: bool
    updateTime: int
    multiAssetsMargin: bool
    tradeGroupId: int
    totalInitialMargin: str
    totalMaintMargin: float
    totalWalletBalance: float
    totalUnrealizedProfit: str
    totalMarginBalance: str
    totalPositionInitialMargin: str
    totalOpenOrderInitialMargin: str
    totalCrossWalletBalance: str
    totalCrossUnPnl: float
    availableBalance: float
    maxWithdrawAmount: str
    assets: List[Asset]
    positions: List[Position]
