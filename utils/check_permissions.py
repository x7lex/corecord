from discord import Interaction, Embed
from discord.app_commands import CheckFailure
from utils.check_config import get_guild_config
from utils.colours import Colour
from typing import Optional

async def is_admin_or_owner(interaction: Interaction) -> bool:
    config: Optional[dict] = get_guild_config(interaction.guild_id)
    admin_role_id: Optional[str] = config.get("admin_role") if config else None

    if admin_role_id:
        role = interaction.guild.get_role(int(admin_role_id))
        if role and role in interaction.user.roles:
            return True
        
    return interaction.user.id == interaction.guild.owner_id

async def is_support(interaction: Interaction) -> bool:
    config: Optional[dict] = get_guild_config(interaction.guild_id)
    support_role_id: Optional[str] = config.get("support_role") if config else None

    if support_role_id:
        role = interaction.guild.get_role(int(support_role_id))
        if role and role in interaction.user.roles:
            return True

    return False

async def handle_permission_error(interaction: Interaction, error: Exception) -> None:
    if isinstance(error, CheckFailure):
        embed = Embed(
            title="Permission Error",
            description="You are not allowed to use that command.",
            color=EmbedColor.RED.value
        )
        
        try:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception:
            try:
                await interaction.followup.send(embed=embed, ephemeral=True)
            except Exception:
                pass