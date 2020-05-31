import discord
from discord.ext import commands
from discord.utils import get
import random
from pathlib import Path
import sys
import praw
import traceback
import requests
import json
import os
from os import listdir


import mysql.connector
from mysql.connector import errorcode


#######################################################################
#################     GENERAL SETUP     ###############################
#######################################################################

currentWorkingDirectory = Path(__file__).parents[0]
currentWorkingDirectory = str(currentWorkingDirectory)
print("Working directory: ", currentWorkingDirectory)


# Discord- / MYSQL-Authorization

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    bot = commands.Bot(command_prefix='!', case_insensitive=True)
    bot.config_token = os.environ.get('token')
else:
    secretFile = json.load(open(currentWorkingDirectory+'/config/secrets.json'))
    bot = commands.Bot(command_prefix='!', case_insensitive=True)
    bot.config_token = secretFile['devtoken']

    dbhost = secretFile['dbhost']
    dbname = secretFile['db']
    dbuser = secretFile['dbuser']
    dbpass = secretFile['dbpass']


# Open a MYSQL connection

def openMYSQLconnection():
    try:
        cnx = mysql.connector.connect(user=dbuser, password=dbpass,
                                      host=dbhost,
                                      database=dbname)
        print("connection to db opened.")
        return cnx


    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid user credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            cnx.close()


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


if is_prod:
    use_script = os.environ.get('use_script')
    client_secret = os.environ.get('client_secret')
    user_agent = os.environ.get('user_agent')
    username = os.environ.get('username')
    password = os.environ.get('password')

else:
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
            if channel.name.lower() == channelname.lower():
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
                   "**!sendpahie channel:** \n Sends Pahie in a specified channel (Example: !sendpahie cs:go)\n\n"
                   "**!kickpahie:**\n Kick Pahie out of your channel.\n\n"
                   "**!w2g:**\n Pahie sends a watch2gether room. \n\n"
                   "**!skrbl:**\n Pahie sends link to skrbbl.io. \n\n"
                   "**!availableaudio category:**\n Return a list of available audiofiles for the '!play' function. (Currently supported categories: 'atv', 'spongebob', 'misc', 'smoove') \n\n"
                   "**!play category filename:**\n Pahie plays the audiofile passed by the user. This command requires Pahie to be in a voicechannel. (Type 'random' instead of filename to play a random soundfile.) \n\n"
                   "**!dankmeme:**\n Pahie sends a random dank meme thats hot on reddit. \n\n"
                   "**!dmc names:**\n Pahie starts a dickmeasurement-contest with all the names passed to the command. "
                   "(Example: !dmc tick trick track) \n\n"
                   "**!godeep:**\n Pahie makes you think about life. \n\n"
                   "**!joke:**\n Pahie tells you a joke. \n\n"

                     #  "**!troll user game:**\n Pahie trolls by making a random callout of the specified user for the specified game. "
                     #  "This command requires Pahie to be in a voicechannel. "
                     #  "(Example: !troll danschi csgo) \n\n"
                   )



#######################################################################
################      AUDIO PLAYING SECTION     #######################
#######################################################################

#
# return a list of all available files for an audio function
#
@bot.command(pass_context=True)
async def availableaudio(ctx, quotetype):
    supportedQuotes = ['atv', 'spongebob', 'misc', 'smoove']

    if quotetype in supportedQuotes:
        quoteFilePath = f"quotes/{quotetype}/"

        try:
            if os.path.exists(quoteFilePath) is True:
                listofQuotes = listdir(quoteFilePath)
                listofQuotes.sort()
                responseListAsString = ','.join(listofQuotes).replace('.mp3', '')
                responseList = responseListAsString.split(",")


                await ctx.send(f'```css\navailable soundfiles for the category {quotetype}:``````fix\n{responseList}```')
            else:
                await ctx.send("Seems like Pahie does not have any files for that category!")
        except Exception as e:
            print(f"available quotes function crashed: {e}")
    else:
        await ctx.send("Please enter a supported category to see which audiofiles are available! (Currently supported categories are: 'atv', 'spongebob', 'misc' and 'smoove')")



@bot.command(pass_context=True)
async def play(ctx, quotetype, quotename):
    supportedQuotes = ['atv', 'spongebob', 'misc', 'smoove']

    try:
        channelNameOfMessageAuthor = ctx.message.author.voice.channel;
        channelNameOfBotConnection = get(bot.voice_clients, guild=ctx.guild).channel;

        try:
            botVoiceObject = get(bot.voice_clients, guild=ctx.guild)
            commandAuthor = str(ctx.message.author).split('#')[0];

            if quotetype in supportedQuotes:
                quoteFilePath = f"quotes/{quotetype}/"
                fileamountQuoteFolder = len(listdir(quoteFilePath))
                listofQuotes = listdir(quoteFilePath)


                if channelNameOfMessageAuthor == channelNameOfBotConnection:
                    try:
                        if quotename == "random":
                            if botVoiceObject is not None:
                                rand_number = random.randint(1, fileamountQuoteFolder)

                                botVoiceObject.play(
                                    discord.FFmpegPCMAudio(quoteFilePath + listofQuotes[rand_number]),
                                    after=lambda e: print(f"finished playing quote: {listofQuotes[rand_number]}."))
                                botVoiceObject.source = discord.PCMVolumeTransformer(botVoiceObject.source)
                                botVoiceObject.source.volume = 0.5

                            else:
                                await ctx.send("Pahie is not here!")

                        elif quotename + ".mp3" in listofQuotes:
                            if botVoiceObject is not None:
                                botVoiceObject.play(discord.FFmpegPCMAudio(quoteFilePath + quotename + ".mp3"),
                                                    after=lambda e: print(
                                                        f"finished playing quote: {quotename}."))
                                botVoiceObject.source = discord.PCMVolumeTransformer(botVoiceObject.source)
                                botVoiceObject.source.volume = 0.5

                            else:
                                await ctx.send("Pahie is not here!")

                        else:
                            await ctx.send("Pahie could not find this quote :-(")

                    except Exception as e:
                        print(f"couldnt run play function: {e}")

                else:
                    await ctx.send(f"Pahie ignores {commandAuthor} because {commandAuthor} is not in the same channel as him!")

            else:
                await ctx.send("Pahie does not have quotes for this category :-(")


        except discord.errors.ClientException as ce:
            print(f"play function broke: {ce}")

        except Exception as e:
            print("function !play could not be executed because: ", e)
            await ctx.send(f"Pahie is already playing a soundfile!")

    except AttributeError:
        print(f"user: {ctx.message.author} tried to call the command: {ctx.message.content} outside of a voicechannel")
        await ctx.send("Pahie could not be found in any channel.")




'''


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
        
'''

#######################################################################
#####################     MYSQL OPERATIONS     ########################
#######################################################################

#
# insert a userid to usertable table example
#
def insert_user(uid):
    connectorObject = openMYSQLconnection()
    query = "INSERT INTO users VALUES (%s)"
    args = (uid,)

    try:
        print(f"starting operation: insert_user for id {uid}")
        cursor = connectorObject.cursor()
        cursor.execute(query, args)

        connectorObject.commit()

    except Exception as e:
        print("error: ", e)

    finally:
        cursor.close()
        connectorObject.close()
        print("connection to db closed.")


#
# check if userid already exists
#
def find_user(uid):
    connectorObject = openMYSQLconnection()
    query = "SELECT * FROM users WHERE uid=%s"
    args = (uid,)

    try:
        print("starting operation: find_user")
        cursor = connectorObject.cursor(buffered=True)
        cursor.execute(query, args)
        rows = cursor.fetchall()

        if len(rows) > 0:
            #if user already exists in db return False
            return True
        else:
            #if user does not exist in db return False
            return False

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        connectorObject.close()
        print("connection to db closed.")


#######################################################################
##########      PERSONALISED PLAYLIST (MYSQL) SECTION     #############
#######################################################################

#
# create entry for new user
#

@bot.command(pass_context=True)
async def signmeuppahie(ctx):
    try:
        userid = ctx.author.id
        userExists = find_user(userid)

        if userExists is True:
            await ctx.send("Pahie already knows you!")

        elif userExists is False:
            insert_user(userid)
            await ctx.send("Pahiebot will remember you from now on!")

    except Exception as e:
        print("something went wrong: ", e)


#
# add soundfile to favourites
#

@bot.command(pass_context=True)
async def addfavourite(ctx, soundfilename, hotkeyword):
    print("asdf")

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
        randNumberSubreddit = random.randint(0,len(subreddits)-1)
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


#
# Pahie starts a game of eels and escalators
#

@bot.command(pass_context=True)
async def eae(ctx, player1, player2):
    
    await ctx.send("asdf")

#######################################################################
###################      TEXTREPLY SECTION     ########################
#######################################################################


@bot.command(pass_context=True)
async def godeep(ctx):
    try:
        quotesAPIurl = ' https://opinionated-quotes-api.gigalixirapp.com/v1/quotes'
        response = requests.get(quotesAPIurl).json()
        quote = response['quotes'][0]['quote']
        author = response['quotes'][0]['author']

        await ctx.send(f"*\'{quote}\'*\n **- {author}**")
    except Exception as e:
        try:
            quotesAPIurl = ' https://opinionated-quotes-api.gigalixirapp.com/v1/quotes'
            response = requests.get(quotesAPIurl).json()
            quote = response['quotes'][0]['quote']

            await ctx.send(f"*\'{quote}\'*\n **- Unknown**")
        except Exception as e:
            print(f"Could not fetch a quote: {e}")


@bot.command(pass_context=True)
async def joke(ctx):
    try:
        jokeurl = 'https://sv443.net/jokeapi/v2/joke/Miscellaneous?blacklistFlags=racist,sexist'
        payload = {}
        headers = {'Accept': 'application/json'}
        response = requests.request("GET", jokeurl, headers=headers, data=payload).json()
        jokeSetup = response['setup']
        jokeDelivery = response['delivery']

        await ctx.send(f"{jokeSetup}\n**{jokeDelivery}**")

    except Exception as e:
        print(f"Error on joke function: {e}")




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

    if message.content == '!godeep':
        await bot.process_commands(message)

    if message.content == '!joke':
        await bot.process_commands(message)

    if message.content == '!bobquote':
        await bot.process_commands(message)

    if message.content.startswith('!play'):
        await bot.process_commands(message)

    if message.content.startswith('!availableaudio'):
        await bot.process_commands(message)

    if message.content == '!w2g':
        await bot.process_commands(message)

    if message.content == '!dankmeme':
        await bot.process_commands(message)

    if message.content == '!skrbl':
        await bot.process_commands(message)

    if message.content.startswith('!dmc'):
        await bot.process_commands(message)

    if message.content == '!signmeuppahie':
        await bot.process_commands(message)

    if message.content.startswith('!addfavourite'):
        await bot.process_commands(message)

#    if message.content.startswith('!troll'):
#        await bot.process_commands(message)




bot.run(bot.config_token)
