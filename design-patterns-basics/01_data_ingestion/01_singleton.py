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

import requests


#===================================================================
# Implementation 1: Module-level singleton
#===================================================================

s = requests.Session()  # a single shared session for all requests


class DownloadClientV1:
    def __init__(self):
        self.session = s  # always use the same session

    def fetch(self, url):
        return self.session.get(url)


#class Echo:
#    _instance = None
#
#    def __new__(cls):
#        print("__new__ called")
#        if cls._instance is None:
#            cls._instance = super().__new__(cls)   # actually allocate, once
#        return cls._instance
#
#    def __init__(self):
#        print("__init__ called")
#
#a = Echo()
#b = Echo()

if __name__ == "__main__":
    print("=== Singleton pattern (module-level) ===")
    
    client1 = DownloadClientV1()
    client2 = DownloadClientV1()

    print(client1.session is client2.session)  # True, same session object
