import discord
import os
import requests
import json
import random

client = discord.client()

@client.event
async def on_ready():
    print('{0.user} is now active'.format(client))


@client.event
async def on_message(message):


client.run(os.getenv('TOKEN'))