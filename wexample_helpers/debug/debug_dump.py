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

    def _format_class_name(self, class_name: str, module_name: str, indent: str = "") -> str:
        class_info = f"{indent}{Colors.BLUE}→ {class_name}{Colors.RESET}"
        if module_name != "__main__":
            class_info += f" {Colors.GREEN}({module_name}){Colors.RESET}"
        return class_info

    def _format_file_path(self, file_path: str, line_number: int = None, indent: str = "") -> str:
        clickable_path = cli_make_clickable_path(file_path)
        return f"{indent}    {Colors.YELLOW}File: {clickable_path}:{line_number}{Colors.RESET}"

    def _format_instance_name(self, instance_name: str, indent: str = "") -> str:
        return f"{indent}{Colors.BLUE}Instance of {instance_name}{Colors.RESET}"

    def _format_attributes_header(self, indent: str = "") -> str:
        return f"{indent}{Colors.BRIGHT}Instance attributes:{Colors.RESET}"

    def _print_data(self, data: Dict, indent: str = "") -> None:
        if not isinstance(data, dict):
            print(f"{indent}{Colors.YELLOW}[Invalid data structure]{Colors.RESET}")
            return

        data_type = data.get("type", "unknown")
            
        if data_type == "max_depth":
            print(f"{indent}{Colors.YELLOW}[Max depth reached]{Colors.RESET}")
            return
            
        if data_type == "circular":
            print(f"{indent}{Colors.YELLOW}[Circular reference]{Colors.RESET}")
            return
            
        if data_type == "class":
            print(self._format_class_name(data['name'], data['module'], indent))
            if "source_file" in data:
                print(self._format_file_path(data['source_file'], None, indent))
                
            if "attributes" in data:
                for name, value in data["attributes"].items():
                    print(f"{indent}  {Colors.BRIGHT}{name}{Colors.RESET}: {Colors.GREEN}{value}{Colors.RESET}")
                    
            if "bases" in data:
                for base in data["bases"]:
                    self._print_data(base, indent + "    ")
            return
            
        if "instance_of" in data:
            print(self._format_instance_name(data['instance_of'], indent))
            if "dump_location" in data:
                location = data['dump_location']
                print(self._format_file_path(location['file'], location['line'], indent))
            
            if "class_data" in data:
                self._print_data(data["class_data"], indent + "  ")
            
            if "attributes" in data:
                print(self._format_attributes_header(indent))
                for name, value in data["attributes"].items():
                    print(f"{indent}  {Colors.BRIGHT}{name}{Colors.RESET} →")
                    self._print_data(value, indent + "    ")
                    
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
