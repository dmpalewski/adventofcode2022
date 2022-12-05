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


winning_figures_map = {
    Figure.ROCK: Figure.PAPER,
    Figure.PAPER: Figure.SCISSORS,
    Figure.SCISSORS: Figure.ROCK,
}


losing_figures_map = {v: k for k, v in winning_figures_map.items()}


cypher2figure = {
    "A": Figure.ROCK,
    "B": Figure.PAPER,
    "C": Figure.SCISSORS,
    "X": Figure.ROCK,
    "Y": Figure.PAPER,
    "Z": Figure.SCISSORS,
}


cypher2outcome = {"X": Outcome.LOSE, "Y": Outcome.DRAW, "Z": Outcome.WIN}


def get_outcome(opponent_figure: Figure, your_figure: Figure) -> Outcome:
    if opponent_figure == your_figure:
        outcome = Outcome.DRAW
    elif your_figure == losing_figures_map.get(opponent_figure):
        outcome = Outcome.LOSE
    else:
        outcome = Outcome.WIN
    return outcome


def get_your_figure_from_outcome(opponent_figure: Figure, outcome: Outcome) -> Figure:
    if outcome == Outcome.DRAW:
        your_figure = opponent_figure
    elif outcome == Outcome.LOSE:
        your_figure = losing_figures_map.get(opponent_figure)
    else:
        your_figure = winning_figures_map.get(opponent_figure)
    return your_figure


def process_input_pt1(path: Path) -> int:
    total_score = 0
    with open(path, "r") as fin:
        for line in fin.readlines():
            opponent_figure, your_figure = [
                cypher2figure.get(c) for c in line.strip().split()
            ]
            round_outcome = get_outcome(opponent_figure, your_figure)
            round_score = round_outcome + your_figure
            total_score += round_score
    return total_score


def process_input_pt2(path: Path) -> int:
    total_score = 0
    with open(path, "r") as fin:
        for line in fin.readlines():
            opponent_figure, outcome = [c for c in line.strip().split()]
            opponent_figure = cypher2figure.get(opponent_figure)
            round_outcome = cypher2outcome.get(outcome)
            your_figure = get_your_figure_from_outcome(opponent_figure, round_outcome)
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
    total_score = process_input_pt2(args.input)
    print(f"Total score: {total_score}")
