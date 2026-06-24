import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import text

from pip.database.database import get_session
from pip.utils.config import TEST_GUILD_ID


class Health(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(
        self,
        interaction: discord.Interaction,
    ) -> bool:

        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message(
                "❌ This command is owner only.",
                ephemeral=True,
            )
            return False

        return True

    @app_commands.guilds(discord.Object(id=TEST_GUILD_ID))
    @app_commands.guild_only()
    @app_commands.command(
        name="health",
        description="View bot health information.",
    )
    async def health(
        self,
        interaction: discord.Interaction,
    ):

        latency = round(self.bot.latency * 1000)

        database_status = "🟢 OK"

        try:
            session = get_session()

            session.execute(text("SELECT 1"))

        except Exception as e:
            database_status = f"🔴 FAILED\n" f"{type(e).__name__}: {e}"

        embed = discord.Embed(
            title="🩺 Pip Health Check",
            color=discord.Color.green(),
        )

        embed.add_field(
            name="Discord",
            value="🟢 Connected",
            inline=False,
        )

        embed.add_field(
            name="Database",
            value=database_status,
            inline=False,
        )

        embed.add_field(
            name="Latency",
            value=f"{latency}ms",
            inline=False,
        )

        embed.add_field(
            name="Guilds",
            value=str(len(self.bot.guilds)),
            inline=True,
        )

        embed.add_field(
            name="Loaded Cogs",
            value=str(len(self.bot.cogs)),
            inline=True,
        )

        embed.add_field(
            name="Cached Users",
            value=str(len(self.bot.users)),
            inline=True,
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Health(bot))
