from datetime import UTC, datetime

import discord


class EmbedFactory:
    FOOTER_TEXT = "Pip Moderation"

    SUCCESS_COLOR = discord.Color.green()
    ERROR_COLOR = discord.Color.red()
    WARNING_COLOR = discord.Color.gold()
    INFO_COLOR = discord.Color.blurple()

    @staticmethod
    def _base_embed(
        title: str,
        description: str | None = None,
        color: discord.Color = INFO_COLOR,
    ) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.now(UTC),
        )
        embed.set_footer(text=EmbedFactory.FOOTER_TEXT)
        return embed

    @staticmethod
    def success(title: str, description: str) -> discord.Embed:
        return EmbedFactory._base_embed(
            title=title,
            description=description,
            color=EmbedFactory.SUCCESS_COLOR,
        )

    @staticmethod
    def error(title: str, description: str) -> discord.Embed:
        return EmbedFactory._base_embed(
            title=title,
            description=description,
            color=EmbedFactory.ERROR_COLOR,
        )

    @staticmethod
    def warning(title: str, description: str) -> discord.Embed:
        return EmbedFactory._base_embed(
            title=title,
            description=description,
            color=EmbedFactory.WARNING_COLOR,
        )

    @staticmethod
    def info(title: str, description: str) -> discord.Embed:
        return EmbedFactory._base_embed(
            title=title,
            description=description,
            color=EmbedFactory.INFO_COLOR,
        )

    @staticmethod
    def health(
        latency: int,
        database_status: str,
        guild_count: int,
        loaded_cogs: int,
        cached_users: int,
    ) -> discord.Embed:
        embed = EmbedFactory._base_embed(
            title="Pip Health Check",
            color=EmbedFactory.SUCCESS_COLOR,
        )
        embed.add_field(name="Discord", value="Connected", inline=False)
        embed.add_field(name="Database", value=database_status, inline=False)
        embed.add_field(name="Latency", value=f"{latency}ms", inline=False)
        embed.add_field(name="Guilds", value=str(guild_count), inline=True)
        embed.add_field(name="Loaded Cogs", value=str(loaded_cogs), inline=True)
        embed.add_field(name="Cached Users", value=str(cached_users), inline=True)
        return embed

    @staticmethod
    def case(
        case_number: int,
        action: str,
        user_id: int,
        moderator_id: int | None,
        reason: str,
        automated: bool | None = None,
        *,
        color: discord.Color | None = None,
        title: str | None = None,
        timestamp: datetime | None = None,
    ) -> discord.Embed:
        embed = EmbedFactory._base_embed(
            title=title or f"Case #{case_number} • {action}",
            color=color or EmbedFactory.INFO_COLOR,
        )

        if timestamp is not None:
            embed.timestamp = timestamp

        embed.add_field(
            name="Action",
            value=action,
            inline=False,
        )

        embed.add_field(
            name="User",
            value=f"<@{user_id}>",
            inline=False,
        )

        embed.add_field(
            name="Moderator",
            value="Automated" if moderator_id is None else f"<@{moderator_id}>",
            inline=False,
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False,
        )

        if automated is not None:
            embed.add_field(
                name="Automated",
                value="Yes" if automated else "No",
                inline=True,
            )

        return embed
