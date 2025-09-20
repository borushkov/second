import config 
import requests
import json
class APIException(Exception):
    pass
class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException("Невозможно конвертировать одну и ту же валюту")
        try:
            quote_ticker = config.keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}")
        try:
            base_ticker = config.keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        data = json.loads(r.content)
        if quote_ticker not in data:
            raise APIException(f"Курс для валюты {quote} не найден в ответе API")
        rate = data[quote_ticker]
        total_base = rate * amount
        return total_base