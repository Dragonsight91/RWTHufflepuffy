import discord
import re

# handle all voting command stuff


async def vote_handler(message, bot):
    msg = str(message.content).split(" ")
    command = msg[0:2] + [" ".join(msg[2:])]
    print(command)

    devRole = message.guild.get_role(678262267279572993)
    pattern = re.compile("\:(.*)\:")

    try:
        if command[1] == "create":
            await vote_create(bot, message, command)
            
        elif command[1] == "end":
            result = list(filter(lambda vote: vote[1]['title'] == command[2] and vote[1]["active"], enumerate(bot.votes)))
            print(result)

            if result == None or len(result) <= 0:
                ongoing = list(filter(lambda vote: vote["active"], bot.votes))
                
                votelist = ""
                for i in ongoing:
                    votelist += f"- {i['title']}\n"
                if len(ongoing) == 0:
                    response = f"There are no active votes"
                else:
                    response = f"That Doesn't seem to be a vote, here's a list of currently ongoing votes\n```asciidoc\n{votelist}\n```"
                await message.channel.send(response) 

            if len(result)>0:
                print("getting results")
                response = await vote_end(bot, result[0][0])
                await message.channel.send(response)
        else:
            await message.channel.send(f"{message.author.mention} -- `{command[1]}` is not a valid action for the command `{command[0]}` ")
    except Exception as e:
        await message.channel.send(f"hey {devRole.mention} There was an error.\n```\n{e}\n```")


# put vote into DB
async def vote_create(bot, message, command):
    # create vote entry
    vote = await vote_compile(command[2], message)

    msg = f'**{vote["title"]}**\n{vote["message"]}'
    sent = await message.channel.send(msg)
    vote["discMsg"] = sent
    bot.votes.append(vote)

    for i in range(len(vote["options"])):
        emoji = await get_emoji(len(vote["options"]), i)
        await sent.add_reaction(emoji["emoji"])


async def vote_add(bot, reaction, voteIdx):
    index = await emoji_to_id(reaction.emoji)
    message = reaction.message.content
    bot.votes[voteIdx]["options"][index]["votes"] += 1
    
    print(bot.votes[voteIdx])

async def vote_remove(bot, reaction, voteIdx):
    index = await emoji_to_id(reaction.emoji)
    message = reaction.message.content
    bot.votes[voteIdx]["options"][index]["votes"] -= 1
    
    print(bot.votes[voteIdx])

async def vote_end(bot, voteIdx):
    results = bot.votes[voteIdx]["options"]
    bot.votes[voteIdx]["active"] = False
    total = 0
    for x in results:
        total += x["votes"]
    print(total)

    message = f"**VOTE ENDED -- Total Votes: {total}**\n ```asciidoc\n==== RESULTS ====\n{bot.votes[voteIdx]['title']}\n"
    for i in results:
        if total <= 0 or i["votes"] <= 0:
            percent = 0
        else:
            percent = round((100/total) * i["votes"], 2)
        message += f"[{percent}%] {i['name']} --- Received {i['votes']} votes\n"

    message += "```"
    return message

# create a vote dict
async def vote_compile(string: str, msg):
    args = string.split(";")
    options = args[1].split(",")
    print(options)
    vote = {
        "title": args[0],
        "options": [],
        "message": "",
        "active": True,
        "discMsg":msg
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
        vote["message"] += f"{emoji['name']}` -- {elem}`\n\n"

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


async def emoji_to_id(emoji: str):
    emoji_dict = {
        # thumbsup/thumbsdown
        "👍": 0,
        "👎": 1,

        # numeric
        "0️⃣": 0,
        "1️⃣": 1,
        "2️⃣": 2,
        "3️⃣": 3,
        "4️⃣": 4,
        "5️⃣": 5,
        "6️⃣": 6,
        "7️⃣": 7,
        "8️⃣": 8,
        "9️⃣": 9,
        "🔟": 10
    }
    return emoji_dict[emoji]
