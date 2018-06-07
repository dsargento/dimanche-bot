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


def setup(bot):
    bot.add_cog(Memes(bot))

