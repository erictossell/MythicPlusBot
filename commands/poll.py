import discord

class Poll:
    def __init__(self):
        self.poll_id = 0 
        self.question = ''
        self.answers = {}    
        self.votes = {}
        print("Poll is initialized")   

    def new_poll(self,question, answers):
        self.question = question
        self.answers = answers
        self.votes = {answer: 0 for answer in answers}
        print("Poll is new") 

    def update_vote(self, votes):
        self.votes = votes

    async def send(self, channel):
        embed = discord.Embed(title=self.question, description='\n'.join([f'{i+1}. {answer}' for i, answer in enumerate(self.answers)]), color=discord.Color.blue())
        for option in self.answers:
            embed.add_field(name=option, value=self.votes[option], inline=True)
        
        message = await channel.send(embed=embed)
        for i in range(len(self.answers)):
            await message.add_reaction(chr(0x1F1E6 + i))

            
        
 