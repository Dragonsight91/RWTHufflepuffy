import discord

async def role_handler(bot, message):
    command = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    devRole = discord.utils.get(message.author.guild.roles, name="Developer")

    try:
        if len(message.role_mentions) == 0 or len(command) < 3:
            response = f"**ROLE - NO ROLE MENTIONED**\nSorry, but it seems like you didn't mention the role you wanted to {command[1]}."
        # add a role
        elif command[1] == "add":
            await message.author.add_roles(message.role_mentions[0])
            response = f"**ROLE - ROLE ADDED**\n{message.author.mention}, Thou hast now been blesseth with the role of {message.role_mentions[0].mention}."
        elif command[1] == "remove":
            await message.author.remove_roles(message.role_mentions[0])
            response = f"**ROLE - ROLE REMOVED**\n{message.author.mention}, Thou hast now been demoted from the role of {message.role_mentions[0].mention} to a mere peasant."
        else:
            response = f"**ROLE - WRONG ACTION**\n{message.author.mention} -- `{command[1]}` is not a valid action for the command `{command[0]}`\n Use `$help role to get the possible actions."
        
        await message.chanel.send(response)
    except Exception as e:
        await message.channel.send(f"**ROLE - ERROR**\nHey {devRole.mention} There was an error.\n```\n{e}\n```")