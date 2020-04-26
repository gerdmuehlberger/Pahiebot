import os
from os import listdir
import discord
from discord.ext import commands
from discord.utils import get
import random
from pathlib import Path
import json
import sys
import logging
import time
import youtube_dl
import praw
import itertools
import traceback


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



#######################################################################
#################     ERRORHANDLING      ##############################
#######################################################################


@bot.event
async def on_command_error(ctx, error):
    """The event triggered when an error is raised while invoking a command.
    ctx   : Context
    error : Exception"""

    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (commands.CommandNotFound, commands.UserInputError)

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("Seems like you forgot to enter a required argument for that command! (Type !helpmepahie for more infos.)")

    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except:
            pass

    # For this error example we check to see where it came from...
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
            return await ctx.send('I could not find that member. Please try again.')

    # Anything in ignored will return and prevent anything happening.
    # This should be checked every now and then to maybe update the errorhandling
    elif isinstance(error, ignored):
        print(f"Unknown error to the Pahiebot errorhandling occured: {error}")
        return


    # All other Errors not returned come here... And we can just print the default TraceBack.
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



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
# implement a sneak into channel funciton here (if possible somehow)
#

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
        await ctx.send("You need to be in a voicechannel to be able to summon Pahie!")
        print(f"user: {ctx.message.author} tried to call the command: {ctx.message.content} outside of a voicechannel")

#
# let the bot join a voice channel of the users choice
#
@bot.command(pass_context=True)
async def sendpahie(ctx, channelname):

    try:
        voicechannels = ctx.guild.voice_channels
        channelToSendBotTo = None

        for channel in voicechannels:
            if channel.name == channelname:
                channelToSendBotTo = channel

        if channelToSendBotTo != None:
            try:
                global voice
                channel = channelToSendBotTo
                voice = get(bot.voice_clients, guild=ctx.guild)
                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    voice = await channel.connect()
                await ctx.send(f'Pahie joined {channel}')

            except AttributeError:
                await ctx.send("Could not send Pahie!")

        else:
            await ctx.send(f"There is no voicechannel called \'{channelname}\' on this server!")


    except AttributeError:
        print("didnt work.")


#
# send the bot out of the voice channel
#
@bot.command(pass_context=True)
async def kickpahie(ctx):
    try:
        channelNameOfMessageAuthor = ctx.message.author.voice.channel;

        try:
            channelNameOfBotConnection = get(bot.voice_clients, guild=ctx.guild).channel;

            if channelNameOfMessageAuthor == channelNameOfBotConnection:
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

            else:
                await ctx.send("You can't kick Pahie if youre not in the same channel as him...")

        except Exception as e:
            await ctx.send("Pahie could not be found in any channel!")
            print(f"user: {ctx.message.author} tried to call the command: {ctx.message.content} outside of a voicechannel")
            print(f"error raised by kickfunction: {e}")


    except Exception as e:
        await ctx.send("You need to be on the Server to be able to kick Pahie!")
        print(f"user: {ctx.message.author} tried to call the command: {ctx.message.content} outside of a voicechannel")
        print(f"error raised by kickfunction: {e}")

#
# create a watch2gether room
# extend this so users can choose between room 1-3 in case more rooms are needed
#
@bot.command(pass_context=True)
async def w2g(ctx):
    await ctx.send("https://www.watch2gether.com/rooms/zuckerimkaffee-d9d68w37fb6sr2ir35?lang=de")


#
# Post link to a skrbbl.io room
#
@bot.command(pass_context=True)
async def skrbl(ctx):
    await ctx.send("https://skribbl.io/")


#
# send list of available commands to textchat
#
@bot.command(pass_context=True)
async def helpmepahie(ctx):
    await ctx.send("**!summonpahie:**\n Summon Pahie into your channel.\n\n"
                   "**!kickpahie:**\n Kick Pahie out of your channel.\n\n"
                   "**!bobquote:**\n Pahie plays Spongebobquote (Requires summoning to a channel first). \n\n"
                   "**!w2g:**\n Pahie sends a watch2gether room. \n\n"
                   "**!dankmeme:**\n Pahie sends a random dank meme thats hot on reddit. \n\n"
                   "**!dmc names:**\n Pahie starts a dickmeasurement-contest with all the names passed to the command. "
                   "(Example: !dmc tick trick track) \n\n"
                   "**!skrbl:**\n Pahie sends link to skrbbl.io. \n\n"
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

    except AttributeError:
        print("user: {} tried to call the command: {} outside of a voicechannel".format(ctx.message.author, ctx.message.content))
        await ctx.send("Pahie could not be found in any channel.")


#
# Pahie trolls ingame
#

@bot.command(pass_context=True)
async def troll(ctx, user, game):

    try:
        channelNameOfBotConnection = get(bot.voice_clients, guild=ctx.guild).channel;

        try:
            botVoiceObject = get(bot.voice_clients, guild=ctx.guild)
            #commandAuthor = str(ctx.message.author).split('#')[0];
            trollFilePath = f"trollfiles/{game}"


            if os.path.exists(trollFilePath) is True:
                listOfFilesInTrollFilePath = (listdir(trollFilePath))

                listOfAvailableFilesForName = []

                for fileName in listOfFilesInTrollFilePath:
                    if user in fileName:
                        listOfAvailableFilesForName.append(fileName)

                if len(listOfAvailableFilesForName) == 0:
                    await ctx.send(f"{user} is immune to Pahie's trolling abilities for the game {game}! Maybe try for another game!")
                else:
                    randomSoundFile = random.choice(listOfAvailableFilesForName)
                    botVoiceObject.play(discord.FFmpegPCMAudio(trollFilePath + "/" + randomSoundFile),
                                        after=lambda e: print(f"Pahie trolled {user} in the game {game}."))
                    botVoiceObject.source = discord.PCMVolumeTransformer(botVoiceObject.source)
                    botVoiceObject.source.volume = 0.12

            else:
                inputErrorCheck = f"trollfiles/{user}"

                if os.path.exists(inputErrorCheck):
                    await ctx.send(f"Pahie thinks you switched the argument order! Could it be that you ment to write: \'!troll {game} {user}\'?")
                else:
                    await ctx.send("Please pick a game Pahie knows! (wow, csgo)")


        except Exception as e:
            print(f"error occured: {e}")


    except Exception as e:
        print(f"user: {ctx.message.author} tried to call the command: {ctx.message.content} outside of a voicechannel")
        print(f"Exception: {e}")
        await ctx.send("Pahie needs to be in a voicechannel to troll somebody.")

    except AttributeError as ae:
        print(f"e: {ae}")
        await ctx.send("Oops, Pahie could not troll.")


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

        subreddits = ["memes", "dankmemes", "DeepFriedMemes"]
        randNumberSubreddit = random.randint(0,2)
        randNumberMeme = random.randint(2, 14)
        subRedditObject = reddit.subreddit(subreddits[randNumberSubreddit])
        topPostsOfsubRedditObject = subRedditObject.hot(limit=15)
        URLSofPosts = []
        for i in topPostsOfsubRedditObject:
            URLSofPosts.append(i.url)

        randomlyChosenMeme = URLSofPosts[randNumberMeme]
        await ctx.send(randomlyChosenMeme)

    except Exception as e:
        print(f"could not run !dankmeme command: {e}")
        await  ctx.send("Could not fetch a meme!")


#######################################################################
###################  MINIGAME COMMANDS SECTION     ####################
#######################################################################

#
# dick measurement contest:
# needs doublecheck fpr errorhandling implemented
#
@bot.command(pass_context=True)
async def dmc(ctx, *args):
    try:
        # return type of args = tuple
        auxillaryListArgs = list(args)
        randomLengthsList = []
        dmcWinnerDict = {}

        if len(args) <= 1:
            await ctx.send("Please enter more than 1 participants for the dick measurement contest!")

        elif 2 <= len(args) <= 20:

            while len(randomLengthsList) < len(args):
                tempRandomNum = random.randint(1,22)
                if tempRandomNum not in randomLengthsList:
                    randomLengthsList.append(tempRandomNum)
                else:
                    pass

            randomLengthsList.sort(reverse=True)

            for i in range(0, len(args)):
                loopWinner = random.choice(auxillaryListArgs)

                auxillaryListArgs.remove(loopWinner)

                dmcWinnerDict.update({loopWinner: f"8{randomLengthsList[i] * '='}D"})

            await ctx.send("\n".join("{}:\t{}".format(k, v) for k, v in dmcWinnerDict.items()))

        else:
            await ctx.send("Too many participants for a dickmeasurement contest! Pahie can only count up to 20")

    except Exception as e:
        print(f"could not run !dmc command: {e}")




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
    if message.content == '!summonpahie':
        await bot.process_commands(message)

    if message.content.startswith('!sendpahie'):
        await bot.process_commands(message)

    if message.content == '!kickpahie':
        await bot.process_commands(message)

    if message.content == '!helpmepahie':
        await bot.process_commands(message)

    if message.content == '!bobquote':
        await bot.process_commands(message)

    if message.content == '!w2g':
        await bot.process_commands(message)

    if message.content == '!dankmeme':
        await bot.process_commands(message)

    if message.content == '!skrbl':
        await bot.process_commands(message)

    if message.content.startswith('!dmc'):
        await bot.process_commands(message)

    if message.content.startswith('!troll'):
        await bot.process_commands(message)




bot.run(bot.config_token)
