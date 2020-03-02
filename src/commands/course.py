import discord

async def course_handler(bot:any, message:any):
    words = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    command = words[0:2] + " ".join(words[2:]).split(";")
    devRole = discord.utils.get(message.guild.roles, name="Developer")

    try:
        if command[1] == "add":
            if len(command) <6:
                await message.channel.send(f'**:x: COURSE - ARGUMENTS MISSING**\nPlease check the arguments you used, you have to specify all of them. do `$help course` to find out more.')
                return

            cp = int(command[2].strip())
            name = command[3].strip()
            channels = list(filter(lambda x : x != " " and x != "", command[4].split(",")))
            voice = True if command[5].strip() == "y" else False
            await course_add(message.guild, cp, name, channels, voice)
            await message.channel.send(f'**:white_check_mark: COURSE - SUCCESS**\nThe new course has been added successfully')

    except Exception as e:
        await message.channel.send(f"**:x: COURSE - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")

async def course_add(server:any, cp:int, name:str, channels:list, voice:bool):
    print(channels)
    # basic stuff
    title     = f'{cp} CP: {name}'
    textName  = f'{name.replace(" ", "-").strip().lower()}'
    voiceName = f'{name}'

    # create category
    category = await server.create_category(title)
    await category.edit(position=category.position-2)
    
    text = await server.create_text_channel(textName, category=category)
    if voice:
        voice = await server.create_voice_channel(voiceName, category=category)
    
    for channel in channels:
        name = channel.strip().replace(" ", "-").lower()
        await server.create_text_channel(name, category=category)

