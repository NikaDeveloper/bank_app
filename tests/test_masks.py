import pytest
from src.masks import get_mask_card_number, get_mask_account

# Тесты для get_mask_card_number
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56 ** **** 3456"),  # Стандартный 16-значный номер
        (1234567890123456, "1234 56 ** **** 3456"),   # Номер как int
        ("123456789012345", "1234 56 ** **** 2345"),   # 15-значный номер
        ("1234567890123", "1234 56 ** **** 0123"),     # 13-значный номер
        ("123456", "1234 56 ** **** 3456"),         # Короткий номер (текущее поведение)
        ("12345", "1234 5 ** **** 2345"),           # Очень короткий номер
        ("123", "123 ** **** 123"),               # Еще короче
    ],
)
def test_get_mask_card_number_valid(card_number, expected):
    """Тестирование правильности маскирования номера карты."""
    assert get_mask_card_number(card_number) == expected

@pytest.mark.parametrize(
    "invalid_input, expected_message",
    [
        ("ABC123456789012", "Некорректный номер карты"), # Не цифры
        ("1234-5678-9012-3456", "Некорректный номер карты"), # С разделителями
        ("", "Некорректный номер карты"), # Пустая строка (не isdigit)
        (None, "Некорректный номер карты") # None (после str(None) -> "None")
    ]
)
def test_get_mask_card_number_invalid_input(invalid_input, expected_message):
    """Проверка обработки нецифровых входных строк."""
    assert get_mask_card_number(invalid_input) == expected_message

def test_get_mask_card_number_no_number():
    """Проверка, что функция корректно обрабатывает входные строки, где отсутствует номер карты (пустая строка)."""
    # Поведение isdigit() для пустой строки - False
    assert get_mask_card_number("") == "Некорректный номер карты"


# Тесты для get_mask_account
@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("12345678901234567890", "**7890"),  # Длинный номер счета (20 цифр)
        (9876543210, "**3210"),             # Номер как int
        ("12345", "**2345"),                # Номер короче стандартного
        ("1234", "**1234"),                 # Минимальная длина для маскирования последних 4 цифр
        ("123", "**123"),                   # Номер счета меньше 4 цифр
        ("12", "**12"),
        ("1", "**1"),
    ],
)
def test_get_mask_account_valid(account_number, expected):
    """Тестирование правильности маскирования номера счета."""
    assert get_mask_account(account_number) == expected

@pytest.mark.parametrize(
    "invalid_input, expected_message",
    [
        ("ABC12345", "Некорректный номер счета"), # Не цифры
        ("123-456", "Некорректный номер счета"), # С разделителями
        ("", "Некорректный номер счета"), # Пустая строка (не isdigit)
        (None, "Некорректный номер счета") # None
    ]
)
def test_get_mask_account_invalid_input(invalid_input, expected_message):
    """Проверка обработки нецифровых входных строк для счета."""
    assert get_mask_account(invalid_input) == expected_message

def test_get_mask_account_shorter_than_expected():
    """Проверка, что функция корректно обрабатывает номера счета меньше ожидаемой длины (но маскирует что есть)."""
    assert get_mask_account("789") == "**789"
    assert get_mask_account("5") == "**5"

def test_get_mask_account_no_number():
    """Проверка обработки пустой строки для номера счета."""
    assert get_mask_account("") == "Некорректный номер счета"
