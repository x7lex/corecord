import os, discord, importlib, pkgutil, modules, utils
from discord import app_commands
from dotenv import load_dotenv
from enum import Enum

class Colour(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4

ANSI_MAP = {
    Colour.RED: "\033[31m",
    Colour.GREEN: "\033[32m",
    Colour.YELLOW: "\033[33m",
    Colour.BLUE: "\033[34m",
}

RESET = "\033[0m"

def log(text: str, colour: Colour = None):
    if colour and colour in ANSI_MAP:
        print(f"{ANSI_MAP[colour]}{text}{RESET}")
    else:
        print(text)

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
            await self.load_utils()
            await self.load_modules()
            self._modules_loaded = True

    async def load_utils(self):
        log("Loading utils...", Colour.BLUE)
        for _, util_name, _ in pkgutil.iter_modules(utils.__path__):
            try:
                util_module = importlib.import_module(f"utils.{util_name}")
                if hasattr(util_module, "register"):
                    util_module.register(self)
                log(f"Loaded util: {util_name}", Colour.GREEN)
            except Exception as e:
                log(f"Failed to load util {util_name}: {e}", Colour.RED)

    async def load_modules(self):
        log("Loading modules...", Colour.BLUE)
        for _, module_name, _ in pkgutil.iter_modules(modules.__path__):
            try:
                module = importlib.import_module(f"modules.{module_name}")
                if hasattr(module, "register"):
                    module.register(self)
                log(f"Loaded module: {module_name}", Colour.GREEN)
            except Exception as e:
                log(f"Failed to load module {module_name}: {e}", Colour.RED)
        try:
            await self.tree.sync()
            log("Command tree synced", Colour.GREEN)
        except Exception as e:
            log(f"Command tree sync failed: {e}", Colour.RED)

client = Init()

@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    try:
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You do not have permission to run this command.", ephemeral=True)
            log(f"Missing permissions: {error}", Colour.YELLOW)
        else:
            raise error
    except Exception as e:
        log(f"Unhandled command error: {e}", Colour.RED)
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)
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
