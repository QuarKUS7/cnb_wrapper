import requests
from datetime import datetime, date


class WrongDateCombination(Exception):
    """Error for missing or wrong date in history"""
    pass


def constrain_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(value[:10], '%Y-%m-%d').date()


class CnbRates():

    actions = {"latest": "latest",
               "convert": "currency_converter?amount={amount}&input_currency={input}&output_currency={output}",
               "convert_date": "currency_converter?amount={amount}&input_currency={input}&output_currency={output}&date={date}",
               "history_day":"history?date={date}",
               "history_range": "history?start_date={start}&end_date={end}"}

    base_url = "http://cnbrates.pgc.sk/"
    
    def _request(self, action, **kwargs):

        template = self.base_url + self.actions[action]
        url = template.format(**kwargs)

        response = requests.get(url)

        response.raise_for_status()

        if response.content:
            return response.json()
        return None

    def convert(self, amount, input_currency, output_currency, date=None):
        if not date:
            return self._request("convert", amount=amount, input=input_currency, output=output_currency)
        else:
            try:
                date = constrain_date(date)
            except ValueError:
                print("Unknown date format!")
        return self._request("convert_date", amount=amount, input=input_currency, output=output_currency, date=date)
    
    def latest(self):
        return self._request("latest")

    def history(self, date=None, start=None, end=None):
        if date and not start and not end:
            try:
                date = constrain_date(date)
            except ValueError:
                print("Unknown date format!")
            return self._request("history_day", date=date)
        if not date and start and end:
            try:
                start = constrain_date(start)
                end = constrain_date(end)
            except ValueError:
                print("Unknown date format!")
            return self._request("history_range", start=start, end=end)
        raise WrongDateCombination()



c = CnbRates()

print("latest")
print(c.latest())
print("convert")
print(c.convert(100,"EUR", "USD"))
print("convert date")
print(c.convert(100,"EUR", "USD", date="2018-06-06"))
print("history day")
print(c.history(date="2018-05-05"))
