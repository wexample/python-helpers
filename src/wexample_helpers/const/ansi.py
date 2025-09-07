from __future__ import annotations

import re

# filestate: python-constant-sort
OSC8_RE = re.compile(r"\x1B\]8;;.*?\x1B\\")
CSI_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
