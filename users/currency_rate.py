import requests
from datetime import datetime

from requests.structures import CaseInsensitiveDict


def send_msg_to_telegram(limit):
    url = f"https://api.telegram.org/bot5261757413:AAGFf36Piy1Wqim32QJ8es09AltGXakbZ-4/sendMessage?chat_id=256841597&text={limit}"
    requests.request("POST", url)


def get_currency_rate():
    # url = "https://api.apilayer.com/currency_data/live?source=RUB&currencies=USD,EUR,UZS"
    url = "https://api.currencyapi.com/v3/latest?currencies=EUR%2CUSD%2CUZS&base_currency=RUB"

    payload = {}
    # headers = {
    #     # "apikey": "ARxegN1T5Xq7vCTEyq0j3HgGizJbl0xs"
    # }
    headers = CaseInsensitiveDict()
    headers["apikey"] = "ojPAu3Qj3VAKHGFSBZQ7zz2jhJPqJriUzV2DiLgO"

    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()

    # rate = result["quotes"]
    limit = response.headers["x-ratelimit-remaining-quota-month"]
    send_msg_to_telegram(limit)

    rate = {
        "RUBUSD": result["data"]["USD"]["value"],
        "RUBEUR": result["data"]["EUR"]["value"],
        "RUBUZS": result["data"]["UZS"]["value"],
        "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    return rate


# {'RUBUSD': 0.013689, 'RUBEUR': 0.01298, 'RUBUZS': 154.141127, 'updated_at': '2023-01-05 02:54:58'}

if __name__ == '__main__':
    # print(get_currency_rate())
    # send_msg_to_telegram(284)
    pass
