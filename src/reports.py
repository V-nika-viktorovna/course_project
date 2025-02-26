import datetime
import json
import logging
import os.path
from typing import Optional

import pandas as pd

CURRENT_DIR = os.path.dirname(__file__)
LOGS_DIR = os.path.join(CURRENT_DIR, '..', 'logs')
log_file = os.path.join(LOGS_DIR, 'reports.log')

logger = logging.getLogger('reports')
logger.setLevel(logging.DEBUG)
logger_hendler = logging.FileHandler(log_file, 'w')
logger_formater = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
logger_hendler.setFormatter(logger_formater)
logger.addHandler(logger_hendler)


def biggest_expenses(df: pd.DataFrame, year: str, month: str) -> dict["json"]:
    """Функция позволяет оценить по каким трем категориям за указанный месяц были самые большие траты
    Для аназила принимает DataFrame, нужные год и месяц.
    Возвращает словарь с названием категорий и суммой трат по каждой, в формате json."""

    data_dicts = df.to_dict(orient='records')

    logger.info('Filtering the DataFrame by the desired month')
    analyzed_month_dicts = []
    for data_dict in data_dicts:
        date_transaction = data_dict.get('Дата операции')
        if data_dict.get('Статус') == 'OK':
            if data_dict.get('Сумма операции') < 0:
                if int(date_transaction[6:10]) == year and int(date_transaction[3:5]) == month:
                    analyzed_month_dicts.append(data_dict)

    logger.info('Creating a list of categories')
    categories_list = []
    for month_dict in analyzed_month_dicts:
        if month_dict.get('Категория') not in categories_list:
            categories_list.append(month_dict.get('Категория'))

    logger.info('Creating and sorting a list of expenses by category')
    total_amount_categorie = []
    for categorie in categories_list:
        total_amount = 0
        for month_dict in analyzed_month_dicts:
            if month_dict.get('Категория') == categorie:
                total_amount += month_dict.get('Сумма платежа')
                total_dict = {
                    'categorie': categorie,
                    'total_amount': total_amount
                }
        total_amount_categorie.append(total_dict)
    sort_categories = sorted(total_amount_categorie, key=lambda x: x['total_amount'])
    result = []

    try:
        logger.info('We are creating a list with three categories with the most expenses per month.')
        categorie1 = {sort_categories[0].get('categorie'): round(sort_categories[0].get('total_amount'), 2)}
        categorie2 = {sort_categories[1].get('categorie'): round(sort_categories[1].get('total_amount'), 2)}
        categorie3 = {sort_categories[2].get('categorie'): round(sort_categories[2].get('total_amount'), 2)}
        result = [categorie1, categorie2, categorie3]

    except Exception:
        logger.info('We are creating a list with two categories with the most expenses per month.')
        if categorie1 and categorie2:
            result = [categorie1, categorie2,]
        elif categorie1:
            logger.info('Creating a list by the category with the most expenses for the month')
            result = [categorie1]
        else:
            logger.error("Couldn't generate a list")
            result = []

    finally:
        return json.dumps(result, ensure_ascii=False, indent=4)


#@decorator_write_result_file
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list[dict]:
    """Функция принимает DataFrame, название категории и опционально дату в формате YYYY-MM-DD.
    Возвращает список словарей с транзакциями по заданной категории за последние три месяца (от переданной даты)"""

    logger.info('We check if the date is entered, if not, the current date will be assigned.')
    if not date:
        date = str(datetime.datetime.now())

    data_dicts = transactions.to_dict(orient='records')

    logger.info('We are creating a list with expenses for the last three months (from the transmitted date)')
    analyzed_month_dicts = []
    for data_dict in data_dicts:
        date_dict = data_dict.get('Дата операции')
        month_data = int(date[5:7])
        if (data_dict.get('Категория') == category and data_dict.get('Статус') == 'OK'
                and data_dict.get('Сумма операции') < 0):

            if month_data > 2:
                if (int(date_dict[6:10]) == int(date[:4]) and int(date_dict[3:5]) == month_data
                        and int(date_dict[0:2]) <= int(date[8:10])):
                    analyzed_month_dicts.append(data_dict)
                if int(date_dict[6:10]) == int(date[:4]) and int(date_dict[3:5]) == month_data-1:
                    analyzed_month_dicts.append(data_dict)
                if int(date_dict[6:10]) == int(date[:4]) and int(date_dict[3:5]) == month_data-2:
                    analyzed_month_dicts.append(data_dict)
                if (int(date_dict[6:10]) == int(date[:4]) and int(date_dict[3:5]) == month_data-3
                        and int(date_dict[0:2]) >= int(date[8:10])):
                    analyzed_month_dicts.append(data_dict)

            elif month_data == 2:
                if (int(date_dict[6:10]) == int(date[:4]) and int(date_dict[3:5]) == month_data
                        and int(date_dict[0:2]) <= int(date[8:10])):
                    analyzed_month_dicts.append(data_dict)
                if int(date_dict[6:10]) == int(date[:4]) and int(date_dict[3:5]) == month_data-1:
                    analyzed_month_dicts.append(data_dict)
                if int(date_dict[6:10]) == int(date[:4])-1 and int(date_dict[3:5]) == 12:
                    analyzed_month_dicts.append(data_dict)
                if (int(date_dict[6:10]) == int(date[:4])-1 and int(date_dict[3:5]) == 11
                        and int(date_dict[0:2]) >= int(date[8:10])):
                    analyzed_month_dicts.append(data_dict)

            elif month_data == 1:
                if (int(date_dict[6:10]) == int(date[:4]) and int(date_dict[3:5]) == month_data
                        and int(date_dict[0:2]) <= int(date[8:10])):
                    analyzed_month_dicts.append(data_dict)
                if int(date_dict[6:10]) == int(date[:4])-1 and int(date_dict[3:5]) == 12:
                    analyzed_month_dicts.append(data_dict)
                if int(date_dict[6:10]) == int(date[:4])-1 and int(date_dict[3:5]) == 11:
                    analyzed_month_dicts.append(data_dict)
                if (int(date_dict[6:10]) == int(date[:4])-1 and int(date_dict[3:5]) == 10
                        and int(date_dict[0:2]) >= int(date[8:10])):
                    analyzed_month_dicts.append(data_dict)

    return analyzed_month_dicts


if __name__ == '__main__':
    CURRENT_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')
    FILE_DIR = os.path.join(DATA_DIR, 'operations.xlsx')
    a = pd.read_excel(FILE_DIR)
    print(biggest_expenses(a,  '2019', '1'))
    print(spending_by_category(a, 'Супермаркеты', '2020-02-12'))
