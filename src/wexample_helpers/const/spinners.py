from __future__ import annotations

# Common spinner frame sequences for terminal UIs.
# Braille-style spinner (smooth, compact, good Unicode support in modern terminals)
BRAILLE_SPINNER_FRAMES: list[str] = [
    "⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾",
]

# Default spinner exported for convenience
DEFAULT_SPINNER_FRAMES: list[str] = BRAILLE_SPINNER_FRAMES
