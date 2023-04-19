import discord

import app.db as db

def announce_guild_run_embed(announcement : db.AnnouncementDB = None,
                             color : discord.Color = discord.Color.green(),
                             dungeon_run : db.DungeonRunDB = None,
                             characters : list[db.CharacterDB] = None):
    """This function creates an embed for the guild dungeon run announcement.

    Args:
        title (str, optional): The title of the embed. Defaults to 'Guild Dungeon Run'.
        description (str, optional): The description of the embed. Defaults to 'Guild Dungeon Run'.
        color (discord.Color, optional): The color of the embed. Defaults to discord.Color.green().
        fields (list, optional): A list of fields to add to the embed. Defaults to None.

    Returns:
        discord.Embed: The embed object.
    """
    embed = discord.Embed(title=announcement.title, description=announcement.description, color=color)
    if characters is not None:
        for character in characters:
            embed.add_field(name=f'{character.name} - {character.spec_name}' , value=f'Score: {character.score}\nClass Rank: {character.rank}', inline=False)
    return embed