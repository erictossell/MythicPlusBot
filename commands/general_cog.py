# Description: General commands for the bot.
import time
import raiderIO as RaiderIO
from discord.ext import commands
from objects.dice import Dice
from objects.poll.createPollButton import CreatePollButton

class GeneralCog(commands.Cog):
    """The general commands cog.

    Args:
        commands (commands.Cog): Cog definition
    """
    def __init__(self, bot):
        self.bot = bot
        print("General cog is initialized")       
    @commands.command(name='ping', help='Pings the bot to see if it is online. (Latency in ms)')
    async def ping(self,ctx):
        """Ping the bot to see if it is online.

        Args:
            ctx (context): The current discord context.
        """
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')            
    
    @commands.command(name='roll', help='Rolls a dice with the specified number of sides.')
    async def roll(self,ctx, num_sides):
        """Roll a dice with the specified number of sides.

        Args:
            ctx (context): The current discord context.
            num_sides (int): The number of sides on the dice.
        """
        try:
            dice = Dice(int(num_sides))
            await ctx.send(dice.roll())
        except Exception as exception:
            await ctx.channel.send('@Eriim needs to fix this particular command :(')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !roll command: {exception}')
    
    @commands.command(name='testPoll', help='Sends a poll to the channel.')
    async def test_poll (self,ctx):
        """A poll using the new modal features.

        Args:
            ctx (context): The current discord context.
        """
        print('testPoll command called')
        view = CreatePollButton()
        await ctx.send('Take a Lap Discord Poll', view=view)
    
    @commands.command(name="crawl")
    @commands.has_role("Guild Masters")
    async def crawl(self, ctx):
        """Crawl the guild for new runs.

        Args:
            ctx (context): the current discord context.
        """
        async with ctx.typing():
            print('crawl command called')
            start_time = time.time()
            await ctx.send('Crawling Raider.IO characters...')
            output = await RaiderIO.crawl_characters(ctx.guild.id)
            await ctx.send(output)
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            await ctx.send('Finished crawling Raider.IO guild members for new runs after ' + str(elapsed_time) + ' seconds.')
    
    @commands.command(name="crawlGuild")
    @commands.has_role("Guild Masters")
    async def crawl_guild(self, ctx):
        """Crawl the guild for new members.

        Args:
            ctx (context): The current discord context.
        """
        async with ctx.typing():
            print('crawl guild command called')
            start_time = time.time()
            await ctx.send('Crawling Raider.IO guild members...')
            await RaiderIO.crawl_guild_members()
            end_time = time.time()
            elapsed_time = end_time - start_time
            await ctx.send('Finished crawling Raider.IO guild members after ' + str(elapsed_time) + ' seconds.')
    
    @commands.command(name="crawlRuns")
    @commands.has_role("Guild Masters")
    async def crawl_runs(self, ctx):
        """Compare runs to the database and update the database.

        Args:
            ctx (context): The current discord context.
        """
        async with ctx.typing():
            print('crawl runs command called')
            await ctx.send('Crawling Raider.IO guild runs...')
            start_time = time.time()
            output = await RaiderIO.crawl_runs()
            await ctx.send(output)
            end_time = time.time()
            elapsed_time = end_time - start_time
            await ctx.send('Finished crawling Raider.IO guild runs after ' + str(elapsed_time) + ' seconds.')
def setup(bot):
    """Set up the general cog.

    Args:
        bot (discord.bot): The current discord bot class.
    """
    bot.add_cog(GeneralCog(bot))
    