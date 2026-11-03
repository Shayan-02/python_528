import asyncio
import time


async def call_api_a():
    await asyncio.sleep(2)
    print("API A done")


async def call_api_b():
    await asyncio.sleep(3)
    print("API B done")


async def call_api_c():
    await asyncio.sleep(1)
    print("API C done")


async def main():
    start = time.time()
    await asyncio.gather(call_api_a(), call_api_b(), call_api_c())
    print(f"Total time: {time.time() - start:.1f}s")


asyncio.run(main())
