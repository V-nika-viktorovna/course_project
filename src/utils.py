import datetime
import logging
import os.path

import pandas as pd

CURRENT_DIR = os.path.dirname(__file__)
LOGS_DIR = os.path.join(CURRENT_DIR, '..', 'logs')
log_file = os.path.join(LOGS_DIR, 'utils.log')

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)
logger_hendler = logging.FileHandler(log_file, 'w')
logger_formater = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
logger_hendler.setFormatter(logger_formater)
logger.addHandler(logger_hendler)


def time_of_day() -> str:
    """Функция определяет впемя суток(утро, день, вечер, ночь)"""

    logger.info('We get the current date and time')
    date_time_now = datetime.datetime.now().hour

    hour = int(date_time_now)
    if 4 <= hour < 12:
        time_of_day = 'утро'
    elif 11 <= hour < 17:
        time_of_day = 'день'
    elif 17 <= hour < 22:
        time_of_day = 'вечер'
    else:
        time_of_day = 'ночь'

    return time_of_day


def filеter_df_date(df: pd.DataFrame, date_str: str) -> pd.DataFrame:
    """Функция фильтрует полученный DataFrame по дате.
    Возвращает отфильтрованный DataFrame, в котором транзакции с начала месяца и по введенную дату"""

    logger.info('Converting the entered date to datetime')
    date_filter = datetime.datetime(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]),
                                    int(date_str[11:13]), int(date_str[14:16]), int(date_str[17:19]))
    data_dicts = df.to_dict(orient='records')

    logger.info('Filtering the DataFrame')
    result = []
    for data_dict in data_dicts:
        date_transaction = data_dict.get('Дата операции')
        date_obj = datetime.datetime(int(date_transaction[6:10]), int(date_transaction[3:5]),
                                     int(date_transaction[0:2]), int(date_transaction[11:13]),
                                     int(date_transaction[14:16]), int(date_transaction[17:19]))
        if date_obj.year == date_filter.year and date_obj.month == date_filter.month:
            if date_obj.day <= date_filter.day:
                result.append(data_dict)

    return pd.DataFrame(result)


def get_cards_numbers(df: pd.DataFrame) -> list[dict]:
    """Функция принимает DataFrame и возвращает список всех номеров карт, которые есть в DataFrame"""

    logger.info("Getting a list of all the user's cards")
    data_dicts = df.to_dict(orient='records')

    cards_numbers = []
    for data_dict in data_dicts:
        if data_dict.get('Номер карты') not in cards_numbers:
            if type(data_dict.get('Номер карты')) == float or not data_dict.get('Номер карты'):
                continue
            cards_numbers.append(data_dict.get('Номер карты'))
    return cards_numbers


def get_data_cards(df: pd.DataFrame, users_cards_numbers=[]) -> list[dict]:
    """Функция принимает DataFrame и список карт, которые есть у пользователя.
    Возвращает список словарей с данными по каждой карте
    -последние 4 цифры номера карты,
    -расход по данной карте
    -кешбек по данной карте"""

    data_dicts = df.to_dict(orient='records')
    results = []
    cards_numbers = []

    logger.info('Creating a list of maps in a filtered DataFrame')
    for data_dict in data_dicts:
        if data_dict.get('Номер карты') not in cards_numbers:
            if type(data_dict.get('Номер карты')) == float or not data_dict.get('Номер карты'):
                continue
            cards_numbers.append(data_dict.get('Номер карты'))

    logger.info('Creating a list of expenses for each card')
    for card in cards_numbers:
        transaction_amount = 0
        cashback = 0
        card_data = df[df['Номер карты'] == card].to_dict(orient='records')

        for card_dict in card_data:
            if card_dict.get('Статус') == 'OK':
                if card_dict.get('Сумма операции') < 0:
                    transaction_amount += card_dict.get('Сумма операции')
                if card_dict.get('Кэшбэк'):
                    cashback_data = str(card_dict.get('Кэшбэк'))
                    if cashback_data != 'nan':
                        cashback += card_dict.get('Кэшбэк')

        result_dict = {
            'last_digits': card[1:],
            'total_spent': round(transaction_amount, 2),
            'cashback': cashback
            }
        results.append(result_dict)

    card_result_list = []
    for result in results:
        card_result_list.append(f'*{result.get('last_digits')}')

    logger.info('Adding the cards for which there were no expenses to the list')
    for card in users_cards_numbers:
        if card not in card_result_list:
            result_dict = {
                'last_digits': card[1:],
                'total_spent': 0,
                'cashback': 0
            }
            results.append(result_dict)

    return results


def get_top_five_transactions(df: pd.DataFrame) -> list[dict]:
    """Функция принимает DataFrame с транзакциями, фильтрует его по суммне операции.
    Возвращает список словарей с пятью наибольшими тратами, содержащими данные:
    - дату операции,
    - сумму операции,
    - категорию операции,
    - описание операции"""
    try:
        logger.info('Editing the DataFrame')
        sort_df = df.sort_values('Сумма операции')
        sort_dicts = sort_df.to_dict(orient='records')

    except KeyError:
        logger.error('KeyError during filtering')
        sort_dicts = {}

    except Exception as e:
        logger.error(f'Error: {e}')
        sort_dicts = {}

    finally:
        logger.info('Creating a list of the top five expenses')
        top_transactions = []
        index_sort = 5
        for sort_dict in sort_dicts:
            if index_sort > 0 and sort_dict.get('Сумма операции') < 0:
                result = {
                    "date": sort_dict.get('Дата операции'),
                    "amount": sort_dict.get('Сумма операции'),
                    "category": sort_dict.get('Категория'),
                    "description": sort_dict.get('Описание')
                    }
                top_transactions.append(result)
                index_sort -= 1

        return top_transactions


if __name__ == '__main__':
    CURRENT_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')
    FILE_DIR = os.path.join(DATA_DIR, 'operations.xlsx')
    data = pd.read_excel(FILE_DIR)
    try_filеter_df_date = filеter_df_date(data, '2020-01-26 04:07:25')
    try_get_cards_numbers = get_cards_numbers(data)
    print(get_data_cards(try_filеter_df_date, try_get_cards_numbers))
    print(get_top_five_transactions(try_filеter_df_date))
    #print(type(2022-01-01 04:07:25))
    print(time_of_day())
