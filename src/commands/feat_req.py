import discord 

# handle the $feature command
async def handle_feat(mongo, message):
    # get command and dev role
    words = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    command = words[0:2] + [" ".join(words[2:])]
    devRole = discord.utils.get(message.guild.roles, name="Developer")

    try:
        # add feature request
        if command[1] == "add":
            # okay... really? i showed you how to use this...
            if len(command)<3 or command[2] == "":
                response = f"**:x: FEATURE - MISSING PARAMETER {{text}}**\nPlease specify the text you wish to add as feature."
            
            # gooood, you got this, buddy
            else:
                await feat_add(mongo, command[2])
                response = f"**:white_check_mark: FEATURE - ADD **\nInserted The Following into the Feature Requests:\n```asciidoc\n=== FEATURE REQUEST ===\n- {command[2]}\n```"
            await message.channel.send(response)

        # purge DB
        elif command[1] == "purge":

            # is that person a DEV?? i hope not...
            if devRole in message.author.roles:
                # purge feature request DB
                await purge_feat(mongo)
                await message.channel.send(f"**:white_check_mark: FEATURE - PURGE **\n{message.author.mention} Feature Request Database Purged.")
            
            # HAH woulda thunk ya dumbass
            else:
                await message.channel.send(f"**:no_entry: FEATURE - MISSING ROLE **\nYOU SHALL NOT PASS {message.author.mention}. \n Jokes aside, you gotta be {devRole.mention} to use that.")
        
        # well that seems quite wrong... wanna try again?
        else:
            await message.channel.send(f"**:x: FEATURE - WRONG ACTION **\n{message.author.mention} -- `{command[1]}` is not a valid action for the command `{command[0]}` ")
    
    # okay... REALLY?? ANOTHER FUCKING ERROR???
    except Exception as e:
        await message.channel.send(f"**:x: FEATURE - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")
    

# add feature request
async def feat_add(mongo, feature):
    # create a template
    dict = {
        "feature":feature
    }
    
    # UP UP AND AWAY
    col = mongo["rwthufflepuffy"]["feature-requests"]
    col.insert_one(dict)

# purge DB
async def purge_feat(mongo):
    
    # EXTERMINATEE
    col = mongo["rwthufflepuffy"]["feature-requests"]
    col.delete_many({})