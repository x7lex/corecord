# /hello example command
from discord import Interactixxon
from discord.ext import commands

def register(client: commands.Bot):
    @client.tree.command(name="hello", description="Sends a greeting message!")
    async def hello(interaction: Interaction):
        await interaction.response.send_message("Hello there!")
