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
