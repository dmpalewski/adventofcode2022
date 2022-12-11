import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class Tree:
    row_id: int
    col_id: int
    height: int


@dataclass
class Grid:
    trees: List[Tree] = field(default_factory=list)
    trees_by_row_id: Dict[int, List[Tree]] = field(default_factory=dict)
    trees_by_col_id: Dict[int, List[Tree]] = field(default_factory=dict)

    def add_tree(self, tree: Tree):
        self.trees.append(tree)
        if tree.row_id in self.trees_by_row_id:
            self.trees_by_row_id[tree.row_id].append(tree)
        else:
            self.trees_by_row_id[tree.row_id] = [tree]

        if tree.col_id in self.trees_by_col_id:
            self.trees_by_col_id[tree.col_id].append(tree)
        else:
            self.trees_by_col_id[tree.col_id] = [tree]

    def _get_trees_to_the_left(self, tree: Tree) -> List[Tree]:
        trees = [t for t in self.trees_by_row_id[tree.row_id] if t.col_id < tree.col_id]
        return trees

    def _get_trees_to_the_right(self, tree: Tree) -> List[Tree]:
        trees = [t for t in self.trees_by_row_id[tree.row_id] if t.col_id > tree.col_id]
        return trees

    def _get_trees_to_the_top(self, tree: Tree) -> List[Tree]:
        trees = [t for t in self.trees_by_col_id[tree.col_id] if t.row_id < tree.row_id]
        return trees

    def _get_trees_to_the_bottom(self, tree: Tree) -> List[Tree]:
        trees = [t for t in self.trees_by_col_id[tree.col_id] if t.row_id > tree.row_id]
        return trees

    def is_tree_hidden(self, tree: Tree) -> bool:
        hidden_from_left = any(
            [t.height >= tree.height for t in self._get_trees_to_the_left(tree)]
        )
        hidden_from_right = any(
            [t.height >= tree.height for t in self._get_trees_to_the_right(tree)]
        )
        hidden_from_top = any(
            [t.height >= tree.height for t in self._get_trees_to_the_top(tree)]
        )
        hidden_from_bottom = any(
            [t.height >= tree.height for t in self._get_trees_to_the_bottom(tree)]
        )
        is_hidden = (
            hidden_from_left
            and hidden_from_right
            and hidden_from_top
            and hidden_from_bottom
        )
        return is_hidden


def process_input(path: Path) -> int:
    grid = Grid()
    with open(path, "r") as fin:
        for row_id, line in enumerate(fin.readlines()):
            for col_id, height in enumerate(line.strip()):
                grid.add_tree(Tree(row_id, col_id, int(height)))
    visible_trees = [t for t in grid.trees if not grid.is_tree_hidden(t)]
    num_visible_trees = len(visible_trees)
    return num_visible_trees


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Treetop tree house")
    parser.add_argument(
        "--input",
        type=Path,
        default="day8/input/input.txt",
        help="Path to the input file.",
    )
    args = parser.parse_args()
    num_visible_trees = process_input(args.input)
    print(f"Total visible trees {num_visible_trees}")
