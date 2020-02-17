# imports
import requests as req
import json

class quotable(object):

    def __init__(self):
        self.name = "quotable"
        self.url = "https://api.quotable.io"
    
    async def get_quote(self):
        data = await self.__get_data()

        try:
            quote = data["content"]
        except Exception:
            return False
        else:
            return quote

    async def __get_data(self):
        try:
            url = f'{self.url}/random'
            response = req.get(url)
            response.raise_for_status()
        except Exception:
            return False
        else:   
            return json.loads(response.text)
