import logging
from unittest.mock import mock_open, patch

import pytest

from src.utils import get_path_json


@pytest.fixture
def valid_json_data():
    """Корректные данные JSON в виде списка словарей."""
    return '[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]'


def test_read_valid_json_file(valid_json_data):
    """Возвращает список словарей при корректном JSON."""
    with patch("builtins.open", mock_open(read_data=valid_json_data)):
        result = get_path_json("dummy_path.json")
        assert len(result) == 2
        assert result[0]["id"] == 1


def test_read_empty_file():
    """Возвращает пустой список при пустом JSON-файле."""
    with patch("builtins.open", mock_open(read_data="")):
        result = get_path_json("empty.json")
        assert result == []


def test_read_non_list_json():
    """Возвращает пустой список, если JSON — не список."""
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        result = get_path_json("not_list.json")
        assert result == []


def test_read_nonexistent_file():
    """Возвращает пустой список, если файл не найден."""
    result = get_path_json("nonexistent.json")
    assert result == []


def test_log_on_valid_json(caplog, valid_json_data):
    """
    Проверяет, что при корректном JSON логируются сообщения INFO и DEBUG.
    """
    with patch("builtins.open", mock_open(read_data=valid_json_data)):
        with caplog.at_level(logging.DEBUG):
            get_path_json("valid.json")
    assert "Чтение файла: valid.json" in caplog.text
    assert "Файл успешно прочитан. Кол-во записей: 2" in caplog.text


def test_log_on_empty_file(caplog):
    """
    Проверяет, что при пустом JSON-файле логирование не вызывает ошибок,
    и функция возвращает пустой список.
    """
    with patch("builtins.open", mock_open(read_data="")):
        with caplog.at_level(logging.DEBUG):
            result = get_path_json("empty.json")
    assert result == []


def test_log_on_non_list_json_log(caplog):
    """
    Проверяет, что при JSON, не являющемся списком, логируется предупреждение (WARNING).
    """
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        with caplog.at_level(logging.WARNING):
            get_path_json("not_list.json")
    assert "Файл не содержит список" in caplog.text


def test_log_on_file_not_found_log(caplog):
    """
    Проверяет, что при отсутствии файла логируется ошибка (ERROR).
    """
    with caplog.at_level(logging.ERROR):
        get_path_json("nonexistent.json")
    assert "Файл не найден: nonexistent.json" in caplog.text


def test_log_on_json_decode_error_log(caplog):
    """
    Проверяет, что при ошибке декодирования JSON логируется ошибка (ERROR).
    """
    with patch("builtins.open", mock_open(read_data="{invalid_json}")):
        with caplog.at_level(logging.ERROR):
            get_path_json("broken.json")
    assert "Ошибка чтения json" in caplog.text
