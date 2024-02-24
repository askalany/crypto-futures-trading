import asyncio
from rich import print

import ccxt.async_support as ccxt  # link against the asynchronous version of ccxt


async def main():
    exchange = ccxt.binanceusdm(
        {
            'apiKey': '',
            'secret': '',
        }
    )  # default id
    exchange.set_sandbox_mode(True)  # enable sandbox mode
    markets = await exchange.load_markets()  # load
    result = await exchange.fetch_l2_order_book("BTC/USDT", limit = 10)
    print(f"{result=}")
    await exchange.close()


if __name__ == "__main__":
    asyncio.run(main())
