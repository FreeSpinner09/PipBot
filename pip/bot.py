import discord
import os
from discord.ext import commands
from utils.config import DISCORD_TOKEN
from utils.logger import logger


class Client(commands.Bot):

    async def setup_hook(self):
        await self.load_cogs()

    async def load_cogs(self):
        for file in os.listdir("./pip/cogs"):
            if file.endswith(".py"):
                extension = f"cogs.{file[:-3]}"

                try:
                    await self.load_extension(extension)
                    print(f"Loaded {extension}")

                except Exception as e:
                    print(f"Failed to load {extension}: {e}")

    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_error(self, event, *args, **kwargs):
        logger.exception(f"Unhandled exception in event: {event}")


intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix="!", intents=intents)

TEST_GUILD_ID = discord.Object(id=1027186489672613918)

client.run(f"{DISCORD_TOKEN}")
