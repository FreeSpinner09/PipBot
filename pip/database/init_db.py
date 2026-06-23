from pip.database.base import Base
from pip.database.database import engine
from pip.database.models.case import Case  # noqa: F401
from pip.database.models.guild import Guild  # noqa: F401
from pip.database.models.guild_config import GuildConfig  # noqa: F401
from pip.database.models.heat_events import HeatEvent  # noqa: F401
from pip.database.models.punishment_thresholds import PunishmentThresholds  # noqa: F401
from pip.database.models.user import User  # noqa: F401
from pip.database.models.warn import Warn  # noqa: F401

print(Base.metadata.tables.keys())

Base.metadata.create_all(engine)
