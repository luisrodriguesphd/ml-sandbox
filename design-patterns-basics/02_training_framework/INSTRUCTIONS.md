# Problem 2: ML Training & Experimentation Framework

## Overview

A small online/incremental-learning framework where the model type, the
preprocessing strategy, and the post-update side effects (logging, early
stopping, checkpointing) are all pluggable rather than hard-coded. Instead
of training on a fixed dataset over many epochs, the model here keeps
learning as new batches of data arrive — the flow is: **new data batch →
preprocessing strategy → incremental model update → notify observers**.

This connects naturally with `01_data_ingestion/`: Problem 1 handles *how
data arrives* (lazily streamed one file/chunk at a time via `FileSource` /
`FileIterator` / `stream_files`); Problem 2 handles *how the system
processes and learns from each new batch* of it.

## Why these three patterns fit together

- **Factory Method** decides *which online-capable model* gets built from
  config — one that supports incremental updates (e.g. scikit-learn's
  `partial_fit`) rather than a single one-shot `fit` over the whole dataset.
- **Strategy** decides *which preprocessing/scaling* runs on each batch,
  independently of the model — and must itself be compatible with an
  incremental setting, since there's no full dataset to fit against upfront.
- **Observer** decides *what happens* after each training update/batch,
  independently of both the model and the scaling choice.

A single `Trainer` can combine all three: build a model via the factory,
scale each incoming batch via a strategy, update the model incrementally,
and notify observers after every update — with each concern swappable
without touching the others.

## Files

| File | Pattern | Summary |
|---|---|---|
| `01_factory_method.py` | Factory Method (Creational) | Create an online-capable model instance from a config string, decoupled from training code. |
| `02_strategy.py` | Strategy (Behavioral) | Swap batch-compatible preprocessing/scaling strategies at runtime. |
| `03_observer.py` | Observer (Behavioral) | Notify subscribers after each incremental training update (logger, early stopping, checkpointing) from the training loop. |

## Requirements

- Python 3.12+ (managed automatically by `uv`)
- `scikit-learn` — provides the online-capable/incremental estimators used
  by the Factory Method exercise, restricted to ones that support
  `partial_fit`: an SGD-based linear model (`SGDClassifier`/`SGDRegressor`),
  `Perceptron`, a suitable Naive Bayes model (`GaussianNB`/`MultinomialNB`),
  or an incremental neural network / MLP (`MLPClassifier`/`MLPRegressor` via
  `partial_fit`). Its `StandardScaler`/`MinMaxScaler` (both also support
  `partial_fit`) are natural fits for the Strategy exercise.
- Optional extension: [River](https://riverml.xyz) offers estimators built
  natively for online learning (`learn_one`/`predict_one` instead of
  batch-oriented `partial_fit`) — not a project dependency, so install it
  yourself (e.g. in a throwaway environment) only if you want to compare its
  ergonomics to scikit-learn's.

Dependencies are managed at the repo root via `uv` — see the root
`pyproject.toml`/`uv.lock`. From the repo root, run:

```bash
uv sync
```

## How to Run

From the repo root (or from within this folder, `uv` finds the project
automatically):

```bash
uv run python 01_factory_method.py
uv run python 02_strategy.py
uv run python 03_observer.py
```
