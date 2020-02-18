# global
import discord

# internal
from . import ieee745
from . import permutations
from . import convert_binary as conv_bin


async def math_handler(bot:any, message:any):
    command = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    devRole = discord.utils.get(message.guild.roles, name="Developer")

    try:
        
        if command[1] == "bin":
            num = int(command[3])

            if num <0:
                response ="**:x: MATH - INVALID NUMBER**\nThis Module does not currently support negative numbers, please input positive integers."
            elif num % 1 != 0:
                response = "**:x: MATH - INVALID NUMBER**\nThis module does not support floating point numbers. Please use the `ieee745` Module for that."

            bin = conv_bin.conv_Bin(num)
            response = f"**:bar_chart: MATH - BIN**\n```asciidoc\n==== BINARY CONVERSION ====\nYour Input: num\nThe Output:{bin}\n```"
        
        elif command[1] == "dec":
            pass

        elif command[1] == "ieee745":
            pass

        elif command[1] == "permutations":
            pass

    except Exception as e:
        await message.channel.send(f"**:x: MATH - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")

