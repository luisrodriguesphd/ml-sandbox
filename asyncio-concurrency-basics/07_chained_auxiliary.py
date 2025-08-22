"""
This example demonstrates an alternative to the queue-based dependency handling
shown in 06_queue_dependencies.py, using an auxiliary function to chain dependent
tasks together.

Key differences from the queue approach:
1. Simpler implementation - no queue management needed
2. More explicit dependency chain
3. BUT less flexible for complex dependency patterns
4. AND potentially less efficient for certain scenarios:
   - Can't start third() independently in the TaskGroup
   - May block other tasks in more complex scenarios
   - Harder to handle dynamic dependencies or fan-out patterns

The main tradeoff is simplicity vs flexibility:
- Auxiliary function: Better for simple, static dependencies
- Queue approach: Better for complex, dynamic dependencies or when you need
  to decouple the producer (second) from the consumer (third)
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

async def main_auxiliary():
    print("\nRunning with auxiliary function...")
    t0 = time.perf_counter()

    async def second_and_third():
        """Chains second() and third() together"""
        second_result = await second()
        third_result = await third(second_result)
        return second_result, third_result

    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(first())
        # second and third are chained together as one task
        t23 = tg.create_task(second_and_third())

    # Unpack the results
    second_result, third_result = t23.result()
    
    print(f"Results:")
    print(f"Task 1: {t1.result()}")
    print(f"Task 2: {second_result}")
    print(f"Task 3: {third_result}")
    print(f"total elapsed: {time.perf_counter()-t0:.2f}s")

async def main():
    # Run the auxiliary function implementation
    await main_auxiliary()

if __name__ == "__main__":
    asyncio.run(main())
