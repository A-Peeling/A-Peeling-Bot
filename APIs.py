from discord.ext import commands
import requests
import ast
import discord
import datetime
import os
import time
from pyfiglet import Figlet


def exists(path):            # Checks if a request is ok.
    r = requests.head(path)  # This is also a functions so I can use it for more things to check for errors
    return r.status_code == requests.codes.ok

def sendgarf(one, two):
    garfurl = "http://www.professorgarfield.org/ipi1200/" + one + '/ga' + two + ".gif"
    if(exists(garfurl)):
        e = discord.Embed(title="Garfield Comic for " + one + "-" + two[2:4] + "-" + two [4:])
        e.set_image(url=garfurl)
        return e
    else:
        e = discord.Embed(title="Invalid Garfield Comic. You better not be looking for Heathcliff comics. :rage:",
                          description='The comic you want to see has to be in YYYY-MM-DD format. For example 2000-07-30')
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
            garf = arg.replace('-','')
            await ctx.send(embed=sendgarf(garf[0:4], garf[2:]))
        else:
            garfone = str(datetime.datetime.now().date())[0:4]
            garftwo = str(datetime.datetime.now().date())[2:].replace('-','')
            await ctx.send(embed=sendgarf(garfone, garftwo))
    
    @commands.command()
    async def folding(self, ctx):
        team = 267098
        getgot = requests.get("https://stats.foldingathome.org/api/team/" + str(team))
        getgot = getgot.content.decode("utf-8")
        getgot = ast.literal_eval(getgot)
        embed = discord.Embed(title="Stats for " + getgot['name'], url="https://stats.foldingathome.org/team/" + str(team), description="on Folding@home", color=0xd68717)
        embed.set_thumbnail(url=getgot['logo'])
        embed.add_field(name="Last Work Unit", value=getgot['last'], inline=True)
        embed.add_field(name="Active CPUs", value=getgot['active_50'], inline=True)
        embed.add_field(name="Grand Score", value=getgot['credit'], inline=True)
        embed.add_field(name="Work Unit Count", value=getgot['wus'], inline=True)
        embed.add_field(name="Team Ranking", value=getgot['rank'], inline=True)
        #embed.add_field(name="Donors", value=, inline=False)
        embed.set_footer(text="Fold with us sometime :^)")
        await ctx.send(embed=embed)

    @commands.command(brief="Some cool text stuff ngl.")
    async def figlet(self, ctx, arg1=None, *arg2):
        if arg1 and arg2:
            f = Figlet(font=arg1)
            epictext = ''
            for x in arg2:
                epictext += " "+x
            storefiglet = f.renderText(epictext[1:])
            await ctx.send("```"+storefiglet+"```")
        else:
            await ctx.send('To use this command it\'s ;figlet (font) (text). '
                           'For a list of fonts use the fontlist command.')

    @commands.command(brief="Font list for Figlet.")
    async def fontlist(self, ctx):
        fonts = os.listdir('./pyfiglet/fonts')
        fontlist = ""
        for x in fonts:
            if (x == "__pycache__") or (x == "__init__.py"):
                print("epic")
            else:
                fontlist += ", " + x[:-4]
                print(x)
        print(fontlist[2:-18])
        await ctx.send("Check your DMs for the fonts ;).")
        await ctx.message.author.send("```"+fontlist[2:1000]+"```")
        time.sleep(.300)
        await ctx.message.author.send("```" + fontlist[1000:2003] + "```")
        time.sleep(.300)
        await ctx.message.author.send("```" + fontlist[2003:3000] + "```")
        time.sleep(.300)
        await ctx.message.author.send("```" + fontlist[3000:4005] + "```")
        time.sleep(.300)
        await ctx.message.author.send("```" + fontlist[4005:] + "```")


def setup(bot):
    bot.add_cog(APIs(bot))
