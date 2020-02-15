import discord

def vote_handler(mongo, message):
    msg = str(message.content).split(" ")
    command = 