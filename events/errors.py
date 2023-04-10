#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the errors cog for the bot.
# Author: Eriim

from discord.ext import commands

class ErrorsCog(commands.Cog):
    """The errors cog for the bot.

    Args:
        commands (_type_): _description_
    """
    def __init__(self, bot):
        self.bot = bot
        print("Error events are initialized")
        
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        """Listens for errors in commands.

        Args:
            ctx (context): The current context of the bot.
            error (error): The type of error that was thrown.
        """
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("That command doesn't exist. Please try again.")
        if isinstance(error,commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing a required argument. Please try again.")


def setup(bot):
    """Set up the errors cog.

    Args:
        bot (bot): The current discord Bot.
    """
    bot.add_cog(ErrorsCog(bot))