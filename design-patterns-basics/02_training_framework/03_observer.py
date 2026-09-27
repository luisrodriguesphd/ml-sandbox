"""
Observer pattern (Behavioral) — Problem 2: ML Training & Experimentation
Framework.

Lets a training loop notify a list of independent subscribers after each
incremental training update — a metrics logger, an early-stopping check, a
checkpoint saver — without the training loop itself knowing what those
subscribers do. This is the same shape as real streaming/online-learning
callback systems, just not tied to a fixed epoch loop over a fixed dataset.

Example to implement:
    A `Trainer` (the subject) that, for each incoming batch, scales it via a
    strategy from `02_strategy.py` and calls a model's
    `partial_fit(X, y, ...)` (see `01_factory_method.py` — every model the
    factory produces supports this call shape) — optionally driven by
    batches sourced from `01_data_ingestion`'s streaming (`FileSource` /
    `stream_files`), or from a simple in-file batch generator if you'd
    rather keep this file self-contained. After each update, the `Trainer`
    notifies a list of `Observer`s (e.g. `MetricsLogger`, `EarlyStopping`,
    `CheckpointSaver`) implementing a common interface such as
    `on_update_end(step, metrics)` — `step` here means "the Nth batch/update
    processed," not "epoch."

Learning objectives:
    - Implement the Observer pattern to decouple a training loop from the
      side effects (logging, stopping, checkpointing) that react to it.
    - Recognize this as the general shape behind streaming/online-ML
      callback systems (e.g. River's own event hooks, or Kafka-consumer-
      style pipelines that call `partial_fit` per message).
"""
