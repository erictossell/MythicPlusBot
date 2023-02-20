import requests
import discord
from discord.ext import commands

class RaiderIO(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("RaiderIO cog is initialized")

    @commands.command(name='raider', help='Gets the RaiderIO score of a character.')
    async def raider(self, ctx, *args):
        character = requests.get('https://raider.io/api/v1/characters/profile?region=us&realm=Area-52&name=Khair&fields=mythic_plus_best_runs')

        embed =discord.Embed(title='RaiderIO', description=character.json()['name']+' RaiderIO Score', color=discord.Color.blue())
        
        for runs in character.json()['mythic_plus_best_runs']:
            embed.add_field(name=runs['dungeon'], value=runs['mythic_level'], inline=True)

        await ctx.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RaiderIO(bot))