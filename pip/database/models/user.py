from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from pip.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(BigInteger)

    guild_id: Mapped[int] = mapped_column(BigInteger)

    heat: Mapped[int] = mapped_column(default=0)

    warning_count: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )

    last_infraction_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
