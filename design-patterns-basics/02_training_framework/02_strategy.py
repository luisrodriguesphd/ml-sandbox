"""
Strategy pattern (Behavioral) — Problem 2: ML Training & Experimentation
Framework.

Makes an algorithm family (feature scaling, in this example) swappable at
runtime, so the training pipeline can pick between e.g. standardization and
min-max scaling without an if/else ladder scattered through the code.

Example to implement:
    A common `ScalingStrategy` interface with implementations such as
    `StandardScalerStrategy` and `MinMaxScalerStrategy`, injected into a
    `Trainer`/`Pipeline` object that calls `strategy.scale(X)` without
    knowing which concrete strategy it holds. Because `03_observer.py`'s
    `Trainer` processes one incoming batch at a time rather than a fixed
    dataset, each strategy needs to update its scaling statistics
    incrementally too — there's no full dataset to fit against upfront.
    scikit-learn's `StandardScaler`/`MinMaxScaler` both support
    `partial_fit(X)` for exactly this: call it on each new batch (instead of
    a one-shot `fit`) before transforming it. Ties in naturally with the
    repo's existing `linear-regression-feature-scaling` experiment, which
    only had to scale a fixed, fully-available dataset.

Learning objectives:
    - Implement the Strategy pattern to make an algorithm swappable
      independently of the client that uses it.
    - Compare this to the Factory Method in `01_factory_method.py`: Factory
      Method picks *what object to create*, Strategy picks *which
      interchangeable behavior to run*.
"""
