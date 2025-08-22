"""
This example demonstrates how to use asyncio.Queue to optimize task dependencies.

Key improvements over 05_chained_dependencies.py:
1. Reduced total execution time from ~8s to ~5s
2. third() starts immediately after second() completes (~2s mark)
3. No need to wait for first() to finish before starting third()
4. More flexible dependency management using queue-based communication

The queue approach allows tasks to start processing as soon as their dependencies
are available, rather than waiting for all concurrent tasks to complete. This is
particularly useful in scenarios where:
- Some tasks have dependencies while others are independent
- You want to start processing results as soon as they're available
- You have a mix of fast and slow tasks, and don't want the slow tasks to block
  the processing of fast task results

Without a queue (05_chained_dependencies.py):
- first() takes 5s
- second() takes 2s
- third() waits for both to finish (5s) before starting its 3s work
- Total time: ~8s

With a queue (this example):
- first() takes 5s (runs independently)
- second() takes 2s and immediately queues its result
- third() starts at ~2s mark when second()'s result is available
- Total time: ~5s (tasks overlap efficiently)
"""

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

async def main_queue():
    print("\nRunning with Queue...")
    t0 = time.perf_counter()
    queue = asyncio.Queue()

    async def second_with_queue():
        """Wraps second() to put its result in the queue"""
        result = await second()
        await queue.put(result)
        return result

    async def third_with_queue():
        """Wraps third() to get its input from the queue"""
        second_result = await queue.get()
        return await third(second_result)

    async with asyncio.TaskGroup() as tg:
        # Start first() and second() concurrently
        t1 = tg.create_task(first())
        t2 = tg.create_task(second_with_queue())
        # Start third() immediately - it will wait for second's result via queue
        t3 = tg.create_task(third_with_queue())

    print(f"Results:")
    print(f"Task 1: {t1.result()}")
    print(f"Task 2: {t2.result()}")
    print(f"Task 3: {t3.result()}")
    print(f"total elapsed: {time.perf_counter()-t0:.2f}s")

async def main():
    # Run the queue-based implementation
    await main_queue()

if __name__ == "__main__":
    asyncio.run(main())
