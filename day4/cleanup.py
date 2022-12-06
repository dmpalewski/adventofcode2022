import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass
class Range:
    lower_bound: int
    upper_bound: int


def get_range_from_string(s: str) -> Range:
    lo, hi = [int(i) for i in s.strip().split("-")]
    range = Range(lower_bound=lo, upper_bound=hi)
    return range


def parse_input_line(line: str) -> Tuple[Range, Range]:
    left_and_right = line.strip().split(",")
    return tuple(get_range_from_string(s) for s in left_and_right)


def is_left_within_right(left: Range, right: Range) -> bool:
    return (
        right.lower_bound <= left.lower_bound and right.upper_bound >= left.upper_bound
    )


def is_overlap(left: Range, right: Range) -> bool:
    return (
        right.lower_bound <= left.upper_bound and right.lower_bound >= left.lower_bound
    ) or (
        right.upper_bound >= left.lower_bound and right.upper_bound <= left.upper_bound
    )


def process_input(path: Path) -> int:
    num_fully_contained_pairs = 0
    with open(path, "r") as fin:
        for line in fin.readlines():
            left, right = parse_input_line(line)
            is_fully_contained = is_left_within_right(
                left, right
            ) or is_left_within_right(right, left)
            if is_fully_contained:
                num_fully_contained_pairs += 1
    return num_fully_contained_pairs


def process_input_pt_2(path: Path) -> int:
    num_overlaping_pairs = 0
    with open(path, "r") as fin:
        for line in fin.readlines():
            left, right = parse_input_line(line)
            is_overlaping = (
                is_overlap(left, right)
                or is_left_within_right(left, right)
                or is_left_within_right(right, left)
            )
            if is_overlaping:
                num_overlaping_pairs += 1
    return num_overlaping_pairs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Cleanup.")
    parser.add_argument(
        "--input",
        type=Path,
        default="day4/input/input.txt",
        help="Path to the input file.",
    )
    args = parser.parse_args()
    num_fully_contained_pairs = process_input_pt_2(args.input)
    print(f"Num overlaping pairs {num_fully_contained_pairs}.")
