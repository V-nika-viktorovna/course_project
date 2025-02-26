import os.path
from functools import wraps
from typing import Any


def decorator_write_result_file(func) -> Any:
    """Декоратор для функций-отчетов, который записывает в файл результат,
    который возвращает функция, формирующая отчет.
    Декоратор записывает данные отчета в файл с названием по умолчанию
    (название функции для которой он был применен)"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = str(func(*args, **kwargs))
        func_name = f'{func.__name__}.txt'
        CURRENT_DIR = os.path.dirname(__file__)
        DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')
        FILE_DIR = os.path.join(DATA_DIR, func_name)

        with open(FILE_DIR, 'w', encoding='UTF-8') as file:
            file.write(result)

    return wrapper
