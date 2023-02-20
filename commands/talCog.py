import discord
from discord.ext import commands
from commands.dice import Dice
from commands.poll import Poll

class talCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog is initialized")
        
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("That command doesn't exist. Please try again.")
        if isinstance(error,commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing a required argument. Please try again.")

    @commands.command(name='ping', help='Pings the bot to see if it is online. (Latency in ms)')
    async def ping(self,ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
   
    @commands.command(name='poll', help='Lets users run a self-made poll for others to vote on.')
    @commands.has_role('Guild Members')
    async def poll(self, ctx, *args):
        print('test')
        poll = Poll()
        poll.new_poll(args[0],args[1:])
        poll.send(ctx.channel)
        

    @commands.command(name='roll', help='Rolls a dice with the specified number of sides.')
    async def roll(self,ctx, num_sides):
        dice = Dice(int(num_sides))
        await ctx.send(dice.roll())
  
async def setup(bot):
    await bot.add_cog(talCog(bot))


