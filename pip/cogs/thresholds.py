import discord
from discord import app_commands
from discord.ext import commands

from pip.services.threshold_service import ThresholdService


class Thresholds(commands.Cog):

    threshold = app_commands.Group(
        name="threshold",
        description="Manage heat punishment thresholds.",
        guild_ids=[1027186489672613918],
        guild_only=True,
    )

    def __init__(self, bot):
        self.bot = bot
        self.threshold_service = ThresholdService()

    # /threshold add Command

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        heat="The heat value needed to trigger this threshold.",
        punishment="The punishment to apply when this threshold is reached.",
        duration="Duration in seconds. Required for timeout punishments.",
    )
    @app_commands.choices(
        punishment=[
            app_commands.Choice(name="warn", value="warn"),
            app_commands.Choice(name="timeout", value="timeout"),
            app_commands.Choice(name="kick", value="kick"),
            app_commands.Choice(name="ban", value="ban"),
        ]
    )
    @threshold.command(name="add", description="Add a heat punishment threshold.")
    async def add(
        self,
        interaction: discord.Interaction,
        heat: int,
        punishment: app_commands.Choice[str],
        duration: int | None = None,
    ):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        if punishment.value == "timeout" and duration is None:
            await interaction.response.send_message(
                "Timeout thresholds require a duration in seconds.",
                ephemeral=True,
            )
            return

        threshold = self.threshold_service.create_threshold(
            guild_id=guild.id,
            threshold_value=heat,
            punishment_type=punishment.value,
            duration=duration,
        )

        await interaction.response.send_message(
            f"Threshold #{threshold.guild_threshold_id} added."
            f"\nHeat: {threshold.threshold_value}"
            f"\nPunishment: {threshold.punishment_type}"
            f"\nDuration: {threshold.duration}",
            ephemeral=True,
        )

    # /threshold remove Command

    @app_commands.checks.has_permissions(administrator=True)
    @threshold.command(name="remove", description="Remove a heat punishment threshold.")
    async def remove(
        self,
        interaction: discord.Interaction,
        threshold_id: int,
    ):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        threshold = self.threshold_service.remove_threshold(
            guild_id=guild.id,
            threshold_id=threshold_id,
        )

        if threshold is None:
            await interaction.response.send_message(
                f"Threshold #{threshold_id} was not found.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Threshold #{threshold_id} has been removed.",
            ephemeral=True,
        )

    # /threshold list Command

    @app_commands.checks.has_permissions(administrator=True)
    @threshold.command(name="list", description="List heat punishment thresholds.")
    async def list(
        self,
        interaction: discord.Interaction,
    ):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        thresholds = self.threshold_service.get_thresholds(guild.id)

        if len(thresholds) == 0:
            await interaction.response.send_message(
                "No thresholds have been configured.",
                ephemeral=True,
            )
            return

        message = "Configured Thresholds:\n\n"

        for threshold in thresholds:
            message += (
                f"Threshold #{threshold.guild_threshold_id}"
                f"\nHeat: {threshold.threshold_value}"
                f"\nPunishment: {threshold.punishment_type}"
                f"\nDuration: {threshold.duration}"
                f"\nEnabled: `{str(threshold.enabled)}`"
                "\n\n"
            )

        await interaction.response.send_message(message, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Thresholds(bot))
