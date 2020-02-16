
# handle help requests
async def help_handler(bot, message):
    msg = str(message.content).split(" ")
    command = msg[0:2]
    devRole = message.guild.get_role(678262267279572993)

    try:
        # main help
        if len(command) < 2 or command[2]=="":
            response = await help_main()
        else:
            pass
        await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"hey {devRole.mention} There was an error.\n```\n{e}\n```")

async def help_main():
    cList = [
        "- help     ::   sends this message",
        "- hello    ::   says hello to the sender",
        "- vote     ::   creates, removes or lists active votes",
        "- feature  ::   submits a feature request to the database",
        "- welcome  ::   gives the sender their study role and nick"
    ]

    comm = ""
    for i in cList:
        comm += i
    response = f"** HELP **\n This is a list of currently available commands.To use a command, write `${{command}} {{action}}` To get more information about actions, write `$help {{command}}`.\n```asciidoc\n==== COMMANDS ====\n{comm}\n```"
    

async def voting():
    pass

async def feature():
    pass