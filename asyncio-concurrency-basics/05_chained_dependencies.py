import asyncio, time

async def first():
    t0 = time.perf_counter()
    print("first: starting; waiting 5s")
    await asyncio.sleep(5)
    result = f"first: finished (total {time.perf_counter()-t0:.2f}s)"
    print(f"first returning: {result}")
    return result

async def second():
    t0 = time.perf_counter()
    print("second: starting; waiting 2s")
    await asyncio.sleep(2)
    result = f"second: finished (total {time.perf_counter()-t0:.2f}s)"
    print(f"second returning: {result}")
    return result

async def third(second_result):
    t0 = time.perf_counter()
    print(f"third: starting with input '{second_result}'; waiting 3s")
    await asyncio.sleep(3)
    result = f"third: finished (total {time.perf_counter()-t0:.2f}s)"
    print(f"third returning: {result}")
    return result

async def main_taskgroup():
    print("\nRunning with TaskGroup...")
    t0 = time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(first())
        t2 = tg.create_task(second())
    # At this point both first() and second() are complete
    t3 = await third(t2.result())
    print(f"Results:")
    print(f"Task 1: {t1.result()}")
    print(f"Task 2: {t2.result()}")
    print(f"Task 3: {t3}")
    print(f"total elapsed: {time.perf_counter()-t0:.2f}s")

async def main_gather():
    print("\nRunning with gather...")
    t0 = time.perf_counter()
    r1, r2 = await asyncio.gather(first(), second())
    # At this point both first() and second() are complete
    r3 = await third(r2)
    print(f"Results:")
    print(f"Task 1: {r1}")
    print(f"Task 2: {r2}")
    print(f"Task 3: {r3}")
    print(f"total elapsed: {time.perf_counter()-t0:.2f}s")

async def main():
    # Run both approaches to compare
    await main_taskgroup()
    await main_gather()

if __name__ == "__main__":
    asyncio.run(main())
