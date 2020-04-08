import os
import discord
from discord.ext import commands
from discord.utils import get
import random
from pathlib import Path
import json
import logging
import time
import youtube_dl
import praw
import itertools


#######################################################################
#################     GENERAL SETUP     ###############################
#######################################################################

currentWorkingDirectory = Path(__file__).parents[0]
currentWorkingDirectory = str(currentWorkingDirectory)
print("Working directory: ", currentWorkingDirectory)


# Authorization
secretFile = json.load(open(currentWorkingDirectory+'/config/secrets.json'))
bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.config_token = secretFile['token']

#activate discord logs by uncommenting this
#logging.basicConfig(level=logging.INFO)


#
#print that the bot is ready to make sure that it actually logged on
#
@bot.event
async def on_ready():
    print(f'{bot.user} has connected! id={bot.user.id}')


#######################################################################
###############     REDDIT CONNECTOR     ##############################
#######################################################################

secretFile = json.load(open(currentWorkingDirectory+'/config/secrets.json'))

use_script=secretFile['use_script']
client_secret=secretFile['client_secret']
user_agent=secretFile['user_agent']
username=secretFile['username']
password=secretFile['password']


try:
    reddit = praw.Reddit(client_id=use_script,
                         client_secret=client_secret,
                         user_agent=user_agent,
                         username=username,
                         password=password)

    print(f"reddit loggin successful.")

except Exception as e:
    print(f"error on reddit loggin: {e}")

#######################################################################
###############     BASIC COMMANDS SECTION     ########################
#######################################################################

#
# let the bot join the voice channel of the user who called it.
#
@bot.command(pass_context=True)
async def summonpahie(ctx):
    try:
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send(f'Pahie joined {channel}')
    except AttributeError:
        print("user: {} tried to call the command: {} outside of a voicechannel".format(ctx.message.author, ctx.message.content))


#
# send the bot out of the voice channel
#
@bot.command(pass_context=True)
async def kickpahie(ctx):
    try:
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f'Bot left {channel}')
            await ctx.send(f'Pahie left {channel}')
        else:
            print("bot was told to leave but wasnt in one...")
            await ctx.send("Pahie could'nt be found in any voice channel...")
    except AttributeError:
        print("user: {} tried to call the command: {} outside of a voicechannel".format(ctx.message.author, ctx.message.content))


#
# create a watch2gether room
#
@bot.command(pass_context=True)
async def w2g(ctx):
    await ctx.send("https://www.watch2gether.com/rooms/zuckerimkaffee-d9d68w37fb6sr2ir35?lang=de")


#
# send list of available commands to textchat
#
@bot.command(pass_context=True)
async def helpmepahie(ctx):
    await ctx.send("!summonpahie: summons Pahie into your channel.\n"
                   "!kickpahie: kicks Pahie out of your channel.\n"
                   "!bobquote: Pahie plays Spongebobquote (Requires summoning to a channel first). \n"
                   "!w2g: sends a watch2gether room. \n"
                  # "!dankmeme: sends a random dank meme thats hot on reddit. \n"
                   )



#######################################################################
################      AUDIO PLAYING SECTION     #######################
#######################################################################
#
# play random spongebob quote
#
@bot.command(pass_context=True)

async def bobquote(ctx):

    try:

        channelNameOfMessageAuthor = ctx.message.author.voice.channel;
        channelNameOfBotConnection = get(bot.voice_clients, guild=ctx.guild).channel;

        try:

            botVoiceObject = get(bot.voice_clients, guild=ctx.guild)
            commandAuthor = str(ctx.message.author).split('#')[0];

            if channelNameOfMessageAuthor == channelNameOfBotConnection:

                if botVoiceObject is not None:
                    rand_number = random.randint(1, 21)
                    botVoiceObject.play(discord.FFmpegPCMAudio(f"bobquotes/{rand_number}.mp3"), after=lambda e: print(f"finished playing quote #{rand_number}."))
                    botVoiceObject.source = discord.PCMVolumeTransformer(botVoiceObject.source)
                    botVoiceObject.source.volume = 0.07

                else:
                    await ctx.send("Pahie is not here!")

            else:
                await ctx.send(f"Pahie ignores {commandAuthor} because {commandAuthor} is not in the same channel as him!")

        except Exception as e:

            print("function !bobquote could not be executed because: ", e)

            await ctx.send(f"Pahie is already playing a bobquote!")
            return

    except AttributeError:
        print("user: {} tried to call the command: {} outside of a voicechannel".format(ctx.message.author, ctx.message.content))
        await ctx.send("Pahie could not be found in any channel.")


#######################################################################
####################      REDDIT API SECTION     ######################
#######################################################################

#
# send random top post of dankmemes subreddit
#
#NOTE: surely there is a better way to select a random index of a generator object in python.
#
#
@bot.command(pass_context=True)
async def dankmeme(ctx):
    try:
        randNumber = random.randint(0, 14)
        subRedditObject = reddit.subreddit("dankmemes")
        topPostsOfsubRedditObject = subRedditObject.hot(limit=15)
        URLSofPosts = []
        for i in topPostsOfsubRedditObject:
            URLSofPosts.append(i.url)

        randomlyChosenMeme = URLSofPosts[randNumber]
        await ctx.send(randomlyChosenMeme)

    except Exception as e:
        print(f"could not run !dankmeme command: {e}")
        await  ctx.send("Could not fetch a meme!")


#######################################################################
###################      LEVELING SECTION     #########################
#######################################################################


#######################################################################
##################     COMMAND PROCESSING SECTION     #################
#######################################################################

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return "pahie..."

    #
    # this fixes the command issue, its just a quickfix though.
    # one needs to escape commands from the on_message function, surely theres a better way than this...
    # bug : https://stackoverflow.com/questions/49331096/why-does-on-message-stop-commands-from-working
    #
    if message.content.startswith('!summonpahie'):
        await bot.process_commands(message)

    if message.content.startswith('!kickpahie'):
        await bot.process_commands(message)

    if message.content.startswith('!helpmepahie'):
        await bot.process_commands(message)

    if message.content.startswith('!bobquote'):
        await bot.process_commands(message)

    if message.content.startswith('!w2g'):
        await bot.process_commands(message)

    if message.content.startswith('!dankmeme'):
        await bot.process_commands(message)


bot.run(bot.config_token)
