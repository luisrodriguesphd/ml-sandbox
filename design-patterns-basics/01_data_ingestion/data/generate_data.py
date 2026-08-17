"""
One-time helper that generates the sample data files used by this problem's
LocalFileSource (Iris, in ./local/) and GitHubRawFileSource (Wine, in
./remote/) examples.

This script requires scikit-learn, but scikit-learn is NOT a runtime
dependency of the pattern demos themselves (01_singleton.py, 02_adapter.py,
03_iterator_generator.py) -- those only ever read plain CSV files. Re-run
this script only if you want to regenerate the sample data from scratch.

Usage:
    pip install scikit-learn
    python generate_data.py
"""

import csv
from pathlib import Path

from sklearn.datasets import load_iris, load_wine

CHUNK_SIZE = 30


def write_chunks(feature_names, target_names, data, target, out_dir: Path, prefix: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    header = list(feature_names) + ["target"]
    n_rows = len(data)
    n_chunks = -(-n_rows // CHUNK_SIZE)  # ceil division, no remainder dropped

    for i in range(n_chunks):
        start = i * CHUNK_SIZE
        end = min(start + CHUNK_SIZE, n_rows)
        chunk_path = out_dir / f"{prefix}_part{i + 1:02d}.csv"

        with chunk_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row_idx in range(start, end):
                writer.writerow(list(data[row_idx]) + [target_names[target[row_idx]]])

        print(f"wrote {chunk_path} ({end - start} rows)")


def main() -> None:
    base = Path(__file__).parent

    iris = load_iris()
    write_chunks(iris.feature_names, iris.target_names, iris.data, iris.target, base / "local", "iris")

    wine = load_wine()
    write_chunks(wine.feature_names, wine.target_names, wine.data, wine.target, base / "remote", "wine")


if __name__ == "__main__":
    main()
