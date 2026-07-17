import discord
from discord import app_commands
from discord.ext import commands
from utils.messages import success_embed, error_embed, info_embed
import logging

logger = logging.getLogger(__name__)

# In-memory warn storage (resets on restart)
_warns: dict[int, list[dict]] = {}


class Moderation(commands.Cog):
    """Discord moderation commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.describe(member="The member to kick", reason="Reason for the kick")
    @app_commands.default_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
    ) -> None:
        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                embed=error_embed("Sin permisos", "No puedo expulsar a un miembro con un rol superior o igual al mío."),
                ephemeral=True,
            )
            return
        try:
            await member.kick(reason=reason)
            logger.info("%s kicked %s — Reason: %s", interaction.user, member, reason)
            await interaction.response.send_message(
                embed=success_embed(
                    "Expulsado",
                    f"**{member}** ha sido expulsado.\n**Razón:** {reason}",
                )
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=error_embed("Error", "No tengo permisos para expulsar a este miembro."),
                ephemeral=True,
            )
        except discord.HTTPException as exc:
            logger.error("Failed to kick %s: %s", member, exc)
            await interaction.response.send_message(
                embed=error_embed("Error", f"Falló la expulsión: {exc}"),
                ephemeral=True,
            )

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.describe(member="The member to ban", reason="Reason for the ban")
    @app_commands.default_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
    ) -> None:
        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                embed=error_embed("Sin permisos", "No puedo banear a un miembro con un rol superior o igual al mío."),
                ephemeral=True,
            )
            return
        try:
            await member.ban(reason=reason, delete_message_days=0)
            logger.info("%s banned %s — Reason: %s", interaction.user, member, reason)
            await interaction.response.send_message(
                embed=success_embed(
                    "Baneado",
                    f"**{member}** ha sido baneado.\n**Razón:** {reason}",
                )
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=error_embed("Error", "No tengo permisos para banear a este miembro."),
                ephemeral=True,
            )
        except discord.HTTPException as exc:
            logger.error("Failed to ban %s: %s", member, exc)
            await interaction.response.send_message(
                embed=error_embed("Error", f"Falló el ban: {exc}"),
                ephemeral=True,
            )

    @app_commands.command(name="unban", description="Unban a user by their ID.")
    @app_commands.describe(user_id="The Discord user ID to unban", reason="Reason for the unban")
    @app_commands.default_permissions(ban_members=True)
    async def unban(
        self,
        interaction: discord.Interaction,
        user_id: str,
        reason: str = "No reason provided",
    ) -> None:
        try:
            uid = int(user_id)
        except ValueError:
            await interaction.response.send_message(
                embed=error_embed("ID inválido", "El ID de usuario debe ser un número."),
                ephemeral=True,
            )
            return
        try:
            user = await self.bot.fetch_user(uid)
            await interaction.guild.unban(user, reason=reason)
            logger.info("%s unbanned user ID %s — Reason: %s", interaction.user, uid, reason)
            await interaction.response.send_message(
                embed=success_embed(
                    "Desbaneado",
                    f"**{user}** ha sido desbaneado.\n**Razón:** {reason}",
                )
            )
        except discord.NotFound:
            await interaction.response.send_message(
                embed=error_embed("No encontrado", "El usuario no está baneado o el ID es incorrecto."),
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=error_embed("Error", "No tengo permisos para desbanear a este usuario."),
                ephemeral=True,
            )
        except discord.HTTPException as exc:
            logger.error("Failed to unban user ID %s: %s", uid, exc)
            await interaction.response.send_message(
                embed=error_embed("Error", f"Falló el unban: {exc}"),
                ephemeral=True,
            )

    @app_commands.command(name="warn", description="Warn a member.")
    @app_commands.describe(member="The member to warn", reason="Reason for the warning")
    @app_commands.default_permissions(moderate_members=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
    ) -> None:
        uid = member.id
        if uid not in _warns:
            _warns[uid] = []
        _warns[uid].append({"reason": reason, "staff": str(interaction.user)})
        count = len(_warns[uid])
        logger.info("%s warned %s (%d warns) — Reason: %s", interaction.user, member, count, reason)
        await interaction.response.send_message(
            embed=info_embed(
                "Advertencia emitida",
                (
                    f"**{member}** ha recibido una advertencia.\n"
                    f"**Razón:** {reason}\n"
                    f"**Total de advertencias:** {count}"
                ),
            )
        )
        try:
            await member.send(
                embed=info_embed(
                    "Has recibido una advertencia",
                    f"**Servidor:** {interaction.guild.name}\n**Razón:** {reason}",
                )
            )
        except discord.Forbidden:
            pass  # DMs disabled — silently continue


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
