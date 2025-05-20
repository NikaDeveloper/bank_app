import pytest

from src.widget import get_date, mask_account_card


# Тесты для mask_account_card
@pytest.mark.parametrize(
    "requisites, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79 ** **** 6361"),
        ("MasterCard 1234567890123450", "MasterCard 1234 56 ** **** 3450"),
        ("Счет 73654108430135874305", "Счет ** 4305"),
        ("Maestro 1234567890123", "Maestro 1234 56 ** **** 0123"),  # 13 цифр
        ("Счет 1234567890", "Счет **7890"),  # 10 цифр
    ],
)
def test_mask_account_card_valid_inputs(requisites, expected):
    """Тесты для проверки, что функция корректно распознает и применяет нужный тип маскировки."""
    assert mask_account_card(requisites) == expected


@pytest.mark.parametrize(
    "requisites, error_message",
    [
        (
            "Visa 123",
            "Ошибка: Некорректная длина номера карты",
        ),  # Карта, короткий номер
        ("Счет 123", "Ошибка: Некорректная длина номера счета"),  # Счет, короткий номер
        (
            "Card 123456789012345678901",
            "Ошибка: Некорректная длина номера карты",
        ),  # Карта, длинный номер
        (
            "Счет 12345678901234567890123",
            "Ошибка: Некорректная длина номера счета",
        ),  # Счет, длинный номер
        ("VisaCard", "Ошибка: Некорректный формат входных данных"),  # Нет номера
        (
            "1234567890123456",
            "Ошибка: Некорректный формат входных данных",
        ),  # Только номер
        (
            "Visa ABCDE12345FGHI6789",
            "Ошибка: Номер карты/счета должен содержать только цифры",
        ),
        ("Счет ABC123DEF45", "Ошибка: Номер карты/счета должен содержать только цифры"),
        ("", "Ошибка: Некорректный формат входных данных"),  # Пустая строка
    ],
)
def test_mask_account_card_invalid_inputs(requisites, error_message):
    """Тестирование функции на обработку некорректных входных данных и проверка ее устойчивости к ошибкам."""
    assert mask_account_card(requisites) == error_message


# Тесты для get_date
@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
    ],
)
def test_get_date_valid_formats(date_str, expected):
    """Тестирование правильности преобразования даты."""
    assert get_date(date_str) == expected


@pytest.mark.parametrize(
    "date_str, expected_part",  # Проверяем, что части даты правильно извлекаются даже если строка длиннее
    [
        ("2021-05-20AnythingElse", "20.05.2021"),
    ],
)
def test_get_date_non_standard_trailing_chars(date_str, expected_part):
    """Проверка работы функции на нестандартных строках с датами (но начало корректное)."""
    assert get_date(date_str) == expected_part


def test_get_date_missing_date_string_too_short():
    """Проверка, что функция вызывает IndexError при слишком короткой входной строке (где отсутствует дата)."""
    with pytest.raises(IndexError):
        get_date("2024-03-")  # Недостаточная длина для day = date_str[8:10]
