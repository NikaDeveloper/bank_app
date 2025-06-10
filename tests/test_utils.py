from unittest.mock import mock_open, patch

import pytest

from src.utils import get_path_json


@pytest.fixture
def valid_json_data():
    return '[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]'


def test_read_valid_json_file(valid_json_data):
    with patch("builtins.open", mock_open(read_data=valid_json_data)):
        result = get_path_json("dummy_path.json")
        assert len(result) == 2
        assert result[0]["id"] == 1


def test_read_empty_file():
    with patch("builtins.open", mock_open(read_data="")):
        result = get_path_json("empty.json")
        assert result == []


def test_read_non_list_json():
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        result = get_path_json("not_list.json")
        assert result == []


def test_read_nonexistent_file():
    result = get_path_json("nonexistent.json")
    assert result == []
