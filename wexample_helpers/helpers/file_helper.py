from pathlib import Path
from typing import Union

from wexample_helpers.const.types import FileStringOrPath


def file_resolve_path(path: FileStringOrPath) -> Path:
    return path if path is Path else Path(path)


def file_mode_octal_to_num(mode: Union[str, int]) -> int:
    return int(mode, 8)


def file_mode_num_to_octal(num: int) -> str:
    return str(oct(num)[-3:])


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
