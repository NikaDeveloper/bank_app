from pprint import pprint

from src.read_transaction import (read_finance_operations_csv,
                                  read_finance_operations_excel)

csv_file_path = "src/transactions.csv"
excel_file_path = "src/transactions_excel.xlsx"

print("--- Чтение из CSV ---")
csv_data = read_finance_operations_csv(csv_file_path)
if csv_data:
    pprint(csv_data[0])  # Печатаем первую транзакцию для проверки

print("\n--- Чтение из Excel ---")
excel_data = read_finance_operations_excel(excel_file_path)
if excel_data:
    pprint(excel_data[0])  # Печатаем первую транзакцию для проверки
