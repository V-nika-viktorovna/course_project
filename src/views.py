import datetime
import json
import os.path

import requests
from dotenv import load_dotenv


def get_exchange_rate() -> list[dict]:
    """Функция возвращает список со словарями курса валют имеющихся в файле 'user_settings'
    Для курса валюты используется Exchange Rates Data API: https://apilayer.com/exchangerates_data-api."""

    CURRENT_DIR = os.path.dirname(__file__)
    FILE_DIR = os.path.join(CURRENT_DIR, '..', 'user_settings.json')

    load_dotenv()
    api_key = os.getenv('API_KEY_EXCHANGE_RATE')
    headers = {"apikey": api_key}
    date_obj = datetime.datetime.now()
    date_now = date_obj.strftime("%Y-%m-%d")

    with open(FILE_DIR, 'r') as file:
        read_data = json.load(file)

    result_currency = []
    if read_data.get("user_currencies"):
        for data in read_data.get("user_currencies"):
            url = f'https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={data}&amount=1&date={date_now}'
            responses = requests.get(url, headers)
            result = round(responses.json().get('result'), 2)
            result_dict = {
                'currency': data,
                'rate': result
            }
            result_currency.append(result_dict)

    return result_currency


def get_share_price() -> list[dict]:
    """Функция возвращает список со словарями цен на акции имеющихся в файле 'user_settings'
    Для получения цен используется Share Price Data API: https://api.marketstack.com."""

    CURRENT_DIR = os.path.dirname(__file__)
    FILE_DIR = os.path.join(CURRENT_DIR, '..', 'user_settings.json')

    with open(FILE_DIR, 'r') as file:
        read_data = json.load(file)

    load_dotenv()
    api_key = os.getenv('API_KEY_SHARE_PRICE')

    result_list = []
    if read_data.get('user_stocks'):
        for data in read_data.get('user_stocks'):
            querystring = {"symbols": {data}}
            responses = requests.get(f"https://api.marketstack.com/v1/eod?access_key={api_key}", params=querystring)
            data_dicts = responses.json().get('data')

            for data_dict in data_dicts:
                result = data_dict.get('close')
                break

            result_dict = {
                "stock": data,
                "price": result
            }
            result_list.append(result_dict)

    return result_list


if __name__ == '__main__':
    #print(get_exchange_rate())
    print(get_share_price())
