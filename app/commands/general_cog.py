# Description: General commands for the bot.
import discord
from discord.ext import commands
from app.objects.dice import Dice
from app.objects.poll.createPollButton import CreatePollButton
import app.raiderIO as raiderIO

class GeneralCog(commands.Cog):
    """The general commands cog.

    Args:
        commands (commands.Cog): Cog definition
    """
    def __init__(self, bot):
        self.bot = bot
        print("General cog is initializing....")
    @commands.slash_command(name='ping', description='Pings the bot to see if it is online. (Latency in ms)')
    async def ping(self,ctx):
        """Ping the bot to see if it is online.

        Args:
            ctx (context): The current discord context.
        """
        await ctx.respond(f'Pong! {round(self.bot.latency * 1000)}ms')
    
    @commands.slash_command(name="roll", description="Rolls a dice with the specified number of sides.")
    async def roll(self,
                   ctx,
                   sides: int):
        """Roll a dice with the specified number of sides.

        Args:
            ctx (context): The current discord context.
            num_sides (int): The number of sides on the dice.
        """        
        try:
            
            dice = Dice(int(sides))
            await ctx.respond(dice.roll())
        except Exception as exception:
            await ctx.respond('@Eriim needs to fix this particular command :(')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !roll command: {exception}')
    @commands.slash_command(name='affixes', help='Gets the current Mythic+ affixes.')
    async def affixes(self, ctx):
        """This command gets the current Mythic+ affixes.

        Args:
            ctx (context): The current discord context.
        """
        try:
            affixes = await raiderIO.get_mythic_plus_affixes()
            embed = discord.Embed(title='Current Mythic+ Affixes', description= '', color=discord.Color.green())
            for affix in affixes:
                embed.add_field(name=affix.name, value=affix.description, inline=False)
            await ctx.respond(embed=embed)
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !affixes command: {exception}')
    @commands.slash_command(name='poll', description='Sends a poll to the channel.')
    async def poll (self,ctx):
        """A poll using the new modal features.

        Args:
            ctx (context): The current discord context.
        """
        print('testPoll command called')
        view = CreatePollButton()
        await ctx.send(view=view)
        await ctx.respond('----- TalBot Poll -----')

def setup(bot):
    """Set up the general cog.

    Args:
        bot (discord.bot): The current discord bot class.
    """
    bot.add_cog(GeneralCog(bot))
    print("General cog is loaded successfully.")
    