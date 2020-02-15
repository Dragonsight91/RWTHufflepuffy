# imports
import requests as req
import json


# constructor
class inspirobot(object):

    # stuff that happens on first call
    def __init__(self, config):
        self.name = "inspirobot"
        self.url = "https://inspirobot.me"
        self.config = config
        self.sessid = self.__get_session()

    # get the list of stuff from inspirobot
    def __get_flow(self):

        # we don't have an id, skip & return false
        if self.sessid == "":
            return False

        # let's try getting something
        try:
            # you know... i don't like that you treat me like an object... 
            url = f'{self.url}/api?SessionID={self.sessid}&generateFlow=1'
            response = req.get(url)

            # YOU RAISE ME UUUUUUUP 
            response.raise_for_status()
        except Exception:

            # I've had enough of this... this is just WRONG
            return False
        else:

            # all is good, return the object
            obj = json.loads(response.text)
            return obj

    # public function that gets data from inspiro and then gets the shortest quote
    def get_quote(self):

        # get a flow and init quotes array
        flow = self.__get_flow()
        data = flow["data"] if type(flow) is dict else False
        quotes = []

        # FUCK, NO. WHY DOESN'T THIS WORK???? ~ Luzi
        if not data:
            return False

        # filter output, we only want quotes, because we are racist
        for elem in data:
            if elem["type"] == "quote":
                quotes.append(elem["text"])

        # sort quotes by length and take the shortest
        quotes.sort(key=lambda elem : len(elem))
        return quotes[0].replace('\n', ' ')

    # get a session
    def __get_session(self):
        key = self.name + "_sessid"

        # is there a sessionid? generate if no or if not valid
        if key in self.config:
            if not self.__test_sessid() and not self.config[key] == "":

                # gimme key, bish
                return self.config[key]

            else:

                # sessionID invalid
                temp = self.__get_sessid()
                return temp if temp else ""
        else:

            # no key? get one and save, otherwise return FU
            temp = self.__get_sessid()
            self.config[key] = temp if temp else ""
            return temp if temp else ""

    # get a sessionid
    def __get_sessid(self):
        try:
            response = req.get(f'{self.url}/api?getSessionID=1')

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except Exception:
            return False
        else:
            sessid = response.text
            self.config[self.name + "_sessid"] = sessid
            return sessid

    def __test_sessid(self):
        try:
            # get object
            url = f'{self.url}/api?SessionID={self.sessid}&generateFlow=1'
            response = req.get(url)

            # any error?
            response.raise_for_status()
        except Exception:
            return False
        else:
            return True

def create(conf):
    return inspirobot(conf)