import pandas as pd


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
