#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the member events for the bot.
# Author: Eriim

from discord.ext import commands

class MembersCog(commands.Cog):
    """The member events for the bot.

    Args:
        commands (commands.Cog): The parent discord class for the cog.
    """
    def __init__(self, bot):
        self.bot = bot
        print("Member events cog is initializing....")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined the server.')
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        print(f'{before} has updated their profile.')

def setup(bot):
    """Set up the member events cog.

    Args:
        bot (bot): The current discord bot.
    """
    bot.add_cog(MembersCog(bot))
    print("Member events cog has loaded successfully.")
    