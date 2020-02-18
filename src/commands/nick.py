import discord


async def nick_handler(bot, message):
    words = list(filter(lambda x : x != "" ,str(message.content).split(" ")))
    command = words[0:2] + [" ".join(words[2:])]
    devRole = discord.utils.get(message.guild.roles, name="Developer")
    adminRole = discord.utils.get(message.guild.roles, name="Admin")   

    # okay, let's try our best
    try:

        # i humbly bow to you, my lord/lady
        if devRole in message.author.roles or adminRole in message.author.roles or message.author == message.channel.guild.owner:
            await message.channel.send(f"**:no_entry: NICK - ADMIN/DEV ROLE DETECTED**\nSorry, but due to discord's role hierarchy, i cannot change the nick of someone with the roles {devRole.mention}, {adminRole.mention} or the person that is the Server Owner.\nSorry, guys, but y'all have the high ground.")
            return        
        
        # seems alright
        elif command[1] == "set":

            # not judging, but yain't no nobody, hun
            if len(command) < 3:
                await message.channel.send(f"**:x: NICK - NO NICK**\nPlease specify a nickname you want to use. The usage of this command is: `$nick set {{nick}}`")
                return

            # IT'S TOO LONG DADDY
            elif len(command[2]) >32:
                await message.channel.send(f"*:x: NICK - TOO LONG**\nPlease use no more than 32 characters for your desired nickname. Sorry, this one's on Discord.")
            
            # who is this weird dude called Nick
            nick = command[2]
            await message.author.edit(nick=nick)
            await message.channel.send(f"**:white_check_mark: NICK - SUCCESS**\nHey {message.author.mention} your nick has now been set to `{nick}`")

        # you wanna do WHAT??
        else:
            await message.channel.send(f"**:x: NICK - ACTION UNSUPPORTED**\nSorry, that's not an action this command currently supports. To get a list of supported actions, write `$help nick`")
    
    # AND WE FAILED.... GREAT... FUCKING IDIOT SANDWICH
    except Exception as e:
        await message.channel.send(f"**:x: NICK - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")