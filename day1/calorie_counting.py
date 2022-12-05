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


def process_input(path: Path):
    max_calories = 0
    current_elf_items = []
    with open(path, "r") as fin:
        for line in fin.readlines():
            line = line.strip()
            if line:
                current_elf_items.append(int(line))
            else:
                elf = Elf(current_elf_items)
                if elf.total_calories > max_calories:
                    max_calories = elf.total_calories
                del elf
                current_elf_items = []
    return max_calories


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Calorie Counter")
    parser.add_argument(
        "--input",
        type=Path,
        # required=True,
        default="day1/input/input.txt",
        help="Path to the input file.",
    )
    args = parser.parse_args()
    max_calories = process_input(args.input)
    print(f"Maximum number of calories is: {max_calories}")
