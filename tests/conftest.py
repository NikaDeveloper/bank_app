import pytest


@pytest.fixture
def sample_operations_data():
    """Фикстура с примерами данных операций."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-07-15T10:30:00.123456"},
        {"id": 2, "state": "EXECUTED", "date": "2024-07-14T12:45:00.789012"},
        {"id": 3, "state": "CANCELED", "date": "2024-07-15T09:00:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2024-07-16T11:00:00.555555"},
        {"id": 5, "state": "EXECUTED", "date": "2023-12-25T08:20:30.987654"},
        {"id": 6, "state": "CANCELED", "date": "2024-07-14T12:45:00.789012"},
        {},
        {"id": 7, "state": "EXECUTED"},
        {"id": 8, "date": "2024-01-01T00:00:00.000000"},
    ]


@pytest.fixture
def operations_for_sorting():
    """Фикстура с данными для тестирования сортировки, включая некорректные даты."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 5, "state": "PENDING", "date": "2020-01-01T00:00:00.000000"},
        {"id": 6, "state": "EXECUTED", "date": "invalid-date-format"},
        {"id": 7, "state": "EXECUTED", "date": "2017-01-01T00:00:00.000000"},
        {"id": 8, "state": "EXECUTED"},
    ]


@pytest.fixture
def usd_transactions():
    return [
        {"operationAmount": {"currency": {"code": "USD"}}, "id": 1},
        {"operationAmount": {"currency": {"code": "EUR"}}, "id": 2},
    ]


@pytest.fixture
def transaction_data():
    return [
        {"description": "Покупка в магазине"},
        {"some_key": "нет описания"},
    ]


@pytest.fixture
def card_range():
    return 1000, 1003
