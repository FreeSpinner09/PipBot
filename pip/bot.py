import discord
from discord.ext import commands
from utils.config import DISCORD_TOKEN


class Client(commands.Bot):

    async def on_ready(self):
        print(f"Logged on as {self.user}")

        try:
            testGuild = discord.Object(id=1027186489672613918)
            synced = await self.tree.sync(guild=testGuild)
            print(f"Synced {len(synced)} commands to guild {testGuild.id}")

        except Exception as e:
            print(f"Error syncing commands: {e}")


intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix="!", intents=intents)

TEST_GUILD_ID = discord.Object(id=1027186489672613918)

client.run(f"{DISCORD_TOKEN}")
