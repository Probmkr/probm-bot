from disnake.ext import commands
from lib import LT, Logger, DLT
import disnake

logger = Logger(DLT)

class OnReady(commands.Cog):
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(LT.INFO, f"Logged in as {self.bot.user.name}")

class Ping(commands.Cog):
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    @commands.slash_command(description="ping to bot")
    async def ping(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_message("pong!")

    @commands.slash_command(description="ping to bot silently")
    async def silent_ping(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_message("pong!", ephemeral=True)

class MessagePing(commands.Cog):
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")
