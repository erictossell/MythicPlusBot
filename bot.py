#---------------Take a Lap Discord Bot-----------------


#Imports
import asyncio
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from commands.talCog import talCog


#Load Environment variables
load_dotenv('configurations/main.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Set up Discord BOT with correct permissions
intents = discord.Intents(messages=True, guilds=True, members=True)
intents.message_content = True #v2
intents.presences = True #v2

bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name="for !help"))

async def load_extensions():
    await bot.load_extension('commands.talCog')

async def main():
    await load_extensions()
    await bot.start(TOKEN)

asyncio.run(main())



servers = {"Aerie-Peak", "Anvilmar", "Arathor","Antonidas","Azuremyst","Baelgun","Blade's Edge","Bladefist","Bronzebeard","Cenarius","Darrowmere","Draenor","Dragonblight","Echo-Isles","Galakrond",
"Gnomeregan","Hyjal","Kilrogg","Korialstrasz","Lightbringer","Misha","Moonrunner","Nordrassil","Proudmoore","Shadowsong","Shu'Halo","Silvermoon","Skywall","Suramar","Uldum","Uther","Velen",
"Windrunner","Blackrock","Blackwing Lair","Bonechewer","Boulderfist","Coilfang","Crushridge","Daggerspine","Dark Iron","Destromath","Dethecus","Dragonmaw","Dunemaul","Frostwolf","Gorgonnash",
"Gurubashi","Kalecgos","Kil'Jaeden","Lethon","Maiev","Nazjatar","Ner'zhul","Onyxia","Rivendare","Shattered Halls","Spinebreaker","Spirestone","Stonemaul","Stormscale","Tichondrius","Ursin","Vashj",
"Azjol-Nerub","Doomhammer","Icecrown","Perenolde","Terenas","Zangarmarsh","Kel'Thuzad","Darkspear","Deathwing","Bloodscalp","Nathrezim","Shadow Council","Aggramar","Alexstrasza","Alleria","Blackhand",
"Borean-Tundra","Cairne","Dawnbringer","Draka","Eitrigg","Fizzcrank","Garona","Ghostlands","Greymane","Grizzly-Hills","Hellscream","Hydraxis","Kael'thas","Khaz Modan","Kul-Tiras","Madoran","Malfurion","Malygos",
"Mok'Nathal","Muradin","Nesingwary","Quel'Dorei","Ravencrest","Rexxar","Runetotem","Sen'Jin","Staghelm","Terokkar","Thunderhorn","Vek'nilash","Whisperwind","Winterhoof","Aegwynn","Agamaggan","Akama","Archimonde",
"Azgalor","Azshara","Balnazzar","Blood Furnace","Burning-Legion","Cho'gall","Chromaggus","Detheroc","Drak'tharon","Drak'thul","Frostmane","Garithos","Gul'dan","Hakkar","Illidan","Korgath","Laughing Skull","Mal'Ganis",
"Malorne","Mug'thol","Stormreaver","Sargeras","The Underbog","Thunderlord","Wildhammer","Area-52","Arygos","Bloodhoof","Dalaran","Drenden","Durotan","Duskwood","Eldre'Thalas","Elune","Eonar","Exodar","Fenris",
"Garrosh","Gilneas","Grizzly-Hills","Kargath","Khadgar","Llane","Lothar","Medivh","Nazgrel","Norgannon","Shandris","Stormrage","Tanaris","Thrall","Trollbane","Turalyon","Uldaman","Undermine","Ysera","Zul'jin",
"Altar of Storms","Alterac Mountains","Andorhal","Anetheron","Anub'arak","Arthas","Auchindoun","Black Dragonflight","Bleeding Hollow","Burning Blade","Dalvengyr","Demon Soul","Eredar","Executus","Firetree",
"Gorefiend","Haomarush","Jaedenar","Lightning's Blade","Mannoroth","Magtheridon","Scilla","Shadowmoon","Shattered Hand","Skullcrusher","Smolderthorn","The Forgotten Coast","Tortheldrin","Warsong","Ysondre",
"Zuluhed"}

