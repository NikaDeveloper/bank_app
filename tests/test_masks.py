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
def test_get_mask_card_number_valid(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("12345678901234567890", "**7890"),
        (9876543210, "Некорректный номер счета"),
    ],
)
def test_get_mask_account_valid(account_number, expected):
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_input, expected_message",
    [
        ("ABC12345", "Некорректный номер счета"),
        ("123-456", "Некорректный номер счета"),
        ("", "Некорректный номер счета"),
        (None, "Некорректный номер счета"),
        ("123", "Некорректный номер счета"),  # слишком короткий
        ("12", "Некорректный номер счета"),
        ("1", "Некорректный номер счета"),
    ],
)
def test_get_mask_account_invalid_input(invalid_input, expected_message):
    assert get_mask_account(invalid_input) == expected_message
