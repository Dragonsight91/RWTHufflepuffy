import discord
import re


async def vote_handler(message, bot):
    msg = str(message.content).split(" ")
    command = msg[0:2] + [" ".join(msg[2:])]
    print(command)

    devRole = message.guild.get_role(678262267279572993)
    pattern = re.compile("\:(.*)\:")

    try:
        if command[1] == "create":
            # create vote entry
            vote = await vote_compile(command[2], message.id)
            await vote_add(vote)

            msg = f'**{vote["title"]}**\n{vote["message"]}'
            sent = await message.channel.send(msg)
            for i in range(len(vote["options"])):
                emoji = await get_emoji(len(vote["options"]), i)
                await sent.add_reaction(emoji["emoji"])
        elif command[1] == "end":
            pass
        else:
            await message.channel.send(f"{message.author.mention} -- `{command[1]}` is not a valid action for the command `{command[0]}` ")
    except Exception as e:
        await message.channel.send(f"hey {devRole.mention} There was an error.\n```\n{e}\n```")

# create a vote dict
async def vote_compile(string: str):
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
    elif len(options) > 11:
        return "Please use no more than 10 vote options."

    # compile vote object
    for i, elem in enumerate(options):
        option = {
            "name": elem,
            "votes": 0
        }
        emoji = await get_emoji(len(options), i)
        vote["options"].append(option)
        vote["message"] += f"{emoji['name']} -- `{elem} `\n\n"

    return vote
# get the appropriate emoji


async def get_emoji(length: int, index: int):
    # vote types
    yes_no = [
        {"name": ":thumbsup:", "emoji": "👍"},
        {"name": ":thumbsdown:", "emoji": "👎"}
    ]
    number = [
        {"name": ":zero:", "emoji": "0️⃣"},
        {"name": ":one:", "emoji": "1️⃣"},
        {"name": ":two:", "emoji": "2️⃣"},
        {"name": ":three:", "emoji": "3️⃣"},
        {"name": ":four:", "emoji": "4️⃣"},
        {"name": ":five:", "emoji": "5️⃣"},
        {"name": ":six:", "emoji": "6️⃣"},
        {"name": ":seven:", "emoji": "7️⃣"},
        {"name": ":eight:", "emoji": "8️⃣"},
        {"name": ":nine:", "emoji": "9️⃣"},
        {"name": ":ten:", "emoji": "🔟"}
    ]

    # return correct emoji
    if length <= 2:
        return yes_no[index]
    else:
        return number[index]

async def vote_add(mongo, feature):
    print(feature)
    dict = {
        "feature":feature
    }
    print(dict)
    col = mongo["rwthufflepuffy"]["feature-requests"]
    col.insert_one(dict)

def vote_create(bot, message: str):
    pass
