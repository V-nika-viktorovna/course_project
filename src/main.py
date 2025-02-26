import json
import logging
import os.path
from typing import Any

import pandas as pd

from src.utils import filеter_df_date, get_cards_numbers, get_data_cards, get_top_five_transactions, time_of_day
from src.views import get_exchange_rate, get_share_price

CURRENT_DIR = os.path.dirname(__file__)
LOGS_DIR = os.path.join(CURRENT_DIR, '..', 'logs')
log_file = os.path.join(LOGS_DIR, 'views.log')

logger = logging.getLogger('views')
logger.setLevel(logging.DEBUG)
logger_hendler = logging.FileHandler(log_file, 'w')
logger_formater = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
logger_hendler.setFormatter(logger_formater)
logger.addHandler(logger_hendler)


def main_page(date_use: str) -> Any:
    """ Функция для страницы 'Главная'.
    Принимающую на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS.
    Возвращающает JSON-ответ со следующими данными:
    1.Приветствие в формате "???",
    где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
    2.По каждой карте:
        -последние 4 цифры карты;
        -общая сумма расходов;
        -кешбэк .
    3.Топ-5 транзакций по сумме платежа.
    4.Курс валют, согласно файла user_settings.
    5.Стоимость акций, согласно файла user_settings."""

    logger.info('Setting the time of day for greeting')
    if time_of_day() == 'утро':
        greeting = 'Доброе утро'
    elif time_of_day() == 'день':
        greeting = 'Добрый день'
    elif time_of_day() == 'вечер':
        greeting = 'Добрый вечер'
    elif time_of_day() == 'ночь':
        greeting = 'Доброй ночи'

    try:
        logger.info('Getting a DataFrame from an excel file with transaction data')
        CURRENT_DIR = os.path.dirname(__file__)
        DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')
        FILE_DIR = os.path.join(DATA_DIR, 'operations.xlsx')
        data = pd.read_excel(FILE_DIR)
    except Exception as e:
        logger.error(f'Ошибка: {e}')
        return 'Не удалось открыть файл'

    logger.info("We filter the DataFrame by date and get a list of all the user's cards.")
    filеter_df_date_try = filеter_df_date(data, date_use)
    get_cards_numbers_try = get_cards_numbers(data)

    logger.info('We receive expenses for each card for the period from '
                'the beginning of the month to the specified date')
    cards = get_data_cards(filеter_df_date_try, get_cards_numbers_try)

    logger.info('We get the 5 biggest expenses for the period from '
                'the beginning of the month to the specified date')
    top_transactions = get_top_five_transactions(filеter_df_date_try)

    logger.info('We get the exchange rates according to the user_settings file')
    currency_rates = get_exchange_rate()

    logger.info('We get the share price according to the user_settings file')
    stock_prices = get_share_price()

    result = {
        'greeting': greeting,
        'cards': cards,
        'top_transactions': top_transactions,
        'currency_rates': currency_rates,
        'stock_prices': stock_prices
    }
    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    print(main_page('2020-03-20 10:20:30'))
