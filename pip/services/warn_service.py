from pip.database.database import get_session
from pip.database.models.warn import Warn
from pip.engines.moderation_engine import ModerationEngine
from pip.services.case_service import CaseService
from pip.services.mod_log_service import ModLogService
from pip.services.user_service import UserService


class WarnService:

    def __init__(self):
        self.case_service = CaseService()
        self.user_service = UserService()
        self.mod_log_service = ModLogService()
        self.moderation_engine = ModerationEngine()

    def create_warn(
        self,
        guild_id: int,
        user_id: int,
        moderator_id: int,
        reason: str,
        points: int,
        automated: bool = False,
    ):

        session = get_session()

        case = self.case_service.create_case(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            action="warn",
            reason=reason,
            automated=automated,
        )

        warn = Warn(
            user_id=user_id,
            guild_id=guild_id,
            guild_case_id=case.guild_case_number,
            points=points,
            reason=reason,
            moderator_id=moderator_id,
            timestamp=case.timestamp,
            automated=automated,
        )

        session.add(warn)
        session.commit()
        session.refresh(warn)

        self.mod_log_service.log_case(case)

        self.user_service.add_heat(guild_id, user_id, points)
        self.user_service.increment_warning_count(guild_id, user_id)

        threshold = self.moderation_engine.evaluate_user(guild_id, user_id)

        return warn, threshold

    def get_warns(self, guild_id: int, user_id: int):
        session = get_session()

        warns = (
            session.query(Warn)
            .filter(Warn.guild_id == guild_id, Warn.user_id == user_id)
            .order_by(Warn.guild_case_id.desc())
            .all()
        )

        return warns

    def set_warn_as_inactive(
        self,
        guild_id: int,
        case_id: int,
        moderator_id: int | None = None,
        reason: str | None = None,
        automated: bool = False,
    ):
        session = get_session()

        warn = (
            session.query(Warn)
            .filter(Warn.guild_id == guild_id, Warn.guild_case_id == case_id)
            .first()
        )

        if warn is None:
            return None

        if warn.active is False:
            return warn

        warn.active = False
        session.commit()
        session.refresh(warn)

        case = self.case_service.create_case(
            guild_id=guild_id,
            user_id=warn.user_id,
            moderator_id=moderator_id,
            action="unwarn",
            reason=reason or f"Warning case #{case_id} removed.",
            automated=automated,
        )
        self.mod_log_service.log_case(case)

        return warn

    def check_warn_status(self, guild_id: int, case_id: int):
        session = get_session()

        warn = (
            session.query(Warn)
            .filter(Warn.guild_id == guild_id, Warn.guild_case_id == case_id)
            .first()
        )

        if warn is None:
            return None

        return warn.active
