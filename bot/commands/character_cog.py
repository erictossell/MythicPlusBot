import os

from typing import Optional
from datetime import datetime
from dotenv import load_dotenv

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

import bot.db as db
import bot.objects.embed_builder as embed_builder
import bot.raiderIO as raiderIO
from bot.objects.character_registration import RegisterView

load_dotenv("configurations/main.env")
SUPPORT_SERVER_ID = os.getenv("SUPPORT_SERVER_ID")
SUPPORT_CHANNEL_ID = os.getenv("SUPPORT_CHANNEL_ID")


class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Character cog is initializing....")

    character = SlashCommandGroup(
        name="character", description="All commands related to characters"
    )

    @character.command(name="set_main", help="Sets the default character for a user.")
    async def set_main(self, ctx, name: str, realm: Optional[str] = "Area-52"):
        """Set your default character for all character commands.

        Args:
            ctx (context): The current discord context.
            character_name (str): The character name.
            character_realm (str, optional): The character realm. Defaults to 'Area-52'.
        """
        try:
            discord_user_id = ctx.author.id
            character_io = await raiderIO.get_character(name, realm)

            if character_io is None:
                await ctx.respond(f"Character {name}-{realm} does not exist.")
                return

            else:
                character = await db.get_character_by_name_realm(
                    name.capitalize(), realm.capitalize()
                )
                main_char = await db.get_discord_user_character_by_guild_user(
                    discord_user_id
                )

                if main_char is None:
                    default = db.DiscordUserCharacterDB(
                        discord_user_id=discord_user_id, character_id=character.id
                    )
                    main_char = await db.add_discord_user_character(default)

                    embed = discord.Embed(
                        title=f"Success! Your main character has been updated to: {main_char[1]}-{main_char[2].capitalize()}.",
                        color=discord.Color.green(),
                    )
                    embed.set_thumbnail(url=character.thumbnail_url)
                    await ctx.respond(embed=embed)

                elif main_char is not None:
                    main_char = await db.update_discord_user_character(
                        discord_user_id=discord_user_id, character=character
                    )

                    embed = discord.Embed(
                        title=f"Success! Your main character has been updated to: {main_char[1]}-{main_char[2].capitalize()}.",
                        color=discord.Color.green(),
                    )
                    embed.set_thumbnail(url=character.thumbnail_url)

                    await ctx.respond(embed=embed)

                else:
                    embed = discord.Embed(
                        title=f"Something went wrong, contact support for assitance.",
                        color=discord.Color.red(),
                    )

                    await ctx.respond(embed=embed)

        except Exception as exception:
            print(exception)
            await ctx.respond(
                "Something went wrong :( Talk to the bot developer for help."
            )
            error_channel = await ctx.bot.fetch_guild(
                int(SUPPORT_SERVER_ID)
            ).fetch_channel(int(SUPPORT_CHANNEL_ID))

            await error_channel.send(f"Error in !register command: {exception}")

    @character.command(
        name="register", help="Register a character that is not in the guild."
    )
    async def register(self, ctx):
        """Register individual characters to the Discord server.

        Args:
            ctx (context): The current discord context.
        """
        try:
            await ctx.respond("Please check your DMs for the registration button.")

            user = await ctx.bot.fetch_user(ctx.author.id)
            channel = await user.create_dm()

            if ctx.guild is None:
                await channel.send(
                    "Call the register command from within the Discord server you would like to register a character to.\nThis is used for analytics purposes."
                )

            else:
                view = RegisterView(ctx.guild.id)
                await channel.send(
                    "Please click the button below to register your character. This message will self destruct in 300 seconds.",
                    view=view,
                    delete_after=300,
                )

        except Exception as exception:
            print(exception)
            await ctx.respond(
                "Something went wrong :( Talk to the bot developer for help."
            )
            error_channel = await ctx.bot.fetch_guild(
                int(SUPPORT_SERVER_ID)
            ).fetch_channel(int(SUPPORT_CHANNEL_ID))

            await error_channel.send(f"Error in !register command: {exception}")

    @character.command(
        name="recent_runs",
        help="View a character's recent runs directly from RaiderIO.",
    )
    async def recent_runs(self, ctx, name: str = None, realm: str = None):
        """Display the most recent runs for a character.

        Args:
            ctx (context): The current discord context.
        """
        try:
            async with ctx.typing():
                if not name:
                    if ctx.guild:
                        main_char = await db.get_discord_user_character_by_guild_user(
                            ctx.author.id
                        )
                        char = await db.get_character_by_name_realm(
                            main_char.character.name, main_char.character.realm
                        )

                        if char:
                            name, realm = char.name, char.realm

                        else:
                            await ctx.respond(
                                "Please provide a character name and realm or set a main character."
                            )
                            return
                    else:
                        await ctx.respond("Please provide a character name and realm.")
                        return

                if not realm:
                    realm = "Area-52"

                bot_user = await ctx.bot.fetch_user(1073958413488369794)
                character = await raiderIO.get_character(name, realm)
                embed = embed_builder.character_recent_runs(character, bot_user)
                await ctx.respond(embed=embed)

                character_db = await db.get_character_by_name_realm(
                    name.capitalize(), realm.capitalize()
                )

                if character_db is not None:
                    character.last_crawled_at = datetime.strptime(
                        character.last_crawled_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    character_db = await db.update_character(character)

        except Exception as exception:
            print(exception)
            await ctx.respond(
                "Something went wrong :( Talk to the bot developer for help."
            )
            error_channel = await ctx.bot.fetch_guild(
                int(SUPPORT_SERVER_ID)
            ).fetch_channel(int(SUPPORT_CHANNEL_ID))

            await error_channel.send(f"Error in !register command: {exception}")

    @character.command(
        name="best_runs",
        help="Usage: !best <character name> <realm> (optional on Area-52)",
    )
    async def best_runs(self, ctx, name: str = None, realm: str = None):
        """Display the best runs for a character.

        Args:
            ctx (context): Pass the current discord context
            character_name (str): Character name
            realm (str): Realm of the character
        """
        try:
            async with ctx.typing():
                if not name:
                    if ctx.guild:
                        main_char = await db.get_discord_user_character_by_guild_user(
                            ctx.author.id
                        )
                        char = await db.get_character_by_name_realm(
                            main_char.character.name, main_char.character.realm
                        )

                        if char:
                            name, realm = char.name, char.realm

                        else:
                            await ctx.respond(
                                "Please provide a character name and realm or set a main character."
                            )
                            return
                    else:
                        await ctx.respond("Please provide a character name and realm.")
                        return

                if not realm:
                    realm = "Area-52"
                bot_user = await ctx.bot.fetch_user(1073958413488369794)
                character = await raiderIO.get_character(name, realm)
                embed = embed_builder.character_best_runs(character, bot_user)
                await ctx.respond(embed=embed)

                character_db = await db.get_character_by_name_realm(
                    name.capitalize(), realm.capitalize()
                )

                if character_db is not None:
                    character.last_crawled_at = datetime.strptime(
                        character.last_crawled_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    character_db = await db.update_character(character)

        except Exception as exception:
            print(exception)
            await ctx.respond(
                "Something went wrong :( Talk to the bot developer for help."
            )
            error_channel = await ctx.bot.fetch_guild(
                int(SUPPORT_SERVER_ID)
            ).fetch_channel(int(SUPPORT_CHANNEL_ID))

            await error_channel.send(f"Error in !register command: {exception}")


def setup(bot):
    bot.add_cog(Character(bot))
    print("Character cog has loaded successfully.")
