import json
import os

from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.read_transaction import (read_finance_operations_csv,
                                  read_finance_operations_excel)
from src.widget import get_date, mask_account_card

VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}
DATA_DIR = "data"


def read_json_transactions(path: str) -> list[dict]:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка чтения JSON: {e}")
        return []


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        path = os.path.join(DATA_DIR, "operations.json")
        data = read_json_transactions(path)
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        path = os.path.join(DATA_DIR, "transactions.csv")
        data = read_finance_operations_csv(path)
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        path = os.path.join(DATA_DIR, "transactions_excel.xlsx")
        data = read_finance_operations_excel(path)
    else:
        print("Программа: Неверный выбор. Завершение работы.")
        return

    # Фильтрация по статусу
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию (EXECUTED, CANCELED, PENDING): "
        ).upper()
        if status in VALID_STATUSES:
            break
        print(f'Программа: Статус операции "{status}" недоступен.')

    data = filter_by_state(data, state=status)
    print(f'Программа: Операции отфильтрованы по статусу "{status}"')

    # Сортировка по дате
    sort_input = (
        input("Программа: Отсортировать операции по дате? Да/Нет: ").strip().lower()
    )
    if sort_input in {"да", "yes", "y"}:
        order_input = (
            input("Программа: Отсортировать по возрастанию или по убыванию? ")
            .strip()
            .lower()
        )
        desc = order_input != "по возрастанию"
        data = sort_by_date(data, desc=desc)

    # Фильтрация по валюте
    currency_input = (
        input("Программа: Выводить только рублевые транзакции? Да/Нет: ")
        .strip()
        .lower()
    )
    if currency_input in {"да", "yes", "y"}:
        data = [
            op
            for op in data
            if op.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    # Фильтрация по описанию
    search_input = (
        input(
            "Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "
        )
        .strip()
        .lower()
    )
    if search_input in {"да", "yes", "y"}:
        keyword = input("Введите ключевое слово для поиска в описании: ").strip()
        data = process_bank_search(data, keyword)

    # Вывод результата
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")
    if not data:
        print(
            "Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
        )
        return

    print(f"Программа: Всего банковских операций в выборке: {len(data)}\n")

    for item in data:
        raw_date = item.get("date", "")
        try:
            date = get_date(raw_date)
        except Exception:
            date = raw_date[:10]

        description = item.get("description", "Без описания")
        from_raw = item.get("from", "Счет неизвестен")
        to_raw = item.get("to", "Счет неизвестен")

        from_acc = (
            mask_account_card(from_raw) if from_raw != "Счет неизвестен" else from_raw
        )
        to_acc = mask_account_card(to_raw) if to_raw != "Счет неизвестен" else to_raw

        amount = item.get("operationAmount", {}).get("amount") or item.get("amount")
        currency = item.get("operationAmount", {}).get("currency", {}).get(
            "name"
        ) or item.get("currency_name")

        print(f"{date} {description}")
        print(f"{from_acc} -> {to_acc}")
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
