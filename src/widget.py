from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(requisites: str) -> str:
    """Принимает строку с типом и номером карты/счета и возвращает маскированную строку с проверкой входных данных."""
    requisites = str(requisites)

    parts = requisites.split()
    if len(parts) < 2:
        return "Ошибка: Некорректный формат входных данных"

    account_type = parts[0]
    number = parts[-1]

    if not number.isdigit():
        return "Ошибка: Номер карты/счета должен содержать только цифры"

    if account_type.lower() == "счет":
        if len(number) <= 10 or len(number) > 20:  # Пример проверки длины счета
            return "Ошибка: Некорректная длина номера счета"
        else:
            masked = get_mask_account(number)
            return f"Счет {masked}"
    else:  # если карта
        if len(number) < 13 or len(number) > 19:  # Пример проверки длины номера карты
            return "Ошибка: Некорректная длина номера карты"
        masked = get_mask_card_number(number)
        type_info = requisites[: requisites.rfind(number)].strip()
        return f"{type_info} {masked}"


def get_date(date_str: str) -> str:
    """Преобразует строку с датой из формата 'ГГГГ-ММ-ДДTчч:мм:сс.микросекунды' в формат 'ДД.ММ.ГГГГ'."""
    if len(date_str) == 26:
        year = date_str[:4]
        month = date_str[5:7]
        day = date_str[8:10]
        formatted_date = f"{day}.{month}.{year}"
        return formatted_date
    else:
        raise ValueError("Неверный формат даты")
