import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тесты для get_mask_card_number
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56 ** **** 3456"),
        (1234567890123456, "1234 56 ** **** 3456"),
    ],
)
def test_get_mask_card_number_valid(card_number, expected, caplog):
    with caplog.at_level("DEBUG"):
        result = get_mask_card_number(card_number)
    assert result == expected
    assert "Успешная маскировка карты" in caplog.text

@pytest.mark.parametrize(
    "invalid_card",
    ['abcd1234', "1234-5678", "", None]
)
def test_get_card_number_invalid(invalid_card, caplog):
    with caplog.at_level("ERROR"):
        result = get_mask_card_number(invalid_card)
    assert result == "Некорректный номер карты"
    assert "Невалидный номер карты" in caplog.text


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("12345678901234567890", "**7890"),
        (9876543210, "Некорректный номер счета"),
    ],
)
def test_get_mask_account_valid(account_number, expected, caplog):
    with caplog.at_level("DEBUG"):
        result = get_mask_account(account_number)
    assert result == expected
    if expected == "Некорректный номер счета":
        assert "Невалидный номер счета" in caplog.text
    else:
        assert "Успешная маскировка счета" in caplog.text


@pytest.mark.parametrize(
    "invalid_input, expected_message",
    [
        ("ABC12345", "Некорректный номер счета"),
        ("123-456", "Некорректный номер счета"),
        ("", "Некорректный номер счета"),
        (None, "Некорректный номер счета"),
        ("123", "Некорректный номер счета"),
        ("12", "Некорректный номер счета"),
        ("1", "Некорректный номер счета"),
    ],
)
def test_get_mask_account_invalid_input(invalid_input, expected_message, caplog):
    with caplog.at_level("ERROR"):
        result = get_mask_account(invalid_input)
    assert result == expected_message
    assert "Невалидный номер счета" in caplog.text
