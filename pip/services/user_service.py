from pip.database.database import get_session
from pip.database.models.user import User


class UserService:
    def get_user(self, guild_id: int, user_id: int):
        session = get_session()
        return (
            session.query(User)
            .filter(User.guild_id == guild_id, User.user_id == user_id)
            .first()
        )

    def create_user(self, guild_id: int, user_id: int):
        session = get_session()

        user = User(guild_id=guild_id, user_id=user_id)

        session.add(user)
        session.commit()

        session.refresh(user)

        return user

    def get_or_create_user(self, guild_id: int, user_id: int):

        user = self.get_user(guild_id, user_id)

        if user is None:
            return self.create_user(guild_id, user_id)
        else:
            return user
