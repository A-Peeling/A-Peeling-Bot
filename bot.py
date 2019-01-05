import discord
import asyncio 

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    p = ";"
    if message.content.startswith(p+'ping'):
        await client.send_message(message.channel, content = "Pong!")

    if message.content.startswith(p+'help'):
        embed = discord.Embed(title="Steam Group", colour=discord.Colour(0x33ff8c), url="https://steamcommunity.com/groups/A-Peeling", description="Commands:")

        embed.set_thumbnail(url="https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/5d/5d6905edee2a6e1b5a8f1cfbc650caf27afa92f1_full.jpg")
        embed.set_footer(text="Bozz Gay")

        embed.add_field(name="-ping", value="It just says 'Pong!'", inline=True)
        embed.add_field(name="-help", value="Brings up this window, you just used this command btw.", inline=True)

        await client.send_message(message.channel, embed=embed)

client.run('TokenHere')
