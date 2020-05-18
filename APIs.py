from discord.ext import commands
import requests
import ast
import discord
import datetime


def sendgarf(one, two):
    garfurl = "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/" + one + '/' + two + ".gif"
    e = discord.Embed(title="Garfield Comic for " + two)
    e.set_image(url=garfurl)
    return e

class APIs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="prints a random taco recipe")
    async def taco(self, ctx):
        req = requests.get("http://taco-randomizer.herokuapp.com/random/")
        req = req.content.decode("utf-8")
        req = ast.literal_eval(req)
        await ctx.send(req['base_layer']['name'] + " with " + req['mixin']['name'] \
                       + " with " + req['condiment']['name'] \
                       + " topped off with " + req['seasoning']['name'] + "" \
                       + " and wrapped in delicious " + req['shell']['name'])
        await ctx.send(req['base_layer']['url'] + " " + req['mixin']['url'] \
                       + " " + req['condiment']['url'] \
                       + " " + req['seasoning']['url'] + "" \
                       + " " + req['shell']['url'])

    @commands.command(brief="Gets the Garfield comic for today, or specify a date using YYYY-MM-DD format")
    async def garfield(self, ctx, arg=None):
        if arg:
            await ctx.send(embed=sendgarf(arg[0:4], arg))
        else:
            await ctx.send(embed=sendgarf(str(datetime.datetime.now().date())[0:4], str(datetime.datetime.now().date())))


def setup(bot):
    bot.add_cog(APIs(bot))