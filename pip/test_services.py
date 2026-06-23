from pip.services.user_service import UserService

service = UserService()

user = service.get_user(
    guild_id=123,
    user_id=456,
)

print(user)
