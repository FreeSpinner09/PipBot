import discord
from discord import app_commands
from discord.ext import commands

from pip.services.case_service import CaseService
from pip.services.user_service import UserService
from pip.services.warn_service import WarnService


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.warn_service = WarnService()
        self.user_service = UserService()
        self.case_service = CaseService()

    # /warn Command

    @app_commands.guilds(discord.Object(id=1027186489672613918))
    @app_commands.guild_only()
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

        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        warn = self.warn_service.create_warn(
            guild_id=guild.id,
            user_id=user.id,
            moderator_id=interaction.user.id,
            reason=reason,
            points=points,
        )
        await interaction.response.send_message(
            f"✅ Warned {user.mention}\n" f"Reason: {reason}\n" f"Points: {points}"
        )

    # /heat Command

    @app_commands.guilds(discord.Object(id=1027186489672613918))
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.guild_only()
    @app_commands.command(name="heat", description="View a user's heat.")
    async def heat(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
    ):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        db_user = self.user_service.get_or_create_user(
            guild.id,
            user.id,
        )

        await interaction.response.send_message(
            f"🔥 {user.mention}\n"
            f"Heat: {db_user.heat}\n"
            f"Warnings: {db_user.warning_count}"
        )

    # /history Command

    @app_commands.guilds(discord.Object(id=1027186489672613918))
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.command(
        name="history", description="View a user's moderation history."
    )
    async def history(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
    ):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        cases = self.case_service.get_user_cases(guild.id, user.id)

        if len(cases) == 0:
            await interaction.response.send_message(
                f"{user.mention} has no moderation history."
            )
            return

        history_text = f"{user.display_name}'s History:\n\n"

        for case in cases:
            history_text += (
                f"Case #{case.guild_case_number} | "
                f"{case.action}\n"
                f"Reason: {case.reason}\n\n"
            )

        await interaction.response.send_message(history_text)

    # /case Command

    @app_commands.guilds(discord.Object(id=1027186489672613918))
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.command(name="case", description="View a case.")
    async def case(
        self,
        interaction: discord.Interaction,
        case_number: int,
    ):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        case = self.case_service.get_case(guild.id, case_number)
        if case is None:
            await interaction.response.send_message(
                f"Case #{case_number} was not found.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title=f"Case #{case.guild_case_number}",
        )
        embed.add_field(
            name="Action",
            value=case.action,
            inline=False,
        )

        embed.add_field(
            name="User",
            value=f"<@{str(case.user_id)}>",
            inline=False,
        )

        embed.add_field(
            name="Moderator",
            value=f"<@{str(case.moderator_id)}>",
            inline=False,
        )

        embed.add_field(
            name="Reason",
            value=case.reason,
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
