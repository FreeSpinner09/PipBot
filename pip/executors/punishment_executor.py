from datetime import UTC, datetime, timedelta

import discord


class PunishmentExecutor:
    async def execute(
        self, member: discord.Member, punishment_type: str, duration: int, reason: str
    ):
        if punishment_type == "warn":
            return

        elif punishment_type == "timeout":
            if duration is None:
                raise ValueError("Timeout punishment requires duration.")
            else:
                await member.timeout(
                    datetime.now(UTC) + timedelta(seconds=duration), reason=reason
                )

        elif punishment_type == "kick":
            await member.kick(reason=reason)

        elif punishment_type == "ban":
            await member.ban(reason=reason)

        else:
            raise ValueError(f"Unknown punishment type: {punishment_type}")
