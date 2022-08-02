from dotenv import load_dotenv
from disnake.ext import commands
from lib import Logging, LT
from cogs import *
import disnake
import os

load_dotenv()

TOKEN: str = os.getenv("TOKEN")
BOT_ID: int = int(os.getenv("BOT_ID"))
BOT_SECRET: str = os.getenv("BOT_SECRET")

bot = commands.Bot(command_prefix='th!', intents=disnake.Intents.all(), sync_commands=True, reload=True)
logger = Logging(LT.DEBUG)

bot.add_cog(OnReady(bot, logger))

bot.run(TOKEN)
