import discord
from discord import app_commands
from discord.ext import commands

from pip.services.warn_service import WarnService


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.warn_service = WarnService()

    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.command(name="warn", description="Warn a user.")
    async def warn(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        points: int,
        reason: str,
        expires_in: str | None = None,
    ):
        if user.bot:
            await interaction.response.send_message(
                "You cannot warn a bot.",
                ephemeral=True,
            )
            return

        if interaction.guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return
        warn = self.warn_service.create_warn(
            guild_id=interaction.guild.id,
            user_id=user.id,
            moderator_id=interaction.user.id,
            reason=reason,
            points=points,
        )
        await interaction.response.send_message(
            f"✅ Warned {user.mention}\n" f"Reason: {reason}\n" f"Points: {points}"
        )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
