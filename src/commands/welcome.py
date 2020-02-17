import discord

# handle the welcome command
async def welcome_handler(bot, message):
    command = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    devRole = discord.utils.get(message.author.guild.roles, name="Developer")
    try:
        # get the author and server
        member = message.author
        server = message.author.guild
        admin = discord.utils.get(server.roles, name="Admin")
        
        # was the role mentioned and name given?
        if len(message.role_mentions) == 0 or len(command) < 3:
            response = "**:x: WELCOME - MISSING PARAMETERS**\nOops, something went wrong. Please @mention the Role AND your Name.\nThe command can be used like this: `$welcome {role} {name}`"
        
        # do you have that role??
        elif message.role_mentions[0] in member.roles:
            response = "**:no_entry: WELCOME - ROLE EXISTS**\nSorry, but you already have that role. If you wanted to change your role, you can use the `$role` command."
        
        # why u try again? 
        elif len(member.roles) >1 and not (admin in member.roles or devRole in member.roles):
            response = "**:x: WELCOME - ALREADY REGISTERED**\nSorry, but you have already been registered. If you wanna change your role, you can use the `$role` command."
        
        # apparently all is good
        else:
            # get role and new Nick
            role = message.role_mentions[0]
            nick = command[2]

            # add role and nick
            await member.add_roles(role)
            await member.edit(nick=nick)

            response = f"**:hibiscus: WELCOME :hibiscus:**\nWelcome to RWTHufflepuff, {member.mention}. You have now been registered as {role.mention} Student.\nHave fun."
        await message.channel.send(response)

    # an error... AGAIN... 
    except Exception as e:
        await message.channel.send(f"**:x: WELCOME - ERROR**\nHey {devRole.mention} There was an error.\n```\n{e}\n```")