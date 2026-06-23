from pip.database.database import get_session
from pip.database.models.warn import Warn
from pip.services.case_service import CaseService
from pip.services.user_service import UserService


class WarnService:

    def __init__(self):
        self.case_service = CaseService()
        self.user_service = UserService()

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

        warn = Warn(user_id=user_id, case_id=case.id, points=points, reason=reason)

        session.add(warn)
        session.commit()
        session.refresh(warn)

        self.user_service.add_heat(guild_id, user_id, points)
        self.user_service.increment_warning_count(guild_id, user_id)

        return warn
