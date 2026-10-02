from fonts_andorra.assistant.redact import redact


def test_redacts_direct_identifiers_and_keeps_dates():
    text = (
        "mail@example.ad +376 123 456 12345678 AD1200000000000000000000 "
        "AB1234567 F123456Z 2026-10-02"
    )
    masked, count = redact(text)
    assert count == 6
    assert "mail@example.ad" not in masked
    assert "123 456" not in masked
    assert "12345678" not in masked
    assert "AD1200000000000000000000" not in masked
    assert "AB1234567" not in masked
    assert "F123456Z" not in masked
    assert "2026-10-02" in masked


def test_redact_counts_each_match():
    masked, count = redact("a@example.ad and b@example.ad")
    assert count == 2
    assert masked.count("[REDACTED_EMAIL]") == 2


def test_redacts_grouped_iban_without_swallowing_following_id():
    masked, count = redact("AD12 0000 0000 0000 0000 0000 AB1234567")
    assert count == 2
    assert "AD12" not in masked
    assert "AB1234567" not in masked
