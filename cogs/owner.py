import discord
import sys
import os
from discord import app_commands
from discord.ext import commands
from utils.messages import success_embed, error_embed
from utils.permissions import owner_check
import logging

logger = logging.getLogger(__name__)


class Owner(commands.Cog):
    """Owner-only administrative commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="shutdown", description="Shut down the bot safely.")
    @owner_check()
    async def shutdown(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            embed=success_embed("Apagado", "El bot se está apagando. Hasta pronto.")
        )
        logger.warning("Bot shutdown requested by %s", interaction.user)
        await self.bot.close()

    @app_commands.command(name="restart", description="Restart the bot process.")
    @owner_check()
    async def restart(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            embed=success_embed("Reinicio", "El bot se está reiniciando…")
        )
        logger.warning("Bot restart requested by %s", interaction.user)
        await self.bot.close()
        os.execv(sys.executable, [sys.executable] + sys.argv)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Owner(bot))
