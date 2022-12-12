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

    def _get_non_blocking_trees_to_the_left(self, tree: Tree) -> List[Tree]:
        trees = []
        row = self.trees_by_row_id[tree.row_id]
        for i in range(tree.col_id - 1, -1, -1):
            left_tree = row[i]
            if left_tree.height < tree.height:
                trees.append(left_tree)
            else:
                trees.append(left_tree)
                break
        return trees

    def _get_non_blocking_trees_to_the_right(self, tree: Tree) -> List[Tree]:
        trees = []
        row = self.trees_by_row_id[tree.row_id]
        for i in range(tree.col_id + 1, len(row)):
            right_tree = row[i]
            if right_tree.height < tree.height:
                trees.append(right_tree)
            else:
                trees.append(right_tree)
                break
        return trees

    def _get_non_blocking_trees_to_the_top(self, tree: Tree) -> List[Tree]:
        trees = []
        column = self.trees_by_col_id[tree.col_id]
        for i in range(tree.row_id - 1, -1, -1):
            top_tree = column[i]
            if top_tree.height < tree.height:
                trees.append(top_tree)
            else:
                trees.append(top_tree)
                break
        return trees

    def _get_non_blocking_trees_to_the_bottom(self, tree: Tree) -> List[Tree]:
        trees = []
        column = self.trees_by_col_id[tree.col_id]
        for i in range(tree.row_id + 1, len(column)):
            bottom_tree = column[i]
            if bottom_tree.height < tree.height:
                trees.append(bottom_tree)
            else:
                trees.append(bottom_tree)
                break
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

    def get_tree_scientific_score(self, tree: Tree) -> int:
        score_left = len(self._get_non_blocking_trees_to_the_left(tree))
        score_right = len(self._get_non_blocking_trees_to_the_right(tree))
        score_top = len(self._get_non_blocking_trees_to_the_top(tree))
        score_bottom = len(self._get_non_blocking_trees_to_the_bottom(tree))
        scientific_score = score_left * score_right * score_top * score_bottom
        return scientific_score


def load_grid(path: Path) -> Grid:
    grid = Grid()
    with open(path, "r") as fin:
        for row_id, line in enumerate(fin.readlines()):
            for col_id, height in enumerate(line.strip()):
                grid.add_tree(Tree(row_id, col_id, int(height)))
    return grid


def process_input(grid: Grid) -> int:
    visible_trees = [t for t in grid.trees if not grid.is_tree_hidden(t)]
    num_visible_trees = len(visible_trees)
    return num_visible_trees


def process_input_pt_2(grid: Grid) -> int:
    scientific_scores = [grid.get_tree_scientific_score(t) for t in grid.trees]
    scientific_score = max(scientific_scores)
    return scientific_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Treetop tree house")
    parser.add_argument(
        "--input",
        type=Path,
        default="day8/input/input.txt",
        help="Path to the input file.",
    )
    args = parser.parse_args()
    grid = load_grid(args.input)
    num_visible_trees = process_input(grid)
    print(f"Total visible trees {num_visible_trees}")

    highest_scientific_score = process_input_pt_2(grid)
    print(f"Highest scientific score {highest_scientific_score}")
