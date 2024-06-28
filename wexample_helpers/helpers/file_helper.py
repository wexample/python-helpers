import os
from pathlib import Path
from typing import Union, Optional, Tuple

from wexample_helpers.const.types import FileStringOrPath


def file_change_mode_recursive(path: str, mode: int) -> None:
    # Change permissions for the current path

    try:
        if not os.path.islink(path):
            os.chmod(path, mode)  # Change owner of the file/directory
    except FileNotFoundError:
        pass

    # If the path is a directory, loop through its contents and call the function recursively
    if os.path.isdir(path) and not os.path.islink(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            file_change_mode_recursive(item_path, mode)


def file_read(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def file_resolve_path(path: FileStringOrPath) -> Path:
    return path if path is Path else Path(path)


def file_mode_octal_to_num(mode: Union[str, int]) -> int:
    return int(mode, 8)


def file_mode_num_to_octal(num: int) -> str:
    return str(oct(num)[-3:])


def file_path_get_octal_mode(path: Path) -> str:
    return file_mode_num_to_octal(path.stat().st_mode)


def file_touch(path: str, times: Optional[Tuple[int, int]] = None) -> None:
    with open(path, "a"):
        os.utime(path, times)


def file_validate_mode_octal(mode: Union[str, int]) -> bool:
    if len(mode) != 3:
        return False
    for char in mode:
        if char not in '01234567':
            return False
    return True


def file_validate_mode_octal_or_fail(mode: Union[str, int]) -> bool:
    if not file_validate_mode_octal(mode):
        raise Exception(f'Bad mode format {mode}')
    return True


def file_write(file_path: str, content: str) -> None:
    with open(file_path, "w") as f:
        f.write(content)
