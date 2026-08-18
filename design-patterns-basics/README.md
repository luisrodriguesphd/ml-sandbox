# Design Patterns Basics

Minimal, focused examples demonstrating the nine classic Gang-of-Four design
patterns, grouped into three realistic ML/data-engineering problems rather
than one artificial scenario per pattern:

1. `01_data_ingestion/` — Singleton, Adapter, Iterator/Generator: fetching
   and lazily streaming files from a local folder or this repo's public
   GitHub URLs.
2. `02_training_framework/` — Factory Method, Strategy, Observer: a
   pluggable model-training loop (model choice, scaling algorithm,
   epoch-end callbacks).
3. `03_model_serving/` — Builder, Decorator, Facade: assembling and serving
   an inference pipeline behind one simple `predict()` call.

> Context: This experiment complements the project by providing clear,
> practical examples of the design patterns most relevant to building
> robust ML systems. Each problem is self-contained, and each pattern file
> within it is independently understandable while contributing to that
> problem's shared example.

See [`ROADMAP.md`](./ROADMAP.md) for a suggested, self-paced learning path
through this folder — GoF foundations first, then one phase per problem.

---

## Goals

- Understand all three GoF categories — Creational, Structural, Behavioral
  — through one representative pattern each, times three problems
- See how multiple patterns combine naturally within a single realistic
  component, instead of studied in isolation
- Learn Singleton, Factory Method, and Builder as three different answers
  to "how should this object get created?"
- Learn Adapter, Decorator, and Facade as three different ways to reshape
  or simplify an existing interface
- Learn Iterator/Generator, Strategy, and Observer as three different ways
  to vary behavior at runtime

---

## Requirements

- Python 3.12+ (managed automatically by [`uv`](https://docs.astral.sh/uv/))
- `requests` (used only in `01_data_ingestion/`, for the GitHub-backed file
  source) — the only runtime third-party dependency across this folder
- `scikit-learn` — dev-only, used solely by
  `01_data_ingestion/data/generate_data.py` to (re)generate the sample CSV
  data; not required to run any of the pattern files themselves
- Basic understanding of Python classes, objects, and the material in
  `../oop-inheritance-basics/`

Dependencies are managed at the repo root via `uv` (see the root
`pyproject.toml`/`uv.lock`), not per-folder. From the repo root:

```bash
uv sync
```

---

## Project Structure

```yaml
design-patterns-basics/
├─ ROADMAP.md
├─ 01_data_ingestion/
│  ├─ INSTRUCTIONS.md
│  ├─ data/
│  │  ├─ generate_data.py
│  │  ├─ local/          # Iris CSV chunks (5 files)
│  │  └─ remote/         # Wine CSV chunks (6 files)
│  ├─ 01_singleton.py
│  ├─ 02_adapter.py
│  └─ 03_iterator_generator.py
├─ 02_training_framework/
│  ├─ INSTRUCTIONS.md
│  ├─ 01_factory_method.py
│  ├─ 02_strategy.py
│  └─ 03_observer.py
├─ 03_model_serving/
│  ├─ INSTRUCTIONS.md
│  ├─ 01_builder.py
│  ├─ 02_decorator.py
│  └─ 03_facade.py
└─ README.md
```

Each problem subfolder is self-contained and has its own `INSTRUCTIONS.md`
with the problem's framing and per-file learning goals.

---

## How to Run

Once implemented, run each pattern file from within its problem folder,
prefixing with `uv run` (`uv` finds the repo-root project automatically, no
manual venv activation needed):

```bash
cd 01_data_ingestion
uv run python 01_singleton.py
uv run python 02_adapter.py
uv run python 03_iterator_generator.py
```

The examples will provide clear console output demonstrating each pattern
in action.
