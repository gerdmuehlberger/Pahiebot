import os
import discord
from discord.ext import commands
from discord.utils import get
import random
import youtube_dl


from dotenv import load_dotenv

#load_dotenv()
token = 'NjMxNTgzODMzMDU3Mzk0NzA3.XZ4-vA.i4ZlimCWHkfVYkM4JzDF8H-RNVU'
bot = commands.Bot(command_prefix='!')


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
# send the bot out of the voice channel again
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
#print that the bot is ready to make sure that it actually logged on
#
@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')

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

    if message.content.startswith('!play'):
        await bot.process_commands(message)

    if message.content.startswith('!bobquote'):
        await bot.process_commands(message)


    if "pahie" in message.content:
        response = ("Pahie...")
        await message.channel.send(response)

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
# this needs to be altered. it works but i only want a temp file that plays when a link is pasted
#
'''
@bot.command(pass_context=True)
async def play(ctx, url: str):
    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
            print("removed old song")
    except PermissionError:
        print("song cant be removed when played!")
        await ctx.send("Music is already playing.")
        return

    await ctx.send("Pahie is downloading your song...")
    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_options = {
        'format': 'bestaudio/best',
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        print("downloading audio now")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"renamed file to {file}")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    new_name = name.rsplit("-", 2)
    await ctx.send(f"playing: {new_name}")
    print("playing")
    
'''

#
# play random spongebob quote
#
@bot.command(pass_context=True)
async def bobquote(ctx):

    try:
        voice = get(bot.voice_clients, guild=ctx.guild)
        rand_number = random.randint(1, 11)

        voice.play(discord.FFmpegPCMAudio(f"bobquotes/{rand_number}.mp3"), after=lambda e: print("finished playing quote."))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

    except:
        await ctx.send("Wait until the current quote is finished!")
        return



bot.run(token)