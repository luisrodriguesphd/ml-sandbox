"""
Observer pattern (Behavioral) — Problem 2: ML Training & Experimentation
Framework.

Lets a training loop notify a list of independent subscribers after each
epoch — a metrics logger, an early-stopping check, a checkpoint saver —
without the training loop itself knowing what those subscribers do. This
mirrors real callback systems such as Keras/PyTorch Lightning callbacks.

Example to implement:
    A `Trainer` (the subject) that calls a toy model's
    `fit(X, y, epochs: int)` (see `01_factory_method.py` — every model the
    factory produces supports this call shape) to run a *simulated* epoch
    loop (fake or randomly-generated metrics each iteration — no real
    gradient-based training), and, after each epoch, notifies a list of
    `Observer`s (e.g. `MetricsLogger`, `EarlyStopping`, `CheckpointSaver`)
    implementing a common `on_epoch_end(epoch, metrics)` interface. The
    `Trainer` can also use scaling strategies from `02_strategy.py`.

Learning objectives:
    - Implement the Observer pattern to decouple a training loop from the
      side effects (logging, stopping, checkpointing) that react to it.
    - Recognize this as the general shape behind ML framework callback APIs.
"""
