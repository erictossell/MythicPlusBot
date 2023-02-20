from discord.ext import commands
from objects.poll import Poll

class pollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Poll cog is initialized")
        
    @commands.command(name='poll', help='Lets users run a self-made poll for others to vote on.')
    @commands.has_role('Guild Members')
    async def poll(self, ctx, *args):
        print('test')
        poll = Poll()
        poll.new_poll(args[0],args[1:])
        await poll.send(ctx.channel)

async def setup(bot):
    await bot.add_cog(pollCog(bot))