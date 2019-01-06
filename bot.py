import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random

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

@client.command(pass_context=True, brief='It\'s just a 8ball.')
async def magicball(ctx, *arg):
    if not arg:
        await client.say('You need to supply a question')
    else:
     ball8 = random.choice(['It is certain','As i see it, yes', 'Dont count on it', 'Without a doubt', 'Definitely', 'Very doubtful', 'Outlook not so good', 'My sources say no', 'My reply is no', 'Most likely', 'You may rely on it', 'Ask again later'])
     await client.say(ball8)
         
client.run(token)
