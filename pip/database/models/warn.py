from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from pip.database.base import Base


class Warn(Base):
    __tablename__ = "warns"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(BigInteger)

    case_id: Mapped[int] = mapped_column(BigInteger)

    points: Mapped[int] = mapped_column(default=0)

    reason: Mapped[str] = mapped_column(String(1000))

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    active: Mapped[bool] = mapped_column(default=True)
