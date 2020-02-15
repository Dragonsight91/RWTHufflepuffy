# imports
import discord
import pymongo
from urllib.parse import quote

# import all action handlers
import commands


class RWTHufflepuffy(discord.Client):

    # bot logon event
    async def on_ready(self):
        dbuser = "rwthufflepuffy"
        dbpass = "GwoGykaZLbFonSQZ"
        dburl = "rwthufflepuffy-wxfsh.gcp.mongodb.net/test?retryWrites=true&w=majority"
        mongoUri = f"mongodb+srv://{dbuser}:{dbpass}@{dburl}"
 
        self.mongo = pymongo.MongoClient(mongoUri, port=47410)
        print(self.mongo)
        print(f'\nLogged on as {self.user}!')

    # message event
    async def on_message(self, message):
        # no self-replies
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            author = str(message.author).split("#")

            user = discord.utils.get(
                message.channel.members, name=author[0], discriminator=author[1])
            await message.channel.send(f'Hello {user.mention} !')

        if message.content.startswith('$feature'):
            # create a mongodb connection

            print(self.mongo.list_database_names())

            # send to command handler
            await actions.feat_req.handle_feat(self.mongo, message)
            print(message.content)

        if message.content.startswith('$vote'):
            # await commands.voting.vote_handler(message, self)

        if message.content.startswith("$study"):
            pass




bot = RWTHufflepuffy()
bot.run("Njc4MTg0MzMwOTY2ODU5Nzg2.XkfTLg.oxem-VXXxsRMrJmzST8lQpzl_A8")
