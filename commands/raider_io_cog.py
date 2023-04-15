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
    @commands.command(name='best', help='Usage: !best <character name> <realm> (optional on Area-52)')
    async def best(self, ctx, character_name: str = None, realm: str = None):
        """The best command returns the best runs for a given character.

        Args:
            ctx (context): Pass the current discord context
            character_name (str): Character name
            realm (str): Realm of the character
        """
        try:
            if not character_name:
                main_char = db.lookup_default_character(ctx.guild.id, ctx.author.id)
                char = db.lookup_character(main_char.character.name, main_char.character.realm)
                if char:
                    character_name, realm = char.name, char.realm
                else:
                    await ctx.send('Please provide a character name and realm or set a main character.')
                    return

            if not realm:
                realm = 'Area-52'

            character = await RaiderIO.get_character(character_name, realm)
            await ctx.send(embed=character.get_best_runs_embed())
        
        except Exception as exception:
            await ctx.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !best command: {exception}')
    @commands.command(name='recent', help='Usage: !recent <character name> <realm> (optional on Area-52)')
    async def recent(self, ctx, character_name: str = None, realm: str = None):
        """This command returns the recent runs for a given character.

        Args:
            ctx (context): The current discord context.
        """ 
        try: 
            if not character_name:
                main_char = db.lookup_default_character(ctx.guild.id, ctx.author.id)
                if main_char:
                    character_name, realm = main_char.name, main_char.realm
                else:
                    await ctx.send('Please provide a character name and realm or set a main character.')
                    return
            if not realm:
                realm = 'Area-52'
            character = await RaiderIO.get_character(character_name, realm)
            await ctx.send(embed=character.get_recent_runs_embed())
            
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !recent command: {exception}')  
    @commands.command(name='character', help='Usage: !character <character name> <realm> (optional on Area-52)')
    async def character(self, ctx, character_name: str = None, realm: str = None):
        """This command returns a character's profile.

        Args:
            ctx (context): The current discord context.
            character_name (str): Character name.
            realm (str): Realm of the character.
        """
        try:
            if not character_name:
                if ctx.guild:
                    main_char = db.lookup_default_character(ctx.guild.id, ctx.author.id)
                    char = db.lookup_character(main_char.character.name, main_char.character.realm)
                    if char:
                        character_name, realm = char.name, char.realm
                    else:
                        await ctx.send('Please provide a character name and realm or set a main character.')
                        return
                else:
                    await ctx.send('Please provide a character name and realm.')
                    return

            if not realm:
                realm = 'Area-52'

            character = await RaiderIO.get_character(character_name, realm)
            await ctx.send(embed=character.get_character_embed())

        except Exception as exception:
            await ctx.send(f' I was not able to find a character with name: {character_name}. Type !help to see how to use this command.')
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
            if ctx.guild is None:
                await channel.send('Call the register command from within the Discord server you would like to register a character to.\nThis is used for analytics purposes.')
            else:
                view = RegisterView(ctx.guild.id)
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
    async def set_main(self, ctx, character_name: str, character_realm: Optional[str] = 'Area-52'):
        """Sets a user's default character.

        Args:
            ctx (context): The current discord context.
            character_name (str): The character name.
            character_realm (str, optional): The character realm. Defaults to 'Area-52'.
        """
        try:
            character = await RaiderIO.get_character(character_name, character_realm)
            character_db = db.lookup_character(character.name, character.realm.lower())
            default_character = db.lookup_default_character(ctx.guild.id, ctx.author.id)

            if character_db:
                if default_character:
                    default_character.character = character_db
                    default_character = db.update_default_character(default_character)
                else:
                    default_character = db.add_default_character(db.DefaultCharacterDB(ctx.author.id,
                                                                                       ctx.guild.id,
                                                                                       True,
                                                                                       1,
                                                                                       datetime.datetime.now(),
                                                                                       character_db.id))

                await ctx.channel.send(f'Your main character has been set to {character.name}-{character.realm}.')
            else:
                await ctx.channel.send('Something went wrong. Make sure if your character is not in the guild, you have registered it with !register.')

        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !default command: {exception}')
    
    @commands.group(name='leaderboard', help='Gets the current Mythic+ leaderboard.', invoke_without_command=True)
    async def leaderboard(self, ctx):
        """Gets the current Mythic+ leaderboard.

        Args:
            ctx (context): The current discord context.
        """
        try:
            await self.mythic_plus_leaderboard(ctx)
        except Exception as exception:
            await ctx.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard command: {exception}')

    @leaderboard.command(name='achievements')
    async def achievements_leaderboard(self, ctx):
        try:
            await self.leaderboard_embed(ctx, 'achievements')
        except Exception as exception:
            await ctx.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard achievements command: {exception}')

    @leaderboard.command(name='itemlevel')
    async def itemlevel_leaderboard(self, ctx):
        try:
            await self.leaderboard_embed(ctx, 'itemlevel')
        except Exception as exception:
            await ctx.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard itemlevel command: {exception}')

    async def mythic_plus_leaderboard(self, ctx):
        await self.leaderboard_embed(ctx, 'mythic_plus')

    async def leaderboard_embed(self, ctx, leaderboard_type):
        description = '📄 This leaderboard is based on the top 10 registered characters from the Take a Lap Guild.\n\n ⚠️ If you have not registered your off-realm or out-of-guild character, please do so with !register.'
        footer_text = 'Data from [Raider.IO](https://raider.io/)'

        if leaderboard_type == 'mythic_plus':
            characters_list = db.get_top10_character_by_mythic_plus()
            title = 'Mythic+ Score Leaderboard'
            field_func = lambda leader: (f'{leader.score} - {leader.name} | {leader.spec_name} - {leader.class_name}', f'[M+ Class Rank on {leader.realm.capitalize()}: {leader.rank}]({leader.url})')

        elif leaderboard_type == 'achievements':
            characters_list = db.get_top10_character_by_achievement()
            title = 'Achievement Point Leaderboard'
            field_func = lambda leader: (f'{leader.achievement_points} - {leader.name} | {leader.spec_name} - {leader.class_name}', f'Last updated: [{leader.last_crawled_at}]({leader.url})')

        elif leaderboard_type == 'itemlevel':
            characters_list = db.get_top10_character_by_highest_item_level()
            title = 'Item Level Leaderboard'
            field_func = lambda leader: (f'{leader.item_level} - {leader.name} | {leader.spec_name} - {leader.class_name}', f'[M+ Class Rank on {leader.realm.capitalize()}: {leader.rank}]({leader.url})')

        embed = discord.Embed(title=title, description=description, color=discord.Color.green())
        thumbnail = characters_list[0].thumbnail_url
        embed.set_thumbnail(url=thumbnail)

        for index, leader in enumerate(characters_list, start=1):
            field_name, field_value = field_func(leader)
            embed.add_field(name=f'{index}. {field_name}', value=field_value, inline=False)

        embed.set_footer(text=footer_text)
        await ctx.send(embed=embed)
    @commands.command(name='guildRuns', help='Gets the best Mythic+ runs for the guild.')
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
            await ctx.channel.send(embed=embed)
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !guildRuns command: {exception}')

    @commands.command(name='charRuns', help='Gets the best Mythic+ runs for a character.')
    async def char_runs(self,ctx, *args):
        """Gets the best Mythic+ runs for a character."""
        try:
            if len(args) == 0:
                await ctx.channel.send('Type !help to see how to use this command.')
                return
            if len(args) == 1:
                character_title = db.lookup_character(args[0], 'area-52')
                run_list = db.get_all_runs_for_character(character_title)
                for run in run_list:
                    characters_list = db.get_all_characters_for_run(run.id)
                    run_characters = '| '
                    for character in characters_list:
                        run_characters += '['+character.name + f']({character.url})  | '
                    run.characters = run_characters
                embed = discord.Embed(title=f'🏆 Best Runs for {character_title.name}', description= f'[{character_title.name}\'s Raider.IO Profile]({character_title.url})', color=discord.Color.green())
                counter = 1
                for run in run_list:
                    embed.add_field(name=str(counter)+ '.  '+ run.name + '  |  ' + str(run.mythic_level)+'  |  +'+str(run.num_keystone_upgrades), value=run.characters+f'\n[Link to run]({run.url})', inline=True)
                    counter+=1
                embed.set_footer(text='Data from Raider.IO(https://raider.io/)')
                await ctx.channel.send(embed=embed)
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !charRuns command: {exception}')
def setup(bot):
    """Setup function for the cog.

    Args:
        bot (discord.bot): The bot that is running the cog.
    """
    bot.add_cog(RaiderIOCog(bot))
