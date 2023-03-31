from discord.ext import commands
from objects.poll.poll import Poll

class pollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Poll cog is initialized")
        
    @commands.command(name='poll', help='Lets users run a self-made poll for others to vote on.')
    @commands.has_role('Guild Members')
    async def poll(self, ctx, *args):  
        try:      
            poll = Poll()
            poll.new_poll(args[0],args[1:])
            await poll.send(ctx.channel)
        except Exception as e:
            await ctx.channel.send('@Eriim needs to fix this particular command :(')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !poll command: {e}')

def setup(bot):
    bot.add_cog(pollCog(bot))