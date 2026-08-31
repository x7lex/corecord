# /ping command, returns the average of the bot 

from discord import Interaction, app_commands
from discord.ext import commands

class Ping(commands.Cog):

    # create the instance of this class
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @app_commands.command(name="ping", description="returns the delay")
    async def ping(self, interacation: Interaction) -> None:
        await interacation.response.send_message(
            f"{round(self.bot.latency * 1000)}ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))