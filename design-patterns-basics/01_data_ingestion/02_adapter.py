"""
Adapter pattern (Structural) — Problem 1: Data Ingestion Pipeline.

Unifies two different ways of accessing files — the local filesystem and
this repo's public GitHub raw URLs — behind one common `FileSource`
interface, so downstream pipeline code doesn't need to know or care which
source it's reading from.

Example to implement:
    A common `FileSource` interface (e.g. `list_files()` / `read_file(name)`)
    with two adapters:
      - `LocalFileSource`: reads files from a local folder (e.g. this repo's
        `oop-inheritance-basics/` directory) via `os`/`pathlib`.
      - `GitHubRawFileSource`: downloads files from
        `https://raw.githubusercontent.com/luisrodriguesphd/ml-sandbox/...`
        using the shared client from `01_singleton.py`.

Learning objectives:
    - Implement the Adapter pattern to make incompatible interfaces
      (local I/O vs. HTTP download) interchangeable behind one abstraction.
    - See how Adapter composes with Singleton (the remote adapter reuses the
      shared download client) and sets up the source consumed by
      `03_iterator_generator.py`.
"""
