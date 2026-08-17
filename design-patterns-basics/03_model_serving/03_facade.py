"""
Facade pattern (Structural) — Problem 3: Model Serving / Inference Pipeline.

Exposes one simple `predict()` entry point that hides the multi-step
subsystem (preprocessing, model, postprocessing, plus the caching/retry/
timing layers) assembled in `01_builder.py` and `02_decorator.py`, so a
caller doesn't need to know the pipeline was built at all.

Example to implement:
    A `ModelService` facade with a single public method, e.g.
    `predict(raw_input)`, that internally builds (or receives) the
    `InferencePipeline` from `01_builder.py`, wrapped with the decorators
    from `02_decorator.py`, and returns just the final prediction.

Learning objectives:
    - Implement the Facade pattern to give consumers a minimal, stable
      surface over a more complex, multi-pattern subsystem.
    - See how Builder, Decorator, and Facade compose into one deployable
      "serving" unit — the payoff of this problem's three patterns together.
"""
