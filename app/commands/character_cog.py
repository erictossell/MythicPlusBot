import os
from typing import Optional
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
import app.db as db
from app.objects.character_registration import RegisterView
import app.raiderIO as raiderIO
from app.util import hex_to_rgb

load_dotenv('configurations/main.env')
SUPPORT_SERVER_ID = os.getenv('SUPPORT_SERVER_ID')
SUPPORT_SERVER_CHANNEL_ID = os.getenv('SUPPORT_SERVER_CHANNEL_ID')


class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Character cog is initializing....')

    character = SlashCommandGroup(name='character', description='All commands related to characters')

    @character.command(name='runs', help='Gets the best Mythic+ runs for a character.')
    async def runs(self,ctx, name: str = None, realm: str = 'Area-52'):
        """Gets the best Mythic+ runs for a character."""
        try:
            
            if name is None:
                
                character_relationship = await db.get_discord_user_character_by_guild_user(ctx.author.id)
                if character_relationship is None:
                    await ctx.respond('You have not registered a character.  Please register a character with /set_main.')
                    return
                
            name = character_relationship.character.name if name is None else name  
            character_title = await db.get_character_by_name_realm(name.capitalize(), realm.capitalize())
            
            dungeon_list = await db.get_top10_runs_for_character_by_score(character_title)
            bot_user = await ctx.bot.fetch_user(1073958413488369794)
            embed = discord.Embed(title=f'Best Mythic+ Runs for {character_title.name}-{character_title.realm.capitalize()}', color=discord.Color.from_rgb(*hex_to_rgb('#c300ff')))
            embed.set_author(name='Mythic+ Bot', icon_url=bot_user.avatar, url='https://www.mythicplusbot.dev/')
            counter = 1
            for run, characters in dungeon_list:
                run_characters = '| '
                for character in characters:
                    run_characters += '['+character.name + f']({character.url})  | '
                embed.add_field(name=str(counter)+ '.  '+ run.name + '  |  ' + str(run.mythic_level)+'  |  +'+str(run.num_keystone_upgrades), value=run_characters+f'\n[Link to run]({run.url})', inline=False)
                counter+=1
                
            embed.set_footer(text='Data from Raider.IO(https://raider.io/)')
            embed.set_thumbnail(url=character_title.thumbnail_url)
            
            await ctx.respond(embed=embed)
            
        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(SUPPORT_SERVER_ID).fetch_channel(SUPPORT_SERVER_CHANNEL_ID)
           
            await error_channel.send(f'Error in !register command: {exception}')

    @character.command(name='set_main', help='Sets the default character for a user.')
    async def set_main(self, ctx, name: str, realm: Optional[str] = 'Area-52'):
        """Sets a user's default character.

        Args:
            ctx (context): The current discord context.
            character_name (str): The character name.
            character_realm (str, optional): The character realm. Defaults to 'Area-52'.
        """
        try:
            discord_user_id = ctx.author.id
            discord_guild_id = ctx.guild.id
            character_io = await raiderIO.get_character(name, realm)
            
            if character_io is None:
                await ctx.respond(f'Character {name}-{realm} does not exist.')
                return
            
            else:
                
                character = await db.get_character_by_name_realm(name.capitalize(), realm.capitalize())
                main_char = await db.get_discord_user_character_by_guild_user(discord_user_id)
                
                if main_char is None:
                    
                    default = db.DiscordUserCharacterDB(discord_user_id=discord_user_id, character_id=character.id)
                    main_char = await db.add_discord_user_character(default)
                    
                    embed = discord.Embed(title=f'Success! Your main character has been updated to: {main_char[1]}-{main_char[2].capitalize()}.', color=discord.Color.green())
                    embed.set_thumbnail(url=character.thumbnail_url)
                    await ctx.respond(embed=embed)
                    
                elif main_char is not None: 
                    
                    main_char = await db.update_discord_user_character(discord_user_id= discord_user_id,
                                                                character=character)
                    
                    embed = discord.Embed(title=f'Success! Your main character has been updated to: {main_char[1]}-{main_char[2].capitalize()}.', color=discord.Color.green())
                    embed.set_thumbnail(url=character.thumbnail_url)  
                            
                    await ctx.respond(embed=embed)
                    
                else:
                    embed = discord.Embed(title=f'Something went wrong, contact support for assitance.', color=discord.Color.red())
                    
                    await ctx.respond(embed=embed)

        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(SUPPORT_SERVER_ID).fetch_channel(SUPPORT_SERVER_CHANNEL_ID)
           
            await error_channel.send(f'Error in !register command: {exception}')

    @character.command(name='register', help='Register a character that is not in the guild.')
    async def register(self, ctx):
        """The register command allows a user to register a character that is not in the guild. 
            This command will DM the user a button to click to register their character.

        Args:
            ctx (context): The current discord context.
        """
        try:
            
            await ctx.respond('Please check your DMs for the registration link.')
            
            user = await ctx.bot.fetch_user(ctx.author.id)
            channel = await user.create_dm()
            
            if ctx.guild is None:
                await channel.send('Call the register command from within the Discord server you would like to register a character to.\nThis is used for analytics purposes.')
            
            else:                
                view = RegisterView(ctx.guild.id)
                await channel.send('Please click the button below to register your character. This message will self destruct in 60 seconds.', view=view, delete_after=60)
        
        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(SUPPORT_SERVER_ID).fetch_channel(SUPPORT_SERVER_CHANNEL_ID)
           
            await error_channel.send(f'Error in !register command: {exception}')

    @character.command(name='profile', help='View a character\'s profile.')
    async def profile(self, ctx, name: str = None, realm: str = 'Area-52'):
        """This command returns a character's profile.

        Args:
            ctx (context): The current discord context.
            character_name (str): Character name.
            realm (str): Realm of the character.
        """
        try:
            async with ctx.typing():
                if not name:
                    
                    if ctx.guild:
                        
                        main_char = await db.get_discord_user_character_by_guild_user(ctx.author.id)
                        char = await db.get_character_by_name_realm(main_char.character.name, main_char.character.realm)
                        
                        if char:
                            name, realm = char.name, char.realm
                            
                        else:
                            await ctx.respond('Please provide a character name and realm or set a main character.')
                            return                    
                    else:
                        await ctx.respond('Please provide a character name and realm.')
                        return

                character = await raiderIO.get_character(name, realm)
                
                await ctx.respond(embed=character.get_character_embed())
                
                character_db = await db.get_character_by_name_realm(name.capitalize(), realm.capitalize())
                
                if character_db is not None:
                    character_db = await db.update_character(character)
                    
                

        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(SUPPORT_SERVER_ID).fetch_channel(SUPPORT_SERVER_CHANNEL_ID)
           
            await error_channel.send(f'Error in !register command: {exception}')

    @character.command(name='recent_runs', help='View a character\'s recent runs directly from RaiderIO.')
    async def recent_runs(self, ctx, name: str = None, realm: str = None):
        """This command returns the recent runs for a given character.

        Args:
            ctx (context): The current discord context.
        """
        try:
            async with ctx.typing():
                if not name:
                    
                    if ctx.guild:
                        
                        main_char = await db.get_discord_user_character_by_guild_user(ctx.author.id)
                        char = await db.get_character_by_name_realm(main_char.character.name, main_char.character.realm)
                        
                        if char:
                            name, realm = char.name, char.realm
                            
                        else:
                            await ctx.respond('Please provide a character name and realm or set a main character.')
                            return                    
                    else:
                        await ctx.respond('Please provide a character name and realm.')
                        return
                    
                if not realm:
                    realm = 'Area-52'
                    
                character = await raiderIO.get_character(name, realm)
                
                await ctx.respond(embed=character.get_recent_runs_embed())
                
                character_db = await db.get_character_by_name_realm(name.capitalize(), realm.capitalize())
                
                if character_db is not None:
                    character_db = await db.update_character(character)

        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(SUPPORT_SERVER_ID).fetch_channel(SUPPORT_SERVER_CHANNEL_ID)
           
            await error_channel.send(f'Error in !register command: {exception}') 

    @character.command(name='best_runs', help='Usage: !best <character name> <realm> (optional on Area-52)')
    async def best_runs(self, ctx, name: str = None, realm: str = None):
        """The best command returns the best runs for a given character.

        Args:
            ctx (context): Pass the current discord context
            character_name (str): Character name
            realm (str): Realm of the character
        """
        try:
            async with ctx.typing():
                if not name:
                    
                    if ctx.guild:
                        
                        main_char = await db.get_discord_user_character_by_guild_user(ctx.author.id)
                        char = await db.get_character_by_name_realm(main_char.character.name, main_char.character.realm)
                        
                        if char:
                            name, realm = char.name, char.realm
                            
                        else:
                            await ctx.respond('Please provide a character name and realm or set a main character.')
                            return                    
                    else:
                        await ctx.respond('Please provide a character name and realm.')
                        return
                    
                if not realm:
                    realm = 'Area-52'

                character = await raiderIO.get_character(name, realm)
                await ctx.respond(embed=character.get_best_runs_embed())
                
                character_db = await db.get_character_by_name_realm(name.capitalize(), realm.capitalize())
                
                if character_db is not None:
                    character_db = await db.update_character(character)

        except Exception as exception:
            print(exception)
            await ctx.respond('Something went wrong :( Talk to the bot developer for help.')
            error_channel = await ctx.bot.fetch_guild(SUPPORT_SERVER_ID).fetch_channel(SUPPORT_SERVER_CHANNEL_ID)
           
            await error_channel.send(f'Error in !register command: {exception}')

    

def setup(bot):
    bot.add_cog(Character(bot))
    print('Character cog loaded successfully.')
    