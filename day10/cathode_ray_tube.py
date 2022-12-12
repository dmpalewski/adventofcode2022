import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class Program:
    x: int = 1
    cycles: List[int] = field(default_factory=list)

    def run_noop(self):
        self.cycles.append(self.x)

    def run_addx(self, value):
        self.run_noop()
        self.run_noop()
        self.x += value

    def finish(self):
        self.run_noop()

    def get_signal_strenght(self, i):
        signal_strength = i * self.cycles[i - 1]
        return signal_strength


def process_input(
    path: Path,
) -> int:
    program = Program()
    with open(path, "r") as fin:
        for line in fin.readlines():
            if line.startswith("noop"):
                program.run_noop()
            else:
                value = int(line.strip().split()[1])
                program.run_addx(value)
    program.finish()
    signal_ids = range(20, 221, 40)
    signal_strengths = [program.get_signal_strenght(i) for i in signal_ids]
    return sum(signal_strengths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rope Bridge")
    parser.add_argument(
        "--input",
        type=Path,
        default="day10/input/input.txt",
        help="Path to the input file.",
    )
    args = parser.parse_args()
    sum_of_signal_strengths = process_input(args.input)
    print(f"Sum of signal strengths {sum_of_signal_strengths}")
