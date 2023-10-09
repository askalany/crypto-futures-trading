import asyncio
import datetime


def display_date(loop: asyncio.AbstractEventLoop):
    print(datetime.datetime.now())
    loop.call_later(1, display_date, loop)


loop = asyncio.new_event_loop()
loop.call_soon(display_date, loop)

try:
    loop.run_forever()
finally:
    loop.close()
