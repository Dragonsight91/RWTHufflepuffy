# handle help requests
async def help_handler(bot, message):
    msg = str(message.content).split(" ")
    command = msg[0:2]
    devRole = message.guild.get_role(678262267279572993)

    try:
        # main help
        if len(command) < 2 or command[1]=="":
            response = await help_main()
        else:
            if command[1] == "vote":
                response = await voting()
            elif command[1] == "feature":
                response = await feature()
            elif command[1] == "welcome":
                response = await welcome()
            else:
                response = "**:x: HELP - NONEXISTENT COMMAND **\n THAT is not a command currently supported.\n You can add a request with `$feature add {text}` or list the available commands with `$help`"
        await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"**:x: HELP - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")


# main help
async def help_main():
    cList = [
        "- help     ::   sends this message",
        "- hello    ::   says hello to the sender (has no special action)",
        "- vote     ::   creates, removes or lists active votes",
        "- feature  ::   submits a feature request to the database",
        "- welcome  ::   gives the sender their study role and nickname"
    ]

    comm = ""
    for i in cList:
        comm += i + "\n"
    response = f"**:grey_question: HELP**\nThis is a list of currently available commands.\nTo use a command, write `${{command}} {{action}} {{arguments}}`.\nTo get more information about actions and their arguments, write `$help {{command}}`.\n```asciidoc\n==== COMMANDS ====\n{comm}\n```"
    
    return response


# help for vote command
async def voting():
    alist = [
        "- list                       :: list all currently active votes",
        "- create {name};{options}    :: creates a vote  with name {name} and all options separated by comma",
        "- end {name}                 :: removes the active quote with name {name}"
    ]
    comm = ""
    for i in alist:
        comm += i + "\n"
    response = f"**:grey_question: HELP    --    vote **\nThis is a list of actions and their parameters. To use them, write `$vote {{action}} {{arguments}}`.\n```asciidoc\n{comm}\n```"
    return response


# help for feature command
async def feature():
    alist = [
        "- add {text}     :: add {text} as feature request to DB",
        "- purge          :: purge the feature request DB (@Developer Role only)",
    ]
    comm = ""
    for i in alist:
        comm += i + "\n"
    response = f"**:grey_question: HELP    --    feature **\nThis is a list of actions and their parameters. To use them, write `$feature {{action}} {{arguments}}`.\n```asciidoc\n{comm}\n```"
    return response

async def welcome():
    response = f"**:grey_question: HELP    --    welcome **\n The welcome command can be used like this:\n```asciidoc\n==== USAGE ====\n$welcome {{role_mention}} {{name}}\n- role_mention @mentions the role fitting to your study\n- name is the name or nickname you want to be called\n```"
    return response