import discord
from . import logicsolver as logic

async def logic_handler(bot: any, message: any):
    command = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    devRole = discord.utils.get(message.guild.roles, name="Developer")

    try: 

        if command[1] == "unicode":
            expr = logic.Equation(command[2])
            table = await expr.asciiTableSolve()
            response = f"**:bar_chart: MATH - LOGIC SOLVER**\n```asciidoc\n==== LOGIC SOLVER ====\n- Expression: {expr.equation}\n{table['header']}\n\n{table['table']}\n```"
        
        elif command[1] == "ascii":
            print(command[2])
            eq = await convert(command[2])
            expr = logic.Equation(eq)
            table = await expr.asciiTableSolve()
            response = f"**:bar_chart: MATH - LOGIC SOLVER**\n```asciidoc\n==== LOGIC SOLVER ====\n- Expression: {expr.equation}\n{table['header']}\n\n{table['table']}\n```"
    
    except Exception as e:
        await message.channel.send(f"**:x: HELP - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")

async def convert(eq: str):
    list = [
        { "from" : "\\and", "to": "∧"},
        { "from" : "\\lor", "to": "∨"},
        { "from" : "\\xor", "to": "⊕"},
        { "from" : "\\imp", "to": "→"},
        { "from" : "\\equ", "to": "↔"},
        { "from" : "\\neg", "to": "¬"}
    ]
    out = eq
    for char in list:
        out = out.replace(char["from"], char["to"])
    
    print(out)
    return out