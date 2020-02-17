import discord

async def quote_handler(bot, message):
    command = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    devRole = discord.utils.get(message.author.guild.roles, name="Developer")

    # :well at leas
    try:
        # USELESS INSPIRATION
        if command[1] == "inspirobot":
            response = await bot.inspirobot.get_quote()

        # Actual Quotes
        elif command[1] == "quotable":
            response = await bot.quotable.get_quote()

        # NOPE
        else:
            response = f"**:x: QUOTE - ACTION NOT FOUND**\nThat is not a supported API, please try one of the supported APIs. You can find out which APIs are supported by typing `$help quote`"

        # welp... somethin ain't right
        if not response:
            await message.channel.send(f"**:pencil: QUOTE - {command[1].upper()} - ERROR**\nSorry, i couldn't get a response from `{command[1]}`, better luck next time.")
        

        if command[1] == "inspirobot":
            e = discord.Embed(colour=0xff00e7)
            e.set_image(url=response)

            await message.channel.send(f"**:pencil: QUOTE - INSPIROBOT**", embed=e)
        else:
            await message.channel.send(f"**:pencil: QUOTE - {command[1].upper()}**\n```asciidoc\n===== QUOTE =====\n{response}\n```")
    except Exception as e:
        await message.channel.send(f"**:x: QUOTE - ERROR**\nHey {devRole.mention} There was an error.\n```\n{e}\n```")
