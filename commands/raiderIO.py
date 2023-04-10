#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the commands for the RaiderIO cog.
# Author: Eriim

import re
import discord
from discord.ext import commands
from objects.raiderIO.raiderIOService import RaiderIOService
from objects.registration.registerButton import RegisterButton

class RaiderIO(commands.Cog):
    """RaiderIO Commands Cog

    Args:
        commands (commands.Cog): This class houses the section of the bot for RaiderIO Commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print("RaiderIO cog is initialized")
    @commands.command(name='best', help='Usage: !best <character name> <realm> (optional on Area-52)')
    async def best(self, ctx, *args):
        """The best command returns the best runs for a given character.

        Args:
            ctx (context): Pass the current discord context
        """
        try:
            if len(args) == 0:
                await ctx.channel.send('Please provide a character name and realm.')
            if len(args) == 1:
                character = await RaiderIOService.get_character(args[0])          
                await ctx.channel.send(embed=character.get_best_runs_embed())    
            if len(args) == 2:
                character = await RaiderIOService.get_character(args[0], args[1])
                await ctx.channel.send(embed=character.get_best_runs_embed())
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !best command: {exception}') 
    @commands.command(name='recent', help='Usage: !recent <character name> <realm> (optional on Area-52)')
    async def recent(self, ctx, *args):
        """This command returns the recent runs for a given character.

        Args:
            ctx (context): The current discord context.
        """ 
        try:
            if len(args) == 0:
                await ctx.channel.send('Please provide a character name and realm.')
            if len(args) == 1:
                character = await RaiderIOService.get_character(args[0])
                await ctx.channel.send(embed=character.get_recent_runs_embed())
            if len(args) == 2:
                character = await RaiderIOService.get_character(args[0], args[1])
                await ctx.channel.send(embed=character.get_recent_runs_embed())
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !recent command: {exception}')  
    @commands.command(name='character', help='Usage: !character <character name> <realm> (optional on Area-52)')
    async def character(self, ctx, *args):
        """This command returns a character's profile.

        Args:
            ctx (context): The current discord context.
        """
        try:
            pattern = re.compile(r"-")
            if len(args) == 0:
                await ctx.channel.send('Please provide a character name and realm.')
            if len(args) == 1:
                if pattern.search(args[0]) and args[0].count("-") == 1:
                    character = await RaiderIOService.get_character(args[0].split("-")[0], args[0].split("-")[1])
                    await ctx.channel.send(embed=character.get_character_embed())
                    return
                character = await RaiderIOService.get_character(args[0])
                await ctx.send(embed=character.get_character_embed())                
            if len(args) == 2:
                character = await RaiderIOService.get_character(args[0], args[1])
                await ctx.channel.send(embed=character.get_character_embed())
        except Exception as exception:
            await ctx.channel.send(f' I was not able to find a character with name:  {args[0]}  Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !character command: {exception}')
    @commands.command(name='register', help='Register a character that is not in the guild.')
    async def register(self, ctx):
        """The register command allows a user to register a character that is not in the guild. 
            This command will DM the user a button to click to register their character.

        Args:
            ctx (context): The current discord context.
        """
        try:
            user = await ctx.bot.fetch_user(ctx.author.id)
            channel = await user.create_dm()
            view = RegisterButton()
            await channel.send('Please click the button below to register your character. This message will self destruct in 60 seconds.', view=view, delete_after=60)
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !register command: {exception}')
    @commands.command(name='affixes', help='Gets the current Mythic+ affixes.')
    async def affixes(self, ctx):
        """This command gets the current Mythic+ affixes.

        Args:
            ctx (context): The current discord context.
        """
        try:
            affixes = await RaiderIOService.get_mythic_plus_affixes()
            embed = discord.Embed(title='Current Mythic+ Affixes', description= '', color=discord.Color.green())
            for affix in affixes:
                embed.add_field(name=affix.name, value=affix.description, inline=False)
            await ctx.channel.send(embed=embed)
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !affixes command: {exception}')
    @commands.command(name='default', help='Sets the default character for a user.')
    async def default_character(self,ctx):
        """Sets a user's default character.

        Args:
            ctx (context): The current discord context.
        """
        

def setup(bot):
    """Setup function for the cog.

    Args:
        bot (discord.bot): The bot that is running the cog.
    """
    bot.add_cog(RaiderIO(bot))
    