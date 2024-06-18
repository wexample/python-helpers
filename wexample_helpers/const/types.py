from pathlib import Path
from typing import List, Any, Dict, Union

AnyList = List[Any]
StringKeysDict = Dict[str, Any]
BasicInlineValue = str | int | float | bool | None
BasicValue = BasicInlineValue | AnyList | StringKeysDict

FileStringOrPath = Union[str, Path]