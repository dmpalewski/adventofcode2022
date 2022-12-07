import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

OPERATION_PARSER = re.compile(r"^move (\S+) from (\S+) to (\S+)$")


@dataclass
class Stack:
    id: str
    crates: str

    def add_crates_before(self, s: str):
        self.crates = s + self.crates

    def add_crates_after(self, s: str):
        self.crates += s[::-1]

    def remove_n_crates(self, n: int):
        removed_crates = self.crates[-n:]
        self.crates = self.crates[:-n]
        return removed_crates


@dataclass
class Operation:
    num_crates: int
    move_from: str
    move_to: str


@dataclass
class Task:
    ids: List[str]
    stacks: Dict[str, Stack]
    operations: List[Operation]

    def complete_all_operations(self):
        for operation in self.operations:
            removed_crates = self.stacks.get(operation.move_from).remove_n_crates(
                operation.num_crates
            )
            self.stacks.get(operation.move_to).add_crates_after(removed_crates)

    def get_codes_of_top_crates(self):
        codes = "".join([self.stacks[stack_id].crates[-1] for stack_id in self.ids])
        return codes


def parse_input(path: Path) -> Task:
    with open(path, "r") as fin:
        operations = []
        crate_rows = []
        stack_ids = []
        stack_map = {}
        for line in fin.readlines():
            if "move" in line:
                res = OPERATION_PARSER.match(line)
                if res:
                    operations.append(
                        Operation(int(res.group(1)), res.group(2), res.group(3))
                    )
            elif "[" in line:
                crate_rows.append(line)
            elif not line.isspace():
                stack_ids = line.split()
                stack_map = {stack_id: Stack(stack_id, "") for stack_id in stack_ids}
        for crate_row in crate_rows:
            row_len = len(crate_row)
            for i, start in enumerate(range(0, row_len, 4)):
                crate = crate_row[start : min(row_len, start + 4)][1]
                if not crate.isspace():
                    stack_id = stack_ids[i]
                    stack_map[stack_id].add_crates_before(crate)
    return Task(ids=stack_ids, stacks=stack_map, operations=operations)


def process_input(path: Path) -> str:
    task = parse_input(path=path)
    task.complete_all_operations()
    message = task.get_codes_of_top_crates()
    return message


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Supply Stack.")
    parser.add_argument(
        "--input",
        type=Path,
        default="day5/input/input.txt",
        help="Path to the input file.",
    )
    args = parser.parse_args()
    message = process_input(args.input)
    print(f"Message for the elves {message}.")
