import pytest
from user_display.formatters import get_formatter

sample = [
    {"id": 1, "name": "Alice", "email": "a@x.com", "role": "User"},
    {"id": 2, "name": "Bob", "email": "b@x.com", "role": "Admin"},
]


def test_compact():
    fmt = get_formatter("compact")
    out = fmt.format(sample)
    assert "ID=1" in out
    assert "NAME=Alice" in out


def test_json():
    fmt = get_formatter("json")
    out = fmt.format(sample, fields=["id","name"])
    assert "Alice" in out and "Bob" in out


def test_table():
    fmt = get_formatter("table")
    out = fmt.format(sample)
    assert "ID" in out and "NAME" in out
