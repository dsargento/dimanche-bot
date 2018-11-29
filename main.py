#!/usr/bin/python3.6

import os
import random
from os.path import join, dirname
from subprocess import call
from datetime import datetime
from subprocess import check_output
from hurry.filesize import size
from pygtail import Pygtail
import logging
import psutil
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

# Load env values
dotenv_path = join(dirname(__file__), '.env')
pid = os.getpid()
load_dotenv(dotenv_path)
OWNER = int(os.environ.get("OWNER"))
DISCORD_KEY = os.environ.get("DISCORD_KEY")
CURSED_MEMBERS = os.environ.get("CURSED_MEMBERS")

# Bot setup
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
    bot.load_extension("plugins.memes")


@bot.event
async def on_message(message):
    if message.content.startswith('pouet pouet'):
        await message.channel.send('GET OUT OF MY HEAD')
    if message.content.startswith('@everyone') or message.content.startswith('@here'):
        await message.channel.send('<:notifdog:375779565206765578>')
    if '<@395686427100184587>' in message.content or '<@!395686427100184587>' in message.content:
        await message.channel.send('\U0001f44b')
    if '<@&313664375657594880>' in message.content:
        await send_random_meme(message)
    if 'requin' in message.content:
        await message.channel.send('\U0001f988')
    if 'pot!' in message.content or 'POT!' in message.content:
        await message.channel.send(file=discord.File('src/images/ya_pot.gif'))
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
    resp = await ctx.send('Pong! Loading...')
    diff = resp.created_at - ctx.message.created_at
    await resp.edit(content=f'Pong! That took {1000*diff.total_seconds():.1f}ms.')


@bot.command()
async def info(ctx, member: discord.Member = None):
    guilds = len(bot.guilds)
    process = psutil.Process(pid)
    boot_time = datetime.fromtimestamp(process.create_time())
    embed = discord.Embed(title="Dimanche bot stats and info", colour=discord.Colour(0x7ed321),
                          timestamp=datetime.now())
    embed.set_footer(text="Help me", icon_url="https://cdn.discordapp.com/avatars/395686427100184587/71ff314a744afc3ea1e7bb51d4c58eb5.webp?size=128")
    embed.add_field(name="CPU Load", value=str(psutil.cpu_percent())+'%', inline=True)
    embed.add_field(name="RAM Usage", value=str(psutil.virtual_memory().percent)+'%', inline=True)
    embed.add_field(name="Joined guilds", value=guilds)
    embed.add_field(name="Uptime", value=datetime.now() - boot_time)

    await ctx.send(embed=embed)


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


async def send_random_meme(message):
    path = 'src/images/'
    random_meme = random.choice([x for x in os.listdir(path)
                                if os.path.isfile(os.path.join(path, x))])
    path = path + random_meme
    await message.channel.send(file=discord.File(path))

bot.run(DISCORD_KEY)
