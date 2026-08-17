"""
Iterator / Generator pattern (Behavioral) — Problem 1: Data Ingestion Pipeline.

Lazily streams file contents one at a time from any `FileSource` (see
02_adapter.py), instead of loading every file into memory up front — the
realistic constraint in data engineering when a source may hold far more
data than fits in RAM.

Example to implement:
    - A class-based iterator, e.g. `FileIterator`, implementing
      `__iter__`/`__next__` over a `FileSource`.
    - An idiomatic Python generator function equivalent, e.g.
      `stream_files(source)`, using `yield`.
    - A `main()` demo that runs the same traversal through both the
      `LocalFileSource` (Iris chunks) and the `GitHubRawFileSource` (Wine
      chunks) to show the iteration logic is identical regardless of the
      underlying adapter *or* what data it actually holds.

Learning objectives:
    - Implement the Iterator pattern both the "classic" OOP way and the
      Pythonic generator way, and compare their ergonomics.
    - Understand lazy evaluation / streaming as a memory-efficiency strategy
      for data ingestion pipelines.
"""
