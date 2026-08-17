# Problem 1: Data Ingestion Pipeline

## Overview

A small pipeline that fetches files from either the local filesystem or this
repo's public GitHub URLs, and streams their contents without loading
everything into memory at once. This mirrors a common data-engineering task:
pulling a batch of files from a remote or local source and processing them
one by one.

## Why these three patterns fit together

- **Singleton** provides the one shared download client the pipeline needs —
  there's no reason to open a new HTTP session per file.
- **Adapter** lets the pipeline treat "a local folder" and "a GitHub repo"
  as the same kind of thing (`FileSource`), so the rest of the code doesn't
  branch on where the data comes from.
- **Iterator/Generator** is how the pipeline actually consumes a `FileSource`
  — lazily, one file at a time — which is what makes it scale to sources
  larger than memory.

Together they form one coherent flow: `Iterator` pulls from a `FileSource`
(Adapter), and the remote `FileSource` fetches through the shared client
(Singleton).

## Files

| File | Pattern | Summary |
|---|---|---|
| `01_singleton.py` | Singleton (Creational) | Shared download client reused across all fetches. |
| `02_adapter.py` | Adapter (Structural) | Common `FileSource` interface over local files and GitHub raw URLs. |
| `03_iterator_generator.py` | Iterator/Generator (Behavioral) | Lazy, one-at-a-time streaming of file contents from a `FileSource`. |

## Requirements *(placeholder — fill in once implemented)*

- Python 3.8+
- `requests` (only third-party dependency in this folder, used by the
  GitHub-backed `FileSource`)

## How to Run *(placeholder — fill in once implemented)*

```bash
python 01_singleton.py
python 02_adapter.py
python 03_iterator_generator.py
```
