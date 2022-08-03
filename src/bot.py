from typing import List
from dotenv import load_dotenv
from disnake.ext import commands
from lib import Logger, DLT
from cogs import *
import disnake
import os

load_dotenv()

TOKEN: str = os.getenv("TOKEN")
BOT_ID: int = int(os.getenv("BOT_ID"))
BOT_SECRET: str = os.getenv("BOT_SECRET")
ADMIN_IDS: List[int] = list(map(int, os.getenv("ADMIN_IDS").split(",")))

bot = commands.Bot(command_prefix='th!', intents=disnake.Intents.all(), sync_commands=True, reload=True)
logger = Logger(DLT)

bot.add_cog(Ping(bot))
bot.add_cog(MessagePing(bot))
bot.add_cog(Verify(bot))
bot.add_cog(OnReady(bot))

# @bot.command()
# async def ping(ctx: commands.Context):
#     await ctx.send("pong!")

bot.run(TOKEN)
