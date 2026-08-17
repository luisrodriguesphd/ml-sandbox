# Problem 3: Model Serving / Inference Pipeline

## Overview

A small serving layer that assembles a preprocessing -> model ->
postprocessing pipeline, wraps it with cross-cutting concerns like caching
and retries, and exposes it through one simple call — the shape of a
minimal model-serving API.

## Why these three patterns fit together

- **Builder** assembles the multi-step pipeline object piece by piece.
- **Decorator** layers caching/retry/timing onto the pipeline's `predict`
  call without touching its internals.
- **Facade** hides both of the above behind one method, so a caller just
  gets predictions back.

Together: `Facade.predict()` calls into a `Decorator`-wrapped
`InferencePipeline` that was assembled by the `Builder`.

## Files

| File | Pattern | Summary |
|---|---|---|
| `01_builder.py` | Builder (Creational) | Fluently assemble a preprocessing/model/postprocessing pipeline. |
| `02_decorator.py` | Decorator (Structural) | Add caching, retry, and timing around the pipeline's predict call. |
| `03_facade.py` | Facade (Structural) | Expose one simple `predict()` entry point over the whole subsystem. |

## Requirements *(placeholder — fill in once implemented)*

- Python 3.8+
- No third-party packages required

## How to Run *(placeholder — fill in once implemented)*

```bash
python 01_builder.py
python 02_decorator.py
python 03_facade.py
```
