from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

from pip.database.base import Base


class HeatEvent(Base):
    __tablename__ = "heat_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(BigInteger)

    guild_id: Mapped[int] = mapped_column(BigInteger)

    amount: Mapped[int] = mapped_column(BigInteger)

    reason: Mapped[str] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
