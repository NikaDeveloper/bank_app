import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)

# ----------------- Тесты для filter_by_currency -----------------


@pytest.mark.parametrize(
    "transactions,currency,expected_ids",
    [
        (
            [
                {"operationAmount": {"currency": {"code": "USD"}}, "id": 1},
                {"operationAmount": {"currency": {"code": "EUR"}}, "id": 2},
            ],
            "USD",
            [1],
        ),
        (
            [{"operationAmount": {"currency": {"code": "RUB"}}, "id": 3}],
            "USD",
            [],
        ),
        (
            [],  # Пустой список
            "USD",
            [],
        ),
        (
            [{"someKey": 123}],  # Нет нужных ключей
            "USD",
            [],
        ),
    ],
)
def test_filter_by_currency_parametrized(transactions, currency, expected_ids):
    result = list(filter_by_currency(transactions, currency))
    result_ids = [trx.get("id") for trx in result]
    assert result_ids == expected_ids


def test_filter_by_currency_with_fixture(usd_transactions):
    result = list(filter_by_currency(usd_transactions, "USD"))
    assert [r["id"] for r in result] == [1]


# ----------------- Тесты для transaction_descriptions -----------------


@pytest.mark.parametrize(
    "input_data,expected",
    [
        ([{"description": "Test 1"}, {"description": "Test 2"}], ["Test 1", "Test 2"]),
        ([{"some_key": "no description"}], ["Без описания"]),
        ([], []),
    ],
)
def test_transaction_descriptions_parametrized(input_data, expected):
    result = list(transaction_descriptions(input_data))
    assert result == expected


def test_transaction_descriptions_with_fixture(transaction_data):
    result = list(transaction_descriptions(transaction_data))
    assert result == ["Покупка в магазине", "Без описания"]


# ----------------- Тесты для card_number_generator -----------------


@pytest.mark.parametrize(
    "start,end,expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator_parametrized(start, end, expected):
    result = list(card_number_generator(start, end))
    assert result == expected
    for card in result:
        assert len(card) == 19
        assert card.count(" ") == 3
        assert all(part.isdigit() for part in card.split(" "))


def test_card_number_generator_with_fixture(card_range):
    start, stop = card_range
    result = list(card_number_generator(start, stop))
    assert result == [
        "0000 0000 0000 1000",
        "0000 0000 0000 1001",
        "0000 0000 0000 1002",
        "0000 0000 0000 1003",
    ]
