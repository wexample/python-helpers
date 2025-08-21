from typing import Optional, Dict

from wexample_helpers.common.debug.abstract_debug import AbstractDebug
from wexample_helpers.enums.debug_path_style import DebugPathStyle
from wexample_helpers.helpers.trace import trace_get_frames, trace_format


class DebugTrace(AbstractDebug):
    def __init__(
        self,
        path_style: DebugPathStyle = DebugPathStyle.FULL,
        paths_map: Optional[Dict] = None,
        message: Optional[str] = None,
        show_internal: bool = False,
    ):
        self.path_style = path_style
        self.paths_map = paths_map
        self.message = message
        self.show_internal = show_internal
        super().__init__()

    def collect_data(self) -> None:
        # No data collection needed for trace
        pass

    def print(self, silent: bool = False):
        if silent:
            # Build text without printing
            frames = trace_get_frames(
                skip_frames=(1 if not self.show_internal else None),
                path_style=self.path_style,
                paths_map=self.paths_map,
            )
            return trace_format(frames)

        # Print by formatting frames directly to honor truncate_stack and show_internal
        frames = trace_get_frames(
            skip_frames=(1 if not self.show_internal else None),
            path_style=self.path_style,
            paths_map=self.paths_map,
        )
        text = trace_format(frames)
        if text:
            print(text)
        return ""
