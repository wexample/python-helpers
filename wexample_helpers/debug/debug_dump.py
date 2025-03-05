import inspect
from typing import Any, Dict, List, Optional, Set

from wexample_helpers.debug.abstract_debug import AbstractDebug
from wexample_helpers.const.colors import Colors
from wexample_helpers.helpers.cli import cli_make_clickable_path

class DebugDump(AbstractDebug):
    def __init__(self, obj: Any, max_depth: int = 100):
        self.obj = obj
        self.max_depth = max_depth
        self.current_depth = 0
        # Get caller frame info
        frame = inspect.currentframe()
        caller = frame.f_back if frame else None
        self.caller_info = inspect.getframeinfo(caller) if caller else None
        super().__init__()
        
    def collect_data(self) -> None:
        self.data = self._collect_data(self.obj)
        if self.caller_info:
            self.data["dump_location"] = {
                "file": self.caller_info.filename,
                "line": self.caller_info.lineno
            }

    def _collect_data(self, obj: Any, depth: int = 0, seen: Optional[Set[int]] = None) -> Dict:
        if seen is None:
            seen = set()

        # Check for max depth
        if depth >= self.max_depth:
            return {"type": "max_depth"}

        # Get object id for circular reference detection
        obj_id = id(obj)
        if obj_id in seen:
            return {"type": "circular"}
        seen.add(obj_id)

        # Handle different types of objects
        if isinstance(obj, (str, int, float, bool)):
            return {
                "type": type(obj).__name__,
                "value": repr(obj)
            }
        elif isinstance(obj, (list, tuple, set)):
            return {
                "type": type(obj).__name__,
                "elements": [self._collect_data(item, depth + 1, seen.copy()) for item in obj]
            }
        elif isinstance(obj, dict):
            return {
                "type": "dict",
                "items": [
                    {
                        "key": self._collect_data(key, depth + 1, seen.copy()),
                        "value": self._collect_data(value, depth + 1, seen.copy())
                    }
                    for key, value in obj.items()
                ]
            }
        else:
            # Handle class instance
            class_data = {
                "type": "class",
                "name": obj.__class__.__name__,
                "module": obj.__class__.__module__,
                "source_file": inspect.getfile(obj.__class__)
            }

            # Collect instance attributes
            attrs = {}
            for name, value in obj.__dict__.items():
                if not name.startswith('__'):
                    attrs[name] = self._collect_data(value, depth + 1, seen.copy())

            return {
                "instance_of": obj.__class__.__name__,
                "class_data": class_data,
                "attributes": attrs
            }

    def print(self) -> None:
        self._print_data(self.data)
