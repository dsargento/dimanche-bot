#!/usr/bin/python3.6

import os
from os.path import join, dirname
from subprocess import call
from pygtail import Pygtail
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

if not os.path.exists('logs'):
    os.makedirs('logs')
# Init Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/dimanche_bot.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#Load env values
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
OWNER = int(os.environ.get("OWNER"))
DISCORD_KEY = os.environ.get("DISCORD_KEY")
CURSED_MEMBERS = os.environ.get("CURSED_MEMBERS")

#Bot setup
description = '''I am Dimanche bot, and soon I'll take over the world!'''
bot = commands.Bot(command_prefix='!', description=description)
startup_extensions = ["plugins.secret", "plugins.music"]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print('------')
    bot.load_extension("plugins.secret")
    bot.load_extension("plugins.music")


@bot.event
async def on_message(message):
    if message.content.startswith('pouet pouet'):
        await message.channel.send('GET OUT OF MY HEAD')
    cursed_members = CURSED_MEMBERS.split()
    cursed_members = list(map(int, cursed_members))
    if message.author.id in cursed_members:
        await message.add_reaction('\N{HEAVY BLACK HEART}')
    await bot.process_commands(message)


@bot.command()
async def return_message(ctx, *, arg):
    await ctx.send("Your message is {}".format(arg))


@bot.command()
async def playing(ctx, *, arg, member: discord.member = None):
    if member is None:
        member = ctx.message.author
    logger.info("{} ({}) used Playing with args: {}".format(member.name, member.id, arg))
    await bot.change_presence(activity=discord.Game(name=arg))



@bot.command()
async def ping(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    logger.info("{} ({}) used Ping".format(member.name, member.id))
    await ctx.send("Pong!")

@bot.command()
async def info(ctx, member: discord.Member = None):
    guilds = bot.guilds
    guilds_list = []
    for guild in guilds:
        guilds_list.append(guild.name)
    await ctx.send(guilds)

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
    if member == OWNER:
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
    if member == OWNER:
        await ctx.send('Your user id is {0}, identified as root operator\n'
                       'Stopping SVN logging...'.format(member))
        call('cd /home/pi/Documents/scriptsvn')
        call('pm2 stop app.js')
        return
    await ctx.send('Your user id is {0}, you are not root'.format(member))


@bot.command(pass_context=True)
async def tail_logs(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id
    if member == OWNER:
        for line in Pygtail("logs/dimanche_bot.log"):
            await ctx.send('``{}``'.format(line))


bot.run(DISCORD_KEY)
