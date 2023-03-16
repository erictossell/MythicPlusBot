from discord.ext import commands

class membersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Member events are initialized")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined the server.')
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        print(f'{before} has updated their profile.')        
   
        
    
    
    
    
    
async def setup(bot):
    await bot.add_cog(membersCog(bot))