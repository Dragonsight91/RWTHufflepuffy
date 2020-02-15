# imports
import requests as req
import json


class evilinsult(object):
    
    def __init__(self, config):
        self.name   = "evilinsult"
        self.url    = "https://evilinsult.com"
        self.config = config
    
    def __get_data(self):
        try:
            url = f'{self.url}/generate_insult.php?lang=en&type=json'
            response = req.get(url)

            response.raise_for_status()
        except Exception:
            return False
        else:
            return json.loads(response.text)

    def get_quote(self):
        data = self.__get_data()

        if not data:
            return False
        
        return data["insult"]

def create(config):
    return evilinsult(config)