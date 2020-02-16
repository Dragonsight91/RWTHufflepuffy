# imports
import discord
import pymongo
import re
from urllib.parse import quote
import os

# import all action handlers
import commands


class RWTHufflepuffy(discord.Client):

    # bot logon event
    async def on_ready(self):
        dbuser = os.environ["MONGO_USER"]
        dbpass = os.environ["MONGO_PASS"]
        dburl = os.environ["MONGO_URL"]
        mongoUri = f"mongodb+srv://{dbuser}:{dbpass}@{dburl}"
        
        self.votes = []
        self.mongo = pymongo.MongoClient(mongoUri, port=47410)

        await self.change_presence(activity=discord.Game(name='with fire'))
        print(self.mongo)
        print(f'\nLogged on as {self.user}!')


    # reaction added to message
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
            await commands.voting.vote_edit(bot, reaction, result[0][0], True)

    
    # reaction removed from message
    async def on_reaction_remove(self, reaction, user):
        # no reacting to own reactions
        if user == self.user:
            return
        # find the vote
        title = re.compile("\*\*(.*)\*\*")
        result = list(filter(lambda vote: vote[1]['title'] == title.search(reaction.message.content).group(1) and vote[1]["active"], enumerate(self.votes)))

        # use vote, or return on None
        if result == None:
            return 
        if len(result)>0:
            print("adding vote")
            await commands.voting.vote_edit(bot, reaction, result[0][0], False)

    # message event
    async def on_message(self, message):
        # no self-replies
        if message.author == self.user:
            return

        # handle the $hello command
        if message.content.startswith('$hello'):
            await message.channel.send(f'Hello {message.author.mention} !')

        # handle the $feature command
        elif message.content.startswith('$feature'):
            # send to command handler
            await commands.feat_req.handle_feat(self.mongo, message)
            print(message.content)

        # handle the $vote command
        elif message.content.startswith('$vote'):
            await commands.voting.vote_handler(message, self)

        # handle $study command
        elif message.content.startswith("$welcome"):
            await commands.welcome.welcome_handler(bot, message)

        # handle the $help command
        elif message.content.startswith("$help"):
            await commands.help.help_handler(bot, message)




bot = RWTHufflepuffy()
bot.run(os.environ['DISCORD_KEY'])
