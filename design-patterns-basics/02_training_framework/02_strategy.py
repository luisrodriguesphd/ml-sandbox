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
    knowing which concrete strategy it holds.
    Ties in naturally with the repo's existing
    `linear-regression-feature-scaling` experiment.

Learning objectives:
    - Implement the Strategy pattern to make an algorithm swappable
      independently of the client that uses it.
    - Compare this to the Factory Method in `01_factory_method.py`: Factory
      Method picks *what object to create*, Strategy picks *which
      interchangeable behavior to run*.
"""
