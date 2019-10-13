import os
import discord
from discord.ext import commands
from discord.utils import get
import random
import time
import youtube_dl


from dotenv import load_dotenv

#load_dotenv()
token = 'NjMxNTgzODMzMDU3Mzk0NzA3.XZ4-vA.i4ZlimCWHkfVYkM4JzDF8H-RNVU'
bot = commands.Bot(command_prefix='!')

#
#print that the bot is ready to make sure that it actually logged on
#
@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')


#######################################################################
###############     COMMANDS SECTION     ##############################
#######################################################################

#
# let the bot join the voice channel of the user who called it.
#
@bot.command(pass_context=True)
async def summonpahie(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await ctx.send(f'Pahie joined {channel}')


#
# send the bot out of the voice channel
#
@bot.command(pass_context=True)
async def kickpahie(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Bot left {channel}')
        await ctx.send(f'Pahie is pissed and left {channel}')
    else:
        print("bot was told to leave but wasnt in one...")
        await ctx.send("Pahie could'nt be found in any voice channel...")


#
# send list of available commands to textchat
#
@bot.command(pass_context=True)
async def helpmepahie(ctx):
    await ctx.send("!summonpahie: summons Pahie into your channel.\n"
                   "!kickpahie: kicks Pahie out of your channel.\n"
                   "!bobquote: Pahie plays Spongebobquote (Requires summoning to a channel first). \n"
                   "!unleashpahie: Pahie runs away and appears randomly in your channel at some point. "
                   "(He will not listen to commands while unleashed.)\n"
                   "!leashpahie: Pahie starts following your commands again.")


#
# once the bot is ready, run a function thats called at random times and
# lets the bot join into a random channel, play a soundfile and leave again
#

pahie_is_unleashed = False

def globallyChange():
    global pahie_is_unleashed
    pahie_is_unleashed = not pahie_is_unleashed


async def play_pahie_sound(ctx):
    try:
        if voice is not None:
            voice.play(discord.FFmpegPCMAudio(f"bobquotes/1.mp3"),
                       after=lambda e: "song finished playing")
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
        else:
            await ctx.send("Pahie is not here!")

    except Exception as e:
        print(e)
        await ctx.send("Wait until the current quote is finished!")
        return



@bot.command(pass_context=True)
async def unleashpahie(ctx):

    await ctx.send("You see Pahie running away in the distance...\n"
                   "He will not listen to any commands until he visits or you caught him again.\n"
                   "Type !leashpahie to catch him next time hes visiting.")

    globallyChange()
    starttime = time.time()

    while pahie_is_unleashed is True:
        #
        # bot joins the channel
        #
        random_timestamp = random.randint(20, 60)

        global voice
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        #await ctx.send(f'Pahie runs towards {ctx.message.author}!')

        #
        # bot plays sound and waits for the soundfile to finish
        #

        await play_pahie_sound(ctx)
        time.sleep(6)

        #
        # bot leaves channel again and waits for repeat
        #


        if voice and voice.is_connected():
            await voice.disconnect()
            #await ctx.send(f'Pahie run away from {ctx.message.author} again.')
        else:
            await ctx.send("Pahie could'nt be found in any voice channel...")

        time.sleep(random_timestamp - ((time.time() - starttime) % random_timestamp))

#
# this should stop the bot from joining again
#
@bot.command(pass_context=True)
async def leashpahie(ctx):
    if pahie_is_unleashed is True:
        globallyChange()
        await ctx.send(f'You leashed Pahie again...')
    else:
        await ctx.send(f'Pahie has not been unleashed yet.')


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

    if message.content.startswith('!unleashpahie'):
        await bot.process_commands(message)

    if message.content.startswith('!leashpahie'):
        await bot.process_commands(message)

    if message.content.startswith('!bobquote'):
        await bot.process_commands(message)


    #
    # bot answers with "pahie" everytime he is mentioned
    #
    if "pahie" in message.content:
        response = ("Pahie...")
        await message.channel.send(response)

    #
    # bot tells "story"
    #
    if "pahie" and "story" in message.content:

        def getSentence():
            sentence_count = random.randint(5, 15)
            punctuation_marks = [".", ",", "?", "!"]
            words = ""
            story = ""

            for x in range(sentence_count):
                for y in range(random.randint(1, 8)):
                    words = words + " " + "Pahie"
                words = words + random.choice(punctuation_marks)
            story = story + words

            return story

        response = getSentence()

        await message.channel.send(response)



#######################################################################
################      AUDIO PLAYING SECTION     #######################
#######################################################################
#
# play random spongebob quote
#
@bot.command(pass_context=True)
async def bobquote(ctx):

    try:
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice is not None:
            rand_number = random.randint(1, 21)

            voice.play(discord.FFmpegPCMAudio(f"bobquotes/{rand_number}.mp3"), after=lambda e: print("finished playing quote."))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
        else:
            await ctx.send("Pahie is not here!")

    except Exception as e:
        print(e)
        await ctx.send("Wait until the current quote is finished!")
        return

#######################################################################
####################      STORY SECTION     ###########################
#######################################################################


#######################################################################
###################      LEVELING SECTION     #########################
#######################################################################

bot.run(token)