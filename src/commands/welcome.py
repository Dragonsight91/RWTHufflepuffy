import discord

# handle the welcome command
async def welcome_handler(bot, message):
    msg = str(message.content).split(" ")
    command = msg[0] + [" ".join(msg[1:])]
    devRole = message.guild.get_role(678262267279572993)
    try:
        member = message.author
        server = message.author.guild
        print(message.role_mentions[0])
    except Exception as e:
        await message.channel.send(f"hey {devRole.mention} There was an error.\n```\n{e}\n```")