# imports
import json, random, textwrap, sys, os
import services # get the services package

# global vars
cache = {}      # empty cache dict
cache_size = 200 # max amount of quotes cached 

# main function
def run():

    # get a quote from a given service
    quote = get_service().get_quote()

    # error? go to fallback cache
    if quote:
        # store quote in cache
        # if the cache isn't completely filled, just add it, otherwise replace a random quote
        if(len(cache["quote_cache"]) < cache_size):
            cache["quote_cache"].append(quote)
        else:
    
            index = random.randint(0, len(cache["quote_cache"])-1)
            cache["quote_cache"][index] = quote
    else:
        quote = get_fallback()
        
    print(quote)

    # rewrite cache
    use_cache_file(cache=cache, write=True)
    return quote


# use the cache
def use_cache_file(write=False, cache={}):
    action = "w+" if write else "r+"
    with open(f'/home/{os.getenv("USER")}/.scripts/expandable-quotes-script/cache.json', action) as f:
        if(write):
            json.dump(cache, f, indent=4)
            return True
        else:
            obj = json.load(f)
            return obj

# get one of the cached quotes 
def get_fallback():
    index = random.randint(0, len(cache["quote_cache"])-1)
    return cache["quote_cache"][index]


def get_service():
    index = random.randint(0, len(services.__all__)-1)
    return sys.modules[f'services.{services.__all__[index]}'].create(cache)


# initializer
if __name__ == "__main__":
    # initialize cache
    cache = use_cache_file(write=False)

    # start script
    run()
