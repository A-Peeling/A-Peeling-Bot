import discord
import fnmatch
import os
from discord.ext import commands
from SporeAPICoreUtils import *


class Spore(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Displays profile information about user")
    async def profile(self, ctx, arg=None):
        if arg:
            buddies = str(len(GetBuddiesForUser(arg)))
            creations = str(len(GetAssetIdsForUser(arg)))
            profileurl = "https://www.spore.com/view/myspore/" + arg
            url = ProfileForUserURL(arg)
            myxml = GetXMLForREST(url)
            if(myxml):
                try:
                    brackettagline = str(TryGetNodeValues(myxml, "tagline"))
                    tagline = brackettagline[1:-1]
                except:
                    tagline = "Change your tag line!"
                if not TryGetNodeValues(myxml, "image") == ['http://www.spore.com/static/null']:
                    try:
                        listimage = TryGetNodeValues(myxml, "image")
                        image = listimage[0]
                    except:
                        image = "http://www.spore.com/static/war/images/global/avatar_none.png"
                else:
                    image = "http://www.spore.com/static/war/images/global/avatar_none.png"
                if TryGetNodeValues(myxml, "status") == ['0']:
                    tagline = "User not found"

            embed = discord.Embed(
                title=arg,
                description=tagline,
                url=profileurl
            )
            embed.set_thumbnail(url=image)
            embed.add_field(name="Creations", value="This player has made " + creations + " creations")
            embed.add_field(name="Buddies", value="This player currently has " + buddies + " buddy(ies)")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Please provide a Spore screen name")

    @commands.command(brief="Displays status about spore")
    async def sporestats(self, ctx, arg=None):
        embed = discord.Embed(
            title="Spore Stats",
            description="The current Spore Stats",
            url="http://www.spore.com/sporepedia"
        )
        embed.add_field(name="Total Uploads", value=StatsAtTime())
        embed.add_field(name="Uploads Today", value=StatsOfDay())
        embed.add_field(name="Total Users", value=StatsUsers())
        embed.add_field(name="New Users in the past 24 Hours", value=StatsUsersToday())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Spore(bot))