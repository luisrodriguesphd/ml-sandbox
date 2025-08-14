# Asyncio Concurrency Basics

Minimal, side-by-side examples showing **sequential** vs **concurrent** async execution in Python:

1. `01_sequential_await.py` — runs two coroutines one after the other (~7s total).
2. `02_taskgroup_concurrent.py` — runs both concurrently with `asyncio.TaskGroup` (~5s total).
3. `03_gather_concurrent.py` — runs both concurrently with `asyncio.gather` (~5s total).
4. `04_error_handling_taskgroup_vs_gather.py` — compares **error propagation & cancellation** in `TaskGroup` vs `gather` (with and without `return_exceptions=True`).

> Context: This repo’s experiments are small, focused, and reproducible. This one complements ML service work by clarifying when async I/O lifts throughput without extra processes or threads. 
>
> See the main repo’s *Available Experiments* section for how items are listed. 

---

## Goals

- Understand the event loop and why **`await`** enables concurrency for **I/O-bound** tasks.
- Compare **structured concurrency** (`TaskGroup`, Python 3.11+) vs **`gather`**.
- Measure wall-clock differences between sequential and concurrent execution.
- See how **failures** cancel sibling tasks and how exceptions are surfaced by each pattern.

---

## Requirements

- Python **3.11+** (recommended) for `asyncio.TaskGroup`.
  - On Python **3.8–3.10**, run `01_...` and `03_...` (skip `02_...` or replace with `gather`).
- No third-party packages required.

---

## Project Structure

```yaml
asyncio-concurrency-basics/
├─ 01_sequential_await.py
├─ 02_taskgroup_concurrent.py
├─ 03_gather_concurrent.py
├─ 04_error_handling_taskgroup_vs_gather.py
└─ README.md
```

Each script is self-contained and executable.

---

## How to Run

From this folder:

```bash
# Run sequential version (≈ 7s total: 5s + 2s)
python 01_sequential_await.py

# Run TaskGroup version (≈ 5s total, tasks overlap)
python 02_taskgroup_concurrent.py

# Run gather version (≈ 5s total, tasks overlap)
python 03_gather_concurrent.py

# Compare error handling & cancellation behavior
python 04_error_handling_taskgroup_vs_gather.py
```

Expected console output pattern (times will vary slightly):

```yaml
Running sequentially with await...
first: starting; waiting 5s
second: starting; waiting 2s
first: finished (total 4.99s)
second: finished (total 2.00s)
total elapsed: 7.00s

Running with TaskGroup...
first: starting; waiting 5s
second: starting; waiting 2s
first: finished (total 4.99s)
second: finished (total 2.00s)
total elapsed: 4.99s

Running with asyncio.gather...
first: starting; waiting 5s
second: starting; waiting 2s
first: finished (total 5.01s)
second: finished (total 2.01s)
total elapsed: 5.01s
```

For `04_error_handling_taskgroup_vs_gather.py`, you’ll see:
- `TaskGroup`: failing task raises → sibling is **cancelled** → you catch an **ExceptionGroup**.
- `gather` (default): failing task raises → sibling **cancelled** → `gather` raises the **first exception**.
- `gather(return_exceptions=True)`: returns a **list mixing normal results and exception objects**. Siblings are **not cancelled** just because one fails (so you’ll typically see a `RuntimeError` for the failing task and a normal result for the other). If you cancel a task manually, you’ll get a `CancelledError` object in the results (it may not subclass `Exception`, but subclasses `BaseException` and have an empty message, so use `isinstance(x, BaseException)` and `print type(x).__name__ or {x!r})`.
