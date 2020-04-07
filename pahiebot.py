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

currentWorkingDirectory = Path(__file__).parents[0]
currentWorkingDirectory = str(currentWorkingDirectory)
print("Working directory: ", currentWorkingDirectory)

# Authorization
secretFile = json.load(open(currentWorkingDirectory+'/config/secrets.json'))
bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.config_token = secretFile['token']
logging.basicConfig(level=logging.INFO)


#
#print that the bot is ready to make sure that it actually logged on
#
@bot.event
async def on_ready():
    print(f'{bot.user} has connected! id={bot.user.id}')


#######################################################################
###############     COMMANDS SECTION     ##############################
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
                   )


#######################################################################
##################     MESSAGING SECTION     ##########################
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


#######################################################################
################      AUDIO PLAYING SECTION     #######################
#######################################################################
#
# play random spongebob quote
#
@bot.command(pass_context=True)

async def bobquote(ctx):
    try:
        try:
            voice = get(bot.voice_clients, guild=ctx.guild)
            if voice is not None:
                rand_number = random.randint(1, 21)

                print("wd = ", currentWorkingDirectory)

                voice.play(discord.FFmpegPCMAudio(f"bobquotes/{rand_number}.mp3"), after=lambda e: print("finished playing quote."))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07
            else:
                await ctx.send("Pahie is not here!")

        except Exception as e:
            print(e)

            await ctx.send("Could not play a bobquote!")
            return
    except AttributeError:
        print("user: {} tried to call the command: {} outside of a voicechannel".format(ctx.message.author,
                                                                                        ctx.message.content))

#######################################################################
####################      STORY SECTION     ###########################
#######################################################################


#######################################################################
###################      LEVELING SECTION     #########################
#######################################################################

bot.run(bot.config_token)