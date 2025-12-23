import re
from user_display.filters import RegexFilter, CompositeFilter


USERS = [
    {"id": 1, "name": "Alice Wonderland", "email": "alice@example.com", "role": "Admin"},
    {"id": 2, "name": "Bob", "email": "bob@examples.org", "role": "User"},
    {"id": 3, "name": "Carol", "email": "carol@x.com", "role": "User"},
]


def test_regex_filter_case_insensitive():
    f = RegexFilter()
    res = f.apply(USERS, {"email": "EXAMPLE"})
    assert len(res) == 2


def test_regex_filter_exact():
    f = RegexFilter(flags=0)
    res = f.apply(USERS, {"email": "^bob@examples\\.org$"})
    assert len(res) == 1 and res[0]["id"] == 2


def test_composite_filter():
    f = CompositeFilter([RegexFilter(), RegexFilter()])
    res = f.apply(USERS, {"name": "o", "email": "x\\.com"})
    assert len(res) == 1 and res[0]["id"] == 3
