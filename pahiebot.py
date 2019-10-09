import os
import discord
from dotenv import load_dotenv

#load_dotenv()
token = 'NjMxNTgzODMzMDU3Mzk0NzA3.XZ4-vA.i4ZlimCWHkfVYkM4JzDF8H-RNVU'

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return "pahie..."

    if "pahie" in message.content:
        response = ("pahie...")
        await message.channel.send(response)

client.run(token)