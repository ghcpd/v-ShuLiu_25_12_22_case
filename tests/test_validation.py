from user_display.validation import DefaultValidator


def test_default_validator_recovery():
    v = DefaultValidator()
    bad = {"id": None, "name": None, "created": "not-a-date"}
    out = v.validate(bad)
    assert out["id"] == ""
    assert out["name"] == ""
    assert out["created_at"] == ""
