from pip.database.database import get_session
from pip.database.models.guild_config import GuildConfig


class GuildConfigService:
    def get_config(self, guild_id: int):
        session = get_session()

        config = (
            session.query(GuildConfig).filter(GuildConfig.guild_id == guild_id).first()
        )

        if config is None:
            raise ValueError(f"No config found for guild {guild_id}")

        return config

    def create_config(self, guild_id: int):
        session = get_session()

        config = GuildConfig(guild_id=guild_id)

        session.add(config)
        session.commit()

        session.refresh(config)
        return config

    def set_automod(self, guild_id: int, enabled: bool):
        session = get_session()

        config = self.get_config(guild_id)

        config.automod_enabled = enabled

        session.merge(config)
        session.commit()

        return config

    def set_ai(self, guild_id: int, enabled: bool):
        session = get_session()

        config = self.get_config(guild_id)

        config.ai_enabled = enabled

        session.merge(config)
        session.commit()

        return config

    def set_mod_log_channel(self, guild_id: int, channel_id: int | None):
        session = get_session()

        config = self.get_config(guild_id)

        config.mod_log_channel = channel_id

        session.merge(config)
        session.commit()

        return config
