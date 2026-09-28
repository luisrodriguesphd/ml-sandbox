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

from typing import Any, Callable, Protocol


# Implementation 1: A simple factory function that returns a model instance based on the
# provided model_type string. This is a straightforward approach, but it can become
# unwieldy as the number of model types increases.
def create_model_from_config(model_type: str, **params) -> Any:
    """Factory function that creates and returns a model instance based on the model_type."""
    if model_type == "sgdclassifier":
        from sklearn.linear_model import SGDClassifier

        return SGDClassifier(**params)
    elif model_type == "sgdregressor":
        from sklearn.linear_model import SGDRegressor

        return SGDRegressor(**params)
    elif model_type == "perceptron":
        from sklearn.linear_model import Perceptron

        return Perceptron(**params)
    elif model_type == "naive_bayes":
        from sklearn.naive_bayes import GaussianNB

        return GaussianNB(**params)
    elif model_type == "mlpclassifier":
        from sklearn.neural_network import MLPClassifier

        return MLPClassifier(**params)
    elif model_type == "mlpregressor":
        from sklearn.neural_network import MLPRegressor

        return MLPRegressor(**params)
    else:
        raise ValueError(f"Unknown model type: {model_type}")


# Implementation 2: A more structured approach using a ModelFactory class.
# This encapsulates the factory logic and provides additional utility methods for managing model types.
class ModelFactory:
    """Factory class that creates and returns model instances based on the model_type."""

    @staticmethod
    def create_model_from_config(model_type: str, **params) -> Any:
        """Static method to create and return a model instance based on the model_type."""
        if model_type == "sgdclassifier":
            from sklearn.linear_model import SGDClassifier

            return SGDClassifier(**params)
        elif model_type == "sgdregressor":
            from sklearn.linear_model import SGDRegressor

            return SGDRegressor(**params)
        elif model_type == "perceptron":
            from sklearn.linear_model import Perceptron

            return Perceptron(**params)
        elif model_type == "naive_bayes":
            from sklearn.naive_bayes import GaussianNB

            return GaussianNB(**params)
        elif model_type == "mlpclassifier":
            from sklearn.neural_network import MLPClassifier

            return MLPClassifier(**params)
        elif model_type == "mlpregressor":
            from sklearn.neural_network import MLPRegressor

            return MLPRegressor(**params)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    @staticmethod
    def get_available_model_types() -> list:
        """Return a list of available model types that the factory can create."""
        return [
            "sgdclassifier",
            "sgdregressor",
            "perceptron",
            "naive_bayes",
            "mlpclassifier",
            "mlpregressor",
        ]

    @staticmethod
    def is_model_type_supported(model_type: str) -> bool:
        """Check if the given model_type is supported by the factory."""
        return model_type in ModelFactory.get_available_model_types()


# Implementation 3: A more advanced approach using a registry pattern.
# This allows for dynamic registration of model types and can be extended
# without modifying the factory code. New model types can be registered at
# runtime, making it flexible for future expansions.

import importlib

_model_registry: dict[str, Any] = {
    "sgdclassifier": importlib.import_module("sklearn.linear_model").SGDClassifier,
    "sgdregressor": importlib.import_module("sklearn.linear_model").SGDRegressor,
    "perceptron": importlib.import_module("sklearn.linear_model").Perceptron,
    "naive_bayes": importlib.import_module("sklearn.naive_bayes").GaussianNB,
    "mlpclassifier": importlib.import_module("sklearn.neural_network").MLPClassifier,
    "mlpregressor": importlib.import_module("sklearn.neural_network").MLPRegressor,
}


# Function to register a new model type with its corresponding class
# This allows for dynamic extension of the factory without modifying the core logic.
# For functions, you could also use a decorator to register them, but for classes,
# this is a straightforward approach.
def register_model(model_type: str, model_class: Any):
    """Register a model class with a specific model_type in the registry."""
    _model_registry[model_type] = model_class


# Function to create a model instance from the registry
def create_model_from_registry(model_type: str, **params) -> Any:
    """Create and return a model instance based on the model_type using the registry."""
    if model_type not in _model_registry:
        raise ValueError(f"Unknown model type: {model_type}")
    return _model_registry[model_type](**params)


# Implementation 4: Same registry pattern as Implementation 3, but typed with a
# structural Protocol instead of Any. sklearn's estimators don't share a common
# base class that guarantees partial_fit, so a Protocol describing exactly the
# shape this factory needs (partial_fit/predict) lets a type checker (mypy) catch
# a registered class that doesn't actually support it — Any can't.
class IncrementalEstimator(Protocol):
    """Structural contract every model produced by this factory must satisfy."""

    def partial_fit(self, X, y, **kwargs) -> "IncrementalEstimator": ...
    def predict(self, X): ...


_typed_model_registry: dict[str, Callable[..., IncrementalEstimator]] = {
    "sgdclassifier": importlib.import_module("sklearn.linear_model").SGDClassifier,
    "sgdregressor": importlib.import_module("sklearn.linear_model").SGDRegressor,
    "perceptron": importlib.import_module("sklearn.linear_model").Perceptron,
    "naive_bayes": importlib.import_module("sklearn.naive_bayes").GaussianNB,
    "mlpclassifier": importlib.import_module("sklearn.neural_network").MLPClassifier,
    "mlpregressor": importlib.import_module("sklearn.neural_network").MLPRegressor,
}


def register_typed_model(
    model_type: str, model_class: Callable[..., IncrementalEstimator]
) -> None:
    """Register a model class with a specific model_type in the typed registry."""
    _typed_model_registry[model_type] = model_class


def create_model_from_typed_registry(model_type: str, **params) -> IncrementalEstimator:
    """Create and return a model instance based on the model_type using the typed registry."""
    if model_type not in _typed_model_registry:
        raise ValueError(f"Unknown model type: {model_type}")
    return _typed_model_registry[model_type](**params)


# Example usage of the factory methods
if __name__ == "__main__":
    # Using the simple factory function
    model1 = create_model_from_config("sgdclassifier", max_iter=1000, tol=1e-3)
    print(f"Created model using factory function: {model1}")

    # Using the ModelFactory class
    model2 = ModelFactory.create_model_from_config(
        "mlpclassifier", hidden_layer_sizes=(50,), max_iter=500
    )
    print(f"Created model using ModelFactory class: {model2}")

    # Using the registry pattern
    model3 = create_model_from_registry("perceptron", max_iter=1000, tol=1e-3)
    print(f"Created model using registry pattern: {model3}")

    ## Demonstrate that the registry can be extended with a new model type
    from sklearn.linear_model import PassiveAggressiveRegressor

    register_model("passive_aggressive_regressor", PassiveAggressiveRegressor)
    model4 = create_model_from_registry(
        "passive_aggressive_regressor", max_iter=1000, tol=1e-3
    )
    print(f"Created model using extended registry: {model4}")
    ### Note: This model is deprecated in version 1.8 and will be removed in 1.10.

    # Using the typed registry pattern
    model5 = create_model_from_typed_registry("sgdregressor", max_iter=1000, tol=1e-3)
    print(f"Created model using typed registry pattern: {model5}")


# ===================================================================
# Claude Code Review:
#
# Runs cleanly end-to-end. All four implementations are correct and
# do what the docstring asks:
#
# - Implementation 1 (plain function) and Implementation 2
#   (ModelFactory staticmethods) are functionally identical — same
#   if/elif ladder, just one wrapped in a class namespace. That's a
#   fair thing to show side by side (bare function vs. class-based
#   factory are both legitimate Factory Method shapes), but note they
#   are genuinely redundant with each other, not two different ideas.
#
# - Implementation 3 (registry) is the interesting one, and it's
#   correctly extensible: register_model() lets a caller add
#   "passive_aggressive_regressor" -> PassiveAggressiveRegressor
#   *without editing create_model_from_registry at all* — exactly the
#   open/closed property Implementations 1/2 lack (adding a model type
#   to either of those still means editing the if/elif chain). The
#   demo proves this concretely by registering and using a model type
#   the registry didn't ship with.
#
# - Implementation 4 takes Implementation 3 and replaces `Any` with a
#   structural `IncrementalEstimator` Protocol (`partial_fit`/`predict`)
#   via `Callable[..., IncrementalEstimator]` — a good fit since
#   sklearn's estimators don't share a common base class that
#   guarantees `partial_fit`, so nominal typing (`type[BaseEstimator]`)
#   wouldn't actually express the contract this factory needs.
#   Verified with `uv run mypy` that this isn't just decorative: a
#   custom class missing `partial_fit`/`predict` registered into a
#   `Callable[..., IncrementalEstimator]`-typed dict is correctly
#   flagged (`error: ... expected "Callable[..., IncrementalEstimator]"`).
#   Caveat worth knowing: that check only fires for types mypy can see
#   into. sklearn ships no `py.typed` marker, so `mypy` on this file
#   itself reports `Skipping analyzing "sklearn.*": missing library
#   stubs` for every sklearn import — meaning mypy can't actually
#   verify (or refute) that `SGDClassifier`/`Perceptron`/etc. satisfy
#   `IncrementalEstimator` here. The Protocol still documents the
#   contract precisely and would catch a *custom* misfit class, just
#   not a wrong sklearn one — worth knowing the guarantee is partial
#   in this specific file, not because the Protocol is wrong.
#
# One thing worth knowing, not a bug: the per-branch `from sklearn...
# import X` inside Implementations 1 and 2 means sklearn submodules
# get re-imported on every call (Python caches imported modules, so
# this isn't a real cost, just a style choice — a single import block
# at module level would be the more usual layout). The registry
# versions (3 and 4) sidestep this naturally since each class is only
# resolved once, at module load, via the dict literal.
#
# get_available_model_types() / is_model_type_supported() are a nice
# touch not asked for in the docstring — genuinely useful for a caller
# that wants to validate a config value before calling the factory,
# and they'd extend cleanly to either registry version too (dict
# lookups instead of the list literal you built here for
# Implementations 1/2).
# ===================================================================
