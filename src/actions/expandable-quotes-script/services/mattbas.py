# imports
import requests as req
import json


class mattbas(object):
    
    def __init__(self, config):
        self.name   = "mattbas"
        self.url    = "https://insult.mattbas.org"
        self.config = config

    def __get_data(self):
        try:
            url = f'{self.url}/api/en/insult.json'
            response = req.get(url)

            response.raise_for_status()
        except Exception:
            return False
        else:
            return json.loads(response.text)
    
    def get_quote(self):
        data = self.__get_data()
        
        if type(data) is bool:
            return False
        if not "error" in data:
            return False
        
        quote = data["insult"]
        return quote
        
def create(config):
    return mattbas(config)