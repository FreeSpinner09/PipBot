from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from pip.database.base import Base


class Guild(Base):
    __tablename__ = "guilds"

    id: Mapped[int] = mapped_column(primary_key=True)

    guild_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    name: Mapped[str] = mapped_column(String(100))
