def filter_by_currency(list_transactions, currency):
    """
    Функция, которая принимает на вход список словарей, представляющих транзакции.
    Функция возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной.
    """
    for trx in list_transactions:
        if (
                "operationAmount" in trx
                and "currency" in trx["operationAmount"]
                and trx["operationAmount"]["currency"].get("code") == currency
        ):
            yield trx

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {
                "name": "EUR",
                "code": "EUR"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160"
    }
]

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))


def transaction_descriptions(gen_desc):
    """
    Генератор, который по очереди возвращает описание каждой транзакции из списка.
    """
    for trx in gen_desc:
        description = trx.get("description", "Без описания")
        yield description

list_desc = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод с карты на карту"},
    {"description": "Перевод организации"},
]

descriptions = transaction_descriptions(list_desc)

for _ in range(5):
    print(next(descriptions))


def card_number_generator(start, end):
    """
    Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX,
    где X — цифра. Диапазон задается аргументами start и end.
    """
    for number in range(start, end + 1):
        card_number = f"{number:016d}"  # форматируем в строку длиной 16 с ведущими нулями
        formatted = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted


for num in card_number_generator(1, 5):
    print(num)

