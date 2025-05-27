# Data Processing Toolkit

## Описание

Этот проект представляет собой набор инструментов для обработки данных, в частности, списков словарей. В текущей версии реализованы функции для фильтрации и сортировки данных.

## Установка

1.  Клонируйте репозиторий:
    ```bash
    [git clone] (<https://github.com/NikaDeveloper/project10.11>)
    ```

2.  Перейдите в директорию проекта:
    ```bash
    cd package-name
    ```

3.  Установите зависимости с помощью Poetry:
    ```bash
    poetry install
    ```
    *(Убедитесь, что у вас установлен Poetry)*

## Использование

### `filter_by_state(list_of_dicts: list[dict], state: str = "EXECUTED") -> list[dict]`

Фильтрует список словарей по значению ключа `'state'`. Возвращает новый список, содержащий только те словари, где значение `'state'` соответствует указанному. По умолчанию фильтрует по `'EXECUTED'`.

**Пример:**

```python
from pprint import pprint
from src.processing import filter_by_state

data = [
    {'id': 1, 'state': 'EXECUTED', 'value': 10},
    {'id': 2, 'state': 'PENDING', 'value': 20},
    {'id': 3, 'state': 'EXECUTED', 'value': 30}
]

executed_items = filter_by_state(data)
pprint(executed_items)
# Вывод:
# [{'id': 1, 'state': 'EXECUTED', 'value': 10},
#  {'id': 3, 'state': 'EXECUTED', 'value': 30}]

pending_items = filter_by_state(data, state='PENDING')
pprint(pending_items)
# Вывод:
# [{'id': 2, 'state': 'PENDING', 'value': 20}]
```

### `sort_by_date(list_of_dicts: list[dict], desc: bool = True) -> list[dict]`

Сортирует список словарей по значению ключа 'date'. По умолчанию сортирует по убыванию (desc=True).

**Пример:**

```python
from pprint import pprint
from src.processing import sort_by_date

data = [
    {'id': 1, 'date': '2025-05-11'},
    {'id': 2, 'date': '2025-05-10'},
    {'id': 3, 'date': '2025-05-12'}
]

sorted_data_desc = sort_by_date(data)
pprint(sorted_data_desc)
# Вывод:
# [{'date': '2025-05-12', 'id': 3},
#  {'date': '2025-05-11', 'id': 1},
#  {'date': '2025-05-10', 'id': 2}]

sorted_data_asc = sort_by_date(data, desc=False)
pprint(sorted_data_asc)
# Вывод:
# [{'date': '2025-05-10', 'id': 2},
#  {'date': '2025-05-11', 'id': 1},
#  {'date': '2025-05-12', 'id': 3}]
```

# Зависимости 

+ certifi 
+ requests
+ idna
+ numpy
+ charset-normalizer
+ urllib3

## Структура проекта

``` package-name/
├── src/
│   └── processing.py
└── README.md
└── pyproject.toml
└── poetry.lock
```
## Тестирование

Для запуска тестов:

```bash
pytest
