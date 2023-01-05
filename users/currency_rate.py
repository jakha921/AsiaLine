import requests
from datetime import datetime

from requests.structures import CaseInsensitiveDict


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
    rate = {
        "RUBUSD": result["data"]["USD"]["value"],
        "RUBEUR": result["data"]["EUR"]["value"],
        "RUBUZS": result["data"]["UZS"]["value"],
        "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    return rate


# {'RUBUSD': 0.013689, 'RUBEUR': 0.01298, 'RUBUZS': 154.141127, 'updated_at': '2023-01-05 02:54:58'}

if __name__ == '__main__':
    print(get_currency_rate())
    pass
