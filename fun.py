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
         
    @commands.command(pass_context=True, brief='Guessing Game', description='Guess the Correct Number to win.')
    async def guess(self, ctx):
    
        await self.bot.say('Guess a number between 1 to 10')

        def guess_check(m):
            return m.content.isdigit()

        guess = await self.bot.wait_for_message(timeout=5.0, author=ctx.message.author, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await self.bot.say(fmt.format(answer))
            return
        if int(guess.content) == answer:
            await self.bot.say('You are right!')
        else:
            await self.bot.say('Sorry. It is actually {}.'.format(answer))

    @commands.command()
    async def roll(self, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)    
            
def setup(bot):
    bot.add_cog(Fun(bot))
