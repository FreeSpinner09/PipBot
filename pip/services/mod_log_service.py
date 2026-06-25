import discord
from discord.ext import commands

from pip.database.models.case import Case
from pip.services.guild_config_service import GuildConfigService
from pip.utils.embed_factory import EmbedFactory
from pip.utils.logger import logger


class ModLogService:

    def __init__(self):
        self.guild_config_service = GuildConfigService()

    async def log_case(
        self,
        bot: commands.Bot,
        case: Case,
    ) -> None:
        """
        Sends a moderation log for a case if a mod log channel is configured.
        """

        try:
            config = self.guild_config_service.get_config(case.guild_id)

        except ValueError:
            logger.warning(
                "Cannot log moderation case. Guild config not found. guild_id=%s",
                case.guild_id,
            )
            return

        if config.mod_log_channel is None:
            return

        channel = bot.get_channel(config.mod_log_channel)

        if not isinstance(channel, discord.TextChannel):
            logger.warning(
                "Configured mod log channel is invalid. guild_id=%s channel_id=%s",
                case.guild_id,
                config.mod_log_channel,
            )
            return

        embed = EmbedFactory.case(
            case_number=case.guild_case_number,
            action=case.action,
            user_id=case.user_id,
            moderator_id=case.moderator_id,
            reason=case.reason,
            automated=case.automated,
            color=EmbedFactory.WARNING_COLOR,
            timestamp=case.timestamp,
        )

        try:
            await channel.send(embed=embed)

            logger.info(
                "Moderation case logged. guild_id=%s case=%s channel_id=%s",
                case.guild_id,
                case.guild_case_number,
                channel.id,
            )

        except discord.Forbidden:
            logger.exception(
                "Missing permission to send moderation log. guild_id=%s channel_id=%s",
                case.guild_id,
                channel.id,
            )

        except discord.HTTPException:
            logger.exception(
                "Discord rejected moderation log. guild_id=%s case=%s",
                case.guild_id,
                case.guild_case_number,
            )
