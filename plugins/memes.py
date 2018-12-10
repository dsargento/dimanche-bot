import os
from os.path import join, dirname
import requests
import mimetypes
import discord
import asyncio
import youtube_dl
from discord.ext import commands
from dotenv import load_dotenv

dotenv_path = join('../', dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Memes:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_meme(self, ctx, arg):
        url = arg
        # Count files in directory for image renaming
        count = os.listdir('src/images/')
        count = str(len(count)+1).zfill(3)
        print(count)
        response = requests.get(url)
        img_data = response.content
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        if extension == '.jpe':
            extension = '.jpg'
        with open('src/images/meme_'+count+extension, 'wb') as handler:
            handler.write(img_data)
        await ctx.send('Added image meme_'+count+extension)

    @commands.command()
    async def pot(self, ctx):
        await ctx.send(file=discord.File('src/images/ya_pot.gif'))

    @commands.command()
    async def communiste(self, ctx):
        await ctx.send(file=discord.File('src/images/communiste.gif'))

    @commands.command()
    async def dance(self, ctx):
        await ctx.send(file=discord.File('src/images/dance.gif'))

    @commands.command()
    async def formulaire(self, ctx):
        await ctx.send(file=discord.File('src/images/formulaire.gif'))

    @commands.command()
    async def love(self, ctx):
        await ctx.send(file=discord.File('src/images/love.gif'))

    @commands.command()
    async def meilleurs(self, ctx):
        await ctx.send(file=discord.File('src/images/meilleurs.gif'))

    @commands.command()
    async def merdier(self, ctx):
        await ctx.send(file=discord.File('src/images/merdier.gif'))

    @commands.command()
    async def marre(self, ctx):
        await ctx.send(file=discord.File('src/images/ras_le_bol.gif'))

    @commands.command()
    async def risque(self, ctx):
        await ctx.send(file=discord.File('src/images/risque.gif'))

    @commands.command()
    async def tampon(self, ctx):
        await ctx.send(file=discord.File('src/images/tampon.gif'))

    @commands.command()
    async def midi(self, ctx):
        await ctx.send(file=discord.File('src/images/midi.gif'))


def setup(bot):
    bot.add_cog(Memes(bot))

