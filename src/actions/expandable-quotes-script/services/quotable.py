# imports
import requests as req
import json

class quotable(object):

    def __init__(self, config):
        self.name = "quotable"
        self.url = "https://api.quotable.io"
        self.config = config
    
    def get_quote(self):
        data = self.__get_data()

        try:
            quote = data["content"]
        except Exception:
            return False
        else:
            return quote

    def __get_data(self):
        try:
            url = f'{self.url}/random'
            response = req.get(url)
            response.raise_for_status()
        except Exception:
            return False
        else:   
            return json.loads(response.text)

def create(config):
    return quotable(config)