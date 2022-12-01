import requests
from datetime import datetime


def get_currency_rate():
    url = "https://api.apilayer.com/currency_data/live?source=RUB&currencies=USD,EUR,UZS"

    payload = {}
    headers= {
        "apikey": "ARxegN1T5Xq7vCTEyq0j3HgGizJbl0xs"
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.json()
    ts = result['timestamp']
    date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return {'currency_rate': result['quotes'], 'date': date}




if __name__ == '__main__':
    print(get_currency_rate())