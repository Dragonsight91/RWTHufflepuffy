# imports
import discord
import pymongo
from urllib.parse import quote

# import all action handlers
import actions

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
    
        if message.content.startswith('$feature'):
            # create a mongodb connection
            dbuser = "hufflepuffy"
            dbpass = "XP!1NNF$^AZzXyKHGZmfvMghBg$BTK9d3TsYa17f#@yhlkwKfHcHBp&qX2fPG^#Y%6EHRdH5Oig#YX^XVWpPoN$L%Fvc28iWvJr"
            dburl = "ds247410.mlab.com/heroku_0mjbn9cl"
            mongoUri = quote(f"{dbuser}\:{dbpass}@{dburl}", safe='')
            mongo = pymongo.MongoClient(mongoUri, port=47410)
            print(mongo.list_database_names())

            # send to command handler
            await actions.feat_req.handle_feat(None, message)
            print(message.content)

        if message.content.startswith("$study"):
            pass

bot = RWTHufflepuffy()
bot.run("Njc4MTg0MzMwOTY2ODU5Nzg2.XkfTLg.oxem-VXXxsRMrJmzST8lQpzl_A8")