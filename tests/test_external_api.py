from unittest.mock import patch

import pytest

from src.external_api import convert_trx_rub


@pytest.fixture
def usd_transaction():
    return {"amount": "100", "currency": "USD"}


@pytest.fixture
def eur_transaction():
    return {"amount": "50", "currency": "EUR"}


@pytest.fixture
def rub_transaction():
    return {"amount": "5000", "currency": "RUB"}


@patch("requests.get")
def test_convert_usd_to_rub(mock_get, usd_transaction):
    mock_response = {"rates": {"RUB": 75.0}, "success": True}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    result = convert_trx_rub(usd_transaction)
    assert result == 7500.0


@patch("requests.get")
def test_convert_eur_to_rub(mock_get, eur_transaction):
    mock_response = {"rates": {"RUB": 85.0}, "success": True}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    result = convert_trx_rub(eur_transaction)
    assert result == 4250.0


def test_convert_rub_no_conversion(rub_transaction):
    result = convert_trx_rub(rub_transaction)
    assert result == 5000.0
