import discord

async def course_handler(bot:any, message:any):
    words = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    command = words[0:2] + " ".join(words[2:]).split(";")
    devRole = discord.utils.get(message.guild.roles, name="Developer")

    try:
        if command[1] == "add":
            if len(command) <5:
                await message.channel.send(f'**:x: COURSE - ARGUMENTS MISSING**\nPlease check the arguments you used, you have to specify all of them. do `$help course` to find out more.')
                return
            
            name = command[3].strip()
            channels = list(filter(lambda x : x != " " and x != "", command[4].split(",")))
            voice = True if command[5].strip() == "y" else False
            response = await course_add(message.guild, cp, name, channels, voice)
            
        elif command[1] == "edit":
            if len(command) <4:
                await message.channel.send(f'**:x: COURSE - ARGUMENTS MISSING**\nPlease check the arguments you used. You have to specify all of them. do `$help course` to find out more.')
                return
            name = command[2]
            channels = command[3]
            
            response =  await course_edit(message.guild, name, channels)
        await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"**:x: COURSE - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")

async def course_add(server:any, name:str, channels:list, voice:bool):
    print(channels)
    # basic stuff
    title     = f'📝 {name}'
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

    return f'**:white_check_mark: COURSE - SUCCESS**\nThe new course has been added successfully'

async def course_edit(server:any, name:str, channels:list):
    channels = channels.split(",")
    category = list(filter(lambda x: name in x.name, server.categories))

    if len(category) == 0:
        return f'**:x: COURSE - CATEGORY NOT FOUND**\nThe category `{name}`, which you tried to edit, could not be found.'

    course = category[0]
    print(course)
    for i in channels:
        channel = i.split(":")
        channelName = channel[1].strip()
        channelType = channel[0].strip()

        if channelType == "both":
            await course.create_text_channel(name=channelName.replace(" ", "-").lower())
            await course.create_voice_channel(name=channelName)
        elif channelType == "text":
            await course.create_text_channel(name=channelName.replace(" ", "-").lower())
        elif channelType == "voice":
            await course.create_voice_channel(name=channelName)

    return f'**:white_check_mark: COURSE - SUCCESS**\nThe course has been edited successfully'
