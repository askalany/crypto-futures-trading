#!/usr/bin/env python
from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Asset(BaseModel):
    asset: str
    walletBalance: str
    unrealizedProfit: str
    marginBalance: str
    maintMargin: str
    initialMargin: str
    positionInitialMargin: str
    openOrderInitialMargin: str
    maxWithdrawAmount: str
    crossWalletBalance: str
    crossUnPnl: str
    availableBalance: str
    updateTime: int


class Position(BaseModel):
    symbol: str
    positionAmt: str
    initialMargin: str
    maintMargin: str
    unrealizedProfit: str
    positionInitialMargin: str
    openOrderInitialMargin: str
    leverage: str
    isolated: bool
    positionSide: str
    entryPrice: str
    breakEvenPrice: str
    maxQty: str
    updateTime: int


class AccountResponse(BaseModel):
    assets: List[Asset]
    positions: List[Position]
    canDeposit: bool
    canTrade: bool
    canWithdraw: bool
    feeTier: int
    updateTime: int


class PositionInformation(BaseModel):
    symbol: str
    positionAmt: str
    entryPrice: str
    breakEvenPrice: str
    markPrice: str
    unRealizedProfit: str
    liquidationPrice: str
    leverage: str
    maxQty: str
    marginType: str
    isolatedMargin: str
    isAutoAddMargin: str
    positionSide: str
    updateTime: int


class PositionInformationResponse(BaseModel):
    positionInformationList: List[PositionInformation]


class Balance(BaseModel):
    accountAlias: str
    asset: str
    balance: str
    withdrawAvailable: str
    crossWalletBalance: str
    crossUnPnl: str
    availableBalance: str
    updateTime: int


class AccountBalanceResponse(BaseModel):
    balanceList: List[Balance]


class OrderBookResponse(BaseModel):
    lastUpdateId: int
    symbol: str
    pair: str
    E: int
    T: int
    bids: List[List[float]]
    asks: List[List[float]]
