import re
from user_display.filters import RegexFilter, CompositeFilter
from user_display.validation import DefaultValidator

sample = [
    {"id": 1, "name": "Alice", "email": "a@x.com", "role": "User", "status":"Active"},
    {"id": 2, "name": "Bob", "email": "b@x.com", "role": "Admin", "status":"Inactive"},
]


def test_regex_filter():
    f = RegexFilter("email", r"@x\\.com$")
    # pattern with a single escaped dot
    f2 = RegexFilter("email", r"@x\.com$")
    assert f2.match(sample[0])
    assert f2.match(sample[1])


def test_composite():
    f1 = RegexFilter("email", r"^a")
    f2 = RegexFilter("status", r"Active")
    comp = CompositeFilter([f1,f2])
    assert comp.match(sample[0])
    assert not comp.match(sample[1])


def test_validator_repair():
    v = DefaultValidator()
    ok, u = v.validate({"name":"X"})
    assert ok
    assert "email" in u and "id" in u
