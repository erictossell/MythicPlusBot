from typing import Optional
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
import app.db as db
from app.objects.registration import RegisterView
import app.raiderIO as raiderIO

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Character cog is initializing....')
    
    character = SlashCommandGroup(name='character', description='All commands related to characters')
    
    @character.command(name='runs', help='Gets the best Mythic+ runs for a character.')
    async def runs(self,ctx, name: str = None, realm: str = 'area-52'):
        """Gets the best Mythic+ runs for a character."""
        try:       
            if name is None:
                character_relationship = await db.lookup_default_character(ctx.guild.id,ctx.author.id)
                if character_relationship is None:
                    await ctx.respond('You have not registered a character.  Please register a character with /set_main.')
                    return
            name = character_relationship.character.name if name is None else name  
            character_title = await db.lookup_character(name, realm)
            run_list = await db.get_all_runs_for_character(character_title)
            for run in run_list:
                characters_list = await db.get_all_characters_for_run(run.id)
                run_characters = '| '
                for character in characters_list:
                    run_characters += '['+character.name + f']({character.url})  | '
                run.characters = run_characters
            embed = discord.Embed(title=f'🏆 Best Runs for {character_title.name}', description= f'[{character_title.name}\'s Raider.IO Profile]({character_title.url})', color=discord.Color.green())
            counter = 1
            for run in run_list:
                embed.add_field(name=str(counter)+ '.  '+ run.name + '  |  ' + str(run.mythic_level)+'  |  +'+str(run.num_keystone_upgrades), value=run.characters+f'\n[Link to run]({run.url})', inline=True)
                counter+=1
            embed.set_footer(text='Data from Raider.IO(https://raider.io/)')
            await ctx.respond(embed=embed)
        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !charRuns command: {exception}')
    
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
                character = await db.lookup_character(name, realm)
                main_char = await db.lookup_default_character(discord_guild_id, discord_user_id)
                if main_char is None:
                    default = db.DefaultCharacterDB(discord_user_id=discord_user_id, discord_guild_id=discord_guild_id, character_id=character.id)
                    main_char = await db.add_default_character(default)
                    await ctx.respond(f'Your main character has been set to: {main_char[1]}-{main_char[2]}.')
                elif main_char is not None: 
                    main_char = await db.update_default_character(discord_user_id= discord_user_id,
                                                                discord_guild_id =discord_guild_id,
                                                                character=character)                
                    await ctx.respond(f'Your main character has been set to: {main_char[1]}-{main_char[2]}.')
                else:
                    await ctx.respond(f'Something went wrong, contact support for assitance.')

        except Exception as exception:
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !register command: {exception}')

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
            await ctx.channel.send('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !register command: {exception}')
    
    @character.command(name='profile', help='View a character\'s profile.')
    async def profile(self, ctx, name: str = None, realm: str = 'Area-52'):
        """This command returns a character's profile.

        Args:
            ctx (context): The current discord context.
            character_name (str): Character name.
            realm (str): Realm of the character.
        """
        try:
            if not name:
                if ctx.guild:
                    main_char = await db.lookup_default_character(ctx.guild.id, ctx.author.id)
                    char = await db.lookup_character(main_char.character.name, main_char.character.realm)
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
            await ctx.respond(embed=character.get_character_embed())

        except Exception as exception:
            await ctx.respond(f' I was not able to find a character with name: {name}. Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !character command: {exception}')
    
    @character.command(name='recent_runs', help='View a character\'s recent runs directly from RaiderIO.')
    async def recent_runs(self, ctx, name: str = None, realm: str = None):
        """This command returns the recent runs for a given character.

        Args:
            ctx (context): The current discord context.
        """
        try:
            if not name:
                main_char = await db.lookup_default_character(ctx.guild.id, ctx.author.id)
                char = await db.lookup_character(main_char.character.name, main_char.character.realm)
                if char:
                    name, realm = char.name, char.realm
                else:
                    await ctx.respond('Please provide a character name and realm or set a main character.')
                    return
            if not realm:
                realm = 'Area-52'
            character = await raiderIO.get_character(name, realm)
            await ctx.respond(embed=character.get_recent_runs_embed())
            
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !recent command: {exception}')  
    
    @character.command(name='best_runs', help='Usage: !best <character name> <realm> (optional on Area-52)')
    async def best_runs(self, ctx, name: str = None, realm: str = None):
        """The best command returns the best runs for a given character.

        Args:
            ctx (context): Pass the current discord context
            character_name (str): Character name
            realm (str): Realm of the character
        """
        try:
            if not name:
                main_char_relationship = await db.lookup_default_character(ctx.guild.id, ctx.author.id)
                char = await db.lookup_character(main_char_relationship.character.name, main_char_relationship.character.realm)
                
                if char:
                    name, realm = char.name, char.realm
                else:
                    await ctx.respond('Please provide a character name and realm or set a main character.')
                    return

            if not realm:
                realm = 'Area-52'

            character = await raiderIO.get_character(name, realm)
            await ctx.respond(embed=character.get_best_runs_embed())
        
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !best command: {exception}')
            
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.respond('Something went wrong :( Talk to Eriim about this error. ')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard command: {error}')
            
def setup(bot):
    bot.add_cog(Character(bot))
    print('Character cog loaded successfully.')
    