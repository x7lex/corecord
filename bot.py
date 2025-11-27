import os, discord, importlib, pkgutil, modules
from discord import app_commands
from dotenv import load_dotenv
from utils.check_permissions import handle_permission_error
from utils.console import log
from utils.colours import Colour

def load_any_env():
    for file in os.listdir("."):
        if file.endswith(".env"):
            load_dotenv(file)
            log(f"Loaded environment file: {file}", Colour.BLUE)
            return
    log("Warning: No .env file found.", Colour.YELLOW)

load_any_env()

class Init(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self._modules_loaded = False

    async def setup_hook(self):
        if not self._modules_loaded:
            await self.load_modules()
            self._modules_loaded = True

    async def load_modules(self):
        log("Loading modules...", Colour.BLUE)
        for _, module_name, _ in pkgutil.iter_modules(modules.__path__):
            try:
                module = importlib.import_module(f"modules.{module_name}")
                if hasattr(module, "register"):
                    module.register(self)
                log(f"Loaded: {module_name}", Colour.GREEN)
            except Exception as e:
                log(f"Failed to load {module_name}: {e}", Colour.RED)
        try:
            await self.tree.sync()
            log("Command tree synced", Colour.GREEN)
        except Exception as e:
            log(f"Command tree sync failed: {e}", Colour.RED)

client = Init()

@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    try:
        await handle_permission_error(interaction, error)
    except Exception as e:
        log(f"Unhandled command error: {e}", Colour.RED)
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "An unexpected error occurred.", ephemeral=True
                )
        except Exception:
            pass

@client.event
async def on_ready():
    log(f"Logged in as {client.user}", Colour.GREEN)

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set!")

try:
    client.run(TOKEN)
except discord.LoginFailure:
    log("Invalid token provided.", Colour.RED)
except Exception as e:
    log(f"Bot failed to start: {e}", Colour.RED)

