import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import text

from pip.database.database import get_session
from pip.utils.config import TEST_GUILD_ID
from pip.utils.embed_factory import EmbedFactory


class Health(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(
        self,
        interaction: discord.Interaction,
    ) -> bool:

        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message(
                "This command is owner only.",
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

        database_status = "OK"

        try:
            session = get_session()

            session.execute(text("SELECT 1"))

        except Exception as e:
            database_status = f"FAILED\n{type(e).__name__}: {e}"

        embed = EmbedFactory.health(
            latency=latency,
            database_status=database_status,
            guild_count=len(self.bot.guilds),
            loaded_cogs=len(self.bot.cogs),
            cached_users=len(self.bot.users),
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Health(bot))
