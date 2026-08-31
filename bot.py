import logging
import os
import pkgutil
from datetime import datetime
from logging.handlers import RotatingFileHandler

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import src.modules as modules

LOG_FILE = os.path.join(
    "logs",
    f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt",
)

logger = logging.getLogger("botcore")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# DEBUG: #0000AA
# INFO: #00AA00
# WARNING: #AAAA00
# ERROR: #AA0000
# CRITICAL: #AA0000
class ColourFormatter(logging.Formatter):
    COLOURS = {
        logging.DEBUG: "\033[34m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[31m",
    }

    RESET = "\033[0m"

    def format(self, record) -> str:
        message = super().format(record)
        colour = self.COLOURS.get(record.levelno, "")
        return f"{colour}{message}{self.RESET}" if colour else message

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    ColourFormatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        "%H:%M:%S",
    )
)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# load up any .env file to grab discord token in the future
def load_env() -> None:
    for filename in os.listdir("."):
        if filename.endswith(".env"):
            load_dotenv(filename)
            logger.info(f"Loaded environment file: {filename}")

    logger.warning("No .env file found.")


load_env()

class Init(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
        )

    # load everything from src/modules
    async def setup_hook(self):
        for _, module_name, _ in pkgutil.iter_modules(modules.__path__):
            try:
                await self.load_extension(
                    f"src.modules.{module_name}"
                )
                logger.info(f"Loaded module: {module_name}")
            except Exception:
                logger.exception(
                    f"Failed to load module: {module_name}"
                )

        await self.tree.sync()
        logger.info("Command tree synced.")

client = Init()

@client.tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        logger.warning(f"Missing permissions: {error}")

        await interaction.response.send_message(
            "You do not have permission to run this command.",
            ephemeral=True,
        )

    logger.exception(
        "Unhandled command error",
        exc_info=(
            type(error),
            error,
            error.__traceback__,
        ),
    )

    try:
        if interaction.response.is_done():
            await interaction.followup.send(
                "An unexpected error occurred.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "An unexpected error occurred.",
                ephemeral=True,
            )
    except discord.HTTPException:
        logger.exception(
            "Failed to send command error response."
        )

@client.event
async def on_ready():
    logger.info(
        f"Logged in as {client.user} ({client.user.id})"
    )

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN environment variable is not set!"
    )

try:
    client.run(TOKEN)
except discord.LoginFailure:
    logger.critical("Invalid Discord token provided.")
except Exception:
    logger.exception("Bot failed to start.")