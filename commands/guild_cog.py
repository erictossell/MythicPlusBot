import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
import db

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Guild cog is initializing....')
        
    guild = SlashCommandGroup('guild', description='Guild information commands.')
    
    @guild.command(name='runs', help='Gets the best Mythic+ runs for the guild for the week.')
    async def runs(self,ctx):
        """Get the best Mythic+ runs for the guild.

        Args:
            ctx (_type_): _description_
        """
        try:
            description = '📄 This leaderboard is based on the top 10 registered characters from the Take a Lap Guild.\n\n  ⚠️ If you have not registered your off-realm or out-of-guild character, please do so with !register.'
            dungeon_list = db.get_top10_guild_runs_this_week()
            
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
    
    @guild.command(name='top_runs', help='Gets the top 10 Mythic+ runs for the guild.')
    async def top_runs(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_
        """
        try:
            description = '📄 This leaderboard is based on the top 10 registered characters from the Take a Lap Guild.\n\n  ⚠️ If you have not registered your off-realm or out-of-guild character, please do so with !register.'
            dungeon_list = db.get_top10_guild_runs_all_time()
            
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
    
    @guild.command(name='achievements')
    async def achievements(self, ctx):
        try:
            await self.leaderboard_embed(ctx, 'achievements')
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard achievements command: {exception}')
            
    @guild.command(name='item_level')
    async def item_level(self, ctx):
        try:
            await self.leaderboard_embed(ctx, 'itemlevel')
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard itemlevel command: {exception}')
            
    @guild.command(name='mythic_plus', help='Gets the current Mythic+ leaderboard.')
    async def mythic_plus(self, ctx):
        """Gets the current Mythic+ leaderboard.

        Args:
            ctx (context): The current discord context.
        """
        try:
            await self.mythic_plus_leaderboard(ctx)
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard command: {exception}')
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
        await ctx.respond(embed=embed)
        
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.respond('Something went wrong :( Talk to Eriim about this error. ')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard command: {error}')
            
def setup(bot):
    bot.add_cog(Guild(bot))
    print('Guild Cog loaded successfully.')
        