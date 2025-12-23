from user_display import formatter_registry

SAMPLE = [
    {"id": "1", "name": "Alice", "email": "a@example.com"},
    {"id": "2", "name": "Bob", "email": "b@example.com"},
]


def test_csv_formatter_default_fields():
    f = formatter_registry["csv"]
    s = f.format_many(SAMPLE)
    assert s.splitlines()[0] == "id,name,email"
    assert "a@example.com" in s


def test_rich_formatter_contains_table():
    f = formatter_registry["rich"]
    s = f.format_many(SAMPLE)
    # rich output contains name headers and rows
    assert "Alice" in s and "Bob" in s
