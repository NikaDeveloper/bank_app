from unittest.mock import patch

import pandas as pd

from src.read_transaction import (read_finance_operations_csv,
                                  read_finance_operations_excel)

# Ожидаемый результат, который должны вернуть наши функции
EXPECTED_TRANSACTIONS = [
    {"id": 1, "amount": 100.50, "currency": "USD"},
    {"id": 2, "amount": 75.20, "currency": "EUR"},
]

# Создаем DataFrame, который будет "возвращать" наш mock
MOCK_DF = pd.DataFrame(EXPECTED_TRANSACTIONS)


PD_PATH = "src.read_transaction.pd"


@patch(f"{PD_PATH}.read_csv")
def test_read_csv_transactions(mock_read_csv):
    """Тестируем функцию чтения CSV с использованием mock."""
    # Настраиваем mock: при вызове он вернет наш DataFrame
    mock_read_csv.return_value = MOCK_DF

    # Вызываем нашу функцию
    result = read_finance_operations_csv("dummy_path.csv")

    # Проверяем, что функция вернула то, что мы ожидали
    assert result == EXPECTED_TRANSACTIONS
    # Проверяем, что mock был вызван с правильным путем к файлу
    mock_read_csv.assert_called_once_with("dummy_path.csv")


@patch(f"{PD_PATH}.read_excel")
def test_read_excel_transactions(mock_read_excel):
    """Тестируем функцию чтения Excel с использованием mock."""
    # Настраиваем mock
    mock_read_excel.return_value = MOCK_DF

    # Вызываем функцию
    result = read_finance_operations_excel("dummy_path.xlsx")

    # Проверяем результат
    assert result == EXPECTED_TRANSACTIONS
    mock_read_excel.assert_called_once_with("dummy_path.xlsx")


# ... (в файле tests/test_read_transaction.py, после существующих тестов)


@patch(f"{PD_PATH}.read_csv")
def test_read_csv_file_not_found(mock_read_csv):
    """Тестируем обработку FileNotFoundError для CSV."""
    # Настраиваем mock так, чтобы он вызывал ошибку FileNotFoundError
    mock_read_csv.side_effect = FileNotFoundError

    # Вызываем функцию и проверяем, что она возвращает пустой список
    result = read_finance_operations_csv("non_existent_path.csv")
    assert result == []


@patch(f"{PD_PATH}.read_excel")
def test_read_excel_file_not_found(mock_read_excel):
    """Тестируем обработку FileNotFoundError для Excel."""
    # Настраиваем mock так, чтобы он вызывал ошибку FileNotFoundError
    mock_read_excel.side_effect = FileNotFoundError

    # Вызываем функцию и проверяем, что она возвращает пустой список
    result = read_finance_operations_excel("non_existent_path.xlsx")
    assert result == []


@patch(f"{PD_PATH}.read_csv")
def test_read_csv_general_exception(mock_read_csv):
    """Тестируем обработку общего исключения для CSV."""
    # Настраиваем mock так, чтобы он вызывал любую другую ошибку
    mock_read_csv.side_effect = Exception("Something went wrong")

    result = read_finance_operations_csv("dummy_path.csv")
    assert result == []


@patch(f"{PD_PATH}.read_excel")
def test_read_excel_general_exception(mock_read_excel):
    """Тестируем обработку общего исключения для Excel."""
    # Настраиваем mock так, чтобы он вызывал любую другую ошибку
    mock_read_excel.side_effect = Exception("Something went wrong")

    result = read_finance_operations_excel("dummy_path.xlsx")
    assert result == []
