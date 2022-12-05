import argparse
import string
from pathlib import Path
from typing import Iterable, Set, Tuple


def get_priority(char: str) -> int:
    ascii_dec = ord(char)
    priority = ascii_dec - 96 if char in string.ascii_lowercase else ascii_dec - 38
    return priority


def split_input(s: str) -> Tuple[str, str]:
    id_half = len(s) // 2
    return s[:id_half], s[id_half:]


def find_duplicates(rucksacks: Iterable[str]) -> Set[str]:
    return set.intersection(*[set(rucksack) for rucksack in rucksacks])


def process_input(path: Path) -> int:
    total_priority = 0
    with open(path, "r") as fin:
        for line in fin.readlines():
            rucksacks = split_input(line.strip())
            duplicates = find_duplicates(rucksacks)
            for duplicate in duplicates:
                total_priority += get_priority(duplicate)
    return total_priority


def process_input_pt_2(path: Path, group_size: int = 3) -> int:
    total_priority = 0
    group = []
    with open(path, "r") as fin:
        for line in fin.readlines():
            line = line.strip()
            group.append(line)
            if len(group) == group_size:
                duplicates = find_duplicates(group)
                for duplicate in duplicates:
                    total_priority += get_priority(duplicate)
                group = []
    return total_priority


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Rucksack Reorganization.")
    parser.add_argument(
        "--input",
        type=Path,
        default="day3/input/input.txt",
        help="Path to the input file.",
    )
    args = parser.parse_args()
    total_priority = process_input_pt_2(args.input)
    print(f"Total priority: {total_priority}")
