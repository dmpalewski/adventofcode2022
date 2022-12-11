import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Union

FILE_PATTERN = re.compile(r"^(\d+) (\S+)$")
FOLDER_PATTERN = re.compile(r"^dir (\S+)$")
GET_PARENT_PATTERN = re.compile(r"^\$ cd \.\.$")
VISIT_FOLDER_PATTERN = re.compile(r"^\$ cd (?!\.\.)(\S+)$")

TOTAL_SPACE = 70000000
REQUIRED_SPACE = 30000000


@dataclass
class File:
    name: str
    size: int

    def get_size(self) -> int:
        return self.size


@dataclass
class BaseFolder:
    name: str
    size: int = 0


@dataclass
class Folder(BaseFolder):
    files: List[File] = field(default_factory=list)
    folders: List[BaseFolder] = field(default_factory=list)
    parent: Union[None, BaseFolder] = None

    def get_size(self) -> int:
        own_files_size = sum(f.get_size() for f in self.files)
        own_folders_size = sum(f.get_size() for f in self.folders)  # type:ignore
        total_size = own_files_size + own_folders_size
        self.size = total_size
        return total_size

    def add_file(self, file: File):
        self.files.append(file)

    def add_folder(self, folder: BaseFolder):
        self.folders.append(folder)

    def get_subfolder(self, name: str) -> Union[None, BaseFolder]:
        result = None
        for folder in self.folders:
            if folder.name == name:
                result = folder
                break
        return result

    def get_root(self):
        current_dir = self
        while current_dir.parent:
            current_dir = current_dir.parent
        return current_dir


def build_folder_structure(path: Path) -> Folder:
    current_folder = Folder("root")
    with open(path, "r") as fin:
        for line in fin.readlines():
            line = line.strip()
            if VISIT_FOLDER_PATTERN.match(line):
                folder_name = line.split()[-1]
                current_folder = (
                    current_folder.get_subfolder(folder_name) or current_folder
                )
            elif FOLDER_PATTERN.match(line):
                folder_name = line.split()[-1]
                folder = Folder(folder_name, parent=current_folder)
                current_folder.add_folder(folder)
            elif FILE_PATTERN.match(line):
                size, name = line.split()
                file = File(name, int(size))
                current_folder.add_file(file)
            elif GET_PARENT_PATTERN.match(line):
                current_folder = current_folder.parent
            else:
                continue
    root = current_folder.get_root()
    return root


def find_sizes_bfs(root: Folder) -> List[BaseFolder]:
    queue_ = [root]
    visited = [root]
    folders_with_sizes = []
    while queue_:
        current_folder = queue_.pop()
        folders_with_sizes.append(
            BaseFolder(current_folder.name, current_folder.get_size())
        )

        for child in current_folder.folders:
            if child not in visited:
                visited.append(child)
                queue_.append(child)
    return folders_with_sizes


def find_best_smallest_folder_to_delete(
    folders_with_sizes: List[BaseFolder], need_to_free: int
) -> BaseFolder:
    result = folders_with_sizes[0]  # delete root by default
    for folder in sorted(folders_with_sizes, key=lambda x: x.size):
        if folder.size >= need_to_free:
            result = folder
            break
    return result


def process_input(path: Path, limit: int) -> int:
    root_folder = build_folder_structure(path)
    folders_with_sizes = find_sizes_bfs(root_folder)
    folders_smaller_then_limit = [f for f in folders_with_sizes if f.size <= limit]
    total_size_smaller_than_limit = sum([f.size for f in folders_smaller_then_limit])
    return total_size_smaller_than_limit


def process_input_pt_2(path: Path) -> int:
    root_folder = build_folder_structure(path)
    folders_with_sizes = find_sizes_bfs(root_folder)
    current_free_space = TOTAL_SPACE - root_folder.size
    need_to_free_space = REQUIRED_SPACE - current_free_space
    folder_to_del = find_best_smallest_folder_to_delete(
        folders_with_sizes, need_to_free_space
    )
    return folder_to_del.size


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run No Space Left on the Device.")
    parser.add_argument(
        "--input",
        type=Path,
        default="day7/input/input.txt",
        help="Path to the input file.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100000,
        help="Max size of the dir to consider.",
    )
    args = parser.parse_args()
    total_size = process_input(args.input, args.limit)
    print(f"Total size of the directories {total_size}")

    size_to_del = process_input_pt_2(args.input)
    print(f"Size of the smallest folder to delete {size_to_del}")
