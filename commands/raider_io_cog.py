#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the commands for the RaiderIO cog.
# Author: Eriim

import datetime
import re
import discord
from discord.ext import commands
import db
import raiderIO as RaiderIO
from objects.registration.registerButton import RegisterButton

class RaiderIOCog(commands.Cog):
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
                main_char = db.lookup_default_character(ctx.guild.id,ctx.author.id)
                if main_char is not None:
                    character = await RaiderIO.get_character(main_char.name, main_char.realm)
                    await ctx.channel.send(embed=character.get_best_runs_embed())
                    return
                else:
                    await ctx.channel.send('Please provide a character name and realm or set a main character.')
            if len(args) == 1:
                character = await RaiderIO.get_character(args[0])          
                await ctx.channel.send(embed=character.get_best_runs_embed())    
            if len(args) == 2:
                character = await RaiderIO.get_character(args[0], args[1])
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
                main_char = db.lookup_default_character(ctx.guild.id,ctx.author.id)
                if main_char is not None:
                    character = await RaiderIO.get_character(main_char.name, main_char.realm)
                    await ctx.channel.send(embed=character.get_recent_runs_embed())
                    return
                else:
                    await ctx.channel.send('Please provide a character name and realm or set a main character.')
            if len(args) == 1:
                character = await RaiderIO.get_character(args[0])
                await ctx.channel.send(embed=character.get_recent_runs_embed())
            if len(args) == 2:
                character = await RaiderIO.get_character(args[0], args[1])
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
            if len(args) == 0 and ctx.guild is not None:
                main_char = db.lookup_default_character(ctx.guild.id,ctx.author.id)
                if main_char is not None:
                    character = await RaiderIO.get_character(main_char.name, main_char.realm)
                    await ctx.channel.send(embed=character.get_character_embed())
                    return
                else:
                    await ctx.channel.send('Please provide a character name and realm or set a main character.')
            if len(args) == 1:
                if pattern.search(args[0]) and args[0].count("-") == 1:
                    character = await RaiderIO.get_character(args[0].split("-")[0], args[0].split("-")[1])
                    await ctx.channel.send(embed=character.get_character_embed())
                    return
                character = await RaiderIO.get_character(args[0])
                await ctx.send(embed=character.get_character_embed())                
            if len(args) == 2:
                character = await RaiderIO.get_character(args[0], args[1])
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
            affixes = await RaiderIO.get_mythic_plus_affixes()
            embed = discord.Embed(title='Current Mythic+ Affixes', description= '', color=discord.Color.green())
            for affix in affixes:
                embed.add_field(name=affix.name, value=affix.description, inline=False)
            await ctx.channel.send(embed=embed)
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !affixes command: {exception}')
    @commands.command(name='setMain', help='Sets the default character for a user.')
    async def set_main(self, ctx, *args):
        """Sets a user's default character.

        Args:
            ctx (context): The current discord context.
        """
        try:
            if len(args) == 0:
                await ctx.channel.send('Please provide a character name and realm.')
            if len(args) == 1:
                character = await RaiderIO.get_character(args[0])
                character_db = db.lookup_character(character.name, character.realm)
                default_character = db.lookup_default_character(ctx.guild.id, ctx.author.id)
                if default_character is None:
                    new_default_character = db.DefaultCharacterDB(ctx.author.id,
                                                                  ctx.guild.id,
                                                                  True,
                                                                  1,
                                                                  datetime.datetime.now(),
                                                                  character_db)
                    db.add_default_character(new_default_character)
                    await ctx.channel.send(f'Your main character has been set to {character.name}-{character.realm}.')
                elif default_character is not None:
                    db.remove_default_character(default_character)
                    new_default_character = db.DefaultCharacterDB(ctx.author.id,
                                                                  ctx.guild.id,
                                                                  True,
                                                                  1,
                                                                  datetime.datetime.now(),
                                                                  character_db)
                    db.add_default_character(new_default_character)
                    await ctx.channel.send(f'Your main character has been set to {character.name}-{character.realm}.')
                else: 
                    await ctx.channel.send('Something went wrong.')
            elif len(args) == 2:
                character = await RaiderIO.get_character(args[0], args[1])
                character_db = db.lookup_character(character.name, character.realm)
                default_character = db.lookup_default_character(ctx.guild.id, ctx.author.id)
                if default_character is None:
                    new = db.DefaultCharacterDB(ctx.author.id,
                                                ctx.guild.id,
                                                True,
                                                1,
                                                datetime.datetime.now(),
                                                character_db)
                    db.add_default_character(new)
                    await ctx.channel.send(f'Your main character has been set to {character.name}-{character.realm}.')
                elif default_character is not None:
                    db.remove_default_character(default_character)
                    new_default_character = db.DefaultCharacterDB(ctx.author.id,
                                                                  ctx.guild.id,
                                                                  True,
                                                                  default_character.version+1,
                                                                  datetime.datetime.now(),
                                                                  character_db)
                    db.add_default_character(new_default_character)
                    await ctx.channel.send(f'Your default character has been set to {character.name}-{character.realm}.')
                else:
                    await ctx.channel.send('Something went wrong. Make sure if your character is not in the guild, you have registered it with !register.')

        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !default command: {exception}')
    @commands.command(name='leaderboard', help='Gets the current Mythic+ leaderboard.')
    async def leaderboard(self,ctx):
        """Gets the current Mythic+ leaderboard.

        Args:
            ctx (context): The current discord context.
        """
        try:
            characters_list = db.get_top10_character_by_mythic_plus()
            embed = discord.Embed(title='Current Mythic+ Leaderboard', description= '', color=discord.Color.green())
            embed.add_field(name='Taken from Raider.IO', value='[Raider.IO](https://raider.io/)', inline=False)
            embed.add_field(name='Name - Score ', value='Last Updated - Profile', inline=False)
            for leader in characters_list:
                embed.add_field(name=leader.name + ' - ' + str(leader.score), value='Last updated: '+str(leader.last_crawled_at) +f"  |  [Profile]({leader.url})", inline=False)
            await ctx.channel.send(embed=embed)
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard command: {exception}') 
def setup(bot):
    """Setup function for the cog.

    Args:
        bot (discord.bot): The bot that is running the cog.
    """
    bot.add_cog(RaiderIOCog(bot))
