from discord.ext import commands
import random
import asyncio
import os
import datetime
import discord

class Fun(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, brief='It\'s just a 8ball.')
    async def magicball(self, ctx, *arg):
        if not arg:
            await ctx.send('You need to supply a question')
        else:
         ball8 = random.choice(['It is certain','As i see it, yes', 'Dont count on it', 'Without a doubt', 'Definitely', 'Very doubtful', 'Outlook not so good', 'My sources say no', 'My reply is no', 'Most likely', 'You may rely on it', 'Ask again later'])
         await ctx.send(ball8)
         
    @commands.command(pass_context=True, brief='Guessing Game', description='Guess the Correct Number to win.')
    async def guess(self, ctx):
            await ctx.send('Guess a number between 1 and 10.')

            def guess_check(m):
                return m.author == ctx.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.bot.wait_for('message', check=guess_check, timeout=5.0)
            except asyncio.TimeoutError:
                fmt = 'Sorry, you took too long. It was {}.'
                await ctx.send(fmt.format(answer))
                return
            if int(guess.content) == answer:
                await ctx.send('You are right!')
            else:
                await ctx.send('Sorry. It is actually {}.'.format(answer))

    @commands.command()
    async def roll(self, ctx, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NDN. For example 1d20 rolls 1 20 sided dice.')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @roll.error
    async def define_error(self, ctx, error):
        await ctx.send('Format has to be in NDN. For example 1d20 rolls 1 20 sided dice.')

    @commands.command(brief="Sends an image for the day of the week")
    async def calendar(self, ctx):
        dayofweek = datetime.datetime.today().weekday()
        filepath = random.choice(
            [x for x in os.listdir("days/" + str(dayofweek)) if
             os.path.isfile(os.path.join("days/" + str(dayofweek), x))])
        print(filepath)
        fullpath = "days/" + str(dayofweek) + "/" + filepath
        file = discord.File(fullpath, filename=filepath)
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        await ctx.send("it is " + days[dayofweek] + " or as i like to call it... " + days[dayofweek], file=file)

    @calendar.error
    async def calendar_error(self, ctx, error):
        await  ctx.send("CALENDAR ERROR")

def setup(bot):
    bot.add_cog(Fun(bot))
