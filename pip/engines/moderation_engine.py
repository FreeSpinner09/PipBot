from pip.services.threshold_service import ThresholdService
from pip.services.user_service import UserService


class ModerationEngine:
    def __init__(self):
        self.user_service = UserService()
        self.threshold_service = ThresholdService()

    def evaluate_user(self, guild_id: int, user_id: int):
        user = self.user_service.get_or_create_user(guild_id, user_id)
        heat = user.heat
        thresholds = self.threshold_service.get_thresholds_for_evaluation(guild_id)

        for threshold in thresholds:
            if heat >= threshold.threshold_value:
                return threshold

        return None
