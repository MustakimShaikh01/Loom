import asyncio
import random

async def background_worker(name, delay):
    for i in range(5):
        await asyncio.sleep(delay)
        print(f"[worker {name}] tick {i}")
    return f"{name}-done"

async def main():
    # spawn background tasks
    tasks = []
    tasks.append(asyncio.create_task(background_worker('A', 0.9)))
    tasks.append(asyncio.create_task(background_worker('B', 1.5)))
    # simulate some work in main
    for i in range(3):
        print(f"[main] step {i}")
        await asyncio.sleep(0.7)
    # wait for all tasks to finish
    await asyncio.gather(*tasks)
    print('example complete')
