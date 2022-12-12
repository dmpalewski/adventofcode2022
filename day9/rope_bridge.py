import argparse
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Set, Tuple, Union


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
    visited: Set[Tuple[int, int]]

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

    def mark_current_as_visited(self):
        self.visited.add(
            (
                self.position.x,
                self.position.y,
            )
        )


@dataclass
class TailKnot(Knot):
    previous_knot: Knot
    position_diff: Position = Position(0, 0)

    def _calculate_position_diff(self):
        x_diff = self.previous_knot.position.x - self.position.x
        y_diff = self.previous_knot.position.y - self.position.y
        self.position_diff = Position(x_diff, y_diff)

    def _diagonal_move_y(self):
        if self.position_diff.y < 0:
            self.move_down()
        elif self.position_diff.y > 0:
            self.move_up()

    def _diagonal_move_x(self):
        if self.position_diff.x < 0:
            self.move_left()
        elif self.position_diff.x > 0:
            self.move_right()

    def adjust(self):
        self._calculate_position_diff()
        if self.position_diff.x == -2:
            self.move_left()
            self._diagonal_move_y()
        elif self.position_diff.x == 2:
            self.move_right()
            self._diagonal_move_y()
        if self.position_diff.y == -2:
            self.move_down()
            self._diagonal_move_x()
        elif self.position_diff.y == 2:
            self.move_up()
            self._diagonal_move_x()


@dataclass
class Rope:
    head: Knot
    tail: List[TailKnot]

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
        self.head.mark_current_as_visited()

        for tail_knot in self.tail:
            tail_knot.adjust()
            tail_knot.mark_current_as_visited()


def process_input(path: Path) -> int:
    pos_head, pos_tail = Position(0, 0), Position(0, 0)
    head = Knot(position=pos_head, visited=set())
    tail = TailKnot(position=pos_tail, visited=set(), previous_knot=head)
    rope = Rope(head, [tail])
    with open(path, "r") as fin:
        for line in fin.readlines():
            direction, num_steps = line.split()
            for _ in range(int(num_steps)):
                rope.move_rope(direction)
    num_visited_by_tail = len(rope.tail[-1].visited)
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
