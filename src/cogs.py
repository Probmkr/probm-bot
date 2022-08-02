from disnake.ext import commands
from lib import LT

class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.log(LT.INFO, f"Logged in as {self.bot.user.name}")