import freezegun
import pandas as pd
import pytest

from src.utils import filеter_df_date, get_cards_numbers, get_data_cards, get_top_five_transactions, time_of_day


@pytest.mark.parametrize('expected', ['утро'])
def test_time_of_day_try_morning(expected):
    with freezegun.freeze_time("2025-02-25 06:35:50.032596"):
        assert time_of_day() == expected


@pytest.mark.parametrize('expected', ['вечер'])
def test_time_of_day_try_evening(expected):
    with freezegun.freeze_time("2025-02-25 18:35:50.032596"):
        assert time_of_day() == expected


@pytest.mark.parametrize('expected', ['день'])
def test_time_of_day_try_day(expected):
    with freezegun.freeze_time("2025-02-25 14:35:50.032596"):
        assert time_of_day() == expected


@pytest.mark.parametrize('expected', ['ночь'])
def test_time_of_day_try_night(expected):
    with freezegun.freeze_time("2025-02-25 03:35:50.032596"):
        assert time_of_day() == expected


def test_filеter_df_date_try(df_transactions):
    df_list = [
                {
                    "Дата операции": "01.01.2018 20:27:51",
                    "Дата платежа": "04.01.2018",
                    "Номер карты": "*7197",
                    "Статус": "OK",
                    "Сумма операции": -316.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -316.0,
                    "Валюта платежа": "RUB",
                    "Кэшбэк": None,
                    "Категория": "Красота",
                    "MCC": 5977.0,
                    "Описание": "OOO Balid",
                    "Бонусы (включая кэшбэк)": 6,
                    "Округление на инвесткопилку": 0,
                    "Сумма операции с округлением": 316.0
                },
                {
                    "Дата операции": "01.01.2018 12:49:53",
                    "Дата платежа": "01.01.2018",
                    "Номер карты": None,
                    "Статус": "OK",
                    "Сумма операции": -3000.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -3000.0,
                    "Валюта платежа": "RUB",
                    "Кэшбэк": None,
                    "Категория": "Переводы",
                    "MCC": 2.3,
                    "Описание": "Линзомат ТЦ Юность",
                    "Бонусы (включая кэшбэк)": 0,
                    "Округление на инвесткопилку": 0,
                    "Сумма операции с округлением": 3000.0
                }
            ]
    try_func = filеter_df_date(df_transactions, '2018-01-02 04:07:25')
    result = try_func.to_dict(orient='records')
    assert result == df_list


def test_filеter_df_date_none():
    df = pd.DataFrame([])
    try_func = filеter_df_date(df, '2018-01-02 04:07:25')
    result = try_func.to_dict()
    assert result == {}


def test_get_cards_numbers_try(df_transactions):
    assert get_cards_numbers(df_transactions) == ["*5441", "*7197", "*4556"]


def test_get_data_cards_try(df_transactions):
    assert get_data_cards(df_transactions, ["*5441", "*7197", "*4556"]) == [
                                                                                          {
                                                                                            'last_digits': '5441',
                                                                                            'total_spent': 0,
                                                                                            'cashback': 0
                                                                                          },
                                                                                          {
                                                                                            'last_digits': '7197',
                                                                                            'total_spent': -4069.95,
                                                                                            'cashback': 0
                                                                                          },
                                                                                          {
                                                                                            'last_digits': '4556',
                                                                                            'total_spent': -250.0,
                                                                                            'cashback': 0
                                                                                          }
                                                                                        ]


def test_get_data_cards_df_none():
    df = pd.DataFrame([])
    assert get_data_cards(df) == []


def test_get_top_five_transactions_try(df_transactions):
    try_func = [
                {
                    "date": "10.01.2018 12:41:24",
                    "amount": -87068.0,
                    "category": None,
                    "description": "Перевод с карты"
                },
                {
                    "date": "10.01.2018 12:42:44",
                    "amount": -40068.0,
                    "category": None,
                    "description": "Перевод с карты"
                },
                {
                    "date": "10.01.2018 12:43:34",
                    "amount": -30068.0,
                    "category": None,
                    "description": "Перевод с карты"
                },
                {
                    "date": "01.01.2018 12:49:53",
                    "amount": -3000.0,
                    "category": "Переводы",
                    "description": "Линзомат ТЦ Юность"
                },
                {
                    "date": "04.01.2018 14:05:08",
                    "amount": -1065.9,
                    "category": "Супермаркеты",
                    "description": "Пятёрочка"
                }
            ]
    assert get_top_five_transactions(df_transactions) == try_func


def test_get_top_five_transactions_none():
    df = pd.DataFrame([])
    assert get_top_five_transactions(df=df) == []
