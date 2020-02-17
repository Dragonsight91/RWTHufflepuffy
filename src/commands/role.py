import discord

async def role_handler(bot, message):
    # get the commands and dev role
    command = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    devRole = discord.utils.get(message.author.guild.roles, name="Developer")

    try:
        admin = discord.utils.get(message.channel.guild.roles, name="Admin")
        # oh come on, you should specify a role
        if len(message.role_mentions) == 0 or len(command) < 3:
            response = f"**:x: ROLE - NO ROLE MENTIONED**\nSorry, but it seems like you didn't mention the role you wanted to {command[1]}."
        
        # add a role
        elif command[1] == "add":
            # you have the high ground...
            if admin in message.role_mentions or devRole in message.role_mentions:
                response = f"**:x: ROLE - NOT PERMITTED**\nYou cannot give yourself the {admin.mention} or the {devRole.mention} Roles."
            
            # DON'T UNDERESTIMATE MY POWER
            else:
                await message.author.add_roles(message.role_mentions[0])
                response = f"**:white_check_mark: ROLE - ROLE ADDED**\n{message.author.mention}, Thou hast now been blesseth with the role of {message.role_mentions[0].mention}."

        # remove a role
        elif command[1] == "remove":
            # you have the high ground...
            if admin in message.role_mentions or devRole in message.role_mentions:
                response = f"**:x: ROLE - NOT PERMITTED**\nYou cannot remove the {admin.mention} or the {devRole.mention} Roles from yourself."
            
            # I've got the power
            else:
                await message.author.remove_roles(message.role_mentions[0])
                response = f"**:white_check_mark: ROLE - ROLE REMOVED**\n{message.author.mention}, Thou hast now been demoted from the role of {message.role_mentions[0].mention} to a mere peasant."
       
        # invalid action
        else:
            # WRONG
            response = f"**:x: ROLE - WRONG ACTION**\n{message.author.mention} -- `{command[1]}` is not a valid action for the command `{command[0]}`\n Use `$help role to get the possible actions."
        
        await message.channel.send(response)
    
    # huston, we have a problem
    except Exception as e:
        await message.channel.send(f"**:x: ROLE - ERROR**\nHey {devRole.mention} There was an error.\n```\n{e}\n```")