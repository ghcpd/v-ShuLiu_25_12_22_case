import os
import time
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string

SAMPLE = [
    {"id": "1", "name": "Alice", "email": "a@example.com"},
    {"id": "2", "name": "Bob", "email": "b@example.com"},
]


def test_display_default_table():
    out = display_users(users=SAMPLE, fmt="table")
    assert "Alice" in out and "Bob" in out


def test_get_user_by_id_found():
    display_users(users=SAMPLE)
    u = get_user_by_id("1")
    assert u["name"] == "Alice"


def test_get_user_by_id_not_found():
    display_users(users=SAMPLE)
    try:
        get_user_by_id("missing")
        assert False, "expected exception"
    except Exception:
        pass


def test_export_json():
    s = export_users_to_string(users=SAMPLE, fmt="json")
    assert "a@example.com" in s


def test_filter_callable():
    display_users(users=SAMPLE)
    out = filter_users(lambda u: u["name"].startswith("A"))
    assert len(out) == 1 and out[0]["name"] == "Alice"
