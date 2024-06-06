import sys
import discord
from io import StringIO
from discord import Interaction
from discord.ext import commands
from discord import app_commands
sys.path.insert(0, '..')
import database

class Request(commands.Cog):
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
    
    async def check_player_name_format(self, interaction: Interaction):
        old_format = f'{interaction.user.name}#{interaction.user.discriminator}'
        new_format = str(interaction.user.id)

        # Search for the player by old name to check if it exists, if it does, update the name
        old_player = database.search_player(old_format)

        if old_player:
            database.update_player_name(old_format, new_format)
            await interaction.user.send(
                f'I detected that your profile is using an outdated method of storing your name, I have attempted to updated it so changing your discord nickname or discriminator will no longer cause issues. This message will only show once, if you have any issues please contact your server admin.'
            )
            new_player = database.search_player(new_format)
            if not new_player:
                await interaction.user.send(
                    f'Something went wrong with updating your name, this needs to be manually fixed. Contact your server admin with the following information:\n\nOld name: {old_format}\nNew name: {new_format}'
                )
    
    # Display player command (def search_player(playername))
    @app_commands.command(name="displayplayer", description="Display a player's characters")
    @app_commands.guild_only()
    async def displayplayer(self, interaction: Interaction):
        await self.check_player_name_format(interaction)
        player = database.search_player(str(interaction.user.id))

        if player:
            # Store previous character names so we don't display them twice
            prev_names = []

            # Player may have multiple accounts, so create embed for each one
            for p in player:
                # Check if the character name is already in the previous names list
                if p[2] in prev_names:
                    continue

                # Create the embed with player info
                embed = discord.Embed(
                    title = f'',
                    description=f"""
                        🔹**Name**: {p[2]}

                        **Level**: {p[3]}

                        **DT**: {p[4]}

                        **SP**: {p[5]}

                        **Ryo**: {p[6]} ¥""",
                    colour = discord.Colour.yellow()
                )
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/1034936084502696017/1035097757549068339/SHtest3.gif")
                embed.set_image(url="https://media.discordapp.net/attachments/1094512367171280927/1098190586235854898/full.png")
                
                # Store the charcter name in the previous names list
                prev_names.append(p[2])

                # Send the embed
                if interaction.response.is_done():
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.response.send_message(embed = embed)
        else:
            await interaction.response.send_message(f'It seems you have no character data!', ephemeral=True)
    
    # Show history command (def show_history(charactername, playername))
    @app_commands.command(name="showhistory", description="Show a character's history from a player")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(1096582913967009902, 1096583210114224229, 1098315530600976555)
    async def showhistory(self, interaction: Interaction, player_mention: str, charactername: str):
        id = await self.get_player_id(interaction, player_mention)
        if not id: return

        history = database.show_history(charactername, id)

        if history:
            full_history_message = ''

            # History can be multiple rows, so create embed for each one
            for h in history:
                # Add the affected field, amount changed, reason and date to the full history message
                full_history_message += f"Added {int(h[4]) - int(h[3])} to {h[2]} | {h[6]} | {h[5]}\n\n"

            # Create a file-like object to store the full history message
            file_object = StringIO(full_history_message)

            # Create the discord file object attachment
            file = discord.File(file_object, filename=f'{player_mention}\'s history for {charactername}.txt')

            # Delete the file object from memory
            del file_object

            await interaction.response.send_message(f'{player_mention}\'s history for {charactername}', file=file)
        else:
            await interaction.response.send_message('No history found!', ephemeral=True)

    @showhistory.error
    async def showhistory_error(self, interaction: Interaction, error):
        if isinstance(error, app_commands.errors.MissingAnyRole):
            await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error has occured!', ephemeral=True)
    
async def setup(client):
    await client.add_cog(Request(client))