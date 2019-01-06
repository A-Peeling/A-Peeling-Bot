import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random

startup_extensions = ["fun"]

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
    
@client.command(pass_context=True, brief='Responds \'Pong!\'.', description='Responds \'Pong!\', This command is used for testing the bot.')
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

@client.command(pass_context=True, brief='Guessing Game', description='Guess the Correct Number to win.')
async def guess(ctx):
    
        await client.say('Guess a number between 1 to 10')

        def guess_check(m):
            return m.content.isdigit()

        guess = await client.wait_for_message(timeout=5.0, author=ctx.message.author, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.say(fmt.format(answer))
            return
        if int(guess.content) == answer:
            await client.say('You are right!')
        else:
            await client.say('Sorry. It is actually {}.'.format(answer))

@client.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await client.say('{0.name} joined this server on {0.joined_at}'.format(member))
     
@client.command(pass_context=True, brief='Work.')
async def work(ctx):
        await client.say("Yes you can work on the bot https://github.com/A-Peeling/A-Peeling-Bot")


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))        
        
client.run(token)
