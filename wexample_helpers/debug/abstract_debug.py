from abc import ABC, abstractmethod
from typing import Any

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
