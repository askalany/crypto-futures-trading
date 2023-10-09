import asyncio
import time


def say_after(delay, what):
    if what == "hello":
        raise ValueError(f"say_after can't say {what}")
    time.sleep(delay)
    print(what)


async def say_after_async(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    async_it = True
    t0 = time.perf_counter()
    if async_it:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(say_after_async(1, "hello"))
            task2 = tg.create_task(say_after_async(1, "world"))
        print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")
    else:
        say_after(1, "hello")
        say_after(1, "world")
    t1 = time.perf_counter()
    t_diff = t1 - t0
    print(f"{t_diff} seconds")


if __name__ == "__main__":
    asyncio.run(main())
