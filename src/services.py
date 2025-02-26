import json
import logging
import os.path

import pandas as pd

CURRENT_DIR = os.path.dirname(__file__)
LOGS_DIR = os.path.join(CURRENT_DIR, '..', 'logs')
log_file = os.path.join(LOGS_DIR, 'services.log')

logger = logging.getLogger('services')
logger.setLevel(logging.DEBUG)
logger_hendler = logging.FileHandler(log_file, 'w')
logger_formater = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
logger_hendler.setFormatter(logger_formater)
logger.addHandler(logger_hendler)


def profitable_cashback_categories(df: pd.DataFrame, year: str, month: str) -> dict[json]:
    """Функция принимает DataFrame с транзакциями, год и месяц, проводит анализ транзакций по кешбеку.
    Возвращает словарь в формате json с категориями, по которым в данном месяце был получен кешбек,
    и сумму кешбека в каждой категории за месяц."""

    data_dicts = df.to_dict(orient='records')
    logger.info('Filtering the DataFrame by date')
    analyzed_cashback_dicts = []
    for data_dict in data_dicts:
        date_transaction = data_dict.get('Дата операции')
        if data_dict.get('Кэшбэк') > 0:
            if int(date_transaction[6:10]) == year and int(date_transaction[3:5]) == month:
                analyzed_cashback_dicts.append(data_dict)

    logger.info('Creating a list of categories')
    categories_list = []
    for cashback_dict in analyzed_cashback_dicts:
        if cashback_dict.get('Категория') not in categories_list:
            categories_list.append(cashback_dict.get('Категория'))

    logger.info("Let's summarize the cashback by category'")
    total_dict = {}
    for categorie in categories_list:
        total_amount = 0
        for cashback_dict in analyzed_cashback_dicts:
            if cashback_dict.get('Категория') == categorie:
                total_amount += cashback_dict.get('Кэшбэк')
                total_dict[categorie] = total_amount

    return json.dumps(total_dict, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    CURRENT_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')
    FILE_DIR = os.path.join(DATA_DIR, 'operations.xlsx')
    a = pd.read_excel(FILE_DIR)
    print(profitable_cashback_categories(a, 2021, 11))
