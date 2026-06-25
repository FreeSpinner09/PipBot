from pip.database.database import get_session
from pip.database.models.case import Case


class CaseService:
    def create_case(
        self,
        guild_id: int,
        user_id: int,
        moderator_id: int | None,
        action: str,
        reason: str,
        automated: bool = False,
    ):
        session = get_session()

        guild_case_number = self.get_next_case_number(guild_id)

        case = Case(
            guild_id=guild_id,
            guild_case_number=guild_case_number,
            user_id=user_id,
            moderator_id=moderator_id,
            action=action,
            reason=reason,
            automated=automated,
        )

        session.add(case)
        session.commit()

        session.refresh(case)
        return case

    def get_next_case_number(
        self,
        guild_id: int,
    ):
        session = get_session()

        last_case = (
            session.query(Case)
            .filter(Case.guild_id == guild_id)
            .order_by(Case.guild_case_number.desc())
            .first()
        )

        if last_case is None:
            return 1
        else:
            return last_case.guild_case_number + 1

    def get_case(self, guild_id: int, guild_case_number: int):
        session = get_session()
        return (
            session.query(Case)
            .filter(
                Case.guild_id == guild_id, Case.guild_case_number == guild_case_number
            )
            .first()
        )

    def get_user_cases(self, guild_id: int, user_id: int, action_filter: str | None):
        session = get_session()

        if action_filter is None:
            cases = (
                session.query(Case)
                .filter(Case.guild_id == guild_id, Case.user_id == user_id)
                .order_by(Case.guild_case_number.desc())
                .all()
            )
            return cases

        else:
            cases = (
                session.query(Case)
                .filter(
                    Case.guild_id == guild_id,
                    Case.user_id == user_id,
                    Case.action == action_filter,
                )
                .order_by(Case.guild_case_number.desc())
                .all()
            )
            return cases
