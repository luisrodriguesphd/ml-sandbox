# Problem 2: ML Training & Experimentation Framework

## Overview

A small training framework where the model type, the feature-scaling
algorithm, and the epoch-end side effects (logging, early stopping,
checkpointing) are all pluggable rather than hard-coded — the shape of most
real ML training frameworks.

## Why these three patterns fit together

- **Factory Method** decides *which model* gets built from config.
- **Strategy** decides *which scaling algorithm* runs, independently of the
  model.
- **Observer** decides *what happens* after each epoch, independently of
  both the model and the scaling choice.

A single `Trainer` can combine all three: build a model via the factory,
scale features via a strategy, and notify observers each epoch — with each
concern swappable without touching the others.

## Files

| File | Pattern | Summary |
|---|---|---|
| `01_factory_method.py` | Factory Method (Creational) | Create a model instance from a config string, decoupled from training code. |
| `02_strategy.py` | Strategy (Behavioral) | Swap feature-scaling algorithms at runtime. |
| `03_observer.py` | Observer (Behavioral) | Notify epoch-end subscribers (logger, early stopping, checkpointing) from the training loop. |

## Requirements *(placeholder — fill in once implemented)*

- Python 3.8+
- No third-party packages required (pure-Python model/strategy stand-ins;
  real `sklearn` models are an optional extension)

## How to Run *(placeholder — fill in once implemented)*

```bash
python 01_factory_method.py
python 02_strategy.py
python 03_observer.py
```
