from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from pip.database.base import Base


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)

    guild_id: Mapped[int] = mapped_column(BigInteger)

    guild_case_number: Mapped[int] = mapped_column(BigInteger)

    user_id: Mapped[int] = mapped_column(BigInteger)

    moderator_id: Mapped[int] = mapped_column(BigInteger, nullable=True)

    action: Mapped[str] = mapped_column(String(50))

    reason: Mapped[str] = mapped_column(String(150))

    automated: Mapped[bool] = mapped_column(default=False)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
