from discord.ext import commands
from objects.poll.poll import Poll

class pollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Poll cog is initialized")
        
    @commands.command(name='poll', help='Lets users run a self-made poll for others to vote on.')
    @commands.has_role('Guild Members')
    async def poll(self, ctx, *args):        
        poll = Poll()
        poll.new_poll(args[0],args[1:])
        await poll.send(ctx.channel)

def setup(bot):
    bot.add_cog(pollCog(bot))