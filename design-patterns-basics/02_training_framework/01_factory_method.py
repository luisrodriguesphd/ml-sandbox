"""
Factory Method pattern (Creational) — Problem 2: ML Training & Experimentation
Framework.

Decouples "which model to create" from the training code that uses it, by
instantiating different model types from a config string/dict rather than
hard-coding a specific model class at every call site.

Example to implement:
    A `create_model(model_type: str, **params)` factory (or a
    `ModelFactory` class) that returns one of several interchangeable *toy*
    model stand-ins — e.g. `LinearRegressionModel`, `RandomForestModel` —
    each a small pure-Python class with a trivial/simulated
    `fit(X, y, epochs: int)`/`predict` interface (no real ML library),
    selected purely by a config value such as `model_type="random_forest"`.
    The `epochs` parameter is required on every model produced by this
    factory — `03_observer.py`'s `Trainer` drives a simulated per-epoch
    loop through it and needs every model type to support that call shape,
    however fake the underlying training is. The point of this file is the
    object-creation mechanics, not training correctness; see this problem's
    `INSTRUCTIONS.md` for why no ML library is used here.

Learning objectives:
    - Implement the Factory Method pattern to centralize and decouple object
      creation from usage.
    - See how this enables swapping models via config alone (e.g. a YAML/CLI
      flag) without touching the training loop in `03_observer.py`.
"""
