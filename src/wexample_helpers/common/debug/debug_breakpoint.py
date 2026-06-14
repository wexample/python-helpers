from __future__ import annotations

import pdb

from wexample_helpers.common.debug.abstract_debug import AbstractDebug

_PDB_HELP_TEXT = "\n".join((
    "Commands:",
    "  p variable  : Print variable",
    "  n          : Next line",
    "  c          : Continue execution",
    "  q          : Quit",
    "  h          : Help (more commands)",
))


class DebugBreakpoint(AbstractDebug):
    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__()

    def collect_data(self) -> None:
        # No data collection needed for breakpoint
        pass

    def print(self, silent: bool = False):
        text = (
            f"\n Debug breakpoint: {self.message}\n{_PDB_HELP_TEXT}"
            if self.message
            else _PDB_HELP_TEXT
        )

        if silent:
            # In silent mode, do not start pdb; return the helper text instead
            return text

        print(text)
        pdb.set_trace()
        return ""
