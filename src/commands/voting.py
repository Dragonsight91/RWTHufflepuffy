import discord
import re

# handle all voting command stuff


async def vote_handler(bot: any, message: any):
    msg = str(message.content).split(" ")
    command = msg[0:2] + [" ".join(msg[2:])]
    print(command)

    devRole = discord.utils.get(message.guild.roles, name="Developer")
    pattern = re.compile("\:(.*)\:")

    try:
        # create vote
        if command[1] == "create":
            # is there a vote with that title?
            result = list(filter(lambda vote: vote[1]['title'] == command[2] and vote[1]["active"], enumerate(bot.votes)))
            if len(result) >= 1:
                await message.channel.send(f"**:x: VOTE - EXISTS**\n{message.author.mention} That Title has already been used in an active vote, please use another title or ende the old vote.")
            await vote_create(bot, message, command)
            
        # get a list of all ongoing votes
        elif command [1] == "list":
            # create list of ongoing votes
            ongoing = list(filter(lambda vote: vote["active"], bot.votes))
            votelist = ""
            for i in ongoing:
                votelist += f"- {i['title']}\n"

            # no active votes
            if len(ongoing) == 0:
                response = f"**:x: VOTE - NONE FOUND**\nThere are no active votes"
            # list active votes
            else:
                response = f"\n**:x: VOTE - ONGOING**\n```asciidoc\n==== ONGOING VOTES ====\n{votelist}\n```"
            await message.channel.send(response)
        # end vote
        elif command[1] == "end":
            # try to get the vote to end
            result = list(filter(
                lambda vote: vote[1]['title'] == command[2] and vote[1]["active"], enumerate(bot.votes)))

            # there are no ongoing votes
            if result == None or len(result) <= 0:

                # create list of ongoing votes
                ongoing = list(filter(lambda vote: vote["active"], bot.votes))
                votelist = ""
                for i in ongoing:
                    votelist += f"- {i['title']}\n"

                # no active votes
                if len(ongoing) == 0:
                    response = f"**:x: VOTE - NONE FOUND**\nThere are no active votes"
                # list active votes
                else:
                    response = f"**:x: VOTE - NOT FOUND**\nThat Doesn't seem to be a vote, here's a list of currently ongoing votes\n```asciidoc\n{votelist}\n```"
                await message.channel.send(response)

            # there is a matching vote, get results and end it
            if len(result) > 0:
                response = await vote_end(bot, result[0][0])
                await message.channel.send(response)

        # wrong action
        else:
            await message.channel.send(f"**:x: VOTE - WRONG ACTION**\n{message.author.mention} -- `{command[1]}` is not a valid action for the command `{command[0]}` ")
    except Exception as e:
        await message.channel.send(f"**:x: VOTE**\nHey {devRole.mention} There was an error.\n```\n{e}\n```")


# create vote
async def vote_create(bot: any, message: any, command: list):
    # create vote entry
    vote = await vote_compile(command[2])

    # ERROR
    if vote == 1:
        await message.channel.send("**:x: VOTE - NOT ENOUGH OPTIONS**\nVote is invalid, please give at least two options.")
        return
    elif vote ==2:
        await message.channel.send("**:x: VOTE - TOO MANY OPTIONS**\nVote is invalid, please use no more than 11 options.")
        return
    
    msg = f'**:ballot_bot: VOTE STARTED BY {message.autho.mention}**\n**{vote["title"]}**\n{vote["message"]}'
    sent = await message.channel.send(msg)
    vote["discMsg"] = sent
    bot.votes.append(vote)

    # add all response options to vote
    for i in range(len(vote["options"])):
        emoji = await get_emoji(len(vote["options"]), i)
        await sent.add_reaction(emoji["emoji"])


# edit user vote
async def vote_edit(bot: any, reaction: any, voteIdx: int, mode:bool):
    index = await emoji_to_id(reaction.emoji)
    if index == None:
        return
    message = reaction.message.content

    # add or remove vote
    if mode:
        bot.votes[voteIdx]["options"][index]["votes"] += 1
    else:
        bot.votes[voteIdx]["options"][index]["votes"] -= 1

    print(bot.votes[voteIdx])


# end vote
async def vote_end(bot: any, voteIdx: int):
    # get results and deactivate vote
    results = bot.votes[voteIdx]["options"]
    bot.votes[voteIdx]["active"] = False

    # calculate amount of votes
    total = 0
    for x in results:
        total += x["votes"]
    print(total)

    # create the response message
    message = f"**:no_entry: VOTE ENDED -- VOTES RECEIVED: {total}**\n```asciidoc\n==== RESULTS ====\n{bot.votes[voteIdx]['title']}\n"
    for i in results:
        if total <= 0 or i["votes"] <= 0:
            percent = 0
        else:
            percent = round((100/total) * i["votes"], 2)
        message += f"[{percent}%] {i['name']} --- Received {i['votes']} votes\n"

    message += "```"
    return message


# create a vote dict
async def vote_compile(string: str):
    # split the strings
    args = string.split(";")
    options = args[1].split(",")

    # vote dict template
    vote = {
        "title": args[0],
        "options": [],
        "message": "",
        "active": True
    }

    # are we in special shit territory??
    if len(options) < 2:
        return 1
    elif len(options) > 11:
        return 2

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


# get the appropriate emoji for the id
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

# get the id of an emoji


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
    try:
        return emoji_dict[emoji]
    except Exception:
        return None