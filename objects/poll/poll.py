import discord
class Poll():
    """This class represents poll objects within the bot.
    """
    def __init__(self) -> None:       
        self.poll_id = 0 
        self.question = ''
        self.answers = {}    
        self.votes = {}         

    def new_poll(self,question, answers) -> None:
        """Creates a new poll object.

        Args:
            question (string): The question that the poll is asking.
            answers (string): The options that the user can choose from.
        """
        self.question = question
        self.answers = answers
        self.votes = {answer: 0 for answer in answers}       

    def update_vote(self, votes) -> None:
        """Updates the number of votes for each answer.

        Args:
            votes (list of int): The number of votes for each answer.
        """
        self.votes = votes

    async def send(self, channel) -> None:
        """Send the poll to the specified channel.

        Args:
            channel (channel): the channel object to send the poll to.
        """
        embed = discord.Embed(title='Take a Lap Discord Poll', description=self.question, color=discord.Color.blue())
        for option in self.answers:
            embed.add_field(name=option, value=self.votes[option], inline=False)
        
        message = await channel.send(embed=embed)
        for i in range(len(self.answers)):
            await message.add_reaction(chr(0x1F1E6 + i))