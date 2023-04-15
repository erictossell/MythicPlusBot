#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the commands for the RaiderIO cog.
# Author: Eriim

import datetime
import re
from typing import Optional
import discord
from discord.ext import commands
import db
import raiderIO as RaiderIO
from objects.registration import RegisterView

class RaiderIOCog(commands.Cog):
    """RaiderIO Commands Cog

    Args:
        commands (commands.Cog): This class houses the section of the bot for RaiderIO Commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print("RaiderIO cog is initialized")
    
    
    
    
    @commands.slash_command(name='affixes', help='Gets the current Mythic+ affixes.')
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
            await ctx.respond(embed=embed)
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !affixes command: {exception}')
    
    
    
    
    @commands.slash_command(name='guildruns', help='Gets the best Mythic+ runs for the guild.')
    async def guild_runs(self,ctx):
        """Get the best Mythic+ runs for the guild.

        Args:
            ctx (_type_): _description_
        """
        try:
            description = '📄 This leaderboard is based on the top 10 registered characters from the Take a Lap Guild.\n\n  ⚠️ If you have not registered your off-realm or out-of-guild character, please do so with !register.'
            dungeon_list = db.get_top10_guild_runs()
            
            embed = discord.Embed(title='🏆 Best Take a Lap Guild Runs', description= description, color=discord.Color.green())
            counter = 1
            for run in dungeon_list:
                characters_list = db.get_all_characters_for_run(run.id)
                run_characters = '| '
                for character in characters_list:
                    run_characters += '['+character.name + f']({character.url})  | '
                embed.add_field(name=str(counter)+ '.  '+ run.name + '  |  ' + str(run.mythic_level)+'  |  +'+str(run.num_keystone_upgrades), value=run_characters+f'\n[Link to run]({run.url})', inline=False)
                counter+=1
            embed.set_footer(text='Data from Raider.IO(https://raider.io/)')
            await ctx.respond(embed=embed)
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !guildRuns command: {exception}')

    
def setup(bot):
    """Setup function for the cog.

    Args:
        bot (discord.bot): The bot that is running the cog.
    """
    bot.add_cog(RaiderIOCog(bot))
