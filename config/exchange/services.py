import requests

# Получение актуального курса доллара к рублю, используя официальный API ЦБ РФ
def get_usd_to_rub_exchange_rate():
    try:
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js') 
        data = response.json()
        usd_to_rub_rate = data['Valute']['USD']['Value']
        return usd_to_rub_rate
    except (requests.RequestException):
        return None