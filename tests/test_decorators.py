import pytest

from src.decorators import log


# Тестируем функцию без ошибок, лог должен пойти в консоль
def test_log_success_console(capsys):
    @log()
    def add(x, y):
        return x + y

    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    assert "add ok" in captured.out


# Тестируем функцию с ошибкой, лог должен пойти в консоль
def test_log_error_console(capsys):
    @log()
    def divide(x, y):
        return x / y  # Деление на ноль вызовет ошибку

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


# Тестируем логирование в файл при успехе
def test_log_success_file(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def multiply(x, y):
        return x * y

    result = multiply(2, 4)
    assert result == 8

    content = log_file.read_text(encoding="utf-8")
    assert "multiply ok" in content


# Тестируем логирование в файл при ошибке
def test_log_error_file(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def subtract(x, y):
        return x / y  # Ошибка при y = 0

    with pytest.raises(ZeroDivisionError):
        subtract(10, 0)

    content = log_file.read_text(encoding="utf-8")
    assert "subtract error: ZeroDivisionError" in content
    assert "Inputs: (10, 0), {}" in content
