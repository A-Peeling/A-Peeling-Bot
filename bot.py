import discord
from discord.ext import commands

startup_extensions = ["fun"]

#These reads what you put in the files.
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
    await client.change_presence(activity=discord.Game(name=argtxt))


@client.command(pass_context=True, brief='Responds \'Pong!\'.', description='Responds \'Pong!\', This command is used for testing the bot.')
async def ping(ctx):
    await ctx.send("Pong!")


@client.command(pass_context=True, brief='[Owner Only] Changes the current game.', description='[Owner Only] Changes the current game.')
async def game(ctx, *, arg: str):
    if ctx.message.author.id == ownerid:
        await ctx.send("Setting game to " + arg)
        print('Game set to '+ arg)
    with open('lastgame.txt', 'w') as file:
        file.write(arg)
        file.close()
    await  client.change_presence(activity=discord.Game(name=arg))


@client.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined this server on {0.joined_at}'.format(member))


@client.command(pass_context=True, brief='Work.')
async def work(ctx):
    await ctx.send("Yes you can work on the bot https://github.com/A-Peeling/A-Peeling-Bot")


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))        
        
client.run(token)