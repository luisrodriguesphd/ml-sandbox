# Suggested Learning Roadmap

A soft, paced path through this folder: one phase for general GoF theory,
then one phase per problem, then a short synthesis. Nothing here is timed —
treat each numbered pattern file as one sitting (9 sittings total across the
three problems), not each problem as one sitting. That pacing is what makes
it "soft."

Throughout, keep one question active for every pattern: *could this have
been solved with a plain if/else or a global variable — and if so, why does
the pattern still win here (or does it)?* That question is the actual point
of the roadmap, more than any specific line of code.

---

## Phase 0 — GoF foundations

Do this once, before opening any file. ~30-45 minutes.

- **What a pattern actually is**: a named, reusable *shape* of solution to a
  recurring design problem — not a library, not code to copy-paste verbatim.
- **The 3 categories, one mental model each**:
  - *Creational* → "how does this object get **made**?"
  - *Structural* → "how do existing pieces get **composed/reshaped** to fit
    together?"
  - *Behavioral* → "how does **runtime behavior/control flow** vary or get
    distributed?"
- **How to read any pattern**: Intent → the problem it solves → the
  tradeoff it accepts. No need for formal UML or the full GoF book.
- **The caveat to internalize now**: every pattern in this folder could be
  "solved" with an if/else or a global variable. The roadmap below is about
  noticing *why* the pattern earns its complexity anyway — or, sometimes,
  that it doesn't.

**Checkpoint:** state, in one sentence each, what problem Creational /
Structural / Behavioral patterns generally solve — without looking it up.

---

## Phase 1 — Problem 1: Data Ingestion

Start here — it's the most concrete problem, since you can watch it work
(files downloading, a session being reused).

1. Read `01_data_ingestion/INSTRUCTIONS.md` fully before opening any `.py`
   file — get the real-world framing first.
2. **Singleton** (`01_singleton.py`): learn just the intent (one shared
   instance) → implement minimally → prove it with a test/print showing two
   "different" instantiations are the same object.
3. **Adapter** (`02_adapter.py`): implement `LocalFileSource` first alone,
   get it working end-to-end → only then add `GitHubRawFileSource` and wire
   in the Singleton client. Adding the second source is what makes
   Adapter's value click.
4. **Iterator/Generator** (`03_iterator_generator.py`): implement the
   generator-function version first (the natural Python instinct) → then
   implement the class-based `__iter__`/`__next__` version and compare the
   two side by side.

**Checkpoint:** run the full pipeline end-to-end (local → remote, streamed
lazily). Ask which of the three patterns you'd miss least if you deleted
it — there's a real answer, and finding it is the point.

---

## Phase 2 — Problem 2: Training Framework

Introduces variation-at-runtime, not just object creation.

1. Read `02_training_framework/INSTRUCTIONS.md`.
2. **Factory Method** (`01_factory_method.py`) first — closest cousin to
   Singleton (both Creational), good for contrast: *Singleton controls how
   many, Factory Method controls which kind*.
3. **Strategy** (`02_strategy.py`) next — implement two scaling strategies
   and swap them at runtime without touching the trainer.
4. **Observer** (`03_observer.py`) last — the most novel concept here
   (pub/sub), so give it the most time; implement one observer, get it
   firing, then add a second to see the decoupling payoff.

**Checkpoint:** compare Factory Method vs. Strategy in your own words —
both are "pluggable," but one picks an object, the other picks a behavior.

---

## Phase 3 — Problem 3: Model Serving

The capstone — composition of patterns rather than one pattern in
isolation.

1. Read `03_model_serving/INSTRUCTIONS.md`.
2. **Builder** (`01_builder.py`) — build the pipeline with just one step
   first (e.g. only `.set_model()`), run it, then add
   preprocessing/postprocessing steps incrementally.
3. **Decorator** (`02_decorator.py`) — add one decorator (timing) working
   alone before stacking caching/retry on top. Stacking is where
   Decorator's value shows up.
4. **Facade** (`03_facade.py`) — write this *last*, once Builder and
   Decorator both work, since its whole job is hiding what you just built.

**Checkpoint:** call `ModelService.predict()` and trace, from memory, every
pattern it passes through underneath. If you can narrate that chain, the
capstone landed.

---

## Phase 4 — Synthesis

Short, but don't skip it.

- Write a one-sentence-per-pattern cheat sheet (9 lines total) — forces you
  to compress each intent to its essence.
- Pick one pattern you found least convincing and try removing it from its
  problem, replacing it with the naive alternative (if/else, global, direct
  construction). Notice concretely what you lose.
