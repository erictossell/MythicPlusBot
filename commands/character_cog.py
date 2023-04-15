from typing import Optional
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
import db
from objects.registration import RegisterView
import raiderIO

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Character cog loaded.')
    
    character = SlashCommandGroup(name='character', description='All commands related to characters')
    
    @character.command(name='runs', help='Gets the best Mythic+ runs for a character.')
    async def runs(self,ctx, character_name: str = None, realm: str = 'Area-52'):
        """Gets the best Mythic+ runs for a character."""
        try:           
            
            character_title = db.lookup_character(character_name, 'area-52')
            run_list = db.get_all_runs_for_character(character_title)
            for run in run_list:
                characters_list = db.get_all_characters_for_run(run.id)
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
    
    @character.command(name='setmain', help='Sets the default character for a user.')
    async def set_main(self, ctx, character_name: str, character_realm: Optional[str] = 'Area-52'):
        """Sets a user's default character.

        Args:
            ctx (context): The current discord context.
            character_name (str): The character name.
            character_realm (str, optional): The character realm. Defaults to 'Area-52'.
        """
        try:
            character = await raiderIO.get_character(character_name, character_realm)
            character_db = db.lookup_character(character.name, character.realm.lower())
            default_character = db.lookup_default_character(ctx.guild.id, ctx.author.id)

            if character_db:
                if default_character:
                    default_character.character = character_db
                    default_character = db.update_default_character(default_character)
                else:
                    default_character = db.add_default_character(db.DefaultCharacterDB(ctx.author.id,
                                                                                       ctx.guild.id,
                                                                                        character_db,
                                                                                       1,
                                                                                       True))
                                                                                      

                await ctx.respond(f'Your main character has been set to {character.name}-{character.realm}.')
            else:
                await ctx.respond('Something went wrong. Make sure if your character is not in the guild, you have registered it with !register.')

        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !default command: {exception}')
            
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
    
    @character.command(name='profile', help='Usage: !character <character name> <realm> (optional on Area-52)')
    async def profile(self, ctx, character_name: str = None, realm: str = 'Area-52'):
        """This command returns a character's profile.

        Args:
            ctx (context): The current discord context.
            character_name (str): Character name.
            realm (str): Realm of the character.
        """
        try:
            if not character_name:
                if ctx.guild:
                    main_char = db.lookup_default_character(ctx.guild.id, ctx.author.id)
                    char = db.lookup_character(main_char.character.name, main_char.character.realm)
                    if char:
                        character_name, realm = char.name, char.realm
                    else:
                        await ctx.respond('Please provide a character name and realm or set a main character.')
                        return
                else:
                    await ctx.respond('Please provide a character name and realm.')
                    return

            if not realm:
                realm = 'Area-52'

            character = await raiderIO.get_character(character_name, realm)
            await ctx.respond(embed=character.get_character_embed())

        except Exception as exception:
            await ctx.respond(f' I was not able to find a character with name: {character_name}. Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !character command: {exception}')
    
    @character.command(name='recentruns', help='Usage: !recent <character name> <realm> (optional on Area-52)')
    async def recentruns(self, ctx, character_name: str = None, realm: str = None):
        """This command returns the recent runs for a given character.

        Args:
            ctx (context): The current discord context.
        """ 
        try: 
            if not character_name:
                main_char = db.lookup_default_character(ctx.guild.id, ctx.author.id)
                if main_char:
                    character_name, realm = main_char.name, main_char.realm
                else:
                    await ctx.respond('Please provide a character name and realm or set a main character.')
                    return
            if not realm:
                realm = 'Area-52'
            character = await raiderIO.get_character(character_name, realm)
            await ctx.respond(embed=character.get_recent_runs_embed())
            
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !recent command: {exception}')  
    
    @character.command(name='bestruns', help='Usage: !best <character name> <realm> (optional on Area-52)')
    async def bestruns(self, ctx, character_name: str = None, realm: str = None):
        """The best command returns the best runs for a given character.

        Args:
            ctx (context): Pass the current discord context
            character_name (str): Character name
            realm (str): Realm of the character
        """
        try:
            if not character_name:
                main_char = db.lookup_default_character(ctx.guild.id, ctx.author.id)
                char = db.lookup_character(main_char.character.name, main_char.character.realm)
                if char:
                    character_name, realm = char.name, char.realm
                else:
                    await ctx.respond('Please provide a character name and realm or set a main character.')
                    return

            if not realm:
                realm = 'Area-52'

            character = await raiderIO.get_character(character_name, realm)
            await ctx.respond(embed=character.get_best_runs_embed())
        
        except Exception as exception:
            await ctx.respond('Type !help to see how to use this command.')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !best command: {exception}')
            
def setup(bot):
    bot.add_cog(Character(bot))