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
            myxml = GetXMLForREST(ProfileForUserURL(arg))
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

            embed = discord.Embed(title=arg,description=tagline,url=profileurl)
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

    @commands.command()
    async def asset(self,ctx, arg=None):
        if arg:
            if TryGetNodeValues(GetXMLForREST(InfoForAssetURL(arg)), "status") == ['1']:
                if(GetXMLForREST(CommentsForAssetURL(arg,0,1))):
                    try:
                        lastc = TryGetNodeValues(GetXMLForREST(CommentsForAssetURL(arg,0,1)), "message")[0]
                        lasts = TryGetNodeValues(GetXMLForREST(CommentsForAssetURL(arg,0,1)), "sender")[0]
                        lasts += ": "
                    except:
                        lastc = " currently exist."
                        lasts = "No comments"
                if(GetXMLForREST(InfoForAssetURL(arg))):
                        name = TryGetNodeValues(GetXMLForREST(InfoForAssetURL(arg)), "name")[0]
                        author = TryGetNodeValues(GetXMLForREST(InfoForAssetURL(arg)), "author")[0]
                embed = discord.Embed(title=name,
                                      description=GetDescriptionForAsset(arg)[0]
                                      , url="https://www.spore.com/sporepedia#qry=sast-"+arg)
                embed.set_thumbnail(url=AssetURL(arg))
                print(str(GetTagsForAsset(arg)))
                embed.add_field(name="Author", value=author)
                tag = ""
                for i in GetTagsForAsset(arg):
                    tag += i+", "
                embed.add_field(name="Tags", value=tag)
                embed.add_field(name="Last Comment", value=lasts+lastc)
                await ctx.send(embed=embed)
            else:
                await ctx.send("This asset does not exist. You can get the id for an asset from the end of it's url."
                               " For example https://www.spore.com/sporepedia#qry=sast-501071885961"
                               " has the id of 501071885961")


def setup(bot):
    bot.add_cog(Spore(bot))