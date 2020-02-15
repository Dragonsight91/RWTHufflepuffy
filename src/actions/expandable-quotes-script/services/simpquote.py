# imports
import requests as req
import json


class simpquote( object ):
    def __init__(self, config):
        self.name="simpsons quotes"
        self.config = config
        self.url = "https://thesimpsonsquoteapi.glitch.me"

    def __get_data(self):
        
        #let's try getting some data
        try:
            # get object
            url = f'{self.url}/quotes'
            response = req.get(url)

            # any error? throw with stones
            response.raise_for_status()

        except Exception:
            # WRONG ~ Trump, 2k19
            return False

        else:
            # return data
            return json.loads(response.text)
    
    def get_quote(self):

        # get the data
        data = self.__get_data()

        # is it what we expect? if no, shout
        if type(data) is list:

            # get the quote from the object
            quote = data[0]["quote"]
            return quote

        else:
            # NOOOOOOOOOOOOOOOOOOOOOO ~ Darth Vader
            return False

def create(config):
    return simpquote(config)