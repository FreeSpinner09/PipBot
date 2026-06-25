from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from pip.database.base import Base


class Warn(Base):
    __tablename__ = "warns"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(BigInteger)

    guild_id: Mapped[int] = mapped_column(BigInteger)

    guild_case_id: Mapped[int] = mapped_column(BigInteger)

    points: Mapped[int] = mapped_column(default=0)

    moderator_id: Mapped[int] = mapped_column(BigInteger, nullable=True)

    timestamp: Mapped[datetime] = mapped_column(DateTime)

    reason: Mapped[str] = mapped_column(String(1000))

    automated: Mapped[bool] = mapped_column(default=False)

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    active: Mapped[bool] = mapped_column(default=True)
