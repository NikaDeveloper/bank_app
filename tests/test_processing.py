import pytest

from src.processing import (
    filter_by_state,
    process_bank_operations,
    process_bank_search,
    sort_by_date,
)


# Тесты для filter_by_state
def test_filter_by_state_default_executed(sample_operations_data):
    """Тестирование фильтрации по статусу EXECUTED (по умолчанию)."""
    result = filter_by_state(sample_operations_data)
    assert len(result) == 4  # IDs 1, 2, 5, 7
    for item in result:
        assert item["state"] == "EXECUTED"


@pytest.mark.parametrize(
    "state_to_filter, expected_ids",
    [
        ("CANCELED", {3, 6}),
        ("PENDING", {4}),
        ("NON_EXISTENT_STATE", set()),
    ],
)
def test_filter_by_state_various_states(
    sample_operations_data, state_to_filter, expected_ids
):
    """Параметризация тестов для различных возможных значений статуса state."""
    result = filter_by_state(sample_operations_data, state_to_filter)
    assert len(result) == len(expected_ids)
    assert {item["id"] for item in result} == expected_ids


def test_filter_by_state_no_matching_state(sample_operations_data):
    """Проверка работы функции при отсутствии словарей с указанным статусом."""
    result = filter_by_state(sample_operations_data, "UNKNOWN")
    assert len(result) == 0


def test_filter_by_state_empty_list():
    """Проверка работы функции с пустым списком на входе."""
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_items_without_state_key(sample_operations_data):
    """Проверка, что элементы без ключа 'state' игнорируются."""
    # В sample_operations_data есть элементы без 'state'
    # При фильтрации по "EXECUTED" они не должны вызывать ошибку и не должны быть в результате
    result_executed = filter_by_state(sample_operations_data, "EXECUTED")
    ids_executed = {item["id"] for item in result_executed}
    assert 8 not in ids_executed  # id 8 не имеет 'state'
    assert 7 in ids_executed

    result_pending = filter_by_state(sample_operations_data, "PENDING")
    ids_pending = {item["id"] for item in result_pending}
    assert 4 in ids_pending


# Тесты для sort_by_date
def test_sort_by_date_descending_default(operations_for_sorting):
    """Тестирование сортировки списка словарей по датам в порядке убывания (по умолчанию)."""
    # Убираем элемент без ключа 'date' и с некорректной датой для этого теста,
    # так как sorted выбросит TypeError при сравнении dict и str или при некорректных date-строках,
    # если lambda попытается получить доступ к отсутствующему ключу или если формат даты несовместим для сравнения
    valid_data = [
        d
        for d in operations_for_sorting
        if "date" in d and d["date"] != "invalid-date-format"
    ]
    result = sort_by_date(valid_data)
    assert [item["id"] for item in result] == [
        5,
        1,
        4,
        3,
        2,
        7,
    ]  # 2020, 2019-07, 2019-07, 2018-09, 2018-06, 2017


def test_sort_by_date_ascending(operations_for_sorting):
    """Тестирование сортировки списка словарей по датам в порядке возрастания."""
    valid_data = [
        d
        for d in operations_for_sorting
        if "date" in d and d["date"] != "invalid-date-format"
    ]
    result = sort_by_date(valid_data, desc=False)
    assert [item["id"] for item in result] == [
        7,
        2,
        3,
        1,
        4,
        5,
    ]  # 2017, 2018-06, 2018-09, 2019-07, 2019-07, 2020


def test_sort_by_date_identical_dates(operations_for_sorting):
    """Проверка корректности сортировки при одинаковых датах (порядок не гарантирован, но не должно быть ошибки)."""
    valid_data = [
        d
        for d in operations_for_sorting
        if "date" in d and d["date"] != "invalid-date-format"
    ]
    result = sort_by_date(valid_data)
    # Найдем элементы с одинаковой датой
    dates = [item["date"] for item in result]
    # Проверяем, что элементы с id 1 и 4 (одинаковая дата) присутствуют
    assert "2019-07-03T18:35:29.512364" in dates
    count_identical_date = dates.count("2019-07-03T18:35:29.512364")
    assert count_identical_date == 2
    # Порядок между id=1 и id=4 не важен, т.к. sorted() стабилен


def test_sort_by_date_with_missing_date_key(operations_for_sorting):
    """Тесты на работу функции с отсутствующим ключом 'date' в одном из словарей."""
    # sort_by_date использует item["date"], что вызовет KeyError, если ключа нет.
    data_with_missing_key = [
        {"id": 1, "date": "2020-01-01T00:00:00.000000"},
        {"id": 2},  # нет ключа 'date'
    ]
    with pytest.raises(KeyError):
        sort_by_date(data_with_missing_key)


def test_sort_by_date_with_malformed_date_strings(operations_for_sorting):
    """
    Тесты на работу функции с некорректными форматами дат.
    Стандартная сортировка строк будет их сравнивать лексикографически.
    """
    # Берем только элементы, где есть ключ 'date'
    data_with_malformed = [d for d in operations_for_sorting if "date" in d]
    # Ожидаем, что "invalid-date-format" окажется где-то в результате сортировки,
    # в зависимости от лексикографического сравнения
    result_desc = sort_by_date(data_with_malformed, desc=True)
    result_asc = sort_by_date(data_with_malformed, desc=False)

    # Проверяем, что все элементы на месте
    assert len(result_desc) == len(data_with_malformed)
    assert len(result_asc) == len(data_with_malformed)

    # Проверим, что "invalid-date-format" присутствует
    assert any(item["date"] == "invalid-date-format" for item in result_desc)
    assert any(item["date"] == "invalid-date-format" for item in result_asc)

    # Убедимся, что сортировка выполнена и не было ошибки
    assert isinstance(result_desc, list)
    assert isinstance(result_asc, list)


def test_sort_by_date_empty_list():
    """Тестирование сортировки пустого списка."""
    assert sort_by_date([]) == []


@pytest.fixture
def search_data():
    return [
        {"description": "Оплата кофе"},
        {"description": "Покупка книг"},
        {"description": "Кофе в офисе"},
        {"description": "Магазин продуктов"},
        {"description": ""},
        {},
    ]


@pytest.fixture
def operations_data():
    return [
        {"description": "Оплата кофе"},
        {"description": "Кофейня на углу"},
        {"description": "Покупка книг"},
        {"description": "Книги и журналы"},
        {"description": "Магазин"},
        {"description": "КОФЕ"},
    ]


# ---------- Тесты для process_bank_search ----------


def test_process_bank_search_found(search_data):
    result = process_bank_search(search_data, "кофе")
    assert len(result) == 2
    assert all("кофе" in item["description"].lower() for item in result)


def test_process_bank_search_not_found(search_data):
    result = process_bank_search(search_data, "машина")
    assert result == []


def test_process_bank_search_empty_description(search_data):
    result = process_bank_search(search_data, "кофе")
    assert any(
        item.get("description", "") == "Кофе"
        or "кофе" in item.get("description", "").lower()
        for item in result
    )


# ---------- Тесты для process_bank_operations ----------


def test_process_bank_operations_basic(operations_data):
    categories = ["кофе", "книги"]
    result = process_bank_operations(operations_data, categories)
    assert result == {"кофе": 3, "книги": 1}


def test_process_bank_operations_case_insensitive():
    data = [
        {"description": "Оплата КОФЕ"},
        {"description": "кофе"},
    ]
    result = process_bank_operations(data, ["Кофе"])
    assert result == {"Кофе": 2}


def test_process_bank_operations_no_matches():
    data = [
        {"description": "Бензин"},
        {"description": "Еда"},
    ]
    result = process_bank_operations(data, ["Кофе", "Книги"])
    assert result == {"Кофе": 0, "Книги": 0}


def test_process_bank_operations_empty_data():
    result = process_bank_operations([], ["еда", "кофе"])
    assert result == {"еда": 0, "кофе": 0}


def test_process_bank_operations_empty_categories():
    data = [{"description": "Что-то"}]
    result = process_bank_operations(data, [])
    assert result == {}
