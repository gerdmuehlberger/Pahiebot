import discord
from discord.utils import get
import requests
import re
import random
import os
from os import listdir


class Commands:

    def __init__(self, botObject, databaseConnectionObject, redditObject):


        ############################################
        #### RETURN LIST OF AVAILABLE COMMANDS #####
        ############################################
        @botObject.command(pass_context=True)
        async def helpmepahie(ctx):
            await ctx.send("```diff\n"
                           "!summonpahie: \n Summon Pahie into your channel.\n\n"
                           #"!sendpahie channel: \n Sends Pahie in a specified channel.\n\n"
                           "!kickpahie: \n Kick Pahie out of your channel.\n\n"
                           "!w2g: \n Pahie sends a watch2gether room. \n\n"
                           "!poll \"question?\" answeroptions: \n Pahie creates a poll.\n\n"
                           "!skrbl: \n Pahie sends link to skrbbl.io. \n\n"
                           "!dankmeme: \n Pahie sends a random dank meme thats hot on reddit. \n\n"
                           "!dmc names: \n-'names' needs to be a list of strings separated with a space in between. \n Pahie starts a dickmeasurement contest with all the names passed to the command. \n\n"
                           "!godeep: \n Pahie makes you think about life. \n\n"
                           "!joke: \n Pahie tells you a dadjoke. \n\n"
                           "!availableaudio category: \n- 'category' must be one of the currently supported categories: 'atv', 'spongebob', 'misc', 'smoove' \n Return a list of available audiofiles for the '!play' function. \n\n"
                           "!play category filename: \n- 'filename' must be a valid existing filename in a category, for 'categories' check the availableaudio command."
                           "\n- (Type 'random' instead of a 'filename' to play a random soundfile from the specified category.) \n Pahie plays the audiofile passed by the user. This command requires Pahie to be in a voicechannel. \n\n"
                           "!signmeuppahie: \n Enables the functionality to add your own favourite soundfiles to a personal soundboard. \n\n"
                           "!addfavourite soundfile keyword: \n- 'soundfile' must be a valid existing soundfile "
                           "\n- 'keyword' must be any string without special characters thats shorter than 20 characters.\n Adds a specified soundfile under the specified keyword to your personal favourites list. \n\n"
                           "!showfavourites: \n Returns a list of your currently favourited soundfiles and the keywords assigned by the user to play them. \n\n"
                           "!deletefavourite keyword: \n Deletes the soundfile associated with the specified keyword from your favourites list. \n\n"
                           "!fav keyword: \n Pahie plays the soundfile that you saved under the specified keyword."
                           "```"
                           )





        ############################################
        ####### SUMMONS BOT INTO A CHANNEL #########
        ############################################
        @botObject.command(pass_context=True)
        async def summonpahie(ctx):
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
        async def kickpahie(ctx):
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





        #####################################################
        ######### STARTS A DICK MEASUREMENT CONTEST #########
        #####################################################
        @botObject.command(pass_context=True)
        async def dmc(ctx, *args):
            try:
                #return type of args = tuple
                auxillaryListArgs = list(args)
                randomLengthsList = []
                dmcWinnerDict = {}

                if len(args) <= 1:
                    await ctx.send("Please enter more than 1 participants for the dick measurement contest!")

                elif 2 <= len(args) <= 20:

                    while len(randomLengthsList) < len(args):
                        tempRandomNum = random.randint(1, 22)
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
            supportedAudioCategories = ['atv', 'spongebob', 'misc', 'smoove']

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
            supportedAudioCategories = ['atv', 'spongebob', 'misc', 'smoove']

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


##### dbfuncs


        ###################################################
        ################# INSERT NEW USER #################
        ###################################################
        @botObject.command(pass_context=True)
        async def signmeuppahie(ctx):
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



