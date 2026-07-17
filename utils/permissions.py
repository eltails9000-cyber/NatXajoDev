import discord
from discord import app_commands
from config import OWNER_ID


def owner_check() -> app_commands.check:
    """
    Decorator that restricts a slash command to the bot owner only.
    Usage: @owner_check()
    """
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Acceso denegado",
                    description="Este comando solo puede ser usado por el propietario del bot.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return False
        return True

    return app_commands.check(predicate)
