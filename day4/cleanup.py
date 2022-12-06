import argparse
from pathlib import Path


def is_left_within_right(left, right) -> bool:
    raise NotImplementedError


def process_input(path: Path) -> int:
    num_fully_contained_pairs = 0
    with open(path, "r") as fin:
        for line in fin.readlines():
            raise NotImplementedError
    return num_fully_contained_pairs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Cleanup.")
    parser.add_argument(
        "--input",
        type=Path,
        default="day4/input/input.txt",
        help="Path to the input file.",
    )
    args = parser.parse_args()
    num_fully_contained_pairs = process_input(args.input)
    print(f"In {num_fully_contained_pairs} pairs one range fully contains the other.")
