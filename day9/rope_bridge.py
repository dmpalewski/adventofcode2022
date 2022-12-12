import argparse
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Set, Tuple, Union


class Direction(str, Enum):
    RIGHT = "R"
    LEFT = "L"
    UP = "U"
    DOWN = "D"


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Knot:
    position: Position
    visited: Set[Tuple[int, int]] = field(default_factory=set)

    def __post_init__(self):
        self.mark_current_as_visited()

    def move_left(self):
        self.position.x -= 1

    def move_right(self):
        self.position.x += 1

    def move_up(self):
        self.position.y += 1

    def move_down(self):
        self.position.y -= 1

    def diagonal_move_y(self, diff: Position):
        if diff.y < 0:
            self.move_down()
        elif diff.y > 0:
            self.move_up()

    def diagonal_move_x(self, diff: Position):
        if diff.x < 0:
            self.move_left()
        elif diff.x > 0:
            self.move_right()

    def mark_current_as_visited(self):
        self.visited.add(
            (
                self.position.x,
                self.position.y,
            )
        )


@dataclass
class Rope:
    head: Knot
    tail: Knot

    def _get_position_diff(self) -> Position:
        x_diff = self.head.position.x - self.tail.position.x
        y_diff = self.head.position.y - self.tail.position.y
        return Position(x_diff, y_diff)

    def _adjust_tail(self):
        diff = self._get_position_diff()
        if diff.x == -2:
            self.tail.move_left()
            self.tail.diagonal_move_y(diff)
        elif diff.x == 2:
            self.tail.move_right()
            self.tail.diagonal_move_y(diff)

        if diff.y == -2:
            self.tail.move_down()
            self.tail.diagonal_move_x(diff)
        elif diff.y == 2:
            self.tail.move_up()
            self.tail.diagonal_move_x(diff)

    def move_rope(self, direction: Union[str, Direction]):
        match direction:
            case Direction.RIGHT:
                self.head.move_right()
            case Direction.LEFT:
                self.head.move_left()
            case Direction.UP:
                self.head.move_up()
            case Direction.DOWN:
                self.head.move_down()
        self._adjust_tail()
        self.head.mark_current_as_visited()
        self.tail.mark_current_as_visited()


def process_input(path: Path) -> int:
    pos_head, pos_tail = Position(0, 0), Position(0, 0)
    head = Knot(pos_head)
    tail = Knot(pos_tail)
    rope = Rope(head, tail)
    with open(path, "r") as fin:
        for line in fin.readlines():
            direction, num_steps = line.split()
            for _ in range(int(num_steps)):
                rope.move_rope(direction)
    num_visited_by_tail = len(rope.tail.visited)
    return num_visited_by_tail


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rope Bridge")
    parser.add_argument(
        "--input",
        type=Path,
        default="day9/input/input.txt",
        help="Path to the input file.",
    )
    args = parser.parse_args()
    num_visited_by_tail = process_input(args.input)
    print(f"Total positions visited by tail {num_visited_by_tail}")
