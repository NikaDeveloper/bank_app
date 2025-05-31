# Widget Project

## Описание

IT-отдел крупного банка делает новую фичу для личного кабинета клиента. 
Это виджет, который показывает несколько последних успешных банковских операций клиента.
## Установка

1.  Клонируйте репозиторий:
    ```bash
    [git clone] (-> git@github.com:NikaDeveloper/bank_app.git <-)
    ```

2.  Перейдите в директорию проекта:
    ```bash
    cd bank_app
    ```

3.  Установите зависимости с помощью Poetry:
    ```bash
    poetry install
    ```
    *(Убедитесь, что у вас установлен Poetry)*


# Зависимости 

Установленные зависимости можно посмотреть в requirements.txt.

## Модуль generators

Реализованы генераторы:

- `filter_by_currency` — фильтрует транзакции по валюте.
- `transaction_descriptions` — возвращает описания транзакций.
- `card_number_generator` — создает отформатированные номера карт в заданном диапазоне.

### Примеры использования

```python
list(filter_by_currency(transactions, "USD"))
list(transaction_descriptions(transactions))
list(card_number_generator(1, 3))


## Тестирование

Для запуска тестов:

```bash
pytest
