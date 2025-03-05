from abc import ABC, abstractmethod
from wexample_helpers.const.colors import Colors
from wexample_helpers.helpers.cli import cli_make_clickable_path

class AbstractDebug(ABC):
    def __init__(self):
        self.data = None
        self.collect_data()
    
    @abstractmethod
    def collect_data(self) -> None:
        """Collect debug data"""
        pass
    
    @abstractmethod
    def print(self) -> None:
        """Print debug data"""
        pass
    
    def execute(self) -> None:
        """Execute the debug operation"""
        self.print()

    def _format_class_name(self, name: str, module: str, indent: str = "") -> str:
        """Format class name with module."""
        result = f"{indent}{Colors.BLUE}→ {name}{Colors.RESET}"
        if module != "__main__":
            result += f" {Colors.GREEN}({module}){Colors.RESET}"
        return result
        
    def _format_file_path(self, path: str, line: int = None, indent: str = "") -> str:
        """Format file path with optional line number."""
        clickable_path = cli_make_clickable_path(path)
        line_info = f":{line}" if line is not None else ""
        return f"{indent}    {Colors.YELLOW}File: {clickable_path}{line_info}{Colors.RESET}"
        
    def _format_instance_name(self, name: str, indent: str = "") -> str:
        """Format instance name."""
        return f"{indent}{Colors.BLUE}Instance of {name}{Colors.RESET}"
        
    def _format_attributes_header(self, indent: str = "") -> str:
        """Format attributes section header."""
        return f"{indent}{Colors.BRIGHT}Instance attributes:{Colors.RESET}"
