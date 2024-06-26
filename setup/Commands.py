import discord
from discord.utils import get
import requests
import re
import random
import os
from io import BytesIO
from os import listdir
from setup.SSD_Mobilenet_v3 import SSD_Mobilenet_v3


class Commands:

    def __init__(self, botObject, databaseConnectionObject, redditObject):


        ############################################
        #### RETURN LIST OF AVAILABLE COMMANDS #####
        ############################################
        @botObject.command(pass_context=True)
        async def helpme(ctx):
            await ctx.send("https://pahiebot.gerdmuehlberger.com/")


        ############################################
        ####### SUMMONS BOT INTO A CHANNEL #########
        ############################################
        @botObject.command(pass_context=True)
        async def summon(ctx):
            try:
                global voiceChannel
                activeChannelOfMessageAuthor = ctx.message.author.voice.channel
                voiceChannel = get(botObject.voice_clients, guild=ctx.guild)

                if voiceChannel and voiceChannel.is_connected():
                    await voiceChannel.move_to(activeChannelOfMessageAuthor)
                else:
                    voiceChannel = await activeChannelOfMessageAuthor.connect()
                await ctx.send(f'Pahie joined {activeChannelOfMessageAuthor}')

            except AttributeError:
                await ctx.send("You need to be in a voicechannel to be able to summon Pahie!")




        '''
        ############################################
        ######## SENDS BOT INTO A CHANNEL ##########
        ############################################
        @botObject.command(pass_context=True)
        async def sendpahie(ctx, channelname):

            try:
                availableVoicechannelsOnServer = ctx.guild.voice_channels
                channelToSendBotTo = None

                for channel in availableVoicechannelsOnServer:
                    if channel.name.lower() == channelname.lower():
                        channelToSendBotTo = channel

                if channelToSendBotTo != None:
                    try:
                        global voiceChannel
                        channel = channelToSendBotTo
                        voiceChannel = get(botObject.voice_clients, guild=ctx.guild)

                        if voiceChannel and voiceChannel.is_connected():
                            await voiceChannel.move_to(channel)
                        else:
                            voiceChannel = await channel.connect()
                        await ctx.send(f'Pahie joined {channel}')

                    except AttributeError:
                        await ctx.send("Could not send Pahie!")

                else:
                    await ctx.send(f"There is no voicechannel called \'{channelname}\' on this server!")


            except AttributeError as ae:
                print(f"Could not execute !sendpahie command. Error: {ae}")
        '''




        ############################################
        ##### KICKS PAHIE INTO FROM A CHANNEL ######
        ############################################
        @botObject.command(pass_context=True)
        async def kick(ctx):
            try:
                activeChannelOfMessageAuthor = ctx.message.author.voice.channel

                try:
                    activeChannelOfBotConnection = get(botObject.voice_clients, guild=ctx.guild).channel

                    if activeChannelOfMessageAuthor == activeChannelOfBotConnection:
                        try:
                            voice = get(botObject.voice_clients, guild=ctx.guild)

                            if voice and voice.is_connected():
                                await voice.disconnect()
                                await ctx.send(f'Pahie left {activeChannelOfMessageAuthor}.')

                            else:
                                await ctx.send("Pahie could'nt be found in any voice channel...")

                        except AttributeError:
                            await ctx.send("You need to be in a voicechannel to kick Pahie.")
                    else:
                        await ctx.send("You can't kick Pahie if youre not in the same channel as him...")

                except Exception as e:
                    await ctx.send("Pahie could not be found in any channel!")

            except Exception as e:
                await ctx.send("You need to be on the server to be able to kick Pahie!")





        ############################################
        ####### CREATES A WATCH2GETHER ROOM ########
        ############################################
        @botObject.command(pass_context=True)
        async def w2g(ctx):
            await ctx.send("https://www.watch2gether.com/rooms/zuckerimkaffee-d9d68w37fb6sr2ir35?lang=de")





        ############################################
        ########## CREATES A STRAW POLL ############
        ############################################
        @botObject.command(pass_context=True)
        async def poll(ctx, *args):
            if len(args) <= 2:
                await ctx.send("Please enter more than 1 answer for the poll you want to create!")

            else:
                try:
                    pollUrl = 'https://strawpoll.com/api/poll'

                    if ('?' in args[0]) is False:
                        await ctx.send("Please make sure the first argument is a valid question.")

                    else:
                        answerOptionsList = args[1:]
                        jsonConformList = []

                        for i in answerOptionsList:
                            jsonConformList.append(f"{i}")

                        data = {"poll":
                                    {"title": f"{args[0]}",
                                     "description": "",
                                     "answers": jsonConformList,
                                     "priv": True,
                                     "ma": False,
                                     "mip": False,
                                     "co": False,
                                     "vpn": False,
                                     "enter_name": True,
                                     "has_deadline": False,
                                     "deadline": "",
                                     "only_reg": 0,
                                     "has_image": 0,
                                     "image": None}
                                }

                        headers = {'Accept': 'text/plain'}
                        response = requests.post(pollUrl, json=data, headers=headers).json()
                        poll_id = response['content_id']

                        await ctx.send(f"https://strawpoll.com/{poll_id}")

                except Exception as e:
                    print(f"Error on poll function: {e}")





        ############################################
        ######### SENDS LINK TO SKRBBL.IO ##########
        ############################################
        @botObject.command(pass_context=True)
        async def skrbl(ctx):
            await ctx.send("https://skribbl.io/")





        ############################################
        ######### SENDS A MEME FROM REDDIT #########
        ############################################
        @botObject.command(pass_context=True)
        async def dankmeme(ctx):
            try:

                subreddits = ["memes", "dankmemes", "DeepFriedMemes"]
                randNumberSubreddit = random.randint(0, len(subreddits) - 1)
                randNumberMeme = random.randint(2, 14)
                subRedditObject = redditObject.subreddit(subreddits[randNumberSubreddit])
                topPostsOfsubRedditObject = subRedditObject.hot(limit=15)
                URLSofPosts = []
                for i in topPostsOfsubRedditObject:
                    URLSofPosts.append(i.url)

                randomlyChosenMeme = URLSofPosts[randNumberMeme]
                await ctx.send(randomlyChosenMeme)

            except Exception as e:
                print(f"could not run !dankmeme command: {e}")
                await  ctx.send("Could not fetch a meme!")



        ######################################
        ######### SENDS A DEEP QUOTE #########
        ######################################
        @botObject.command(pass_context=True)
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




        ######################################
        ######### SENDS A DAD JOKE ###########
        ######################################
        @botObject.command(pass_context=True)
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




        ##################################################################
        ######### RETURNS A LIST OF ALL AUDIOFILES FOR A CATEGORY ########
        ##################################################################
        @botObject.command(pass_context=True)
        async def availableaudio(ctx, audiocategory):
            supportedAudioCategories = ['atv', 'misc', 'smoove']

            if audiocategory in supportedAudioCategories:
                audioFilePath = f"./audio/audiofiles/{audiocategory}/"

                try:
                    if os.path.exists(audioFilePath) is True:
                        listofAudiofiles = listdir(audioFilePath)
                        listofAudiofiles.sort()
                        audiofileListAsString = ','.join(listofAudiofiles).replace('.mp3', '')
                        audiofileList = audiofileListAsString.split(",")

                        await ctx.send(f'```css\navailable soundfiles for the category {audiocategory}:``````fix\n{audiofileList}```')

                    else:
                        await ctx.send("Seems like Pahie does not have any files for that category!")

                except Exception as e:
                    print(f"Could not execute the command !availableaudio. Error: {e}")
            else:
                await ctx.send( "Please enter a supported category to see which audiofiles are available! (Currently supported categories are: 'atv', 'spongebob', 'misc' and 'smoove')")





        ##################################################################
        ################# PLAYS A SPECIFIED AUDIOFILE ####################
        ##################################################################
        @botObject.command(pass_context=True)
        async def play(ctx, audiocategory, audiofilename):
            supportedAudioCategories = ['atv', 'misc', 'smoove']

            try:
                channelNameOfMessageAuthor = ctx.message.author.voice.channel

                try:
                    channelNameOfBotConnection = get(botObject.voice_clients, guild=ctx.guild).channel

                    try:
                        botVoiceObject = get(botObject.voice_clients, guild=ctx.guild)
                        commandAuthor = str(ctx.message.author).split('#')[0]

                        if audiocategory in supportedAudioCategories:
                            audioFilePath = f"./audio/audiofiles/{audiocategory}/"
                            fileamountAudiocategoryFolder = len(listdir(audioFilePath))
                            listofAudiofiles = listdir(audioFilePath)

                            if channelNameOfMessageAuthor == channelNameOfBotConnection:
                                try:
                                    if audiofilename == "random":
                                        if botVoiceObject is not None:
                                            rand_number = random.randint(1, fileamountAudiocategoryFolder)

                                            botVoiceObject.play(
                                                discord.FFmpegPCMAudio(audioFilePath + listofAudiofiles[rand_number]),
                                                after=lambda e: print(
                                                    f"played quote: {listofAudiofiles[rand_number]}."))
                                            botVoiceObject.source = discord.PCMVolumeTransformer(botVoiceObject.source)
                                            botVoiceObject.source.volume = 0.9

                                        else:
                                            await ctx.send("Pahie is not here!")

                                    elif audiofilename + ".mp3" in listofAudiofiles:
                                        if botVoiceObject is not None:
                                            botVoiceObject.play(
                                                discord.FFmpegPCMAudio(audioFilePath + audiofilename + ".mp3"))
                                            botVoiceObject.source = discord.PCMVolumeTransformer(botVoiceObject.source)
                                            botVoiceObject.source.volume = 0.5

                                        else:
                                            await ctx.send("Pahie is not here!")

                                    else:
                                        await ctx.send("Pahie could not find this quote :-(")

                                except Exception as e:
                                    print(f"couldnt run play function: {e}")

                            else:
                                await ctx.send(
                                    f"Pahie ignores {commandAuthor} because {commandAuthor} is not in the same channel as him!")

                        else:
                            await ctx.send("Pahie does not have quotes for this category :-(")


                    except discord.errors.ClientException as ce:
                        print(f"play function broke: {ce}")

                    except Exception as e:
                        print("function !play could not be executed because: ", e)
                        await ctx.send(f"Pahie is already playing a soundfile!")

                except AttributeError:
                    print(
                        f"user: {ctx.message.author} tried to call the command: {ctx.message.content} while bot was not in a voicechannel")
                    await ctx.send("Pahie could not be found in any channel.")

            except AttributeError:
                print(
                    f"user: {ctx.message.author} tried to call the command: {ctx.message.content} outside of a voicechannel")
                await ctx.send("You need to be on the Server in order to give Pahie instructions.")



        #####################################################
        ############## MARKYFIES A SENTENCE #################
        #####################################################
        @botObject.command(pass_context=True)
        async def markify(ctx, *args):
            try:

                pattern = re.compile('[gkx]')
                replace = {'g': 'd',
                            'k': 't',
                            'x': 'tz',
                            }

                response = "";

                if 1 <= len(args) <= 100:
                    for i in range(0, len(args)):
                        response += f"{re.sub(pattern,lambda x: replace[x.group(0)], args[i])} "

                    await ctx.send(response)

                elif len(args) == 0:
                    await ctx.send("Please enter some words!")

                else:
                    await ctx.send("You can only enter up to 100 words.")

            except Exception as e:
                print(f"could not run !markify command: {e}")


##### dbfuncs


        ###################################################
        ################# INSERT NEW USER #################
        ###################################################
        @botObject.command(pass_context=True)
        async def signmeup(ctx):
            try:
                userid = ctx.author.id
                userExists = databaseConnectionObject.find_user(userid)

                if userExists is True:
                    await ctx.send("Pahie already knows you!")

                elif userExists is False:
                    databaseConnectionObject.insert_user(userid)
                    await ctx.send("Pahiebot will remember you from now on!")

            except Exception as e:
                print("something went wrong: ", e)





        ###################################################
        ######## ADD SOUNDFILE TO USERS FAVOURITES ########
        ###################################################
        @botObject.command(pass_context=True)
        async def addfavourite(ctx, soundfilename, hotkeyword):
            try:
                userid = ctx.author.id
                userExists = databaseConnectionObject.find_user(userid)
                soundfileExists = databaseConnectionObject.find_soundfile(soundfilename)
                hotkeywordForUserExists = databaseConnectionObject.find_keyword_for_user(userid, hotkeyword)
                amountOfExistingSoundfilesForUser = databaseConnectionObject.get_amount_of_user_soundfiles(userid)

                string_check = re.compile('[@_!#$%^&*()<>?/|}{~:;.äöü]')

                allowedAmountOfSoundfilesInFavourites = 11

                if userExists == False:
                    await ctx.send(
                        "Pahie does not know you yet! Please use the !signmeuppahie command first to subscribe to personalised playlists!")

                elif soundfileExists == False:
                    await ctx.send(
                        "Pahie does not know this soundfile. Please make sure to enter an existing soundfile!")

                elif len(hotkeyword) >= 20:
                    await ctx.send("Please enter a shorter keyword!")

                elif hotkeywordForUserExists == True:
                    await ctx.send(f"You already used the keyword '{hotkeyword}'! Please enter a different one.")

                elif (string_check.search(hotkeyword) != None):
                    await ctx.send("The keyword you entered contains special characters. Pahie hates this and refuses to add such a bad keyword, please pick another.")

                elif amountOfExistingSoundfilesForUser >= allowedAmountOfSoundfilesInFavourites:
                    await ctx.send(f"You already used all slots for your personalized playlist! Please delete a soundfile in order to add more.")

                else:
                    soundfile_id = databaseConnectionObject.get_soundfile_id(soundfilename)
                    databaseConnectionObject.insert_user_soundfile(userid, soundfile_id, hotkeyword, amountOfExistingSoundfilesForUser + 1)
                    await ctx.send(f"{soundfilename} was added to your favourites under the keyword {hotkeyword}!")

            except Exception as e:
                print("an error occured on addfavourite function: ", e)





        ##############################################################
        ######## PRINTS A LIST OF ALL CURRENT USER FAVOURITES ########
        ##############################################################
        @botObject.command(pass_context=True)
        async def showfavourites(ctx):
            try:
                user_id = ctx.author.id
                user_name = ctx.author.name
                listOfFavourites = databaseConnectionObject.find_favourites_for_user(user_id)
                outputStrings = []
                outputStrings.append(f'```css\n{user_name}\'s favourited soundfiles:```')

                for soundfile in listOfFavourites:
                    outputStrings.append(f'```yaml\n keyword: {soundfile[0]}, soundfile: {soundfile[1]}, category: {soundfile[2]}```')

                await ctx.send(f"".join(outputStrings))

            except Exception as e:
                print("error in showfavourites: ", e)





        #####################################################################
        ######## REMOVES SPECIFIED SOUNDFILE FROM CURRENT FAVOURITES ########
        #####################################################################
        @botObject.command(pass_context=True)
        async def deletefavourite(ctx, hotkeyword):
            try:
                user_id = ctx.author.id
                user_name = ctx.author.name
                hotkeywordForUserExists = databaseConnectionObject.find_keyword_for_user(user_id, hotkeyword)

                if hotkeywordForUserExists == True:
                    databaseConnectionObject.delete_user_soundfile(user_id, hotkeyword)
                    await ctx.send(f"{hotkeyword} was deleted from your favourited soundfiles")

                else:
                    await ctx.send(f"There is no soundfile saved under the keyword: \'**{hotkeyword}**\' for the user **{user_name}**.")

            except Exception as e:
                print("error in deletefavourite: ", e)





        ###########################################
        ######## PLAY FAVOURITED SOUNDFILE ########
        ###########################################
        @botObject.command(pass_context=True)
        async def fav(ctx, hotkeyword):
            try:
                user_id = ctx.author.id
                keywordExists = databaseConnectionObject.find_keyword_for_user(user_id, hotkeyword)

                if keywordExists == True:

                    soundfileAndCategoryAsList = databaseConnectionObject.get_soundfilename_associated_with_keyword(user_id, hotkeyword)
                    soundfileAndCategoryAsList = soundfileAndCategoryAsList[0]
                    soundfileName = soundfileAndCategoryAsList[0]
                    soundfileCategory = soundfileAndCategoryAsList[1]
                    audioFilePath = f"./audio/audiofiles/{soundfileCategory}/"

                    try:
                        channelNameOfMessageAuthor = ctx.message.author.voice.channel

                        try:
                            channelNameOfBotConnection = get(botObject.voice_clients, guild=ctx.guild).channel

                            try:
                                botVoiceObject = get(botObject.voice_clients, guild=ctx.guild)
                                commandAuthor = str(ctx.message.author).split('#')[0]

                                if channelNameOfMessageAuthor == channelNameOfBotConnection:
                                    try:
                                        if len(soundfileAndCategoryAsList) == 0:
                                            await ctx.send("You do not have a soundfile saved under this keyword!")

                                        else:
                                            if botVoiceObject is not None:
                                                botVoiceObject.play(
                                                    discord.FFmpegPCMAudio(audioFilePath + soundfileName + ".mp3"))
                                                botVoiceObject.source = discord.PCMVolumeTransformer(
                                                    botVoiceObject.source)
                                                botVoiceObject.source.volume = 0.5

                                            else:
                                                await ctx.send("Pahie is not here!")


                                    except Exception as e:
                                        print(f"couldnt run play function: {e}")

                                else:
                                    await ctx.send(
                                        f"Pahie ignores {commandAuthor} because {commandAuthor} is not in the same channel as him!")


                            except discord.errors.ClientException as ce:
                                print(f"play function broke: {ce}")

                            except Exception as e:
                                print("function !play could not be executed because: ", e)
                                await ctx.send(f"Pahie is already playing a soundfile!")

                        except AttributeError:
                            print(
                                f"user: {ctx.message.author} tried to call the command: {ctx.message.content} while bot was not in a voicechannel")
                            await ctx.send("Pahie could not be found in any channel.")

                    except AttributeError:
                        print(
                            f"user: {ctx.message.author} tried to call the command: {ctx.message.content} outside of a voicechannel")
                        await ctx.send("You need to be on the Server in order to give Pahie instructions.")

                else:
                    await ctx.send(f"You don't have a file saved under the keyword: {hotkeyword}.")

            except Exception as e:
                print(f"Couldnt find keyword in favourites: ", e)


### ml functions

        @botObject.command()
        async def whatis(ctx):
            try:
                attachment_url = ctx.message.attachments[0].url
                file_request = requests.get(attachment_url)
                pic = file_request.content
                img = BytesIO(pic)

                # Write the stuff
                with open("./setup/SSD_Mobilenet_v3/img/temp.png", "wb") as f:
                    f.write(img.getbuffer())

                model = SSD_Mobilenet_v3()
                model.runModel()

                await ctx.send(file=discord.File('./setup/SSD_Mobilenet_v3/img/out.png'))


            except Exception as e:
                await ctx.send("An error occured when processing this image. Please try sending it again.")
                print(e)
