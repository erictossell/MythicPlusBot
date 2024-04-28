import discord


# This is not used currently. It is a placeholder for the future.
class PollView(discord.ui.View):
    """The PollView class represents the view for the poll command.

    Args:
        discord (ui.View): The parent class for the PollView class.
    """

    @discord.ui.select(
        placeholder="Select a poll type",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Yes/No",
                description="Yes or No",
            ),
            discord.SelectOption(
                label="Multiple Choice",
                description="Multiple Choice",
            ),
        ],
    )
    async def select_poll_option(self, select, interaction):
        await interaction.response.send_message(
            "You voted for {}".format(select.values[0])
        )
