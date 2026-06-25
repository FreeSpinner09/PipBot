import discord
from discord import app_commands
from discord.ext import commands

from pip.executors.punishment_executor import PunishmentExecutor
from pip.services.case_service import CaseService
from pip.services.user_service import UserService
from pip.services.warn_service import WarnService
from pip.utils.embed_factory import EmbedFactory


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.warn_service = WarnService()
        self.user_service = UserService()
        self.case_service = CaseService()
        self.punishment_executor = PunishmentExecutor()

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
                "You cannot run this command on a bot.",
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

        warn, threshold = self.warn_service.create_warn(
            guild_id=guild.id,
            user_id=user.id,
            moderator_id=interaction.user.id,
            reason=reason,
            points=points,
        )

        current_heat = self.user_service.get_user_heat(guild.id, user.id)

        message = (
            f"✅ Warned {user.mention}\n" f"Reason: {reason}\n" f"Points: {points}"
        )

        if threshold is not None:
            try:
                await self.punishment_executor.execute(
                    member=user,
                    punishment_type=threshold.punishment_type,
                    duration=threshold.duration,
                    reason="Heat Threshold Reached",
                )
                message += (
                    f"\n\n Threshold Triggered:"
                    f"\n{threshold.punishment_type}"
                    f"\nUsers Current Heat: {current_heat}"
                    f"\nThreshold: {threshold.threshold_value}"
                    f"\nStatus: Success"
                )

            except Exception as e:
                message += (
                    f"\n\n Threshold Triggered:"
                    f"\n{threshold.punishment_type}"
                    f"\nUsers Current Heat: {current_heat}"
                    f"\nThreshold: {threshold.threshold_value}"
                    f"\nStatus: Failed"
                    f"\nError: {e}"
                )

        await interaction.response.send_message(message)

    # /unwarn Command
    @app_commands.guilds(discord.Object(id=1027186489672613918))
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.command(
        name="unwarn",
        description="Remove a warning from a player.",
    )
    async def unwarn(
        self,
        interaction: discord.Interaction,
        case_id: int,
        reason: str | None = None,
    ):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        if (
            self.warn_service.check_warn_status(guild_id=guild.id, case_id=case_id)
            is False
        ):
            await interaction.response.send_message(
                "The warning under that Case ID is already inactive.",
                ephemeral=True,
            )
            return

        warn = self.warn_service.set_warn_as_inactive(
            guild_id=guild.id,
            case_id=case_id,
            moderator_id=interaction.user.id,
            reason=reason,
        )

        if warn is None:
            await interaction.response.send_message(
                f"No valid warn found under Case: {str(case_id)}",
                ephemeral=True,
            )

        else:
            await interaction.response.send_message(
                f"The warning against <@{warn.user_id}> under Case: {case_id} has been lifted."
                "\n*FYI: The record* ***still exists*** *in the users history for auditing purposes.*",
                ephemeral=True,
            )

    # /warnings Command
    @app_commands.guilds(discord.Object(id=1027186489672613918))
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.command(
        name="warnings",
        description="Returns all of a users warnings. (Both active and inactive)",
    )
    async def warnings(self, interaction: discord.Interaction, user: discord.Member):
        if user.bot:
            await interaction.response.send_message(
                "You cannot run this command on a bot.",
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

        warnings = self.warn_service.get_warns(guild_id=guild.id, user_id=user.id)

        message = f"<@{user.id}>'s Warnings:\n"

        if len(warnings) == 0:
            await interaction.response.send_message(f"{user.mention} has no warns.")
            return

        count = len(warnings)

        for warn in warnings:
            message += (
                f"Warning {count}"
                f"\nCase ID: {warn.guild_case_id}"
                f"\nReason: {warn.reason}"
                f"\nPoints: {warn.points}"
                f"\nModerator: <@{warn.moderator_id}>"
                f"\nAutomated Warning: `{str(warn.automated)}`"
                f"\nIs Active: `{str(warn.active)}`"
                f"\nTimestamp: `{str(warn.timestamp)}`"
                "\n\n"
            )
            count -= 1

        await interaction.response.send_message(message, ephemeral=True)

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
        if user.bot:
            await interaction.response.send_message(
                "You cannot run this command on a bot.",
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

        db_user = self.user_service.get_or_create_user(
            guild.id,
            user.id,
        )

        await interaction.response.send_message(
            f"🔥 {user.mention}\n"
            f"Heat: {db_user.heat}\n"
            f"Warnings: {db_user.warning_count}",
            ephemeral=True,
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
        if user.bot:
            await interaction.response.send_message(
                "You cannot run this command on a bot.",
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

        cases = self.case_service.get_user_cases(guild.id, user.id, None)

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

        await interaction.response.send_message(history_text, ephemeral=True)

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

        embed = EmbedFactory.case(
            case_number=case.guild_case_number,
            action=case.action,
            user_id=case.user_id,
            moderator_id=case.moderator_id,
            reason=case.reason,
            automated=case.automated,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
