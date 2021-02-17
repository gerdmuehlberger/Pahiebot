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
            if message.content == 'pahie summon':
                await botObject.process_commands(message)

            if message.content.startswith('pahie send'):
                await botObject.process_commands(message)

            if message.content == 'pahie kick':
                await botObject.process_commands(message)

            if message.content == 'pahie helpme':
                await botObject.process_commands(message)

            if message.content == 'pahie godeep':
                await botObject.process_commands(message)

            if message.content == 'pahie joke':
                await botObject.process_commands(message)

            if message.content.startswith('pahie play'):
                await botObject.process_commands(message)

            if message.content.startswith('pahie availableaudio'):
                await botObject.process_commands(message)

            if message.content == 'pahie w2g':
                await botObject.process_commands(message)

            if message.content.startswith('pahie poll'):
                await botObject.process_commands(message)

            if message.content == 'pahie dankmeme':
                await botObject.process_commands(message)

            if message.content == 'pahie skrbl':
                await botObject.process_commands(message)

            if message.content.startswith('pahie dmc'):
                await botObject.process_commands(message)

            if message.content.startswith('pahie markify'):
                await botObject.process_commands(message)

            if message.content == 'pahie signmeup':
                await botObject.process_commands(message)

            if message.content.startswith('pahie addfavourite'):
                await botObject.process_commands(message)

            if message.content == ('pahie showfavourites'):
                await botObject.process_commands(message)

            if message.content.startswith('pahie deletefavourite'):
                await botObject.process_commands(message)

            if message.content.startswith('pahie fav'):
                await botObject.process_commands(message)

            if message.content.startswith('pahie whatis'):
                await botObject.process_commands(message)

        #    if message.content.startswith('!troll'):
        #        await bot.process_commands(message)
