import json
import requests
from config import keys


class APIException(Exception):
    pass


class CheckingDataConverter(Exception):
    @staticmethod
    def checking_data(*args):
        try:
            if len(args[0]) == 3:
                base, quote, amount = args[0]
                if quote != base and quote in keys and base in base:
                    try:
                        if float(amount):
                            return True
                    except ValueError:
                        raise APIException(f'Третий параметр должен быть числом.\n'
                                           f'Не целые числа разделяются точкой.')
                else:
                    raise APIException(f'Коветируемая валюта равна конвертируемой.\n'
                                       f'Введеной валюты нет в базе или введена не корректно.\n'
                                       f'Ознокомиться с перечнем валют можно применив команду: /values.')
            else:
                raise APIException(f'Неверно составлен запрос, ознакомтесь с инструкцией с помощью команды: /help.')
        except Exception:
            raise

    @staticmethod
    def get_price(*args):
        base, quote, amount = args[0]
        try:
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
        except KeyError:
            raise APIException('Неверно введена валюта. '
                                'Ознокомиться с перечнем валют можно применив команду: /values.')
        else:
            total_base = json.loads(r.content)[keys[quote]]
            text = f'Цена {amount} {base} в {quote} - {total_base * float(amount)}'
            return text
