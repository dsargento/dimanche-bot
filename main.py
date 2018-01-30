#!/usr/bin/python3.5

import discord
import asyncio
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	@client.event
	async def on_message(message):
		if message.content.startswith('!return '):
			msg = message.content
			content = msg.split('!return ', 1)[1]
			await client.send_message(message.channel, "Your message is {}".format(content))
		if message.content.startswith("!playing "):
			msg = message.content
			content = msg.split("!playing ", 1)[1]
			await client.change_presence(game=discord.Game(name=content))
		if message.content.startswith("!ping"):
			await client.send_message(message.channel, "Pong!")
		if message.content.startswith("pouet pouet"):
			await client.send_message(message.channel, "Camion!")
client.run(os.environ.get("DISCORD_KEY"))
