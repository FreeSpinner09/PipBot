from pip.services.guild_config_service import GuildConfigService
from pip.utils.logger import logger


class ModLogService:

    def __init__(self):
        self.guild_config_service = GuildConfigService()

    def log_case(self, case):
        try:
            config = self.guild_config_service.get_config(case.guild_id)
        except ValueError:
            logger.info(
                "Moderation case logged without guild config: "
                "guild_id=%s case=%s action=%s user_id=%s moderator_id=%s reason=%s",
                case.guild_id,
                case.guild_case_number,
                case.action,
                case.user_id,
                case.moderator_id,
                case.reason,
            )
            return None

        if config.mod_log_channel is None:
            logger.info(
                "Moderation case logged with mod log disabled: "
                "guild_id=%s case=%s action=%s user_id=%s moderator_id=%s reason=%s",
                case.guild_id,
                case.guild_case_number,
                case.action,
                case.user_id,
                case.moderator_id,
                case.reason,
            )
            return None

        logger.info(
            "Moderation case logged: "
            "guild_id=%s mod_log_channel=%s case=%s action=%s user_id=%s "
            "moderator_id=%s reason=%s",
            case.guild_id,
            config.mod_log_channel,
            case.guild_case_number,
            case.action,
            case.user_id,
            case.moderator_id,
            case.reason,
        )

        return config.mod_log_channel
