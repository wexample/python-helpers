from typing import Any, List


def import_dummy(classes: Any) -> None:
    """
    Fix this error, by importing classes for in a dummy method. These classes are actually not used anywhere :
    pydantic.errors.PydanticUserError: `ClassName` is not fully defined; you should define `Kernel`,
    then call `CountAdminCommand.model_rebuild()`.
    Using this method allow to add missing imports in file, event not used in page, and prevent auto formatters
    to consider import as useless.
    """
    pass
