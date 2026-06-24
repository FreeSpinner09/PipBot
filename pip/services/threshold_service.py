from pip.database.database import get_session
from pip.database.models.punishment_thresholds import PunishmentThresholds


class ThresholdService:
    def create_threshold(
        self,
        guild_id: int,
        threshold_value: int,
        punishment_type: str,
        duration: int | None,
    ):
        session = get_session()

        threshold = PunishmentThresholds(
            guild_id=guild_id,
            threshold_value=threshold_value,
            punishment_type=punishment_type,
            duration=duration,
        )

        session.add(threshold)
        session.commit()

        session.refresh(threshold)
        return threshold

    def get_thresholds(self, guild_id: int):
        session = get_session()

        thresholds = (
            session.query(PunishmentThresholds)
            .filter(PunishmentThresholds.guild_id == guild_id)
            .order_by(PunishmentThresholds.threshold_value.asc())
            .all()
        )

        return thresholds

    def get_thresholds_for_evaluation(self, guild_id: int):
        session = get_session()

        thresholds = (
            session.query(PunishmentThresholds)
            .filter(PunishmentThresholds.guild_id == guild_id)
            .order_by(PunishmentThresholds.threshold_value.desc())
            .all()
        )

        return thresholds
