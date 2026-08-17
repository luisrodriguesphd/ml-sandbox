"""
Decorator pattern (Structural) — Problem 3: Model Serving / Inference
Pipeline.

Adds cross-cutting behavior — caching, retry-on-failure, timing — around an
inference/serving call without modifying the call itself, and without the
behaviors depending on each other.

Example to implement:
    Function or class decorators such as `@cache_predictions`, `@retry`, and
    `@log_timing`, stacked on top of the `InferencePipeline.predict()` method
    built in `01_builder.py`, each adding one independent piece of behavior.

Learning objectives:
    - Implement the Decorator pattern to layer behavior onto a callable
      without subclassing or editing its body.
    - Note the relationship to Python's own decorator syntax, and how it
      differs from the class-wrapping "Decorator object" version of the GoF
      pattern.
"""
