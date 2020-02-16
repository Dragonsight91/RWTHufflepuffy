# imports
import discord
import pymongo
import re
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
        
        self.votes = []
        self.mongo = pymongo.MongoClient(mongoUri, port=47410)

        print(self.mongo)
        print(f'\nLogged on as {self.user}!')

    async def on_reaction_add(self, reaction, user):
        # no reacting to own reactions
        if user == self.user:
            return

        title = re.compile("\*\*(.*)\*\*")
        result = list(filter(lambda vote: vote[1]['title'] == title.search(reaction.message.content).group(1) and vote[1]["active"], enumerate(self.votes)))
        if result == None:
            return 

        if len(result)>0:
            print("adding vote")
            await commands.voting.vote_add(bot, reaction, result[0][0])
    async def on_reaction_remove(self, reaction, user):
        # no reacting to own reactions
        if user == self.user:
            return

        title = re.compile("\*\*(.*)\*\*")
        result = list(filter(lambda vote: vote[1]['title'] == title.search(reaction.message.content).group(1) and vote[1]["active"], enumerate(self.votes)))
        if result == None:
            return 

        if len(result)>0:
            print("adding vote")
            await commands.voting.vote_remove(bot, reaction, result[0][0])

    # message event
    async def on_message(self, message):
        # no self-replies
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send(f'Hello {message.author.mention} !')

        if message.content.startswith('$feature'):
            # send to command handler
            await commands.feat_req.handle_feat(self.mongo, message)
            print(message.content)

        if message.content.startswith('$vote'):
            await commands.voting.vote_handler(message, self)

        if message.content.startswith("$study"):
            pass




bot = RWTHufflepuffy()
bot.run("Njc4MTg0MzMwOTY2ODU5Nzg2.XkfTLg.oxem-VXXxsRMrJmzST8lQpzl_A8")
