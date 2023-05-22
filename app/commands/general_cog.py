# Description: General commands for the bot.
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from app.objects.dice import Dice
from app.objects.poll.createPollButton import CreatePollButton
import app.raiderIO as raiderIO

load_dotenv('configurations/main.env')
SUPPORT_SERVER_ID = os.getenv('SUPPORT_SERVER_ID')
SUPPORT_CHANNEL_ID = os.getenv('SUPPORT_CHANNEL_ID')

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
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))           
            await error_channel.send(f'Error in !register command: {exception}')
    @commands.slash_command(name='affixes', help='Gets the current Mythic+ affixes.')
    async def affixes(self, ctx):
        """Display the weekly M+ Affixes.

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
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))           
           
            await error_channel.send(f'Error in !register command: {exception}')
    @commands.slash_command(name='poll', description='Sends a poll to the channel.')
    async def poll (self,ctx):
        """Create a simple poll to vote as a group.

        Args:
            ctx (context): The current discord context.
        """
        print('Poll command called')
        view = CreatePollButton()
        await ctx.send(view=view)
        await ctx.respond('----- Mythic+ Bot Poll -----')

def setup(bot):
    """Set up the general cog.

    Args:
        bot (discord.bot): The current discord bot class.
    """
    bot.add_cog(GeneralCog(bot))
    print("General cog is loaded successfully.")
    