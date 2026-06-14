from __future__ import annotations

import functools


def abstract_method(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> None:
        cls = type(args[0]).__name__
        raise NotImplementedError(f"{cls}.{func.__name__}() must be implemented")

    wrapper.__isabstract__ = True
    return wrapper
