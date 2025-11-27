import discord, json

from typing import Optional

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
        
    except FileNotFoundError:
        return {}

def save_config(cfg: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)

def validate_ids(
    guild: discord.Guild, 
    ticket_channel_id: str, 
    ticket_category_id: str | None, 
    support_role_id: str
):
    errors = []
    channel = category = role = None

    try:
        ticket_channel_id = int(ticket_channel_id) if ticket_channel_id else None
        ticket_category_id = int(ticket_category_id) if ticket_category_id else None
        support_role_id = int(support_role_id) if support_role_id else None
    except ValueError:
        errors.append("Config contains non-numeric IDs.")
        return None, errors

    if ticket_channel_id:
        channel = guild.get_channel(ticket_channel_id)
        if not isinstance(channel, discord.TextChannel):
            errors.append("Invalid ticket channel ID.")

    if ticket_category_id:
        category = guild.get_channel(ticket_category_id)
        if not isinstance(category, discord.CategoryChannel):
            errors.append("Invalid ticket category ID.")

    if support_role_id:
        role = guild.get_role(support_role_id)
        if role is None:
            errors.append("Invalid support role ID.")

    return (channel, category, role), errors

def get_guild_config(guild_id: int) -> Optional[dict]:
    cfg = load_config()
    return cfg.get(str(guild_id))

    if not guild_cfg:
        return None
    
    if str(guild_id) != str(guild_cfg.get("guild_id")):
        return None
    
    return guild_cfg