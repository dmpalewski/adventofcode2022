import argparse
from dataclasses import dataclass
from typing import List
from pathlib import Path


@dataclass
class Elf:
    items: List[int]
    total_calories: int = 0

    def __post_init__(self):
        self.total_calories = sum(self.items)


@dataclass
class Expedition:
    elves: List[Elf]

    def add_elf(self, elf: Elf):
        self.elves.append(elf)

    def get_top_n_by_calories(self, n: int):
        elves_sorted_desc = sorted(self.elves, key=lambda x: -x.total_calories,)
        return elves_sorted_desc[:n]

    def get_total_calories_for_top_n(self, n: int = 3):
        top_n_elves = self.get_top_n_by_calories(n)
        total_calories_for_top_n = sum([e.total_calories for e in top_n_elves])
        return total_calories_for_top_n


def process_input(path: Path):
    expedition = Expedition([])
    current_elf_items = []
    with open(path, "r") as fin:
        for line in fin.readlines():
            line = line.strip()
            if line:
                current_elf_items.append(int(line))
            else:
                elf = Elf(current_elf_items)
                expedition.add_elf(elf)
                current_elf_items = []
    top_3_calories_total = expedition.get_total_calories_for_top_n(3)
    return top_3_calories_total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Calorie Counter")
    parser.add_argument(
        "--input",
        type=Path,
        # required=True,
        default="day1/input/input.txt",
        help="Path to the input file.",
    )
    parser.add_argument(
        "--top_number",
        type=int,
        # required=True,
        default=3,
        help="Number of elves to be used from the top.",
    )
    args = parser.parse_args()
    max_calories = process_input(args.input)
    print(f"Total number of calories carrying by top {args.top_number} elves: {max_calories}")
