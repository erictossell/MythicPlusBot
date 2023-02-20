from discord.ext import commands

class errorsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Error events are initialized")
        
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("That command doesn't exist. Please try again.")
        if isinstance(error,commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing a required argument. Please try again.")


async def setup(bot):
    await bot.add_cog(errorsCog(bot))