import json
import os

import discord
from discord import app_commands
from dotenv import load_dotenv
from tailscale import Tailscale

description = """
Bot for managing my homelab with simple discord commands (prefix '/'):
    - /invite (generates tailscale invite link)
"""

# env config
load_dotenv()

# for Discord API Client
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set")
# For instant updates while developing
GUILD_ID = os.getenv("GUILD_ID")
if not GUILD_ID:
    raise RuntimeError("GUILD_ID not set")
# for Tailscale API client
TAILSCALE_KEY = os.getenv("TAILSCALE_KEY")
if not TAILSCALE_KEY:
    raise RuntimeError("TAILSCALE_KEY not set")
TAILNET_ID = os.getenv("TAILNET_ID")
if not TAILNET_ID:
    raise RuntimeError("TAILNET_ID not set")


# Tailscale config
async def get_invite() -> str:
    """Generate Invite Link for Tailnet"""
    assert TAILSCALE_KEY is not None
    assert TAILNET_ID is not None
    async with Tailscale(tailnet=TAILNET_ID, api_key=TAILSCALE_KEY) as tailscale:
        try:
            json_str: str = await tailscale._request(
                uri=f"tailnet/{tailscale.tailnet}/user-invites"
            )
            data = json.loads(json_str)
            return data[0]["inviteUrl"]
        except:
            return "Unknown error from tailscale, see Admin Console for details"


# Discord Config
class Bot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # For development, sync to a guild for instant updates
        assert GUILD_ID is not None
        guild = discord.Object(id=GUILD_ID)
        await self.tree.sync(guild=guild)
        print("Slash commands synced")


# init
bot = Bot()


@bot.event
async def on_ready():
    assert bot.user is not None
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


# commands
@bot.tree.command(
    name="ping", description="Health check", guild=discord.Object(id=GUILD_ID)
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)


@bot.tree.command(
    name="invite",
    description="Generate Tailscale invite link",
    guild=discord.Object(id=GUILD_ID),
)
async def invite(interaction: discord.Interaction):
    invite_url = await get_invite()
    await interaction.response.send_message(
        f"Please create an account: {invite_url}\nThen, install the [Tailscale client](https://tailscale.com/download) and sign in to gain private access",
        ephemeral=True,
    )


# run the bot
bot.run(TOKEN)
