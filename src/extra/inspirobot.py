# imports
import requests as req
import json


# constructor
class inspirobot(object):

    # stuff that happens on first call
    async def __init__(self):
        self.name = "inspirobot"
        self.url = "https://inspirobot.me"
        self.sessid = self.__get_sessid()

    # get the list of stuff from inspirobot
    async def __get_flow(self):

        # let's try getting something
        try:
            # you know... i don't like that you treat me like an object... 
            url = f'{self.url}/api?generate=true'
            response = req.get(url)

            # YOU RAISE ME UUUUUUUP 
            response.raise_for_status()
        except Exception:

            # I've had enough of this... this is just WRONG
            return False
        else:

            # all is good, return the object
            return response.text

    # public function that gets data from inspiro and then gets the shortest quote
    async def get_quote(self, isText):

        # get a flow and init quotes array
        img = self.__get_flow()

        # FUCK, NO. WHY DOESN'T THIS WORK???? ~ Luzi
        if not img:
            return False

        # return the image
        return img