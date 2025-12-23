import re
from user_display.filters import RegexFilter, CompositeFilter

SAMPLE = [
    {"id": "1", "name": "Alice", "email": "a@example.com"},
    {"id": "2", "name": "Bob", "email": "b@example.com"},
    {"id": "3", "name": "Carol", "email": "carol@sample.org"},
]


def test_regex_filter_any_field():
    f = RegexFilter(r"sample")
    assert f.matches(SAMPLE[2])
    assert not f.matches(SAMPLE[0])


def test_regex_filter_fields_option():
    f = RegexFilter(r"^A", fields=["name"])
    assert f.matches(SAMPLE[0])
    assert not f.matches(SAMPLE[1])


def test_composite_and_or():
    f1 = RegexFilter(r"^A", fields=["name"])
    f2 = RegexFilter(r"example|sample", fields=["email"])
    both = CompositeFilter([f1, f2], op="and")
    one = CompositeFilter([f1, f2], op="or")
    assert both.matches(SAMPLE[0])
    assert one.matches(SAMPLE[0])
    assert not both.matches(SAMPLE[2])
    assert one.matches(SAMPLE[2])
