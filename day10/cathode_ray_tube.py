import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class Program:
    x: int = 1
    cycles: List[int] = field(default_factory=list)
    line_length: int = 40
    msg_length: int = 0

    def run_noop(self):
        self.cycles.append(self.x)

    def run_addx(self, value):
        self.run_noop()
        self.run_noop()
        self.x += value

    def finish(self):
        self.run_noop()
        self.msg_length = len(self.cycles)

    def get_signal_strenght(self, i):
        signal_strength = i * self.cycles[i - 1]
        return signal_strength

    def _is_lit(self, i):
        return abs(self.cycles[i] - i % self.line_length) < 2

    def draw_pixels(self):
        pixels = "".join(
            ["#" if self._is_lit(i) else "." for i in range(len(self.cycles))]
        )
        return pixels


def run_instructions(path: Path) -> Program:
    program = Program()
    with open(path, "r") as fin:
        for line in fin.readlines():
            if line.startswith("noop"):
                program.run_noop()
            else:
                value = int(line.strip().split()[1])
                program.run_addx(value)
    program.finish()
    return program


def process_input(program: Program) -> int:
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
    program = run_instructions(args.input)
    sum_of_signal_strengths = process_input(program)
    print(f"Sum of signal strengths {sum_of_signal_strengths}")

    pixels = program.draw_pixels()
    for start in range(0, program.msg_length + 1, program.line_length):
        end = min(start + program.line_length, program.msg_length)
        print(pixels[start:end])
