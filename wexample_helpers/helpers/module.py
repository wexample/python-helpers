from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def module_load(file_path: "Path"):
    import importlib
    import os

    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to create spec for {file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
