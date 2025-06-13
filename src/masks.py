import logging
from typing import Union


# настройка логера для masks
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", "w", encoding="utf8")
file_formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H-%M-%S",
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Маскирует номер банковской карты в формате XXXX XX** **** XXXX."""
    card_number_str = str(card_number)

    if not card_number_str.isdigit():
        logger.error(f"Невалидный номер карты: {card_number}")
        return "Некорректный номер карты"

    masked_parts = [
        card_number_str[:4],
        card_number_str[4:6],
        "**",
        "****",
        card_number_str[-4:],
    ]
    result = " ".join(masked_parts)
    logger.debug(f"Успешная маскировка карты: {card_number} -> {result}")
    return result


def get_mask_account(account_number: Union[str, int]) -> str:
    """Маскирует номер банковского счета в формате **XXXX."""
    account_number_str = str(account_number)

    if not account_number_str.isdigit() or len(account_number_str) < 16:
        logger.error(f"Невалидный номер счета: {account_number}")
        return "Некорректный номер счета"

    result = f"**{account_number_str[-4:]}"
    logger.debug(f"Успешная маскировка счета: {account_number} -> {result}")
    return result
