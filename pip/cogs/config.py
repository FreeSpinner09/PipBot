import discord
from discord import app_commands
from discord.ext import commands

from pip.services.guild_config_service import GuildConfigService


class Config(commands.Cog):

    config = app_commands.Group(
        name="config",
        description="Manage server configuration.",
        guild_ids=[1027186489672613918],
        guild_only=True,
    )

    def __init__(self, bot):
        self.bot = bot
        self.guild_config_service = GuildConfigService()

    def get_or_create_config(self, guild_id: int):
        try:
            return self.guild_config_service.get_config(guild_id)
        except ValueError:
            return self.guild_config_service.create_config(guild_id)

    # /config automod Command

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(
        status=[
            app_commands.Choice(name="enable", value="enable"),
            app_commands.Choice(name="disable", value="disable"),
        ]
    )
    @config.command(name="automod", description="Enable or disable automod.")
    async def automod(
        self,
        interaction: discord.Interaction,
        status: app_commands.Choice[str],
    ):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        self.get_or_create_config(guild.id)

        enabled = status.value == "enable"
        config = self.guild_config_service.set_automod(guild.id, enabled)

        await interaction.response.send_message(
            f"Automod enabled: `{str(config.automod_enabled)}`",
            ephemeral=True,
        )

    # /config ai Command

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(
        status=[
            app_commands.Choice(name="enable", value="enable"),
            app_commands.Choice(name="disable", value="disable"),
        ]
    )
    @config.command(name="ai", description="Enable or disable AI features.")
    async def ai(
        self,
        interaction: discord.Interaction,
        status: app_commands.Choice[str],
    ):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        self.get_or_create_config(guild.id)

        enabled = status.value == "enable"
        config = self.guild_config_service.set_ai(guild.id, enabled)

        await interaction.response.send_message(
            f"AI enabled: `{str(config.ai_enabled)}`",
            ephemeral=True,
        )

    # /config modlog Command

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(
        status=[
            app_commands.Choice(name="enable", value="enable"),
            app_commands.Choice(name="disable", value="disable"),
        ]
    )
    @config.command(name="modlog", description="Enable or disable mod log.")
    async def modlog(
        self,
        interaction: discord.Interaction,
        status: app_commands.Choice[str],
    ):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        self.get_or_create_config(guild.id)

        channel_id = interaction.channel_id if status.value == "enable" else None
        config = self.guild_config_service.set_mod_log_channel(guild.id, channel_id)

        if config.mod_log_channel is None:
            message = "Mod log disabled."
        else:
            message = f"Mod log enabled in <#{config.mod_log_channel}>."

        await interaction.response.send_message(
            message,
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Config(bot))
