import discord 

# handle the $feature command
async def handle_feat(mongo, message):
    words = str(message.content).split(" ")
    command = words[0:2] + [" ".join(words[2:])]
    devRole = discord.utils.get(message.guild.roles, name="Developer")

    try:
        # add feature request
        if command[1] == "add":
            if len(command)<3 or command[2] == "":
                response = f"**:x: FEATURE - MISSING PARAMETER {{text}}**\nPlease specify the text you wish to add as feature."
            else:
                await feat_add(mongo, command[2])
                # send a response
                response = f"**FEATURE - ADD **\nInserted The Following into the Feature Requests:\n```asciidoc\n=== FEATURE REQUEST ===\n- {command[2]}\n```"
            await message.channel.send(response)

        # purge DB
        elif command[1] == "purge":
            # is that person a DEV??
            if devRole in message.author.roles:
                # purge feature request DB
                await purge_feat(mongo)
                await message.channel.send(f"**FEATURE - PURGE **\n{message.author.mention} Feature Request Database Purged.")
            else:
                # nice try, better luck next time
                await message.channel.send(f"**:x: FEATURE - MISSING ROLE **\nYOU SHALL NOT PASS {message.author.mention}. \n Jokes aside, you gotta be {devRole.mention} to use that.")
        else:
            await message.channel.send(f"**:x: FEATURE - WRONG ACTION **\n{message.author.mention} -- `{command[1]}` is not a valid action for the command `{command[0]}` ")
    except Exception as e:
        print(e)
        await message.channel.send(f"**:x: FEATURE - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")
    

# add feature request
async def feat_add(mongo, feature):
    print(feature)
    dict = {
        "feature":feature
    }
    print(dict)
    col = mongo["rwthufflepuffy"]["feature-requests"]
    col.insert_one(dict)

# purge DB
async def purge_feat(mongo):
    col = mongo["rwthufflepuffy"]["feature-requests"]
    col.delete_many({})