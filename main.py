import asyncio
import logging
import sys
import discord
from discord.ext import commands
import database as db
from config import TOKEN, OWNER_ID

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("GloryBot")

# ---------------------------------------------------------------------------
# Bot definition
# ---------------------------------------------------------------------------
COGS = [
    "cogs.roblox",
    "cogs.owner",
    "cogs.maintenance",
    "cogs.moderation",
]


class GloryBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="!",  # prefix kept even if slash-only; required by commands.Bot
            intents=intents,
            owner_id=OWNER_ID,
        )

    async def setup_hook(self) -> None:
        """Called once right after login — load cogs and sync commands."""
        db.initialize_database()

        for cog in COGS:
            try:
                await self.load_extension(cog)
                logger.info("Loaded cog: %s", cog)
            except Exception as exc:
                logger.error("Failed to load cog %s: %s", cog, exc)

        # Sync slash commands globally
        try:
            synced = await self.tree.sync()
            logger.info("Synced %d slash command(s).", len(synced))
        except Exception as exc:
            logger.error("Failed to sync commands: %s", exc)

    async def on_ready(self) -> None:
        logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Glory or Death",
            )
        )
        logger.info("Bot is ready.")

    async def on_application_command_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        """Global slash command error handler."""
        logger.error("Unhandled command error from %s: %s", interaction.user, error)
        msg = "Ocurrió un error inesperado. Por favor, inténtalo más tarde."
        try:
            if interaction.response.is_done():
                await interaction.followup.send(msg, ephemeral=True)
            else:
                await interaction.response.send_message(msg, ephemeral=True)
        except Exception:
            pass

    async def on_error(self, event_method: str, *args, **kwargs) -> None:
        logger.exception("Unhandled exception in event: %s", event_method)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
async def main() -> None:
    if not TOKEN:
        logger.critical("DISCORD_TOKEN is not set. Set it in .env or as an environment variable.")
        sys.exit(1)

    bot = GloryBot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
