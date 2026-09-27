"""
Factory Method pattern (Creational) — Problem 2: ML Training & Experimentation
Framework.

Decouples "which model to create" from the training code that uses it, by
instantiating different online-capable model types from a config
string/dict rather than hard-coding a specific model class at every call
site.

Example to implement:
    A `create_model(model_type: str, **params)` factory (or a
    `ModelFactory` class) that returns one of several interchangeable
    scikit-learn estimators restricted to ones that support incremental
    training via `partial_fit` — e.g. `SGDClassifier`/`SGDRegressor` (an
    SGD-based linear model), `Perceptron`, a suitable Naive Bayes model
    (`GaussianNB`/`MultinomialNB`), or `MLPClassifier`/`MLPRegressor` used
    incrementally (an "online" neural network/MLP) — selected purely by a
    config value such as `model_type="sgd"`. Every model produced by this
    factory must support `partial_fit(X, y, ...)` — `03_observer.py`'s
    `Trainer` drives a per-batch incremental update loop through it and
    needs every model type to support that call shape (note: most
    classifiers require a `classes=[...]` argument on their *first*
    `partial_fit` call — worth handling consistently across model types).
    The point of this file is the object-creation mechanics, not model
    tuning; see this problem's `INSTRUCTIONS.md` for the full list of
    in-scope estimators (and an optional River equivalent, if you want to
    compare its `learn_one`-style API to scikit-learn's `partial_fit`).

Learning objectives:
    - Implement the Factory Method pattern to centralize and decouple object
      creation from usage.
    - See how this enables swapping models via config alone (e.g. a YAML/CLI
      flag) without touching the training loop in `03_observer.py`.
"""
