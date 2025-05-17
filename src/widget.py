from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(requisites: str) -> str:
    """Принимает строку с типом и номером карты/счета и возвращает маскированную строку с проверкой входных данных.

    Разбивает входную строку на тип и номер, затем проверяет формат номера
    перед вызовом соответствующей функции маскировки.

    Args:
        requisites: Строка, содержащая тип карты/счета и номер.
                    Пример: "Visa Platinum 7000792289606361" или "Счет 73654108430135874305".

    Returns:
        Маскированная строка с типом и номером карты/счета или сообщение об ошибке,
        если формат номера не соответствует ожидаемому.
        Пример: "Visa Platinum 7000 ** **** 6361" или "Счет ****4305"
                 или "Ошибка: Некорректный формат номера карты/счета".
    """
    parts = requisites.split()
    if len(parts) < 2:
        return "Ошибка: Некорректный формат входных данных"

    account_type = parts[0]
    number = parts[-1]

    if not number.isdigit():
        return "Ошибка: Номер карты/счета должен содержать только цифры"

    if account_type.lower() == "счет":
        if len(number) < 10 or len(number) > 20:  # Пример проверки длины счета
            return "Ошибка: Некорректная длина номера счета"
        masked = get_mask_account(number)
        return f"Счет {masked}"
    else:  # если карта
        if len(number) < 13 or len(number) > 19:  # Пример проверки длины номера карты
            return "Ошибка: Некорректная длина номера карты"
        masked = get_mask_card_number(number)
        type_info = requisites[:requisites.rfind(number)].strip()
        return f"{type_info} {masked}"


def get_date(date_str: str) -> str:
    """Преобразует строку с датой из формата 'ГГГГ-ММ-ДДTчч:мм:сс.микросекунды' в формат 'ДД.ММ.ГГГГ'."""
    year = date_str[:4]
    month = date_str[5:7]
    day = date_str[8:10]
    formatted_date = f"{day}.{month}.{year}"
    return formatted_date


print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))
print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 123"))  # Пример некорректной длины счета
print(mask_account_card("Invalid 7000ABC1234DEF5678"))  # Пример нецифрового номера
print(get_date("2024-03-11T02:26:18.671407"))
