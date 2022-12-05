import argparse
from pathlib import Path
from enum import IntEnum


class Outcome(IntEnum):
    WIN = 6
    DRAW = 3
    LOSE = 0


class Figure(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


cypher2figure = {
    "A": Figure.ROCK,
    "B": Figure.PAPER,
    "C": Figure.SCISSORS,
    "X": Figure.ROCK,
    "Y": Figure.PAPER,
    "Z": Figure.SCISSORS
}


def get_outcome(opponent_figure: Figure, your_figure: Figure) -> Outcome:
    if opponent_figure == your_figure:
        outcome = Outcome.DRAW
    elif (
        (opponent_figure == Figure.ROCK and your_figure == Figure.SCISSORS)
        or (opponent_figure == Figure.PAPER and your_figure == Figure.ROCK)
        or (opponent_figure == Figure.SCISSORS and your_figure == Figure.PAPER)
    ):
        outcome = Outcome.LOSE
    else:
        outcome = Outcome.WIN
    return outcome


def process_input(path: Path) -> int:
    total_score = 0
    with open(path, "r") as fin:
        for line in fin.readlines():
            opponent_figure, your_figure = [cypher2figure.get(c) for c in line.strip().split()]
            round_outcome = get_outcome(opponent_figure, your_figure)
            round_score = round_outcome + your_figure
            total_score += round_score
    return total_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Calorie Counter")
    parser.add_argument(
        "--input",
        type=Path,
        default="day2/input/input.txt",
        help="Path to the input file.",
    )

    args = parser.parse_args()
    total_score = process_input(args.input)
    print(f"Total score: {total_score}")
