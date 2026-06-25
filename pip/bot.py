import os

import discord
from discord.ext import commands

from pip.utils.config import DISCORD_TOKEN
from pip.utils.logger import logger

TEST_GUILD_ID = discord.Object(id=1027186489672613918)


class Client(commands.Bot):

    async def setup_hook(self):
        await self.load_cogs()

    async def load_cogs(self):
        for file in os.listdir("./pip/cogs"):
            if file.endswith(".py"):
                extension = f"pip.cogs.{file[:-3]}"

                try:
                    await self.load_extension(extension)
                    print(f"Loaded {extension}")

                except Exception as e:
                    print(f"Failed to load {extension}: {e}")

    async def on_ready(self):
        commands_to_sync = self.tree.get_commands(guild=TEST_GUILD_ID)
        synced = await self.tree.sync(guild=TEST_GUILD_ID)
        total_commands = sum(
            (
                len(command.commands)
                if isinstance(command, discord.app_commands.Group)
                else 1
            )
            for command in commands_to_sync
        )
        print(f"Synced {len(synced)} top-level commands")
        print(f"Synced {total_commands} total command actions")
        print(f"Logged on as {self.user}")

    async def on_error(self, event, *args, **kwargs):
        logger.exception(f"Unhandled exception in event: {event}")


intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix="!", intents=intents, owner_id=986094035762573312)

client.run(f"{DISCORD_TOKEN}")
