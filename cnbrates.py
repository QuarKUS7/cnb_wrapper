import requests

class CnbRates():

    actions = {"latest": "latest",
               "convert": "currency_converter?amount={amount}&input_currency={input}&output_currency={output}",
               "history_day":"history?date={date}",
               "history_range": "history?start_date={start}&end_date={end}"}

    base_url = "http://cnbrates.pgc.sk/"
    
    def _request(self, action, **kwargs):

        template = self.base_url + self.actions[action]
        url = template.format(**kwargs)

        r = requests.get(url)
        return r.json()
    
    def convert(self, amount, input_currency, output_currency):
        self._request("convert", amount=amount, input=input_currency, output=output_currency)
    
    def latest(self):
        return self._request("latest")

c = CnbRates()

print(c.latest())