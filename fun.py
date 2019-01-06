import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random

class Fun():
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True, brief='It\'s just a 8ball.')
    async def magicball(self, ctx, *arg):
        if not arg:
            await self.bot.say('You need to supply a question')
        else:
         ball8 = random.choice(['It is certain','As i see it, yes', 'Dont count on it', 'Without a doubt', 'Definitely', 'Very doubtful', 'Outlook not so good', 'My sources say no', 'My reply is no', 'Most likely', 'You may rely on it', 'Ask again later'])
         await self.bot.say(ball8)

def setup(bot):
    bot.add_cog(Fun(bot))
