from discord.ext import commands

class DiscordBotConnector:

    botObject = commands.Bot(command_prefix='!', case_insensitive=True)

    def __init__(self, token):
        self.token = token

    def runBot(self):
        try:
            bot = DiscordBotConnector.botObject

            #console log to make sure bot successfully connected in and is ready to process commands.
            @bot.event
            async def on_ready():
                print(f'{bot.user} has connected! id={bot.user.id}')

            bot.run(self.token)
            return bot

        except Exception as e:
            print(f"Discord Connection could not be etablished. Error: {e}")
