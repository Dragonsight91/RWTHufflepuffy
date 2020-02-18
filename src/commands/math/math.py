# global
import discord
import re

# internal
from . import ieee745
from . import permutations
from . import convert_binary as conv_bin


async def math_handler(bot:any, message:any):
    command = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    devRole = discord.utils.get(message.guild.roles, name="Developer")

    try:
        
        if command[1] == "bin":
            num = int(command[2])
            print(num)
            if num <0:
                response ="**:x: MATH - INVALID NUMBER**\nThis Module does not currently support negative numbers, please input positive integers."
            elif num % 1 != 0:
                response = "**:x: MATH - INVALID NUMBER**\nThis module does not support floating point numbers. Please use the `ieee745` Module for that."

            out = await conv_bin.conv_Bin(num)
            print(out)
            response = f"**:bar_chart: MATH - BIN**\n```asciidoc\n==== DEC TO BIN CONVERSION ====\nYour Input: {num}\nThe Output: {out}\n```"
        
        elif command[1] == "dec":
            num = re.compile("[2-9]|\D")
            if num.match(command[2]):
                await message.channel.send("**:x: MATH - DECIMAL NUMBER OR CHARACTER FOUND**\nPlease do not input any decimal numbeers or characterw, this is for converting binary numbers only.")
                return

            out = await conv_bin.conv_Dec(command[2])
            response = f"**:bar_chart: MATH - DEC**\n```asciidoc\n==== BIN TO DEC CONVERSION ====\nYour Input: {command[2]}\nThe Output: {out}\n```"

        elif command[1] == "tofloat":
            num = float(command[2])
            out = await ieee745.convert(num)

            response = f"**:bar_chart: MATH - TOFLOAT**\n```asciidoc\n==== IEEE745 FLOAT TO BIN ====\nYour Input: {num}\nGenerated output:\n- Float32: {out['float32']}\n- Float64: {out['float64']}\n```"
        
        elif command[1] == "permutations":
            out = await permutations.get_permutations(command[2])
            groups = ""
            for i in out["groups"].keys():
                groups += f"    - Group Name: {i}      Count: {out['groups'][i]}\n"
            response = f"**:bar_chart: MATH - PERMUTATIONS**\n```asciidoc\n==== PERMUTATION CALCULATION ====\nYour Input: {command[2]}\nPermutations: {out['perms']}\nGroups:\n{groups}"

        await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"**:x: MATH - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")

