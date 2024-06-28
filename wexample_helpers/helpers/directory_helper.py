import os
import shutil


def directory_remove_tree_if_exists(directory: str) -> None:
    if os.path.exists(directory):
        shutil.rmtree(directory)
