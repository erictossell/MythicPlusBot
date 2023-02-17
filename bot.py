#---------------Take a Lap Discord Bot-----------------


#Imports
import os

import discord
import random
from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import datetime, timedelta

#Load Environment variables
load_dotenv('main.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Global variables
guildIOURL = 'https://raider.io/guilds/us/area-52/Take%20a%20Lap/mythic-plus-characters/season-df-1'


#Set up Discord BOT with correct permissions
intents = discord.Intents(messages=True, guilds=True, members=True)
intents.message_content = True #v2
bot = commands.Bot(command_prefix='!', intents=intents)

class lastPoll:
    def __init__(self):
        self.poll_id = 0        
        self.poll_options = {}       

lastResult = lastPoll()

#!Poll - Bot Command
@bot.command(name='poll', help='Lets users run a self-made poll for others to vote on.')
@commands.has_role('Guild Members')
async def poll(ctx, *args):
    poll_options = ''       
    for i in range(len(args)):         
        emoji = chr(0x1F1E6 + i)
        poll_options = '\n'.join([poll_options, f'{emoji} {args[i]}'])
        lastResult.poll_options[emoji] = args[i]
    response = f"----------Take a Lap Discord Poll---------{poll_options}"
    message = await ctx.send(response)
    
    for i in range(len(args)):
        emoji = chr(0x1F1E6 + i)        
        await message.add_reaction(emoji)
    lastResult.poll_id = message.id
    await ctx.send(f"Poll created with ID: {lastResult.poll_id}. Use !pollresults to print the results.")
    
@bot.command(name='pollresults')
async def poll_results(ctx):
    channel = ctx.channel
    poll_results = 'Here are the results of the last poll:\n'
    if(lastResult.poll_id == 0):
        await ctx.send('There are no polls to show results for.')
        return
    else:
        message = await channel.fetch_message(lastResult.poll_id)
        
        for i in range(len(lastResult.poll_options)):
            emoji = chr(0x1F1E6 + i)
            reaction = discord.utils.get(message.reactions, emoji=emoji)
            reaction_count = reaction.count
        
            poll_results += f'{lastResult.poll_options[emoji]} : {reaction_count}\n'
        await ctx.send(poll_results)
    
@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, num_sides: int):
    
    if num_sides < 1:
        await ctx.send("Please enter a number greater than 0.")
    else:
        roll_result = random.randint(0, num_sides)
        await ctx.send(f"You rolled a {roll_result} (between 0 and {num_sides}).")    
    
    #await ctx.send(f"Votes for {emoji} : {reaction_count}")

#!Rating - Bot Command
@bot.command(name='ratings', help='This call returns the Take a Lap guild M+ Score page')
async def ratings(ctx):    
    await ctx.send('Take a Lap Mythic+: '+ guildIOURL)

@bot.command(name='rating', help='This call returns the Take a Lap guild M+ Score page')
async def rating(ctx, *args):    
    preURL = 'https://raider.io/characters/us/'
    defaultServer = 'Area-52'
    arguments = len(args)
    if arguments == 2:
        if args[0].lower() == defaultServer.lower():
            URL = preURL + args[0] + '/' + args[1]
            await ctx.send(args[1] + ' - ' + args[0] + ': '+ URL)
        elif args[1].lower() == defaultServer:
            URL = preURL + args[1] + '/' + args[0]
            await ctx.send(args[0] + ' - ' + args[1] + ': '+ URL)
        else:
            await ctx.send('The server name you entered is not from Area-52')
    else: 
        URL = preURL + defaultServer + '/' + args[0]
        await ctx.send(args[0] + ' - ' + defaultServer + ': '+ URL)
        
event_days = [1, 2]
event_start = '19:30'
event_end = '22:30'
event_name = ["VoI Heroic", "VoI Heroic"]
event_message = "Weekly Raid Night! 7:30pm EST"
bot_bunker_id = 1074546599239356498
raid_lobby_id = 804157941732474905
async def event_exists(name):
    channel = bot.get_channel(bot_bunker_id)
    async for message in channel.history():
        if message.author == bot.user and message.content ==name:
            return True
    return False

async def create_event(name, start, end, description):   
    raid_channel = bot.get_channel(raid_lobby_id)
    event = await raid_channel.create_event(name=name, start=start, end=end, description=description)
    return event

async def check_and_create_events():
    for name in event_name:
        if not await event_exists(name):
            time = f'{event_days} {event_start}'
            await create_event(name, time)

@bot.command(name='events', help='Creates events for the week')
async def events(ctx):
    #await check_and_create_events()
    await create_event(event_name[0], event_days[0], event_start, event_end, event_message)
    await ctx.send('Events created')

#@tasks.loop(minutes=1)
#async def create_events():
    #now = datetime.utcnow()
    #if now.weekday() in event_days and now.hour == event_time.hour and now.minute == event_time.minute:
        #channel = bot.get_channel(raid_lobby_id)
        #event = await channel.create_event(name="Raid Night", start=event_time + timedelta(hours=1),end=event +timedelta(hours=2),description="Raid Night! 7:30pm EST")
        #bot_bunker = bot.get_channel(bot_bunker_id)
        #await bot_bunker.send(event_message)

@bot.event
async def on_ready():
    #create_events.start()
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user.name} has connected to {guild}!')

# Error - Bot Event
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

#Start the Bot
bot.run(TOKEN)



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