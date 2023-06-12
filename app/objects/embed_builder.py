
from typing import List, Tuple
import discord
from app import util
import app.db as db
from app.db.models.character_db import CharacterDB
from app.db.models.discord_guild_db import DiscordGuildDB
from app.db.models.dungeon_run_db import DungeonRunDB
from app.raiderIO.models.character import Character

TANK_SPECS = ['Blood', 'Vengeance', 'Guardian', 'Brewmaster', 'Protection', 'Protection']
HEALER_SPECS = ['Restoration', 'Holy', 'Discipline', 'Mistweaver', 'Restoration', 'Holy']

footer = 'Data from Raider.IO'
description = 'This board only includes registered characters. If you have not registered your off-realm or out-of-guild character, please do so with /character register.'


def announce_guild_run_embed(announcement : db.AnnouncementDB = None,
                             color : discord.Color = discord.Color.green(),
                             dungeon_run : db.DungeonRunDB = None,
                             characters : List[db.CharacterDB] = None):
    """This function creates an embed for the guild dungeon run announcement.

    Args:
        title (str, optional): The title of the embed. Defaults to 'Guild Dungeon Run'.
        description (str, optional): The description of the embed. Defaults to 'Guild Dungeon Run'.
        color (discord.Color, optional): The color of the embed. Defaults to discord.Color.green().
        fields (list, optional): A list of fields to add to the embed. Defaults to None.

    Returns:
        discord.Embed: The embed object.
    """
    embed = discord.Embed(title=announcement.title, description=announcement.content, color=color)
    if characters is not None:
        for character in characters:
            embed.add_field(name=f'{character.name} - {character.class_name}' , value=f'Score: {character.score}\nClass Rank: {character.rank}', inline=False)
    return embed

def daily_guild_report_embed(discord_guild_db : DiscordGuildDB,
                             guild_run_list : List[Tuple[DungeonRunDB, List[CharacterDB]]] = None,
                             non_guild_run_list : List[Tuple[DungeonRunDB, List[CharacterDB]]] = None,
                             bot_user = None) -> discord.Embed:
    
    title = f'🏆 Daily Mythic+ Report for {discord_guild_db.discord_guild_name}'

    embed = discord.Embed(title=title, description=description, color=discord.Color.from_rgb(*util.hex_to_rgb('#c300ff')))

    embed.set_author(name='Mythic+ Bot', icon_url=bot_user.avatar, url='https://www.mythicplusbot.dev/')
    embed.add_field(name='------- Top Guild Runs in the last 24 hours -------', value='', inline=False)
    counter = 1
    if len(guild_run_list) == 0:
        embed.add_field(name='No runs for today.', value='', inline=False)

    for run, character_runs in guild_run_list:

        guild_run_characters = '| '
        tank = ''
        healer = ''
        dps = ''
        for character_run in character_runs:
            if character_run.spec_name in TANK_SPECS:
                tank = f'🛡️ [{character_run.character.name}]({character_run.character.url})  | '
            elif character_run.spec_name in HEALER_SPECS:
                healer = f'💚 [{character_run.character.name}]({character_run.character.url})  | '
            else:
                dps +=  f'⚔️ [{character_run.character.name}]({character_run.character.url})  | '

        guild_run_characters += tank + healer + dps

        plus = '+' * run.num_keystone_upgrades
        over_under = run.par_time_ms - run.clear_time_ms
        if over_under > 0:
            embed.add_field(name=str(counter)+ '.  '+ str(run.mythic_level)+(plus)+' | ' + run.name , value=guild_run_characters+f'\n[{util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))}/{util.time_without_leading_zeros(util.convert_millis(run.par_time_ms))} - {util.time_without_leading_zeros(util.convert_millis(over_under))} remaining.]({run.url})', inline=False)
        else:
            over_under = abs(over_under)
            embed.add_field(name=str(counter)+ '.  '+ str(run.mythic_level)+(plus)+' | ' + run.name , value=guild_run_characters+f'\n[{util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))}/{util.time_without_leading_zeros(util.convert_millis(run.par_time_ms))} - {util.time_without_leading_zeros(util.convert_millis(over_under))} over time.]({run.url})', inline=False)

        counter+=1

    embed.add_field(name='--------- Top Runs in the last 24 hours ---------',value='', inline=False)
    if len(non_guild_run_list) == 0:
        embed.add_field(name='No runs for today.', value='', inline=False)

    counter = 1
    for run, character_runs in non_guild_run_list:

        run_characters = '| '
        tank = ''
        healer = ''
        dps = ''
        for character_run in character_runs:
            if character_run.spec_name in TANK_SPECS:
                tank = f'🛡️ [{character_run.character.name}]({character_run.character.url})  | '
            elif character_run.spec_name in HEALER_SPECS:
                healer = f'💚 [{character_run.character.name}]({character_run.character.url})  | '
            else:
                dps +=  f'⚔️ [{character_run.character.name}]({character_run.character.url})  | '
                   
        run_characters += tank + healer + dps
        plus = '+' * run.num_keystone_upgrades
        over_under = run.par_time_ms - run.clear_time_ms
        if over_under > 0:
            embed.add_field(name=str(counter)+ '.  '+ str(run.mythic_level)+(plus)+' | ' + run.name, value=run_characters+f'\n[{util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))}/{util.time_without_leading_zeros(util.convert_millis(run.par_time_ms))} - {util.time_without_leading_zeros(util.convert_millis(over_under))} remaining.]({run.url})', inline=False)
        else:
            over_under = abs(over_under)
            embed.add_field(name=str(counter)+ '.  '+ str(run.mythic_level)+(plus)+' | ' + run.name, value=run_characters+f'\n[{util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))}/{util.time_without_leading_zeros(util.convert_millis(run.par_time_ms))} - {util.time_without_leading_zeros(util.convert_millis(over_under))} over time.]({run.url})', inline=False)
        counter+=1
    embed.set_footer(text=footer)

    return embed

def weekly_guild_report_embed( discord_guild_db : DiscordGuildDB,
                             guild_run_list : List[Tuple[DungeonRunDB, List[CharacterDB]]] = None,
                             non_guild_run_list : List[Tuple[DungeonRunDB, List[CharacterDB]]] = None,
                             bot_user = None) -> discord.Embed:
    
    title = f'🏆 Weekly Mythic+ Report for {discord_guild_db.discord_guild_name}'

    embed = discord.Embed(title=title, description=description, color=discord.Color.from_rgb(*util.hex_to_rgb('#c300ff')))

    embed.set_author(name='Mythic+ Bot', icon_url=bot_user.avatar, url='https://www.mythicplusbot.dev/')
    embed.add_field(name='------- Top Guild Runs in the last 7 days -------', value='', inline=False)
    counter = 1
    if len(guild_run_list) == 0:
        embed.add_field(name='No runs for this week.', value='', inline=False)

    for run, character_runs in guild_run_list:

        guild_run_characters = '| '
        tank = ''
        healer = ''
        dps = ''
        for character_run in character_runs:
            if character_run.spec_name in TANK_SPECS:
                tank = f'🛡️ [{character_run.character.name}]({character_run.character.url})  | '
            elif character_run.spec_name in HEALER_SPECS:
                healer = f'💚 [{character_run.character.name}]({character_run.character.url})  | '
            else:
                dps +=  f'⚔️ [{character_run.character.name}]({character_run.character.url})  | '
        
        guild_run_characters += tank + healer + dps
        
        plus = '+' * run.num_keystone_upgrades
        over_under = run.par_time_ms - run.clear_time_ms
        if over_under > 0:
            embed.add_field(name=str(counter)+ '.  '+ str(run.mythic_level)+(plus)+' | ' + run.name , value=guild_run_characters+f'\n[{util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))}/{util.time_without_leading_zeros(util.convert_millis(run.par_time_ms))} - {util.time_without_leading_zeros(util.convert_millis(over_under))} remaining.]({run.url})', inline=False)
        else:
            over_under = abs(over_under)
            embed.add_field(name=str(counter)+ '.  '+ str(run.mythic_level)+(plus)+' | ' + run.name , value=guild_run_characters+f'\n[{util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))}/{util.time_without_leading_zeros(util.convert_millis(run.par_time_ms))} - {util.time_without_leading_zeros(util.convert_millis(over_under))} over time.]({run.url})', inline=False)

        counter+=1

    embed.add_field(name='--------- Top Runs in the last 7 days ---------',value='', inline=False)
    if len(non_guild_run_list) == 0:
        embed.add_field(name='No runs for this week.', value='', inline=False)

    counter = 1
    for run, character_runs in non_guild_run_list:

        run_characters = '| '
        tank = ''
        healer = ''
        dps = ''
        for character_run in character_runs:
            if character_run.spec_name in TANK_SPECS:
                tank = f'🛡️ [{character_run.character.name}]({character_run.character.url})  | '
            elif character_run.spec_name in HEALER_SPECS:
                healer = f'💚 [{character_run.character.name}]({character_run.character.url})  | '
            else:
                dps +=  f'⚔️ [{character_run.character.name}]({character_run.character.url})  | '
                   
        run_characters += tank + healer + dps
        plus = '+' * run.num_keystone_upgrades
        over_under = run.par_time_ms - run.clear_time_ms
        if over_under > 0:
            embed.add_field(name=str(counter)+ '.  '+ str(run.mythic_level)+(plus)+' | ' + run.name, value=run_characters+f'\n[{util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))}/{util.time_without_leading_zeros(util.convert_millis(run.par_time_ms))} - {util.time_without_leading_zeros(util.convert_millis(over_under))} remaining.]({run.url})', inline=False)
        else:
            over_under = abs(over_under)
            embed.add_field(name=str(counter)+ '.  '+ str(run.mythic_level)+(plus)+' | ' + run.name, value=run_characters+f'\n[{util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))}/{util.time_without_leading_zeros(util.convert_millis(run.par_time_ms))} - {util.time_without_leading_zeros(util.convert_millis(over_under))} over time.]({run.url})', inline=False)
        counter+=1
    embed.set_footer(text=footer)

    return embed

def character_recent_runs(character: Character,                          
                          bot_user: discord.User = None):
    """Creates an embed for a character's recent runs."""
    title = character.name.capitalize()+"'s Recent Mythic+ Runs"                
    embed = discord.Embed(title=title, description= '', color=discord.Color.from_rgb(*util.hex_to_rgb(character.score_color)), url=character.url)
    embed.set_author(name='Mythic+ Bot', icon_url=bot_user.avatar, url='https://www.mythicplusbot.dev/')
    
    embed.add_field(name='Class', value=character.class_name, inline=True)
    embed.add_field(name='Last Spec', value=character.spec_name, inline=True)   
    embed.set_thumbnail(url=character.thumbnail_url)             

    for run in character.recent_runs:
        time = util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))
        
        plus = ''
        if run.num_keystone_upgrades > 0:
            plus = '+' * run.num_keystone_upgrades
            
        name = f'{plus}{str(run.mythic_level)} | {run.name}'
        over_under = run.par_time_ms - run.clear_time_ms
        
        
        if over_under > 0:
            over_under_string = util.time_without_leading_zeros(util.convert_millis(over_under))          
            value = f'Time: ** {time} ** | Remaining: {over_under_string} \n  [{run.affixes[0].name}, {run.affixes[1].name}, {run.affixes[2].name}]({run.url})'
        else:
            over_under = abs(over_under)
            over_under_string = util.time_without_leading_zeros(util.convert_millis(over_under))
            value = f'Time: ** {time} ** | Over Time: {over_under_string} \n  [{run.affixes[0].name}, {run.affixes[1].name}, {run.affixes[2].name}]({run.url})'
        embed.add_field(name=name, value=value, inline=False)
    embed.set_footer(text=footer)
    return embed

def character_best_runs(character: Character,
                        bot_user: discord.User = None):
    
    title = character.name.capitalize()+"'s Recent Mythic+ Runs"                
    embed = discord.Embed(title=title, description= '', color=discord.Color.from_rgb(*util.hex_to_rgb(character.score_color)), url=character.url)
    embed.set_author(name='Mythic+ Bot', icon_url=bot_user.avatar, url='https://www.mythicplusbot.dev/')
    
    embed.add_field(name='Class', value=character.class_name, inline=True)
    embed.add_field(name='Last Spec', value=character.spec_name, inline=True)
   
    embed.set_thumbnail(url=character.thumbnail_url)             

    for run in character.best_runs:
        time = util.time_without_leading_zeros(util.convert_millis(run.clear_time_ms))
        plus = ''
        if run.num_keystone_upgrades > 0:
            plus = '+' * run.num_keystone_upgrades
            
        name = f'{plus}{str(run.mythic_level)} | {run.name}'
        over_under = run.par_time_ms - run.clear_time_ms
                
        if over_under > 0:
            over_under_string = util.time_without_leading_zeros(util.convert_millis(over_under))
            value = f'Time: ** {time} ** | Remaining: {over_under_string} \n  [{run.affixes[0].name}, {run.affixes[1].name}, {run.affixes[2].name}]({run.url})'
        else:
            over_under = abs(over_under)
            over_under_string = util.time_without_leading_zeros(util.convert_millis(over_under))
            value = f'Time: ** {time} ** | Over Time: {over_under_string} \n  [{run.affixes[0].name}, {run.affixes[1].name}, {run.affixes[2].name}]({run.url})'
        embed.add_field(name=name, value=value, inline=False)
    embed.set_footer(text=footer) 
    return embed
