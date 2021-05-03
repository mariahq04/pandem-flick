import discord
from discord.ext import commands


class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("help cog online.")

    @commands.command(pass_context=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Commands", color=0xFF5733)
        embed.set_thumbnail(url="https://i.ibb.co/PG5kFmd/Pandem-Flick-Logocopy.png")
        embed.add_field(name="@help",
                        value="You can use this command to get right here, to some helpful information.",
                        inline=False)
        embed.add_field(name="@info <Title Here>",
                        value="You can use this command to get info about TV shows and movies. Example: @info Game of Thrones ",
                        inline=False)
        embed.add_field(name="@command1 <parameter>",
                        value="brief description",
                        inline=False)
        embed.add_field(name="@command2 <parameter>",
                        value="brief description",
                        inline=False)
        embed.add_field(name="@command3 <parameter>",
                        value="brief description",
                        inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(help(client))
