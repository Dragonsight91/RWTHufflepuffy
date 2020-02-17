# external imports
import discord
import pymongo
import re
from urllib.parse import quote
import os

# import all internal things
import commands
import extra

# The Bot
class RWTHufflepuffy(discord.Client):

    # bot logon event
    async def on_ready(self):

        # get all variables and create DB connection
        dbuser = os.environ["MONGO_USER"]
        dbpass = os.environ["MONGO_PASS"]
        dburl = os.environ["MONGO_URL"]
        mongoUri = f"mongodb+srv://{dbuser}:{dbpass}@{dburl}"
        
        # save all necessary things in the bot
        self.votes = []
        self.mongo = pymongo.MongoClient(mongoUri, port=47410)
        self.inspirobot = extra.inspirobot.inspirobot()
        self.quotable = extra.quotable.quotable()

        # change bot's status
        await self.change_presence(activity=discord.Game(name='with fire'))


    # reaction added to message
    async def on_reaction_add(self, reaction, user):

        # no reacting to own reactions, that'd create WEIRD loops
        if user == self.user:
            return

        # is it a vote, get the title
        title = re.compile("\*\*(.*)\*\*")
        result = list(filter(lambda vote: vote[1]['title'] == title.findall(reaction.message.content)[1] and vote[1]["active"], enumerate(self.votes)))
        
        # well it's not a vote
        if result == None:
            return 

        # OH it's a vote, change the vote count
        elif len(result)>0:
            await commands.voting.vote_edit(bot, reaction, result[0][0], True)

    
    # reaction removed from message
    async def on_reaction_remove(self, reaction, user):
        
        # no reacting to own reactions
        if user == self.user:
            return

        # find the vote
        title = re.compile("\*\*(.*)\*\*")
        result = list(filter(lambda vote: vote[1]['title'] == title.findall(reaction.message.content)[1] and vote[1]["active"], enumerate(self.votes)))

        # NOT A VOTE, let#s do something else
        if result == None:
            return 

        # it's a vote, alright
        elif len(result)>0:
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

        # handle the $vote command
        elif message.content.startswith('$vote'):
            await commands.voting.vote_handler(self, message)

        # handle $welcome command (initial join)
        elif message.content.startswith("$welcome"):
            await commands.welcome.welcome_handler(self, message)

        # handle $role command
        elif message.content.startswith("$role"):
            await commands.role.role_handler(self, message)

        # handle the $help command
        elif message.content.startswith("$help"):
            await commands.help.help_handler(bot, message)

        # handle the $quote command
        elif message.content.startswith("$quote"):
            await commands.quote.quote_handler(bot, message)

        # handle teh $nick command
        elif message.content.startswith("$nick"):
            await commands.nick.nick_handler(bot, message)

# START DAT SHIT
bot = RWTHufflepuffy()
bot.run(os.environ['DISCORD_KEY'])
