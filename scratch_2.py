import asyncio
import time

from binance.error import ClientError
from binance.um_futures import UMFutures
from rich import print

from consts import BASE_URL, KEY, SECRET

client = UMFutures(key=KEY, secret=SECRET, base_url=BASE_URL)


async def get_mark_price_async(symbol):
    try:
        return client.mark_price(symbol=symbol)["markPrice"]
    except ClientError as e:
        print(e)

async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')
    
async def main():
    try:
        t0 = time.perf_counter()
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(get_mark_price_async(symbol="BTCUSDT"))
            task2 = tg.create_task(get_mark_price_async(symbol="ETHUSDT"))
        print(f"BTC Mark Price = {task1.result()}")
        print(f"ETH Mark Price = {task2.result()}")
        event = asyncio.Event()
        waiter_task = asyncio.create_task(waiter(event))
        event.set()
        await waiter_task
        t1 = time.perf_counter()
        t_diff = t1 - t0
        print(f"{t_diff} seconds")
    except asyncio.CancelledError:
        print("cancelled")


if __name__ == "__main__":
    asyncio.run(main())
