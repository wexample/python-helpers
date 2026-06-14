from __future__ import annotations


class HasShortClassNameClassMixin:
    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return None

    @classmethod
    def get_name(cls) -> str:
        return cls.get_short_class_name()

    @classmethod
    def get_short_class_name(cls) -> str:
        suffix = cls.get_class_name_suffix()
        if suffix is None:
            return cls.__name__
        short_name = cls.__name__
        suffix_len = len(suffix)
        if short_name.endswith(suffix):
            return short_name[:-suffix_len]
        return short_name
