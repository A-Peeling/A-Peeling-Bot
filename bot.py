import discord
from discord.ext import commands
import platform

startup_extensions = ["fun", "spore", "APIs"]

#These reads what you put in the files.
f = open('token.txt', 'r')
token = f.read()
f.seek(0)
f.close()

f = open('owner.txt', 'r')
ownerId = f.read()
f.seek(0)
f.close()

f = open('lastgame.txt', 'r')
argtxt = f.read()
f.seek(0)
f.close()


p = ";"
client = commands.Bot(command_prefix=p)

@client.event
async def on_command_error(ctx, error):
    err = getattr(error, "original", error)

    if isinstance(err, commands.CommandNotFound):
        return

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name=argtxt))


@client.command(pass_context=True, brief='Responds \'Pong!\'.', description='Responds \'Pong!\', This command is used for testing the bot.')
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency, 4) * 1000) + ' ms')

@client.command(pass_context=True, brief='[Owner Only] Changes the current game.', description='[Owner Only] Changes the current game.')
async def game(ctx, *, arg: str):
    if str(ctx.message.author.id) == str(ownerId):
        print(ownerId)
        await ctx.send("Setting game to " + arg +".")
        print('Game set to '+ arg)
        with open('lastgame.txt', 'w') as file:
            file.write(arg)
            file.close()
        await client.change_presence(activity=discord.Game(name=arg))


@client.command(pass_context=True, brief='Work.')
async def work(ctx):
    user = ctx.author.name
    print(user)
    await ctx.send("Yes " + user + ", you can work on the bot https://github.com/A-Peeling/A-Peeling-Bot")


@client.command(pass_context=True, brief='Print system information')
async def uname(ctx):
    unamee = ' '.join(platform.uname())
    print(unamee)
#    if platform.name == 'Windows':
#        await ctx.send("look at me im a windows clown")
#    if platform.name == 'Darwin':
#        await ctx.send("macintosh systems not officially supported, yall are just along for the ride")
#    if platform.name == 'GNU':
#        await ctx.send("i am very stupid and this is very stupid:")
#    if platform.name == 'SunOS':
#        await ctx.send("hold on im sunning myself")
    await ctx.send("`" + unamee + "`")

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))        
        
client.run(token)
