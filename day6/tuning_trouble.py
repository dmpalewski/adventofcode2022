import argparse
from pathlib import Path


DEFAULT_MARKER_SIZE = 4


def process_input(path: Path, marker_size: int) -> int:
    num_chars_before_marker = -1
    with open(path, "r") as fin:
        stream = fin.read()
        stream_size = len(stream)
        for i in range(0, stream_size - marker_size):
            marker = stream[i: i + marker_size]
            if len(set(marker)) == marker_size:
                num_chars_before_marker = i + marker_size
                break
    return num_chars_before_marker


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Tuning Trouble.")
    parser.add_argument(
        "--input",
        type=Path,
        default="day6/input/input.txt",
        help="Path to the input file.",
    )
    parser.add_argument(
        "--marker_size",
        type=int,
        default=DEFAULT_MARKER_SIZE,
        help="Size of the marker.",
    )
    args = parser.parse_args()
    num_chars = process_input(args.input, marker_size=args.marker_size)
    print(f"Number of chars before the marker: {num_chars}.")
