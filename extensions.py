import json
import requests
from config import keys


class APIException(Exception):
    pass


class CryptoConv:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Валюты должны быть разными. У Вас {base} и {quote}')

        if base in keys.values():
            raise APIException(f'Не удалось обработать валюту {quote}')

        if base in keys.values():
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверное количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
        return round((json.loads(r.content)[keys[quote]]) * amount, 2)
