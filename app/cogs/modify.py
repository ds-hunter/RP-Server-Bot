import sys
from discord import Interaction
from discord.ext import commands
from discord import app_commands
sys.path.insert(0, '..')
import database

class Modify(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Get the player id from the mention
    async def get_player_id(self, interaction: Interaction, player_mention: str):
        # Retrieve the player's ID from the mention
        id = player_mention.replace('<@', '').replace('>', '')

        # Check if the player mention is in the right format
        if not player_mention.startswith('<@') or not player_mention.endswith('>') or not id.isdigit():
            await interaction.response.send_message('Invalid command format, please use player mentions instead of discord names! ex; @PLAYER', ephemeral=True)
            return False
        
        return id

    # Create character command (def create_character(charactername, playername, startinglevel)
    @app_commands.command(name="createcharacter", description="Create a new character")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(1096582913967009902, 1096583210114224229, 1098315530600976555)
    async def createcharacter(self, interaction: Interaction, player_mention: str, charactername: str, startinglevel: int):
        # Create the character
        # success = database.create_character(charactername, playername, startinglevel) -- OLD METHOD
        
        # Retrieve the player's ID from the mention
        id = await self.get_player_id(interaction, player_mention)
        if not id: return
        
        success = database.create_character(charactername, id, startinglevel)

        # Check if the operation was successful
        if success:
            await interaction.response.send_message(f'Created {charactername} for {player_mention}!')
        else:
            await interaction.response.send_message(f'Failed to create {charactername}. Does the character already exist?', ephemeral=True)

    @createcharacter.error
    async def createcharacter_error(self, interaction: Interaction, error):
        if isinstance(error, app_commands.errors.MissingAnyRole):
            await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error has occurred!', ephemeral=True)

    # Delete character command
    @app_commands.command(name="deletecharacter", description="Delete a character")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(1096582913967009902, 1096583210114224229, 1098315530600976555)
    async def deletecharacter(self, interaction: Interaction, player_mention: str, charactername: str):
        # Retrieve the player's ID from the mention
        id = await self.get_player_id(interaction, player_mention)
        if not id: return

        # Delete the character
        success = database.delete_character(charactername, player_mention.replace('<@', '').replace('>', ''))

        # Check if the operation was successful
        if success:
            await interaction.response.send_message(f'Deleted {charactername} from {player_mention}!')
        else:
            await interaction.response.send_message(f'Failed to delete {charactername}. Does the character exist?', ephemeral=True)
    
    @deletecharacter.error
    async def deletecharacter_error(self, interaction: Interaction, error):
        if isinstance(error, app_commands.errors.MissingAnyRole):
            await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error has occurred!', ephemeral=True)

    # Add DT Command
    @app_commands.command(name="adddt", description="Add DT to a character")
    @app_commands.guild_only()
    async def adddt(self, interaction: Interaction, charactername: str, amount: int, reason: str):
        # Get the player id
        playername = str(interaction.user.id)

        # Add DT
        success = database.add_dt(charactername, playername, amount, reason)

        # Check if the operation was successful
        if success:
            await interaction.response.send_message(f'Added {amount} DT to {charactername}!')
        else:
            await interaction.response.send_message(f'Failed to add {amount} DT to {charactername}. Does the character exist?', ephemeral=True)

    # Add SP Command
    @app_commands.command(name="addsp", description="Add SP to a character")
    @app_commands.guild_only()
    async def addsp(self, interaction: Interaction, charactername: str, amount: int, reason: str):
        # Get the player id
        playername = str(interaction.user.id)

        # Add SP
        success = database.add_sp(charactername, playername, amount, reason)

        # Check if the operation was successful
        if success:
            await interaction.response.send_message(f'Added {amount} SP to {charactername}!')
        else:
            await interaction.response.send_message(f'Failed to add {amount} SP to {charactername}. Does the character exist?', ephemeral=True)
    
    # Add Ryo Command
    @app_commands.command(name="addryo", description="Add Ryo to a character")
    @app_commands.guild_only()
    async def addryo(self, interaction: Interaction, charactername: str, amount: int, reason: str):
        # Get the player id
        playername = str(interaction.user.id)

        # Add Ryo
        success = database.add_ryo(charactername, playername, amount, reason)

        # Check if the operation was successful
        if success:
            await interaction.response.send_message(f'Added {amount} Ryo to {charactername}!')
        else:
            await interaction.response.send_message(f'Failed to add {amount} Ryo to {charactername}. Does the character exist?', ephemeral=True)

    # Spend DT command
    @app_commands.command(name="spenddt", description="Spend DT from a character")
    @app_commands.guild_only()
    async def spenddt(self, interaction: Interaction, charactername: str, amount: int, reason: str):
        # Get the player id
        playername = str(interaction.user.id)

        # Spend DT
        success = database.spend_dt(charactername, playername, amount, reason)

        # Check if the operation was successful
        if success:
            await interaction.response.send_message(f'Spent {amount} DT from {charactername}!')
        else:
            await interaction.response.send_message(f'Failed to spend {amount} DT from {charactername}. Does the character exist?', ephemeral=True)
    
    # Spend SP command
    @app_commands.command(name="spendsp", description="Spend SP from a character")
    @app_commands.guild_only()
    async def spendsp(self, interaction: Interaction, charactername: str, amount: int, reason: str):
        # Get the player id
        playername = str(interaction.user.id)

        # Spend SP
        success = database.spend_sp(charactername, playername, amount, reason)

        # Check if the operation was successful
        if success:
            await interaction.response.send_message(f'Spent {amount} SP from {charactername}!')
        else:
            await interaction.response.send_message(f'Failed to spend {amount} SP from {charactername}. Does the character exist?', ephemeral=True)
    
    # Spend Ryo command
    @app_commands.command(name="spendryo", description="Spend Ryo from a character")
    @app_commands.guild_only()
    async def spendryo(self, interaction: Interaction, charactername: str, amount: int, reason: str):
        # Get the player id
        playername = str(interaction.user.id)

        # Spend Ryo
        success = database.spend_ryo(charactername, playername, amount, reason)

        # Check if the operation was successful
        if success:
            await interaction.response.send_message(f'Spent {amount} Ryo from {charactername}!')
        else:
            await interaction.response.send_message(f'Failed to spend {amount} Ryo from {charactername}. Does the character exist?', ephemeral=True)
    @app_commands.command(name="test", description="Test command")
    @app_commands.guild_only()
    async def test(self, interaction: Interaction, playermention: str):
        id = playermention.replace("<@", "").replace(">", "")
        await interaction.response.send_message(f"Hello, this is what I received: {id}")

    # Add level up command (def get_level(charactername, playername)
    @app_commands.command(name="levelup", description="Use SP to level up a character")
    @app_commands.guild_only()
    async def levelup(self, interaction: Interaction, charactername: str):
        # CONFIG (Level: SP Required)
        level_up_requirements = {
            0: 0,
            1: 5,
            2: 5,
            3: 5,
            4: 5,
            5: 6,
            6: 12,
            7: 14,
            8: 19,
            9: 22,
            10: 24,
            11: 25,
            12: 26,
            13: 29,
            14: 35,
            15: 40,
            16: 50,
            17: 65,
            18: 80,
            19: 90,
            20: 99
        }

        # Get the player id
        playername = str(interaction.user.id)

        # Get the current level
        level = database.get_level(charactername, playername)
        sp = database.get_sp(charactername, playername)

        # Assume character exists if level is not None
        if level is not False and sp is not False:
            # Check if the character has enough SP to level up
            if level in level_up_requirements:
                sp_required = level_up_requirements[level]
                if sp >= sp_required:
                    # Level up the character
                    database.set_sp(charactername, playername, sp - sp_required, sp)
                    database.set_level(charactername, playername, level + 1)
                    await interaction.response.send_message(f'{charactername} leveled up to level {level + 1}!')
                else:
                    await interaction.response.send_message(f'{charactername} does not have enough SP to level up! ({sp}/{sp_required})')
            else:
                await interaction.response.send_message(f'{charactername} is already max level!')
        else:
            await interaction.response.send_message(f'Failed to level up {charactername}. Does the character exist?', ephemeral=True)

async def setup(client):
    await client.add_cog(Modify(client))