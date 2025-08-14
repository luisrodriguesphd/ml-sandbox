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
    print("Running sequentially with await...")
    # Running tasks sequentially
    t0 = time.perf_counter()
    r1 = await first()      # runs fully, then...
    r2 = await second()     # ...this runs
    print(r1); print(r2)
    print(f"total elapsed: {time.perf_counter()-t0:.2f}s")  # ~7s

if __name__ == "__main__":
    asyncio.run(main())
