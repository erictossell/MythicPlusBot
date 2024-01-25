# ---------------Take a Lap Discord Bot-----------------
# Description: This file contains the main function for the bot.
# Author: Eriim

# Imports
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SUPPORT_CHANNEL_ID = os.getenv("SUPPORT_CHANNEL_ID")
SUPPORT_SERVER_ID = os.getenv("SUPPORT_SERVER_ID")

# Set up Discord BOT with correct permissions
intents = discord.Intents(guilds=True, members=True)
intents.guilds = True

bot = discord.Bot(
    intents=intents,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="for slash commands!"
    ),
)

cogs_list = [
    "bot.commands.general_cog",
    "bot.commands.admin_cog",
    "bot.commands.member_events_cog",
    "bot.commands.guild_cog",
    "bot.commands.character_cog",
    "bot.commands.announcement_cog",
]


def load_extensions():
    """Load the cogs from the cogs_list."""
    for cog in cogs_list:
        bot.load_extension(cog)


def main():
    """The main function for the bot."""
    load_extensions()
    bot.run(TOKEN)


main()
