import discord
#import commands
#import actions

class RWTHufflepuffy(discord.Client):
    # bot logon event 
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    # message event
    async def on_message(self, message):
        # no self-replies
        if message.author == self.user:
            return
        
        if message.content.startswith('$hello'):
            author = str(message.author).split("#")
            user = discord.utils.get(message.channel.members, name = author[0], discriminator = author[1])
            await message.channel.send(f'Hello {user.mention} !')

bot = RWTHufflepuffy()
bot.run("Njc4MTg0MzMwOTY2ODU5Nzg2.XkfTLg.oxem-VXXxsRMrJmzST8lQpzl_A8")