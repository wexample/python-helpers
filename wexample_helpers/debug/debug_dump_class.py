from typing import Dict, Optional, Set, Type

from wexample_helpers.const.colors import Colors
from wexample_helpers.debug.abstract_debug import AbstractDebug


class DebugDumpClass(AbstractDebug):
    def __init__(self, cls: Type, depth: int = 0):
        self.cls = cls
        self.depth = depth
        super().__init__()

    def collect_data(self) -> None:
        self.data = self._collect_hierarchy(self.cls)

    def _collect_hierarchy(self, cls: Type, seen: Optional[Set[Type]] = None) -> Dict:
        if seen is None:
            seen = set()

        if cls in seen:
            return {
                "type": "circular",
                "name": cls.__name__
            }
        seen.add(cls)

        result = {
            "name": cls.__name__,
            "module": cls.__module__,
            "depth": self.depth
        }

        # Collect attributes
        attrs = {
            name: repr(value)
            for name, value in cls.__dict__.items()
            if not name.startswith('__') and not callable(value)
        }
        if attrs:
            result["attributes"] = attrs

        # Collect base classes
        bases = []
        for base in cls.__bases__:
            if base is not object:
                bases.append(self._collect_hierarchy(base, seen.copy()))
        if bases:
            result["bases"] = bases

        return result

    def print(self) -> None:
        self._print_hierarchy(self.data)

    def _print_hierarchy(self, data: Dict, indent: str = "") -> None:
        if data.get("type") == "circular":
            print(f"{indent}{Colors.YELLOW}↻ {data['name']} (circular){Colors.RESET}")
            return

        # Print class info
        class_info = f"{indent}{Colors.BLUE}→ {data['name']}{Colors.RESET}"
        if data['module'] != "__main__":
            class_info += f" {Colors.GREEN}({data['module']}){Colors.RESET}"
        print(class_info)

        # Print attributes
        if "attributes" in data:
            for name, value in data["attributes"].items():
                print(f"{indent}  {Colors.BRIGHT}{name}{Colors.RESET}: {Colors.GREEN}{value}{Colors.RESET}")

        # Print base classes
        if "bases" in data:
            for base in data["bases"]:
                self._print_hierarchy(base, indent + "    ")
