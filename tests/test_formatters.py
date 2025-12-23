from user_display import formatter_registry

SAMPLE = [
    {"id": "1", "name": "Alice", "email": "a@example.com"},
    {"id": "2", "name": "Bob", "email": "b@example.com"},
]


def test_json_formatter():
    f = formatter_registry["json"]
    s = f.format_many(SAMPLE)
    assert "Alice" in s and s.strip().startswith("[")


def test_compact_formatter_fields():
    f = formatter_registry["compact"]
    s = f.format_many(SAMPLE, fields=["id", "email"])
    assert "a@example.com" in s and "Bob" not in s


def test_table_formatter_columns():
    f = formatter_registry["table"]
    s = f.format_many(SAMPLE)
    assert "id" in s.splitlines()[0]
