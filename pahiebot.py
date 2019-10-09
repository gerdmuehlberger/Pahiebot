import os
import discord
from dotenv import load_dotenv

#load_dotenv()
token = 'NjMxNTgzODMzMDU3Mzk0NzA3.XZ4-vA.i4ZlimCWHkfVYkM4JzDF8H-RNVU'

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected!')

client.run(token)