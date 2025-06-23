import json

import pandas as pd


def read_finance_operations_json(path_file: str) -> list[dict]:
    """Считывает финансовые операции из JSON-файла и возвращает список словарей"""
    try:
        with open(path_file, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл не найден: {path_file}")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении JSON: {e}")
        return []


def read_finance_operations_csv(path_file: str) -> list[dict]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей"""
    try:

        df = pd.read_csv(path_file, delimiter=";")

        df.columns = df.columns.astype(str)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл не найден: {path_file}")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении CSV: {e}")
        return []


def read_finance_operations_excel(path_file: str) -> list[dict]:
    """Считывает финансовые операции из Excel-файла и возвращает список словарей"""
    try:
        df = pd.read_excel(path_file)

        df.columns = df.columns.astype(str)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл не найден: {path_file}")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении Excel: {e}")
        return []


if __name__ == "__main__":
    from pprint import pprint

    path_file = "../data/transactions_excel.xlsx"
    path_file1 = "../data/transactions.csv"
    path_file2 = "../data/operations.json"
    pprint(read_finance_operations_json(path_file2)[:2])
    print("____")
    pprint(read_finance_operations_excel(path_file)[:2])
    print("____")
    pprint(read_finance_operations_csv(path_file1)[:2])
