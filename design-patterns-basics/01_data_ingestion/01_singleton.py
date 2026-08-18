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


#===================================================================
# Implementation 2: Class-level singleton
#===================================================================


class DownloadClientV2:
    _session = None  # a single shared session for all requests

    def __init__(self):
        if DownloadClientV2._session is None:
            DownloadClientV2._session = requests.Session()  # create a single shared session
        self.session = DownloadClientV2._session  # always use the same session

    def fetch(self, url):
        return self.session.get(url)
    

class DownloadClientV2Alt:
    _session = requests.Session()  # a single shared session for all requests

    def __init__(self):
        self.session = self._session  # always use the same session

    def fetch(self, url):
        return self.session.get(url)

  
#===================================================================
# Implementation 3: Singleton via __new__
#===================================================================


class DownloadClientV3:
    _session = None

    def __new__(cls):
        # You can't call cls() because cls() re-enters __new__. 
        # Calling cls() is Python's normal object-construction call — 
        # it triggers cls.__new__(cls) and then cls.__init__(instance).
        # you need to allocate the raw instance without going through 
        # your own __new__ again. That's what super().__new__(cls) does — 
        # it calls object.__new__(cls) (or whatever's next in the MRO).
        instance = super().__new__(cls)     # always allocate a new instance
        if cls._session is None:
            cls._session = requests.Session()  # create the shared resource once
        return instance

    def __init__(self):
        self.session = self._session  # always use the same session

    def fetch(self, url):
        return self.session.get(url)


class DownloadClientV3Alt:
    _session = None

    def __new__(cls):
        # You can't call cls() because cls() re-enters __new__. 
        # Calling cls() is Python's normal object-construction call — 
        # it triggers cls.__new__(cls) and then cls.__init__(instance).
        # you need to allocate the raw instance without going through 
        # your own __new__ again. That's what super().__new__(cls) does — 
        # it calls object.__new__(cls) (or whatever's next in the MRO).
        instance = super().__new__(cls)     # always allocate a new instance
        if cls._session is None:
            cls._session = requests.Session()  # create the shared resource once
        instance.session = cls._session
        return instance

    def __init__(self):
        pass  # no-op, __new__ already wires up the session

    def fetch(self, url):
        return self.session.get(url)


class DownloadClientV3Alt2:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # You can't call cls() because cls() re-enters __new__. 
            # Calling cls() is Python's normal object-construction call — 
            # it triggers cls.__new__(cls) and then cls.__init__(instance).
            # you need to allocate the raw instance without going through 
            # your own __new__ again. That's what super().__new__(cls) does — 
            # it calls object.__new__(cls) (or whatever's next in the MRO).
            cls._instance = super().__new__(cls)  # actually allocate, once
            cls._instance.session = requests.Session()  # create a single shared session
        return cls._instance

    def __init__(self):
        pass  # no-op, since __new__ handles the session creation

    def fetch(self, url):
        return self.session.get(url)


if __name__ == "__main__":
    #===================================================================
    print("=== Singleton pattern (module-level) ===")

    client1 = DownloadClientV1()
    client2 = DownloadClientV1()
    
    print("Is two objects equal?", client1 is client2)  # True, same objects object
    print("Is two sessions equal?", client1.session is client2.session)  # True, same session object

    #===================================================================
    print("=== Singleton pattern (class-level) ===")

    client1 = DownloadClientV2()
    client2 = DownloadClientV2()

    print("Is two objects equal?", client1 is client2)  # True, same objects object
    print("Is two sessions equal?", client1.session is client2.session)  # True, same session object

    
    print("=== Singleton pattern (class-level alternative) ===")

    client1 = DownloadClientV2Alt()
    client2 = DownloadClientV2Alt()

    print("Is two objects equal?", client1 is client2)  # True, same objects object
    print("Is two sessions equal?", client1.session is client2.session)  # True, same session object

    #===================================================================
    print("=== Singleton pattern (__new__) ===")

    client1 = DownloadClientV3()
    client2 = DownloadClientV3()

    print("Is two objects equal?", client1 is client2)  # True, same objects object
    print("Is two sessions equal?", client1.session is client2.session)  # True, same session object

    print("=== Singleton pattern (__new__ alternative) ===")
    
    client1 = DownloadClientV3Alt()
    client2 = DownloadClientV3Alt()

    print("Is two objects equal?", client1 is client2)  # True, same objects object
    print("Is two sessions equal?", client1.session is client2.session)  # True, same session object

    print("=== Singleton pattern (__new__ alternative 2) ===")

    client1 = DownloadClientV3Alt2()
    client2 = DownloadClientV3Alt2()

    print("Is two objects equal?", client1 is client2)  # True, same objects object
    print("Is two sessions equal?", client1.session is client2.session)  # True, same session object


#===================================================================
# Claude Code Review:
#
# Of the six variants, only DownloadClientV3Alt2 is a Singleton in the
# strict GoF sense (same object every call) — it's the only one that
# overrides __new__ to cache and return `cls._instance`.
#
# V1, V2, V2Alt, V3, and V3Alt all return a NEW object on every call
# (none of them override __new__ to return a cached instance, or they
# override it but only cache `_session`, not `_instance`). They share
# the underlying requests.Session via a module- or class-level
# attribute, but `client1 is client2` is False for all five. That's a
# shared-resource / shared-state pattern, not a Singleton — useful for
# the same practical goal (one pooled connection), but a different
# guarantee than "only one instance of this class can exist."
#
# V3 and V3Alt are functionally identical (one sets `instance.session`
# in __init__, the other in __new__) — kept as two ways to wire the
# same idea, not because they behave differently.
#
# Multithreading has two separate concerns here, not one:
#
# 1. Race during CREATION (lazy-init variants only: V2, V3, V3Alt,
#    V3Alt2). Two threads can both pass `if _session/_instance is
#    None` before either assigns, each creating its own Session. The
#    last assignment wins; the other is silently orphaned — wasted
#    resources, not corruption, but breaks the "exactly one" guarantee
#    at that instant. V1 and V2Alt don't have this problem: their
#    session is created eagerly at import/class-definition time,
#    before any threads exist. Fix if it matters: a lock around the
#    check-and-create.
#
# 2. Race during USE — affects all six variants equally, since every
#    one of them eventually hands the same live Session object to
#    concurrent callers. requests.Session is NOT documented as
#    thread-safe: session.cookies is a shared mutable cookie jar
#    updated by every response, and any per-call mutation of session
#    state (e.g. temporarily setting session.headers['Authorization']
#    before a request) is visible to every thread using the session,
#    not just the one that set it. The lower-level connection pooling
#    (via urllib3) IS thread-safe, so plain concurrent .get()/.post()
#    calls with no other shared-state mutation are commonly considered
#    fine in practice — which is what this file's fetch(url) does. The
#    risk only shows up if the pipeline grows to mutate session state
#    (headers/auth/cookies) per request instead of passing those as
#    arguments to .get().
#===================================================================
