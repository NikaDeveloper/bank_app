import re
from pprint import pprint


def filter_by_state(list_of_dicts: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        list_of_dicts: Список словарей, каждый из которых предположительно содержит ключ 'state'.
        state: Опциональное значение для ключа 'state', по которому будет производиться фильтрация.
               По умолчанию установлено значение 'EXECUTED'.

    Returns:
        Новый список словарей, содержащий только те словари, у которых значение
        ключа 'state' соответствует указанному значению.
    """

    filtered = [item for item in list_of_dicts if item.get("state") == state]
    return filtered

    # list_of_dictionary = []
    # for item in list_of_dicts:
    #     if "state" in item and item["state"] == state:
    #         list_of_dictionary.append(item)
    # return list_of_dictionary


def sort_by_date(list_of_dicts: list[dict], desc: bool = True) -> list[dict]:
    """Сортирует список словарей по значению ключа 'date'.

    Args:
        list_of_dicts: Список словарей, каждый из которых должен содержать ключ 'date'
                       со строковым представлением даты.
        desc: Необязательный булевый параметр. Если True (по умолчанию), сортировка
              выполняется по убыванию (от новых дат к старым). Если False,
              сортировка выполняется по возрастанию (от старых дат к новым).

    Returns:
        Новый список словарей, отсортированный по значению ключа 'date'.
    """
    return sorted(list_of_dicts, key=lambda item: item["date"], reverse=desc)


input_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

pprint(filter_by_state(input_data))
pprint(sort_by_date(input_data))


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Возвращает список словарей, у которых в описании есть строка поиска"""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        operation
        for operation in data
        if pattern.search(operation.get("description", ""))
    ]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории."""
    result = {category: 0 for category in categories}
    patterns = {
        category: re.compile(re.escape(category), re.IGNORECASE)
        for category in categories
    }

    for operation in data:
        description = operation.get("description", "")
        for category, pattern in patterns.items():
            if pattern.search(description):
                result[category] += 1

    return result
