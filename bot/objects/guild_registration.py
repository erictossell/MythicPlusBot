import discord
from discord.ui import Button, View, Modal, InputText

import bot.db as db
from bot.logger import Logger as logger


class RegisterGuildView(View):
    """Creates the register and unregister buttons."""

    def __init__(self, discord_guild_id: int, *args, **kwargs) -> None:
        """The constructor for the RegisterButton class.

        Args:
            discord_guild_id (int): The discord guild id.
        """
        super().__init__(*args, **kwargs)
        self.discord_guild_id = discord_guild_id
        self.add_item(RegisterGuildButton(discord_guild_id=self.discord_guild_id))


class RegisterGuildButton(Button):
    def __init__(self, discord_guild_id: int):
        super().__init__(label="Register", style=discord.ButtonStyle.green, emoji="📄")
        self.discord_guild_id = discord_guild_id

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(
                RegisterGuildModal(
                    title="Register your guild", discord_guild_id=self.discord_guild_id
                )
            )

        except Exception as exception:
            print("Error occurred:", exception)
            await interaction.message.delete()
            await interaction.response.send_message(
                "Error occurred while processing your request. Please try again later.",
                ephemeral=True,
            )
            await logger.build_manual_log(
                logger,
                "guild_registration",
                "RegisterGuildButton",
                f"Error occurred while processing your request. Please try again later. Error: {exception}",
            )


class RegisterGuildModal(Modal):
    def __init__(self, discord_guild_id: int, *args, **kwargs) -> None:
        """The constructor for the RegisterModal class."""
        super().__init__(*args, **kwargs)
        self.discord_guild_id = discord_guild_id
        self.add_item(InputText(label="World of Warcraft Guild Name", required=True))
        self.add_item(InputText(label="Guild realm", required=True))
        self.add_item(InputText(label="Guild region", required=True))

    async def callback(self, interaction: discord.Interaction) -> None:
        """Register a guild to the database.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        try:
            wow_guild_name = self.children[0].value
            wow_realm = self.children[1].value.capitalize()
            wow_region = self.children[2].value.lower()

            if not wow_guild_name:
                await interaction.response.send_message(
                    "Guild name is required.", ephemeral=True
                )
                return
            elif not wow_realm:
                await interaction.response.send_message(
                    "Guild realm is required.", ephemeral=True
                )
                return
            elif not wow_region:
                await interaction.response.send_message(
                    "Guild region is required.", ephemeral=True
                )
                return
            else:
                existing_guild = await db.get_discord_guild_by_id(
                    int(self.discord_guild_id)
                )
                if existing_guild:
                    existing_game_guild = await db.get_game_guild_by_name_realm(
                        wow_guild_name, wow_realm
                    )

                    if existing_game_guild:
                        discord_game_guild = db.DiscordGameGuildDB(
                            discord_guild_id=existing_guild.id,
                            game_guild_id=existing_game_guild.id,
                            is_crawlable=True,
                        )

                        await db.add_discord_game_guild(discord_game_guild)

                        embed = discord.Embed(
                            title=f"{existing_game_guild.name} WoW Guild Updated",
                            description=f"Your have added the guild {existing_game_guild.name} - {existing_game_guild.realm} in the {existing_game_guild.region.upper()} region to your Discord Server.",
                            color=0x00FF00,
                        )
                        await interaction.response.send_message(
                            embed=embed, ephemeral=True
                        )
                        await logger.build_item_log(
                            logger,
                            "success",
                            existing_game_guild,
                            f"Guild {existing_game_guild.name} - {existing_game_guild.realm} in the {existing_game_guild.region.upper()} region has been added to the Discord Server {existing_guild.name}",
                        )

                    else:
                        game_guild = db.GameGuildDB(
                            name=wow_guild_name, realm=wow_realm, region=wow_region
                        )

                        discord_game_guild = db.DiscordGameGuildDB(
                            discord_guild_id=existing_guild.id,
                            game_guild=game_guild,
                            is_crawlable=True,
                        )

                        await db.add_discord_game_guild(discord_game_guild)

                        embed = discord.Embed(
                            title=f"{game_guild.name} WoW Guild Updated",
                            description=f"Your have added the guild {game_guild.name} - {game_guild.realm} in the {game_guild.region.upper()} region to your Discord Server.",
                            color=0x00FF00,
                        )
                        await interaction.response.send_message(
                            embed=embed, ephemeral=True
                        )
                        await logger.build_item_log(
                            logger,
                            "success",
                            game_guild,
                            f"Guild {game_guild.name} - {game_guild.realm} in the {game_guild.region.upper()} region has been added to the Discord Server {existing_guild.name}",
                        )

        except Exception as exception:
            print("Error occurred:", exception)
            await interaction.message.delete()
            await interaction.response.send_message(
                "Error occurred while processing your request. Please try again later.",
                ephemeral=True,
            )
            await logger.build_manual_log(
                logger,
                "guild_registration",
                "RegisterGuildModal",
                f"Error occurred while processing your request. Please try again later. Error: {exception}",
            )
