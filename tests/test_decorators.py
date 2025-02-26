import os.path

from src.decorators import decorator_write_result_file


def test_decorator_write_result_file_try(capsys):
    @decorator_write_result_file
    def summ_num(x, y):
        return x + y

    print(summ_num(8, 9))
    CURRENT_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')
    FILE_DIR = os.path.join(DATA_DIR, 'summ_num.txt')
    with open(FILE_DIR, 'r') as file:
        text_file = file.read()
    captured = capsys.readouterr()

    assert captured.out == 'None\n'
    assert text_file == "17"
