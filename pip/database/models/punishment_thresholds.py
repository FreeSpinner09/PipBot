from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from pip.database.base import Base


class PunishmentThresholds(Base):
    __tablename__ = "punishment_thresholds"

    id: Mapped[int] = mapped_column(primary_key=True)

    guild_id: Mapped[int] = mapped_column(BigInteger)

    threshold_value: Mapped[int] = mapped_column(BigInteger)

    punishment_type: Mapped[str] = mapped_column(String)

    duration: Mapped[int] = mapped_column(BigInteger, nullable=True)

    enabled: Mapped[bool] = mapped_column(default=True)
