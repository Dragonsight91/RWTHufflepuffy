import discord 

# handle the $feature command
async def handle_feat(mongo, message):
    words = str(message.content).split(" ")
    action = words[0:2] + [" ".join(words[2:])]
    devRole = message.guild.get_role(678262267279572993)
    print(message.author.roles)
    print(devRole)
    try:
        # add feature request
        if action[1] == "add":
            await feat_add(mongo, action[2])
            # send a response
            response = f"**Inserted The Following into the Feature Requests:**\n```asciidoc\n=== FEATURE REQUEST ===\n- {action[2]}\n```"
            await message.channel.send(response)

        # purge DB
        elif action[1] == "purge":
            # is that person a DEV??
            if devRole in message.author.roles:
                # purge feature request DB
                await purge_feat(mongo)
                await message.channel.send(f"{message.author.mention} Feature Request Database Purged.")
            else:
                # nice try, better luck next time
                await message.channel.send(f"YOU SHALL NOT PASS {message.author.mention}. \n Jokes aside, you gotta be {devRole.mention} to use that.")
   
    except Exception as e:
        print(e)
        await message.channel.send(f"hey {devRole.mention} There was an error.\n```\n{e}\n```")
    else:
        print(action)
    

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