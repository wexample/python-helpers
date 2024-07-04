import os
import shutil
from typing import Any

from wexample_helpers.const.types import AnyCallable


def directory_remove_tree_if_exists(directory: str) -> None:
    if os.path.exists(directory):
        shutil.rmtree(directory)


def directory_execute_inside(target_dir: str, callback: AnyCallable) -> Any:
    original_dir = os.getcwd()
    os.chdir(target_dir)
    response = callback()
    os.chdir(original_dir)

    return response


def directory_get_base_name(path: str) -> str:
    return os.path.basename(
        os.path.normpath(path))


def directory_get_parent_path(path: str) -> str:
    return os.path.dirname(
        os.path.normpath(path)) + os.sep


def directory_empty_dir(dir_path: str) -> None:
    # Iterate over each item in the directory
    for item_name in os.listdir(dir_path):
        # Construct the full path to the item
        item_path = os.path.join(dir_path, item_name)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)  # Remove the file or link
        elif os.path.isdir(item_path):
            # Recursively remove the directory
            shutil.rmtree(item_path)
