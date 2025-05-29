import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)

#  Тесты для filter_by_currency


@pytest.mark.parametrize(
    "transactions,currency,expected_ids",
    [
        (
            [  # Тест на USD
                {"operationAmount": {"currency": {"code": "USD"}}, "id": 1},
                {"operationAmount": {"currency": {"code": "EUR"}}, "id": 2},
            ],
            "USD",
            [1],
        ),
        (
            [  # Нет нужной валюты
                {"operationAmount": {"currency": {"code": "RUB"}}, "id": 3},
            ],
            "USD",
            [],
        ),
        (
            [],  # Пустой список
            "USD",
            [],
        ),
        (
            [  # Отсутствие ключей
                {"someKey": 123},
            ],
            "USD",
            [],
        ),
    ],
)
def test_filter_by_currency(transactions, currency, expected_ids):
    result = list(filter_by_currency(transactions, currency))
    result_ids = [trx.get("id") for trx in result]
    assert result_ids == expected_ids


#  Тесты для transaction_descriptions


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (
            [{"description": "Test 1"}, {"description": "Test 2"}],
            ["Test 1", "Test 2"],
        ),
        (
            [{"some_key": "no description"}],
            ["Без описания"],
        ),
        (
            [],
            [],
        ),
    ],
)
def test_transaction_descriptions(input_data, expected):
    result = list(transaction_descriptions(input_data))
    assert result == expected


#  Тесты для card_number_generator


@pytest.mark.parametrize(
    "start,end,expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator(start, end, expected):
    result = list(card_number_generator(start, end))
    assert result == expected
    for card in result:
        assert len(card) == 19  # 16 цифр + 3 пробела
        assert card.count(" ") == 3
        assert all(part.isdigit() for part in card.split(" "))
