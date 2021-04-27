import discord
import self as self
from discord.ext.commands import MissingRequiredArgument

from MovieFunctions import movie_functions
from discord.ext import commands
import pymongo
from pymongo import MongoClient
from db import DB


class movie_info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("movie info cog online")

    #   don't really need this command
    #
    #    @commands.command(pass_context=True)
    #    async def get_id(self, ctx, *, message):
    #        movie_id = movie_functions.get_id(message)
    #        await ctx.send(movie_id)

    @commands.command(pass_context=True)
    async def rating(self, ctx, *, message):
        movie_id = movie_functions.get_id(message)
        rating = movie_functions.get_ratings(movie_id)

        await ctx.send(f'Rating: {rating}')

    @commands.command(pass_context=True)
    async def info(self, ctx, *, message):
        cluster = MongoClient(
            "mongodb+srv://pfAdmin:ZZ68174@cluster0.pdcfd.mongodb.net/PandemFlickBot?retryWrites=true&w=majority")

        # assigns database
        db = cluster["PandemFlickBot"]

        # assigns collection (a minidatabase within the larger database)
        collection = db["movies"]

        # results = collection.find({"title": {"$regex": message, "$options": 'i'}})

        movie = movie_functions.search(message, collection)
        # all of the code below sets up the embed, the box that we send back to the user
        # we can change colors, etc later & change this to function to clean up code
        # character '173' is empty character, unsure of what to put in description
        embed = discord.Embed(title=movie['title'], url=movie['web_url'], color=0xFF5733)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=movie['image_url'])
        embed.add_field(name="Plot", value=movie['plot'], inline=False)
        embed.add_field(name="Rating", value=movie['rating'], inline=True)
        embed.add_field(name="Running Time", value="{} minutes".format(movie['time']), inline=True)
        embed.add_field(name="Category", value=movie['category'], inline=True)
        embed.add_field(name="Genres", value=movie['genres'], inline=False)
        await ctx.send(embed=embed)

    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please format your command correctly. @info \"Movie Title\"")


def setup(client):
    client.add_cog(movie_info(client))
