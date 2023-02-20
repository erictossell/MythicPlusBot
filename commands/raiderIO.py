import discord
from discord.ext import commands
from objects.getMythicPlusRecentRuns import getMythicPlusRecentRuns
from objects.raiderIO.getMythicPlusBestRuns import getMythicPlusBestRuns
from objects.raiderIO.getMythicPlusAffixes import getMythicPlusAffixes
from util.util import convertMillis

class RaiderIO(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("RaiderIO cog is initialized")

    @commands.command(name='best', help='Usage: !best <character name> <realm> (optional on Area-52)')
    async def best(self, ctx, *args):        
        if len(args) == 0:
            await ctx.channel.send('Please provide a character name and realm.')
        if len(args) == 1:
            character = getMythicPlusBestRuns(args[0],'Area-52')
            title = character.name+"'s Best Mythic+ Runs"         
            
            embed = discord.Embed(title=title, description= '', color=discord.Color.green(), url=character.url)
            embed.add_field(name='Class', value=character.class_name, inline=True)
            embed.add_field(name='Last Spec', value=character.spec_name, inline=True)
            embed.add_field(name='Last Role', value=character.role, inline=True)        
            embed.add_field(name='Achievement Points', value=str(character.achievement_points), inline=True)    
            embed.set_thumbnail(url=character.thumbnail_url)           
            

            for run in character.bestRuns:
                time = convertMillis(run['clear_time_ms'])
                name = run['dungeon'] + ' - ' + str(run['mythic_level'])    
                value = 'Time: **' + time + '** | Score: ' + str(run['score'])
                            
                embed.add_field(name=name, value=value, inline=False)
            embed.set_footer(text='Last updated ' + character.last_crawled_at) 
            await ctx.channel.send(embed=embed)

        if len(args) == 2:
            character = getMythicPlusBestRuns(args[0], args[1])        
            title = character.name+"'s Best Mythic+ Runs"         
            
            embed = discord.Embed(title=title, description= '', color=discord.Color.green(), url=character.url)
            embed.add_field(name='Class', value=character.class_name, inline=True)
            embed.add_field(name='Last Spec', value=character.spec_name, inline=True)
            embed.add_field(name='Last Role', value=character.role, inline=True)        
            embed.add_field(name='Achievement Points', value=str(character.achievement_points), inline=True)    
            embed.set_thumbnail(url=character.thumbnail_url)           
            

            for run in character.bestRuns:
                time = convertMillis(run['clear_time_ms'])
                name = run['dungeon'] + ' - ' + str(run['mythic_level'])    
                value = 'Time: **' + time + '** | Score: ' + str(run['score'])
                            
                embed.add_field(name=name, value=value, inline=False)
            embed.set_footer(text='Last updated ' + character.last_crawled_at) 
            await ctx.channel.send(embed=embed)
        
    @commands.command(name='recent', help='Usage: !recent <character name> <realm> (optional on Area-52)')
    async def recent(self, ctx, *args):            
            if len(args) == 0:
                await ctx.channel.send('Please provide a character name and realm.')
            if len(args) == 1:
                character = getMythicPlusRecentRuns(args[0],'Area-52')
                title = character.name+"'s Recent Mythic+ Runs"                
                embed = discord.Embed(title=title, description= '', color=discord.Color.green(), url=character.url)
                embed.add_field(name='Class', value=character.class_name, inline=True)
                embed.add_field(name='Last Spec', value=character.spec_name, inline=True)
                embed.add_field(name='Last Role', value=character.role, inline=True)        
                embed.add_field(name='Achievement Points', value=str(character.achievement_points), inline=True)    
                embed.set_thumbnail(url=character.thumbnail_url)             
    
                for run in character.recentRuns:
                    time = convertMillis(run['clear_time_ms'])
                    name = run['dungeon'] + ' - ' + str(run['mythic_level'])    
                    value = 'Time: **' + time + '** | Score: ' + str(run['score'])
                                
                    embed.add_field(name=name, value=value, inline=False)
                embed.set_footer(text='Last updated ' + character.last_crawled_at) 
                await ctx.channel.send(embed=embed)
            if(len(args) == 2):
                character = getMythicPlusRecentRuns(args[0], args[1])        
                title = character.name+"'s Recent Mythic+ Runs"         
                
                embed = discord.Embed(title=title, description= '', color=discord.Color.green(), url=character.url)
                embed.add_field(name='Class', value=character.class_name, inline=True)
                embed.add_field(name='Last Spec', value=character.spec_name, inline=True)
                embed.add_field(name='Last Role', value=character.role, inline=True)        
                embed.add_field(name='Achievement Points', value=str(character.achievement_points), inline=True)    
                embed.set_thumbnail(url=character.thumbnail_url)           
                
    
                for run in character.recentRuns:
                    time = convertMillis(run['clear_time_ms'])
                    name = run['dungeon'] + ' - ' + str(run['mythic_level'])    
                    value = 'Time: **' + time + '** | Score: ' + str(run['score'])
                                
                    embed.add_field(name=name, value=value, inline=False)
                embed.set_footer(text='Last updated ' + character.last_crawled_at) 
                await ctx.channel.send(embed=embed)
            
    @commands.command(name='affixes', help='Gets the current Mythic+ affixes.')
    async def affixes(self, ctx):
        affixes = getMythicPlusAffixes()
        embed = discord.Embed(title='Current Mythic+ Affixes', description= '', color=discord.Color.green())
        for affix in affixes.getAffixes():
            embed.add_field(name=affix['name'], value=affix['description'], inline=False)
        await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RaiderIO(bot))