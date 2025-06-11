import json


def get_path_json(path_json_file: str) -> list[dict]:
    """Принимает путь json-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        with open(path_json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
