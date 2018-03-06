import os
from os.path import join, dirname
import discord
import logging
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

dotenv_path = join('../', dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Secret:
    def __init__(self, bot):
        self.bot = bot

    def get_roles(self, ctx):
        guild = ctx.bot.get_guild(int(os.environ.get("GUILD_ID")))
        role = discord.utils.get(guild.roles, name=os.environ.get("PRIVATE_GROUP_NAME"))
        return role.members

    @commands.command(hidden=True)
    async def secret_call(self, ctx, *, arg):
        member_list = self.get_roles(ctx)
        member_from = ctx.message.author.name
        member_from_id = ctx.message.author.id
        if any(member.id == member_from_id for member in member_list):
            for member in member_list:
                embed = discord.Embed(colour=discord.Colour(0x86889c), url="http://discordapp.com",
                                      description=arg,
                                      timestamp=datetime.utcfromtimestamp(1518701166))
                embed.set_author(name=member_from, url="https://discordapp.com",
                                 icon_url=ctx.message.author.avatar_url_as(static_format='png', size=64))
                await member.send(embed=embed)


def setup(bot):
    bot.add_cog(Secret(bot))
