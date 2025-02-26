from unittest.mock import patch

from src.views import get_exchange_rate, get_share_price


@patch('requests.get')
def test_get_exchange_rate_try(mock_get_1):
    mock_lict = [
        {'success': True, 'query': {'from': 'USD', 'to': 'RUB', 'amount': 1},
         'info': {'timestamp': 1738744983, 'rate': 98.954297}, 'date': '2025-02-05', 'historical': True,
         'result': 98.954297}
        ]
    mock_get_1.return_value.json.return_value = mock_lict[0]
    assert get_exchange_rate() == [{'currency': 'USD', 'rate': 98.95}, {'currency': 'EUR', 'rate': 98.95}]


@patch('requests.get')
def test_get_share_price_try(mock_get_1):
    mock_lict = {
                  "pagination": {
                                "limit": 100,
                                "offset": 0,
                                "count": 100,
                                "total": 100
                                },
                  "data": [
                         {
                          "open": 248.0,
                          "high": 249.98,
                          "low": 244.91,
                          "close": 247.04,
                          "volume": 46872348.0,
                          "adj_high": 250.0,
                          "adj_low": 244.91,
                          "adj_close": 247.04,
                          "adj_open": 248.0,
                          "adj_volume": 47275651.0,
                          "split_factor": 1.0,
                          "dividend": 0.0,
                          "symbol": "AAPL",
                          "exchange": "XNAS",
                          "date": "2025-02-25T00:00:00+0000"
                          }
                         ]
                  }
    mock_get_1.return_value.json.return_value = mock_lict
    assert get_share_price() == [{'stock': 'AAPL', 'price': 247.04},
                                 {'stock': 'NVDA', 'price': 247.04},
                                 {'stock': 'MSFT', 'price': 247.04},
                                 {'stock': 'AMZN', 'price': 247.04},
                                 {'stock': 'GOOGL', 'price': 247.04}]
