"""
Singleton pattern (Creational) — Problem 1: Data Ingestion Pipeline.

Ensures a single shared download client (e.g. a requests.Session) is reused
across every file fetch in the ingestion pipeline, instead of opening a new
HTTP connection per request.

Example to implement:
    A `DownloadClient` (or `SessionManager`) class that always returns the
    same underlying `requests.Session` instance no matter how many times or
    where it is instantiated across the pipeline — demonstrated by fetching
    multiple files (see 02_adapter.py / 03_iterator_generator.py) through it
    and confirming they all share one connection-pooled session.

Learning objectives:
    - Implement Singleton via a controlled `__new__`, module-level instance,
      or metaclass — and understand the tradeoffs between them.
    - Recognize when a single shared resource (connection, config, client)
      is the right call in a data-engineering pipeline, and when a Singleton
      is overused / becomes a hidden global.
"""
