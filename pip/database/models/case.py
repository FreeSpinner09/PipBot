from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from pip.database.base import Base


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)

    guild_id: Mapped[int] = mapped_column(BigInteger)

    user_id: Mapped[int] = mapped_column(BigInteger)

    moderator_id: Mapped[int] = mapped_column(BigInteger, nullable=True)

    action: Mapped[str] = mapped_column(String)

    reason: Mapped[str] = mapped_column(String)

    automated: Mapped[bool] = mapped_column(default=False)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
