import requests

from config import EXCHANGE_TOKEN
import db


URL = "https://fxmarketapi.com/"

#Saved so as not to waste unnecessary requests to the api
ALL_CURRENCY = ['USDAED', 'USDARS', 'USDAUD', 'USDBRL', 'BTCUSD', 
    'USDCAD', 'USDCHF', 'USDCLP', 'USDCNY', 'USDCOP', 'USDCZK', 
    'USDDKK', 'USDEUR', 'USDGBP', 'USDHKD', 'USDHUF', 'USDHRK', 
    'USDIDR', 'USDILS', 'USDINR', 'USDISK', 'USDJPY', 'USDKRW', 
    'USDKWD', 'USDMXN', 'USDMYR', 'USDMAD', 'USDNOK', 'USDNZD', 
    'USDPEN', 'USDPHP', 'USDPLN', 'USDRON', 'USDRUB', 'USDSEK', 
    'USDSGD', 'USDTHB', 'USDTRY', 'USDTWD', 'USDXAG', 'USDXAU', 'USDZAR']


# def get_all_name_currencies() -> list:
#     end_url = "apicurrencies"
#     querystring = {"api_key" : EXCHANGE_TOKEN}
#     response = requests.get(URL + end_url, params=querystring)
#     all_currencies = response.json().get('currencies').keys()
#     return all_currencies


def get_list_currencies(user_id: str) -> str:
    end_url = "apilive"
    querystring = {"currency" : ",".join(ALL_CURRENCY), 
                    "api_key" : EXCHANGE_TOKEN}
    response = requests.get(URL + end_url, params=querystring)
    if response.status_code == 200:
        all_currencies = response.json().get('price')
        answer = ""
        for key, value in all_currencies.items():
            answer += f"{key} : %.2f\n" % value
        return answer
    else:
        return "Error"


def exchange_currencies(from_currency: str, to_currency: str,
                        amount: str) -> str:
    end_url = "apiconvert"
    querystring = {"api_key" : EXCHANGE_TOKEN, "from" : from_currency,
                    "to" : to_currency, "amount" : amount}
    response = requests.get(URL + end_url, params=querystring)
    if response.status_code == 200:
        total_price = response.json().get('total')
        return f"{total_price} {to_currency}"
    else:
        return "Error"


def exchange_history(currencys: str, start_date: str,
                     end_date: str) -> str or dict:
    end_url = "apipandas"
    querystring = {"api_key" : EXCHANGE_TOKEN, "currency" : currencys,
                   "start_date" : start_date, "end_date" : end_date}
    response = requests.get(URL + end_url, params=querystring)
    response_json = response.json()
    if response.status_code == 200 and 'error' not in response_json.keys():
        return response_json['open']
    else:
        return "No exchange rate data is available for the selected currency."
    