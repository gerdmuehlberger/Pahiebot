from discord.ext import commands
import sys
import traceback

class Errorhandler:
    def __init__(self, botObject):

        @botObject.event
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
                print(f"Errorhandler: {error}")
                return

            # All other Errors not returned come here... And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
