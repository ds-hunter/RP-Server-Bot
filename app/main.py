import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Load the config from the .env file
SECRET_TOKEN = os.getenv('BOT_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX')

# Set up the client class
class Client(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix=BOT_PREFIX)
        self.Synced = False
    
    async def load_extensions(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                os.system(f'echo [INFO] Loaded commands extension {filename[:-3]}')

    async def on_ready(self):
        await self.wait_until_ready()
        await self.load_extensions()
        if not self.Synced:
            await self.tree.sync()
            self.Synced = True
        os.system(f'echo [INFO] Bot is ready. Logged in as {self.user} ID {self.user.id}')

# Set up and run the bot
client = Client()
client.run(SECRET_TOKEN)