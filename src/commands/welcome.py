import discord

# handle the welcome command
async def welcome_handler(bot, message):
    command = list(filter(lambda x : x!= "" ,str(message.content).split(" ")))
    devRole = message.guild.get_role(678262267279572993)
    try:
    
        member = message.author
        server = message.author.guild
        if len(message.role_mentions) == 0 or len(command) < 3:
            response = "Oops, something went wrong. Please mention the Role and your Name.\nThe command can be used like this: `$welcome {role} {name}`"
        else:
            role = message.role_mentions[0]
            nick = command[2]
            await member.add_roles(role)
            await member.edit(nick=nick)

            response = f"Welcome to RWTHufflepuff, {member.mention}. You have now been registered as {role.mention} Student.\nHave fun."
        await message.channel.send(response)

    except Exception as e:
        await message.channel.send(f"hey {devRole.mention} There was an error.\n```\n{e}\n```")