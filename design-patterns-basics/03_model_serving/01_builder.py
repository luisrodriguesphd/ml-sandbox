"""
Builder pattern (Creational) — Problem 3: Model Serving / Inference Pipeline.

Constructs a multi-step inference pipeline (preprocessing -> model ->
postprocessing) piece by piece via a fluent interface, instead of a single
constructor call with a long, error-prone parameter list.

Example to implement:
    An `InferencePipelineBuilder` with chainable methods such as
    `.add_preprocessor(...)`, `.set_model(...)`, `.add_postprocessor(...)`,
    ending in `.build()` to produce an immutable `InferencePipeline` object
    that `03_facade.py` will expose behind a single `predict()` call.

Learning objectives:
    - Implement the Builder pattern to assemble a complex object step by
      step, keeping construction readable and validated.
    - Distinguish Builder (assembling *one* configured object over several
      steps) from Factory Method (`02_training_framework/01_factory_method.py`,
      choosing *which* object to create in one step).
"""
