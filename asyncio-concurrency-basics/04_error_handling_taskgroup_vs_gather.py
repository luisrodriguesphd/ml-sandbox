import asyncio

async def worker(name: str, delay: float, fail: bool = False):
    print(f"{name}: start (delay={delay}s, fail={fail})")
    try:
        await asyncio.sleep(delay)
        if fail:
            raise RuntimeError(f"{name}: boom!")
        print(f"{name}: done")
        return f"{name}: ok"
    except asyncio.CancelledError:
        # Show that this task was cancelled due to a sibling failing
        print(f"{name}: cancelled")
        raise

async def run_taskgroup():
    print("\n=== TaskGroup (structured concurrency) ===")
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(worker("ok", 3.0, fail=False))
            tg.create_task(worker("bad", 1.0, fail=True))
        # If both succeeded you'd reach here without exceptions.
    except* RuntimeError as eg:
        # Python 3.11+: ExceptionGroup; siblings auto-cancelled
        print(f"TaskGroup raised ExceptionGroup with {len(eg.exceptions)} RuntimeError(s):")
        for e in eg.exceptions:
            print(f"  - {type(e).__name__}: {e}")
    print("TaskGroup: after block")

async def run_gather_default():
    print("\n=== asyncio.gather (default) ===")
    try:
        # By default, first exception cancels the rest and is raised
        await asyncio.gather(
            worker("ok", 3.0, fail=False),
            worker("bad", 1.0, fail=True),
        )
    except Exception as e:
        print(f"gather raised Exception:\n  - {type(e).__name__}: {e}")

async def run_gather_return_exceptions():
    print("\n=== asyncio.gather(return_exceptions=True) ===")
    results = await asyncio.gather(
        worker("ok", 3.0, fail=False),
        worker("bad", 1.0, fail=True),
        return_exceptions=True,
    )
    for i, r in enumerate(results, start=1):
        if isinstance(r, Exception):
            print(f"result {i}: exception -> {type(r).__name__}: {r}")
        else:
            print(f"result {i}: {r}")

async def run_gather_return_exceptions_with_cancel():
    print("\n=== gather(return_exceptions=True) + manual cancel ===")
    t1 = asyncio.create_task(worker("ok", 3.0, fail=False))
    t2 = asyncio.create_task(worker("to_cancel", 5.0, fail=False))

    # Let them start, then cancel one explicitly
    await asyncio.sleep(1.0)
    t2.cancel()

    results = await asyncio.gather(t1, t2, return_exceptions=True)
    for i, r in enumerate(results, start=1):
        if isinstance(r, BaseException):  # catches CancelledError too
            msg = str(r) or "<no message>"
            print(f"result {i}: exception -> {type(r).__name__}: {msg}")
            # or: print(f"result {i}: exception -> {type(r).__name__}: {r!r}")
        else:
            print(f"result {i}: {r}")

async def main():
    await run_taskgroup()
    await run_gather_default()
    await run_gather_return_exceptions()
    await run_gather_return_exceptions_with_cancel()

if __name__ == "__main__":
    asyncio.run(main())
