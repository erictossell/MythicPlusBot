import os
import discord

from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from app import visualizer
import app.db as db
from app.objects.embed_builder import daily_guild_report_embed, weekly_guild_report_embed
from app.util import hex_to_rgb

load_dotenv('configurations/main.env')
SUPPORT_SERVER_ID = os.getenv('SUPPORT_SERVER_ID')
SUPPORT_CHANNEL_ID = os.getenv('SUPPORT_CHANNEL_ID')

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Guild cog is initializing....')
        
    guild = SlashCommandGroup('guild', description='Guild information commands.')

    
    @guild.command(name='daily', help='Gets the daily guild report.')
    async def daily_report(self, ctx):
        """Display the guilds best runs in the last 24 hours.

        Args:
            ctx (discord.ctx): The current discord context.
        """
        try:
            async with ctx.typing():
                
                await ctx.respond('Generating report...')
            
                bot_user = await ctx.bot.fetch_user(1073958413488369794)
                discord_guild_db = await db.get_discord_guild_by_id(ctx.guild.id)
            
                guild_run_list = await db.get_daily_guild_runs(discord_guild_id=ctx.guild.id)            
                run_list = await db.get_daily_non_guild_runs(discord_guild_id=ctx.guild.id, number_of_runs= (8-len(guild_run_list)))
                
                all_runs = await db.get_all_daily_runs(discord_guild_id=ctx.guild.id)

                graph = await visualizer.daily_guild_runs_plot(all_runs, discord_guild_id=ctx.guild.id)
                
                embed = daily_guild_report_embed(discord_guild_db=discord_guild_db,
                                                        guild_run_list=guild_run_list,
                                                        non_guild_run_list=run_list,
                                                        bot_user=bot_user)
                
                if graph is not None:
                    embed.set_image(url=f'attachment://{graph.filename}')
                    await ctx.respond(file= graph, embed=embed)
                else:
                    await ctx.respond(embed=embed)
                                
                
                
            
        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))
           
            await error_channel.send(f'Error in !register command: {exception}')
            
    @guild.command(name='weekly', help='Gets the daily guild report.')
    async def weekly_report(self, ctx):
        """Display the guilds best runs in the last 24 hours.

        Args:
            ctx (discord.ctx): The current discord context.
        """
        try:
            async with ctx.typing():
                
                await ctx.respond('Generating report...')
            
                bot_user = await ctx.bot.fetch_user(1073958413488369794)
                discord_guild_db = await db.get_discord_guild_by_id(ctx.guild.id)

                guild_run_list = await db.get_top10_guild_runs_this_week(discord_guild_id=ctx.guild.id)
                                
                run_list = await db.get_weekly_non_guild_runs(discord_guild_id=ctx.guild.id, number_of_runs= (8-len(guild_run_list)))
                
                all_runs = await db.get_all_weekly_runs(discord_guild_id=ctx.guild.id)
                                
                graph = await visualizer.weekly_guild_runs_plot(all_runs, guild_run_list, discord_guild_id=ctx.guild.id)
                
                embed = weekly_guild_report_embed(discord_guild_db=discord_guild_db,
                                                        guild_run_list=guild_run_list,
                                                        non_guild_run_list=run_list,
                                                        bot_user=bot_user)
                if graph is not None:
                    embed.set_image(url=f'attachment://{graph.filename}')
                    await ctx.respond(file= graph, embed=embed)
                else:
                    await ctx.respond(embed=embed)
            
        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))
           
            await error_channel.send(f'Error in !register command: {exception}')
                
    #Change to all time report    
    @guild.command(name='top_runs', help='Gets the top 5 Mythic+ runs for the guild.')
    async def top_runs(self, ctx):
        """Display the top 5 runs of all time completed as a guild.

        Args:
            ctx (_type_): _description_
        """
        try:
            title = '🏆 Top Guild Runs of All Time'
            description = f'📄 This leaderboard is based on the top runs from registered characters in the {ctx.guild.name} Guild.\n\n  ⚠️ If you have not registered your off-realm or out-of-guild character, please do so with /character register.'
            dungeon_list = await db.get_top5_guild_runs_all_time(discord_guild_id = ctx.guild.id)
            footer = 'Data from raider.io'
            bot_user = await ctx.bot.fetch_user(1073958413488369794)

            embed = discord.Embed(title=title, description=description, color=discord.Color.from_rgb(*hex_to_rgb('#c300ff')))
            
            embed.set_author(name='Mythic+ Bot', icon_url=bot_user.avatar, url='https://www.mythicplusbot.dev/')
            counter = 1
            for run, characters in dungeon_list:
                run_characters = '| '
                for character in characters:
                    run_characters += '['+character.name + f']({character.url})  | '
                embed.add_field(name=str(counter)+ '.  '+ run.name + '  |  ' + str(run.mythic_level)+'  |  +'+str(run.num_keystone_upgrades), value=run_characters+f'\n[Link to run]({run.url})', inline=False)
                counter+=1
            embed.set_footer(text=footer)
            await ctx.respond(embed=embed)
        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))           
           
            await error_channel.send(f'Error in !register command: {exception}')
    
    @guild.command(name='achievements')
    async def achievements(self, ctx):
        """Display the top 10 achievement earners in your guild.

        Args:
            ctx (_type_): _description_
        """
        try:
            await self.leaderboard_embed(ctx, 'achievements')
        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))           
           
            await error_channel.send(f'Error in !register command: {exception}')
            
    @guild.command(name='item_level')
    async def item_level(self, ctx):
        """Display the top 10 players by item level.

        Args:
            ctx (_type_): _description_
        """
        try:
            await self.leaderboard_embed(ctx, 'itemlevel')
        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))           
           
            await error_channel.send(f'Error in !register command: {exception}')
            
    @guild.command(name='mythic_plus', help='Gets the current Mythic+ leaderboard.')
    async def mythic_plus(self, ctx):
        """Display the top 10 players by M+ score.

        Args:
            ctx (context): The current discord context.
        """
        try:
            await self.mythic_plus_leaderboard(ctx)
        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))           
           
            await error_channel.send(f'Error in !register command: {exception}')
            
    async def mythic_plus_leaderboard(self, ctx):
        """Display the top 10 players by M+ score.

        Args:
            ctx (context): The current discord context.
        """
        await self.leaderboard_embed(ctx, 'mythic_plus')

    async def leaderboard_embed(self, ctx, leaderboard_type):
        description = f'📄 This leaderboard is based on the top 10 registered characters from the {ctx.guild.name} Guild.\n\n ⚠️ If you have not registered your off-realm or out-of-guild character, please do so with /character register.'
        footer_text = 'Data from raider.io'

        if leaderboard_type == 'mythic_plus':
            characters_list = await db.get_top10_character_by_mythic_plus(ctx.guild.id)
            title = 'Mythic+ Score Leaderboard'
            field_func = lambda leader: (f'{leader.score} - {leader.name} | {leader.spec_name} - {leader.class_name}', f'[M+ Class Rank on {leader.realm.capitalize()}: {leader.rank}]({leader.url})')

        elif leaderboard_type == 'achievements':
            characters_list = await db.get_top10_character_by_achievement(ctx.guild.id)
            title = 'Achievement Point Leaderboard'
            field_func = lambda leader: (f'{leader.achievement_points} - {leader.name} | {leader.spec_name} - {leader.class_name}', f'Last updated: [{leader.last_crawled_at}]({leader.url})')

        elif leaderboard_type == 'itemlevel':
            characters_list = await db.get_top10_character_by_highest_item_level(ctx.guild.id)
            title = 'Item Level Leaderboard'
            field_func = lambda leader: (f'{leader.item_level} - {leader.name} | {leader.spec_name} - {leader.class_name}', f'[M+ Class Rank on {leader.realm.capitalize()}: {leader.rank}]({leader.url})')

        bot_user = await ctx.bot.fetch_user(1073958413488369794)

        embed = discord.Embed(title=title, description=description, color=discord.Color.from_rgb(*hex_to_rgb('#c300ff')))
        
        embed.set_author(name='Mythic+ Bot', icon_url=bot_user.avatar, url='https://www.mythicplusbot.dev/')
        thumbnail = characters_list[0].thumbnail_url
        embed.set_thumbnail(url=thumbnail)

        for index, leader in enumerate(characters_list, start=1):
            field_name, field_value = field_func(leader)
            embed.add_field(name=f'{index}. {field_name}', value=field_value, inline=False)

        embed.set_footer(text=footer_text)
        await ctx.respond(embed=embed)
        
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            
            print(error)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))           
           
            await error_channel.send(f'Error in !register command: {error}')
            
def setup(bot):
    bot.add_cog(Guild(bot))
    print('Guild Cog has loaded successfully.')
        