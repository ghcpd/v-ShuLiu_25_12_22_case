import os
import json
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string
from user_display import UserStore


SAMPLE = [
    {"id": 1, "name": "Alice", "email": "a@x.com", "role": "Admin", "status": "Active", "last_login": "2025-01-01"},
    {"id": 2, "name": "bob", "email": "b@x.com", "role": "User", "status": "Inactive", "last_login": "2025-02-02"},
]


def test_display_basic():
    out = display_users(SAMPLE)
    assert "PROCESSED=2" in out
    assert "Alice" in out


def test_get_user_by_id_found():
    u = get_user_by_id(SAMPLE, 1)
    assert u["name"] == "Alice"


def test_get_user_by_id_missing():
    assert get_user_by_id(SAMPLE, 999) is None


def test_filter_users_simple():
    res = filter_users(SAMPLE, {"name": "ali"})
    assert len(res) == 1 and res[0]["id"] == 1


def test_export_json():
    s = export_users_to_string(SAMPLE)
    obj = json.loads(s)
    assert obj["count"] == 2


def test_store_api_roundtrip():
    store = UserStore(SAMPLE)
    assert store.get_user_by_id(2)["name"] == "bob"
    assert "PROCESSED" in store.display_users()
