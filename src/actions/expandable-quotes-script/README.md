# The Expandable Quotes Script
What in all heavens is this? Well, it's a Script that takes a package of services, which get data from an API that delivers random quotes and selects a random API service, to get a quote from.
## How to install
Installation is quite easy, here's how:
1. Clone this repo into `~/.scripts`
    ```bash
    mkdir ~/.scripts # create .scripts (only needed if it doesn't exist)
    cd ~/.scripts
    git clone https://github.com/Dragonsight91/expandable-quotes-script
    ```
2. **(optional)** to use it with my lockscreen *(you can find that in my [dotfiles repo](https://github.com/Dragonsight91/dotfiles))*, add a script named `get_quotes` in `~/.local/bin` like this:

    ```bash
    # move to directory
    cd ~/.local/bin

    # create file
    touch get_quotes

    # write to file
    echo "python3 ~/.scripts/expandable-quotes-script/main.py" >> get_quotes
    ```
    Also make sure that `~/.local/bin` is in your PATH. ( do `echo $PATH` and look for `/home/yourname/.local/bin`)
    if it's not, add this to your `~/.xprofile`
    
    ```bash
    export PATH=/home/$USER/.local/bin:$PATH
    ``` 
## Why Expandable?
Well you never have to care about `main.py`, it automatically knows what packages exist without you having to change the code. All one would have to to to expand it is to follow the following instructions:

## How to expand
The key to the expandability is module standardizytion. Each module has the same input and output, no matter what. Here are the rules:

1. Create a file `services/name_of_your_service.py`, replacing "name_of_your_service" with the name of the api, eg. `inspirobot.py`.
2. inside that file create a class that follows this pattern:
    ```python
    # our service class
    class name_of_your_service(object):

        # needed to create the service object
        def __init__(self, config):
            self.name = "name_of_your_service"
            self.url = "url_of_your_service"
            self.config = config
            # if your service has 
            # session key or api-key handling
            # add your key inside cache.json

        # main calls this method when it chose this service to get the quote
        def get_quote(self):
            
            try:
                quote = "some quote from your service" # get your quote from somewhere
            except Exception:
                # we had an error, tell main to use cache
                return False
            else:
                # all is good, return our quote
                return quote

    # main.py calls this to initialize the service
    # IMPORTANT: THIS IS NOT INSIDE THE CLASS
    def create(config):
        return name_of_your_service(config)
    ```
    These three methods are REQUIRED, otherwise `main.py` has no idea what to do with it.

3. ALWAYS return `False` if there is an error, that way you still get a quote from the cache.

4. Add your modules in `services/__init__.py` like this:
    ```python
    from .inspirobot import inspirobot
    from .name_of_your_service import .name_of_your_service
    __all__ = ["inspirobot.py", "name_of_your_service"]
    ```

