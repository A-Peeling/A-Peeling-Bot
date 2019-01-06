import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import sys

ownerid = "DiscordIdHere"
p = ";"
client = commands.Bot(command_prefix=p)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))    
    
@client.command(pass_context=True, brief='Responds \'Poing!\'.', description='Responds \'Poing!\', This command is used for testing the bot.')
async def ping(ctx):
        description('Says Pong')
        await client.say("Pong!")
        
@client.command(pass_context=True, brief='[Owner Only] Changes the current game.', description='[Owner Only] Changes the current game.')
async def game(ctx, arg):
        if ctx.message.author.id == ownerid:
         await client.change_presence(game=discord.Game(name=arg))
         await client.say("Setting game to " + arg)
  
      
client.run('TokenHere')
