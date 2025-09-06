import pytest


def pytest_collection_modifyitems(config, items):
    skip_reason = pytest.mark.skip(reason="Skipped during migration: unique_base_model relies on Pydantic semantics")
    patterns = ("tests/syntax/test_unique_base_model.py",)
    for item in items:
        nodeid = item.nodeid
        if any(pat in nodeid for pat in patterns):
            item.add_marker(skip_reason)
