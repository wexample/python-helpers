import inspect
from typing import Any, Dict, Optional, Set

from wexample_helpers.const.colors import Colors
from wexample_helpers.debug.abstract_debug import AbstractDebug


class DebugDump(AbstractDebug):
    def __init__(self, obj: Any, max_depth: int = 100):
        self.obj = obj
        self.max_depth = max_depth
        super().__init__()

    def collect_data(self) -> None:
        self.data = self._collect_data(self.obj)

    def _collect_data(self, obj: Any, depth: int = 0, seen: Optional[Set[int]] = None) -> Dict:
        if seen is None:
            seen = set()

        if depth > self.max_depth:
            return {"type": "max_depth"}

        obj_id = id(obj)
        if obj_id in seen and not isinstance(obj, (int, float, str, bool)):
            return {"type": "circular"}
        seen.add(obj_id)

        result = {
            "type": type(obj).__name__,
            "depth": depth
        }

        if inspect.isclass(obj):
            from wexample_helpers.debug.debug_dump_class import DebugDumpClass
            class_dump = DebugDumpClass(obj, depth)
            class_dump.collect_data()
            result["class_data"] = class_dump.data

        elif hasattr(obj, '__class__') and not isinstance(obj, (int, float, str, bool, list, tuple, dict)):
            from wexample_helpers.debug.debug_dump_class import DebugDumpClass
            result["instance_of"] = obj.__class__.__name__
            class_dump = DebugDumpClass(obj.__class__, depth + 2)
            class_dump.collect_data()
            result["class_data"] = class_dump.data

            instance_attrs = {
                name: self._collect_data(value, depth + 4, seen.copy())
                for name, value in inspect.getmembers(obj)
                if not name.startswith('_') and not callable(value)
            }
            result["attributes"] = instance_attrs

        elif isinstance(obj, (int, float, str, bool)):
            result["value"] = repr(obj)

        elif isinstance(obj, (list, tuple)):
            result["elements"] = [
                self._collect_data(item, depth + 4, seen.copy())
                for item in obj
            ]

        elif isinstance(obj, dict):
            result["items"] = [
                {
                    "key": repr(key),
                    "value": self._collect_data(value, depth + 4, seen.copy())
                }
                for key, value in obj.items()
            ]

        elif inspect.isfunction(obj) or inspect.ismethod(obj):
            result["name"] = obj.__name__

        return result

    def print(self) -> None:
        self._print_data(self.data)

    def _print_data(self, data: Dict, indent: str = "") -> None:
        if data["type"] == "max_depth":
            print(f"{indent}{Colors.YELLOW}[Max depth reached]{Colors.RESET}")
            return

        if data["type"] == "circular":
            print(f"{indent}{Colors.YELLOW}[Circular reference]{Colors.RESET}")
            return

        if "instance_of" in data:
            print(f"{indent}{Colors.BLUE}Instance of {data['instance_of']}{Colors.RESET}")
            self._print_data(data["class_data"], indent + "  ")

            if "attributes" in data:
                print(f"{indent}{Colors.BRIGHT}Instance attributes:{Colors.RESET}")
                for name, value in data["attributes"].items():
                    print(f"{indent}  {Colors.BRIGHT}{name}{Colors.RESET} →")
                    self._print_data(value, indent + "    ")

        elif "class_data" in data:
            self._print_data(data["class_data"], indent)

        elif "value" in data:
            print(f"{indent}{Colors.BLUE}{data['type']}{Colors.RESET}: {Colors.GREEN}{data['value']}{Colors.RESET}")

        elif "elements" in data:
            print(f"{indent}{Colors.BLUE}{data['type']}{Colors.RESET} ({len(data['elements'])} elements):")
            for i, element in enumerate(data["elements"]):
                print(f"{indent}  {Colors.BRIGHT}[{i}]{Colors.RESET} →")
                self._print_data(element, indent + "    ")

        elif "items" in data:
            print(f"{indent}{Colors.BLUE}{data['type']}{Colors.RESET} ({len(data['items'])} elements):")
            for item in data["items"]:
                print(f"{indent}  {Colors.BRIGHT}{item['key']}{Colors.RESET} →")
                self._print_data(item["value"], indent + "    ")

        elif "name" in data:
            print(f"{indent}{Colors.BLUE}{data['type']}{Colors.RESET}: {Colors.GREEN}{data['name']}{Colors.RESET}")
