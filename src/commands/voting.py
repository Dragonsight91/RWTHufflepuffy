import discord


async def vote_handler(message, bot):
    msg = str(message.content).split(" ")
    command = msg[0:2] + [" ".join(msg[2:])]
    #print(command)

    devRole = message.guild.get_role(678262267279572993)

    try:
        if command[1] == "create":
            vote = await vote_compile(command[2])
            msg = f'**{vote["title"]}**\n{vote["message"]}'
            #sent = await message.channel.send(msg)

            #emoji = [ await get_emoji(len(vote["options"]),x) for x in range(len(vote["options"])) ]
    except Exception as e:
        pass
        #await message.channel.send(f"hey {devRole.mention} There was an error.\n```\n{e}\n```")

# create a vote object
async def vote_compile(string:str):
    args = string.split(";")
    options = args[1].split(",")
    print(options)
    vote = {
        "title": args[0],
        "options": [],
        "message": ""
    }


    # are we in special shit territory??
    if len(options) <= 2:
        options = ["yes", "no"]
    elif len(options) > 10:
        return "Please use no more than 10 vote options."
    
    # compile vote object
    for i, elem in enumerate(options):
        option = {
            "name": elem,
            "votes": 0
        }
        vote["options"].append(option)
        vote["message"] += f":{await get_emoji(len(options), i)}: -- `{elem} `\n\n"

    return vote
# get the appropriate emoji
async def get_emoji(length:int, index:int):
    # vote types 
    yes_no = [
        "thumbsup",
        "thumbsdown"
    ]
    number = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine"
    ]

    # return correct emoji
    if length <= 2:
        return yes_no[index]
    else:
        return number[index]


def vote_create(mongo, message:str):
    pass
