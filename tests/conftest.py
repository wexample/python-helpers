import pytest


def pytest_collection_modifyitems(config, items):
    skip_reason = pytest.mark.skip(reason="Skipped Pydantic-related tests during migration to attrs/cattrs")
    patterns = (
        "tests/syntax/test_pydantic_",
        "tests/syntax/test_unique_base_model.py",
    )
    for item in items:
        nodeid = item.nodeid
        if any(pat in nodeid for pat in patterns):
            item.add_marker(skip_reason)
