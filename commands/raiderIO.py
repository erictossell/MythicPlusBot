import discord
from discord.ext import commands
from objects.raiderIO.raiderIOService import RaiderIOService

class RaiderIO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot             
        print("RaiderIO cog is initialized")
   
    @commands.command(name='best', help='Usage: !best <character name> <realm> (optional on Area-52)')
    async def best(self, ctx, *args):
        try:        
            if len(args) == 0:
                await ctx.channel.send('Please provide a character name and realm.')
            if len(args) == 1:
                character = RaiderIOService.getCharacter(args[0])          
                await ctx.channel.send(embed=character.getBestRunsEmbed())    
            if len(args) == 2:
                character = RaiderIOService.getCharacter(args[0], args[1])           
                await ctx.channel.send(embed=character.getBestRunsEmbed())
        except Exception as e:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !best command: {e}')
        
    @commands.command(name='recent', help='Usage: !recent <character name> <realm> (optional on Area-52)')
    async def recent(self, ctx, *args):        
        try:            
            if len(args) == 0:
                await ctx.channel.send('Please provide a character name and realm.')
            if len(args) == 1:
                character = RaiderIOService.getCharacter(args[0])                 
                await ctx.channel.send(embed=character.getRecentRunsEmbed())
            if len(args) == 2:
                character = RaiderIOService.getCharacter(args[0], args[1])                 
                await ctx.channel.send(embed=character.getRecentRunsEmbed())
        except Exception as e:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !recent command: {e}')
                
                
    @commands.command(name='character', help='Usage: !character <character name> <realm> (optional on Area-52)')
    async def character(self, ctx, *args):       
        try:         
            if len(args) == 0:
                await ctx.channel.send('Please provide a character name and realm.')
            if len(args) == 1:
                character = RaiderIOService.getCharacter(args[0])                 
                await ctx.channel.send(embed=character.getCharacterEmbed())
            if len(args) == 2:
                character = RaiderIOService.getCharacter(args[0], args[1])                 
                await ctx.channel.send(embed=character.getCharacterEmbed())
        except Exception as e:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !character command: {e}')   
                    
    @commands.command(name='affixes', help='Gets the current Mythic+ affixes.')
    async def affixes(self, ctx):
        try:
            affixes = RaiderIOService.getMythicPlusAffixes()
            embed = discord.Embed(title='Current Mythic+ Affixes', description= '', color=discord.Color.green())
            for affix in affixes:
                embed.add_field(name=affix.name, value=affix.description, inline=False)
            await ctx.channel.send(embed=embed)
        except Exception as e:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !affixes command: {e}')

def setup(bot):
    bot.add_cog(RaiderIO(bot))