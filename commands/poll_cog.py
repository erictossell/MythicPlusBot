#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the poll command for the bot.
# Author: Eriim

from discord.ext import commands
from objects.poll.poll import Poll

class PollCog(commands.Cog):
    """The PollCog houses the poll commands.

    Args:
        commands (commands.Cog): This class houses the section of the bot for Poll Commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print("Poll cog is initialized")
    @commands.slash_command(name='poll', help='Lets users run a self-made poll for others to vote on.')
    @commands.has_role('Guild Members')
    async def poll(self, ctx, *args):
        """Generate a poll with the given arguments

        Args:
            ctx (context): the current discord context.
        """
        try:
            poll = Poll()
            poll.new_poll(args[0],args[1:])
            await poll.send(ctx.channel)
        except Exception as exception:
            await ctx.channel.send('@Eriim needs to fix this particular command :(')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !poll command: {exception}')

def setup(bot):
    """Setup the cog for the bot.

    Args:
        bot (discord.bot): The current discord bot.
    """
    bot.add_cog(PollCog(bot))
    