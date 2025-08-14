import asyncio, time

async def first():
    t0 = time.perf_counter()
    print("first: starting; waiting 5s")
    await asyncio.sleep(5)
    return f"first: finished (total {time.perf_counter()-t0:.2f}s)"

async def second():
    t0 = time.perf_counter()
    print("second: starting; waiting 2s")
    await asyncio.sleep(2)
    return f"second: finished (total {time.perf_counter()-t0:.2f}s)"

async def main():
    print("Running with TaskGroup...")
    # Using TaskGroup to run tasks concurrently
    t0 = time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(first())
        t2 = tg.create_task(second())
    print(t1.result()); print(t2.result())
    print(f"total elapsed: {time.perf_counter()-t0:.2f}s")  # ~5s

if __name__ == "__main__":
    asyncio.run(main())
