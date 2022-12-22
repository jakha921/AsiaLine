import requests
from datetime import datetime


def get_currency_rate():
    url = "https://api.apilayer.com/currency_data/live?source=RUB&currencies=USD,EUR,UZS"
    # url = "https://api.exconvert.com/convertMulti?from=RUB&to=USD,%20EUR,%20UZS&amount=1&access_key=22335c1a-1b91f2b7-78eaf94b-106bb131"

    payload = {}
    headers= {
        "apikey": "ARxegN1T5Xq7vCTEyq0j3HgGizJbl0xs"
        # "apikey": "22335c1a-1b91f2b7-78eaf94b-106bb131"
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.json()

    rate = result["quotes"]

    # rate =[(result['base']+key, round(value, 6)) for key, value in result['result'].items()]
    # rate = dict(rate)
    # # add date
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {'currency_rate': rate, 'update_at': date}

# {'currency_rate': {'RUBUSD': 0.014183, 'RUBEUR': 0.013353, 'RUBUZS': 160.26984}, 'update_at': '2022-12-21 01:01:01'}




if __name__ == '__main__':
    print(get_currency_rate())