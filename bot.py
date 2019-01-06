import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import sys

f = open('token.txt', 'r')
token = f.read()
f.seek(0)
f.close()

f = open('owner.txt', 'r')
ownerid = f.read()
f.seek(0)
f.close()

f = open('lastgame.txt', 'r')
argtxt = f.read()
f.seek(0)
f.close()


p = ";"
client = commands.Bot(command_prefix=p)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))    
    await client.change_presence(game=discord.Game(name=argtxt))
    
@client.command(pass_context=True, brief='Responds \'Poing!\'.', description='Responds \'Poing!\', This command is used for testing the bot.')
async def ping(ctx):
        await client.say("Pong!")
        
@client.command(pass_context=True, brief='[Owner Only] Changes the current game.', description='[Owner Only] Changes the current game.')
async def game(ctx, arg):
        if ctx.message.author.id == ownerid:
         await client.say("Setting game to " + arg)
         print('Game set to '+ arg)
         with open('lastgame.txt', 'w') as file:
          file.write(arg)
         file.close()
         await client.change_presence(game=discord.Game(name=arg))
         
client.run(token)
