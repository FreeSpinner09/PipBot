from pip.services.case_service import CaseService

service = CaseService()

case = service.create_case(
    guild_id=123,
    user_id=456,
    moderator_id=789,
    action="warn",
    reason="Testing",
)

print(case.id)
print(case.action)
print(case.reason)
print(case.automated)
