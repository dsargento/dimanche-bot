#!/usr/bin/python3.6

import os
from os.path import join, dirname
from subprocess import call
import discord
from discord.ext import commands
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
description = '''I am Dimanche bot, and soon I'll take over the world!'''
bot = commands.Bot(command_prefix='!', description=description)

startup_extensions = ["plugins.secret"]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print('------')
    bot.load_extension("plugins.secret")


@bot.event
async def on_message(message):
    if message.content.startswith('pouet pouet'):
        await message.channel.send('GET OUT OF MY HEAD')
    await bot.process_commands(message)


@bot.command()
async def return_message(ctx, *, arg):
    await ctx.send("Your message is {}".format(arg))


@bot.command()
async def playing(ctx, *, arg):
    await ctx.bot.change_presence(game=discord.Game(name=arg))


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def pouet_pouet(ctx):
    await ctx.send("Camion!")


@bot.command(pass_context=True)
async def my_name(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id
    await ctx.send('Your user id is {0}'.format(member))


@bot.command(pass_context=True)
async def start_svn_logging(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id
    if member == 106437607738589184:
        await ctx.send('Your user id is {0}, identified as root operator\n'
                       'Starting SVN logging...'.format(member))
        call('cd /home/pi/Documents/scriptsvn')
        call('pm2 start app.js')
        return
    await ctx.send('Your user id is {0}, you are not root'.format(member))


@bot.command(pass_context=True)
async def stop_svn_logging(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id
    if member == 106437607738589184:
        await ctx.send('Your user id is {0}, identified as root operator\n'
                       'Stopping SVN logging...'.format(member))
        call('cd /home/pi/Documents/scriptsvn')
        call('pm2 stop app.js')
        return
    await ctx.send('Your user id is {0}, you are not root'.format(member))
bot.run(os.environ.get("DISCORD_KEY"))
