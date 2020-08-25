from discord.utils import get

class CommandProcessor:
    def __init__(self, botObject):

        @botObject.event
        async def on_message(message):
            if message.author == botObject.user:
                return

            #
            # one needs to escape commands from the on_message function, surely theres a better way than this...
            # bug : https://stackoverflow.com/questions/49331096/why-does-on-message-stop-commands-from-working
            #
            if message.content == '!summonpahie':
                await botObject.process_commands(message)

            if message.content.startswith('!sendpahie'):
                await botObject.process_commands(message)

            if message.content == '!kickpahie':
                await botObject.process_commands(message)

            if message.content == '!helpmepahie':
                await botObject.process_commands(message)

            if message.content == '!godeep':
                await botObject.process_commands(message)

            if message.content == '!joke':
                await botObject.process_commands(message)

            if message.content == '!bobquote':
                await botObject.process_commands(message)

            if message.content.startswith('!play'):
                await botObject.process_commands(message)

            if message.content.startswith('!availableaudio'):
                await botObject.process_commands(message)

            if message.content == '!w2g':
                await botObject.process_commands(message)

            if message.content.startswith('!poll'):
                await botObject.process_commands(message)

            if message.content == '!dankmeme':
                await botObject.process_commands(message)

            if message.content == '!skrbl':
                await botObject.process_commands(message)

            if message.content.startswith('!dmc'):
                await botObject.process_commands(message)

            if message.content == '!signmeuppahie':
                await botObject.process_commands(message)

            if message.content.startswith('!addfavourite'):
                await botObject.process_commands(message)

            if message.content == ('!showfavourites'):
                await botObject.process_commands(message)

            if message.content.startswith('!deletefavourite'):
                await botObject.process_commands(message)

            if message.content.startswith('!fav'):
                await botObject.process_commands(message)

        #    if message.content.startswith('!troll'):
        #        await bot.process_commands(message)
