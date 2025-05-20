from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Маскирует номер банковской карты в формате XXXX XX** **** XXXX."""
    card_number_str = str(card_number)
    if not card_number_str.isdigit():
        return "Некорректный номер карты"
    masked_parts = [
        card_number_str[:4],
        card_number_str[4:6],
        "**",
        "****",
        card_number_str[-4:],
    ]
    return " ".join(masked_parts)


def get_mask_account(account_number: Union[str, int]) -> str:
    """Маскирует номер банковского счета в формате **XXXX."""
    account_number_str = str(account_number)
    if not account_number_str.isdigit():
        return "Некорректный номер счета"
    return f"**{account_number_str[-4:]}"


if __name__ == "__main__":
    card = "1234567890123456"
    masked_card = get_mask_card_number(card)
    print(f"Маскированный номер карты: {masked_card}")

    account = "9876543210"
    masked_account = get_mask_account(account)
    print(f"Маскированный номер счета: {masked_account}")
