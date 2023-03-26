import discord
from discord.ext import commands
class Poll():
    def __init__(self):       
        self.poll_id = 0 
        self.question = ''
        self.answers = {}    
        self.votes = {}         

    def new_poll(self,question, answers):
        self.question = question
        self.answers = answers
        self.votes = {answer: 0 for answer in answers}       

    def update_vote(self, votes):
        self.votes = votes

    async def send(self, channel):
        embed = discord.Embed(title='Take a Lap Discord Poll', description=self.question, color=discord.Color.blue())
        for option in self.answers:
            embed.add_field(name=option, value=self.votes[option], inline=False)
        
        message = await channel.send(embed=embed)
        for i in range(len(self.answers)):
            await message.add_reaction(chr(0x1F1E6 + i))