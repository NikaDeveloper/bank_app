import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_trx_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """Принимает на вход транзакцию и возвращает сумму транзакции в рублях"""
    if not transaction or "amount" not in transaction or "currency" not in transaction:
        return None

    amount = transaction["amount"]
    currency = transaction["currency"]

    if currency == "RUB":
        return float(amount)

    if currency in ("USD", "EUR"):
        try:
            response = requests.get(
                BASE_URL,
                params={"base": currency, "symbols": "RUB"},
                headers={"apikey": API_KEY},
            )
            response.raise_for_status()
            rate = response.json()["rates"]["RUB"]
            return float(amount) * rate
        except (requests.RequestException, KeyError):
            return None
    return None
