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

import importlib


adapter_module = importlib.import_module("02_adapter")
FileSource = adapter_module.FileSource
LocalFileSource = adapter_module.LocalFileSource
GitHubRawFileSource = adapter_module.GitHubRawFileSource


class FileIterator:
    """Class-based iterator that lazily streams file contents from a FileSource."""
    
    def __init__(self, source: FileSource):
        self.source = source
        self.files = iter(source.list_files())
        self.processed_files = []  # Keep track of processed files for debugging

    def __iter__(self):
        return self

    def __next__(self):
        # Raises StopIteration when no more files
        # Alternatively to using `next(self.files)`, you could use a for loop 
        # and raise StopIteration manually, but this is more idiomatic. 
        # Example:
        #   if len(self.processed_files) >= len(self.files):
        #      raise StopIteration  # Signals to Python that iteration is over
        # With that we could simply define self.files = source.list_files()
        filename = next(self.files)  
        self.processed_files.append(filename)
        return self.source.read_file(filename)


def stream_files(source: FileSource):
    """Generator function that lazily streams file contents from a FileSource."""
    for filename in source.list_files():
        yield source.read_file(filename)


def main():
    # File sources setup
    
    ## LocalFileSource
    directory = './data/local/'
    local_source = LocalFileSource(directory)

    ## GitHubRawFileSource
    base_url = 'https://raw.githubusercontent.com/luisrodriguesphd/ml-sandbox/main/design-patterns-basics/01_data_ingestion/data/remote'
    github_source = GitHubRawFileSource(base_url)

    # Example usage of class-based iterator

    ## Demonstrate iteration over LocalFileSource using a class-based iterator
    print("Iterating over LocalFileSource using class-based iterator:")
    local_file_iterator = FileIterator(local_source)
    for chunk in local_file_iterator:
        print(f"Read {len(chunk)} characters from LocalFileSource - file {local_file_iterator.processed_files[-1]}.")

    ## Demonstrate iteration over GitHubRawFileSource using a class-based iterator
    print("\nIterating over GitHubRawFileSource using class-based iterator:")
    github_file_iterator = FileIterator(github_source)
    for chunk in github_file_iterator:
        print(f"Read {len(chunk)} characters from GitHubRawFileSource - file {github_file_iterator.processed_files[-1]}.")

    ### Demonstrate checking the processed files list for GitHubRawFileSource iterator
    github_processed_files = github_file_iterator.processed_files
    print("\nProcessed files from GitHubRawFileSource iterator:")
    for filename in github_processed_files:
        print(f"- {filename}")

    # Example usage of generator function

    ## Demonstrate iteration over LocalFileSource using a generator function
    print("\nIterating over LocalFileSource using generator function:")
    local_file_iterator = stream_files(local_source)
    for chunk in local_file_iterator:
        print(f"Read {len(chunk)} characters from LocalFileSource.")

    ## Demonstrate iteration over GitHubRawFileSource using a generator function
    print("\nIterating over GitHubRawFileSource using generator function:")
    github_file_iterator = stream_files(github_source)
    for chunk in github_file_iterator:
        print(f"Read {len(chunk)} characters from GitHubRawFileSource.")

    ### Demonstrate fetching a single file from the GitHubRawFileSource iterator
    print("\nFetching a single file from GitHubRawFileSource iterator:")
    try:
        chunk = next(github_file_iterator)
        print(f"Read {len(chunk)} characters from GitHubRawFileSource.")
    except StopIteration:
        print("No more files to fetch from GitHubRawFileSource iterator.")


if __name__ == "__main__":
    main()


#===================================================================
# Claude Code Review:
#
# Correct and verified end-to-end (same truststore shim as before, to
# get past this machine's TLS interception): both FileIterator and
# stream_files traverse LocalFileSource and GitHubRawFileSource
# identically, in the same order, reading each file's actual content —
# lazily, one at a time — exactly per the pattern's promise. The
# try/except StopIteration at the end correctly shows what happens
# when you manually call next() past exhaustion on a generator.
#
# The two implementations line up nicely for comparing ergonomics —
# the explicit point of this file:
#   - FileIterator needs __iter__ (return self), __next__, and its own
#     wrapped iterator (self.files = iter(...)) just to get
#     StopIteration propagation "for free" from the inner iterator.
#   - stream_files needs none of that — a for loop + yield gets you
#     the same lazy, one-at-a-time behavior, with local variables
#     doing the job self.files/self.source do explicitly in the class
#     version. This file makes that boilerplate delta concrete rather
#     than just asserting it.
#
# Nice detail: self.files = iter(source.list_files()) means __next__
# just delegates StopIteration to the wrapped list iterator instead of
# reimplementing bounds-checking by hand — the same "let something
# else raise it" trick generators get automatically.
#
# Two things worth knowing, neither a bug:
#   1. list_files() is called eagerly in FileIterator.__init__ (and
#      again, separately, in stream_files() each time it's called) —
#      so for GitHubRawFileSource that's a real network round trip at
#      construction/call time, not deferred until the first item is
#      pulled. Fully lazy would defer even that call to the first
#      __next__/first iteration step; snapshotting the name list up
#      front like this is the common, GoF-idiomatic choice and is fine
#      here — just note it's the *file list* that's eager, not the
#      *file contents*, which do stay lazy.
#   2. Because of #1, this run made list_files() calls to the GitHub
#      Contents API twice for the same directory (once for
#      FileIterator, once for stream_files) — each a fresh network
#      round trip, since the Singleton only shares the connection-
#      pooled session, not a results cache. Not a problem at this
#      scale/demo, just the reason you see the same six wine_partNN
#      names fetched from the network twice in a row rather than once.
#
# processed_files on FileIterator is a nice debugging aid with no
# equivalent in stream_files() — an intentional asymmetry (per its own
# comment), not something the generator is "missing."
#===================================================================
