from pip.services.user_service import UserService

service = UserService()

user = service.get_or_create_user(
    guild_id=123,
    user_id=456,
)

print(f"Current Heat: {user.heat}")

user = service.add_heat(
    guild_id=123,
    user_id=456,
    amount=10,
)

print(f"After Add: {user.heat}")

user = service.remove_heat(
    guild_id=123,
    user_id=456,
    amount=5,
)

print(f"After Remove: {user.heat}")
