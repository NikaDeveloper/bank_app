import json
import logging

# настройка логера для utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/utils.log", "w")
file_formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H-%M-%S",
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_path_json(path_json_file: str) -> list[dict]:
    """Принимает путь json-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        logger.info(f"Чтение файла: {path_json_file}")
        with open(path_json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.debug(f"Файл успешно прочитан. Кол-во записей: {len(data)}")
                return data

            logger.warning("Файл не содержит список. Возвращен пустой список.")
            return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {path_json_file}")
        return []
    except json.JSONDecodeError:
        logger.error(
            f"Ошибка чтения json: файл поврежден или невалиден: {path_json_file}"
        )
        return []
