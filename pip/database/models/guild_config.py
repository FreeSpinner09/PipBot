from sqlalchemy import (
    Boolean,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from pip.database.base import Base


class GuildConfig(Base):
    __tablename__ = "guild_configs"

    guild_id: Mapped[int] = mapped_column(
        ForeignKey("guilds.guild_id"),
        primary_key=True,
    )

    automod_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    ai_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    mod_log_channel: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )
